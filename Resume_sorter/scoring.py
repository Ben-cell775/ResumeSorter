import re


CLEARANCE_LEVELS = {
    "none": 0,
    "confidential": 1,
    "secret": 2,
    "top secret": 3,
    "ts": 3,
    "ts/sci": 4,
    "sci": 4,
}


def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def safe_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [value]
    return []


def clearance_value(clearance):
    if not clearance:
        return 0

    clearance = normalize_text(clearance)

    if clearance in CLEARANCE_LEVELS:
        return CLEARANCE_LEVELS[clearance]

    if "ts/sci" in clearance:
        return 4
    if "top secret" in clearance:
        return 3
    if "secret" in clearance:
        return 2
    if "confidential" in clearance:
        return 1

    return 0


def text_contains_phrase(text_lower, phrase):
    phrase = normalize_text(phrase)
    if not phrase:
        return False

    escaped = re.escape(phrase)
    pattern = rf"\b{escaped}\b"
    return bool(re.search(pattern, text_lower)) or phrase in text_lower


def build_normalized_set(items):
    return {normalize_text(x) for x in items if normalize_text(x)}


def score_ratio(matched_count, total_count, max_points):
    if total_count <= 0:
        return 0.0
    return (matched_count / total_count) * float(max_points)


def candidate_data(applicant):
    parsed = applicant.get("parsed_resume_json") or {}
    resume_text = applicant.get("resume_text", "") or ""
    text_lower = normalize_text(resume_text)

    def list_from_parsed(key):
        value = parsed.get(key, [])
        if isinstance(value, list):
            return [str(x).strip() for x in value if str(x).strip()]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return []

    years_experience = parsed.get("years_experience", 0)
    try:
        years_experience = float(years_experience or 0)
    except Exception:
        years_experience = 0.0

    return {
        "parsed": parsed,
        "resume_text": resume_text,
        "text_lower": text_lower,
        "skills": list_from_parsed("skills"),
        "tools": list_from_parsed("tools"),
        "certifications": list_from_parsed("certifications"),
        "education": list_from_parsed("education"),
        "industries": list_from_parsed("industries"),
        "years_experience": years_experience,
        "clearance": parsed.get("clearance"),
    }


def match_items(target_items, structured_items, text_lower):
    structured_set = build_normalized_set(structured_items)
    matched = []
    missing = []

    for item in safe_list(target_items):
        item_norm = normalize_text(item)

        if item_norm in structured_set or text_contains_phrase(text_lower, item_norm):
            matched.append(item)
        else:
            missing.append(item)

    return matched, missing


def score_keyword_groups(keyword_groups, text_lower, candidate):
    matched_groups = []
    missing_groups = []

    search_pool = set()
    for field in ["skills", "tools", "certifications", "education", "industries"]:
        search_pool.update(build_normalized_set(candidate.get(field, [])))

    for group_name, keywords in (keyword_groups or {}).items():
        found = False
        for keyword in safe_list(keywords):
            keyword_norm = normalize_text(keyword)
            if keyword_norm in search_pool or text_contains_phrase(text_lower, keyword_norm):
                found = True
                break

        if found:
            matched_groups.append(group_name)
        else:
            missing_groups.append(group_name)

    return matched_groups, missing_groups


def fit_label(score, hard_fail):
    if hard_fail:
        if score >= 85:
            return "Strong But Unqualified"
        if score >= 70:
            return "Promising But Unqualified"
        return "Not Qualified"

    if score >= 85:
        return "Strong Match"
    if score >= 70:
        return "Good Match"
    if score >= 50:
        return "Possible Match"
    return "Weak Match"


def score_applicant(applicant, role_config):
    candidate = candidate_data(applicant)
    text_lower = candidate["text_lower"]

    weights = role_config.get("weights", {}) or {}
    hard_fail_rules = role_config.get("hard_fail_rules", {}) or {}

    required_skills = safe_list(role_config.get("required_skills"))
    preferred_skills = safe_list(role_config.get("preferred_skills"))
    required_tools = safe_list(role_config.get("required_tools"))
    preferred_tools = safe_list(role_config.get("preferred_tools"))
    required_education = safe_list(role_config.get("required_education"))
    preferred_education = safe_list(role_config.get("preferred_education"))
    required_certifications = safe_list(role_config.get("required_certifications"))
    preferred_certifications = safe_list(role_config.get("preferred_certifications"))
    preferred_industries = safe_list(role_config.get("preferred_industries"))
    keyword_groups = role_config.get("keyword_groups", {}) or {}

    minimum_years_experience = float(role_config.get("minimum_years_experience", 0) or 0)
    preferred_years_experience = float(role_config.get("preferred_years_experience", 0) or 0)
    required_clearance = role_config.get("required_clearance")
    preferred_clearance = role_config.get("preferred_clearance")

    strengths = []
    gaps = []
    hard_fail_reasons = []
    hard_fail = False

    matched_required_skills, missing_required_skills = match_items(
        required_skills, candidate["skills"], text_lower
    )
    matched_preferred_skills, missing_preferred_skills = match_items(
        preferred_skills, candidate["skills"], text_lower
    )
    matched_required_tools, missing_required_tools = match_items(
        required_tools, candidate["tools"], text_lower
    )
    matched_preferred_tools, missing_preferred_tools = match_items(
        preferred_tools, candidate["tools"], text_lower
    )
    matched_required_education, missing_required_education = match_items(
        required_education, candidate["education"], text_lower
    )
    matched_preferred_education, missing_preferred_education = match_items(
        preferred_education, candidate["education"], text_lower
    )
    matched_required_certs, missing_required_certs = match_items(
        required_certifications, candidate["certifications"], text_lower
    )
    matched_preferred_certs, missing_preferred_certs = match_items(
        preferred_certifications, candidate["certifications"], text_lower
    )
    matched_industries, missing_industries = match_items(
        preferred_industries, candidate["industries"], text_lower
    )
    matched_keyword_groups, missing_keyword_groups = score_keyword_groups(
        keyword_groups, text_lower, candidate
    )

    # Higher weight on required criteria, but still allow strong overall profiles.
    required_skill_score = score_ratio(
        len(matched_required_skills), len(required_skills), weights.get("required_skill", 30)
    )
    preferred_skill_score = score_ratio(
        len(matched_preferred_skills), len(preferred_skills), weights.get("preferred_skill", 15)
    )
    required_tool_score = score_ratio(
        len(matched_required_tools), len(required_tools), weights.get("required_tool", 12)
    )
    preferred_tool_score = score_ratio(
        len(matched_preferred_tools), len(preferred_tools), weights.get("preferred_tool", 6)
    )
    required_education_score = score_ratio(
        len(matched_required_education), len(required_education), weights.get("required_education", 10)
    )
    preferred_education_score = score_ratio(
        len(matched_preferred_education), len(preferred_education), weights.get("preferred_education", 5)
    )
    required_certification_score = score_ratio(
        len(matched_required_certs), len(required_certifications), weights.get("required_certification", 5)
    )
    preferred_certification_score = score_ratio(
        len(matched_preferred_certs), len(preferred_certifications), weights.get("preferred_certification", 3)
    )
    industry_score = score_ratio(
        len(matched_industries), len(preferred_industries), weights.get("industry", 4)
    )
    keyword_group_score = score_ratio(
        len(matched_keyword_groups), len(keyword_groups), weights.get("keyword_group_match", 10)
    )

    total = (
        required_skill_score
        + preferred_skill_score
        + required_tool_score
        + preferred_tool_score
        + required_education_score
        + preferred_education_score
        + required_certification_score
        + preferred_certification_score
        + industry_score
        + keyword_group_score
    )

    years = candidate["years_experience"]
    minimum_experience_score = 0.0
    preferred_experience_score = 0.0

    if years >= minimum_years_experience:
        minimum_experience_score = float(weights.get("minimum_experience", 8))
        total += minimum_experience_score
        strengths.append(f"Meets minimum experience: {years:.1f} years")
    else:
        gaps.append(
            f"Below minimum experience: {years:.1f} years vs {minimum_years_experience:.1f} required"
        )
        if hard_fail_rules.get("fail_if_below_minimum_experience"):
            hard_fail = True
            hard_fail_reasons.append("Below minimum experience requirement")

    if preferred_years_experience > 0 and years >= preferred_years_experience:
        preferred_experience_score = float(weights.get("preferred_experience", 6))
        total += preferred_experience_score
        strengths.append(f"Meets preferred experience: {years:.1f} years")

    candidate_clearance_value = clearance_value(candidate.get("clearance"))
    required_clearance_value = clearance_value(required_clearance)
    preferred_clearance_value = clearance_value(preferred_clearance)

    required_clearance_score = 0.0
    preferred_clearance_score = 0.0

    if required_clearance_value > 0:
        if candidate_clearance_value >= required_clearance_value:
            required_clearance_score = float(weights.get("required_clearance", 5))
            total += required_clearance_score
            strengths.append(f"Meets required clearance: {candidate.get('clearance')}")
        else:
            gaps.append(f"Missing required clearance: {required_clearance}")
            if hard_fail_rules.get("fail_if_missing_required_clearance", True):
                hard_fail = True
                hard_fail_reasons.append("Missing required clearance")

    if preferred_clearance_value > 0 and candidate_clearance_value >= preferred_clearance_value:
        preferred_clearance_score = float(weights.get("preferred_clearance", 3))
        total += preferred_clearance_score
        strengths.append(f"Meets preferred clearance: {candidate.get('clearance')}")

    missing_required_skills_threshold = hard_fail_rules.get("missing_required_skills_threshold")
    if missing_required_skills_threshold is not None and len(missing_required_skills) >= int(missing_required_skills_threshold):
        hard_fail = True
        hard_fail_reasons.append(f"Too many missing required skills ({len(missing_required_skills)})")

    missing_required_tools_threshold = hard_fail_rules.get("missing_required_tools_threshold")
    if missing_required_tools_threshold is not None and len(missing_required_tools) >= int(missing_required_tools_threshold):
        hard_fail = True
        hard_fail_reasons.append(f"Too many missing required tools ({len(missing_required_tools)})")

    if matched_required_skills:
        strengths.append(f"Required skills matched: {', '.join(matched_required_skills)}")
    if matched_preferred_skills:
        strengths.append(f"Preferred skills matched: {', '.join(matched_preferred_skills)}")
    if matched_required_tools:
        strengths.append(f"Required tools matched: {', '.join(matched_required_tools)}")
    if matched_preferred_tools:
        strengths.append(f"Preferred tools matched: {', '.join(matched_preferred_tools)}")
    if matched_required_education:
        strengths.append(f"Required education matched: {', '.join(matched_required_education)}")
    if matched_preferred_education:
        strengths.append(f"Preferred education matched: {', '.join(matched_preferred_education)}")
    if matched_required_certs:
        strengths.append(f"Required certifications matched: {', '.join(matched_required_certs)}")
    if matched_preferred_certs:
        strengths.append(f"Preferred certifications matched: {', '.join(matched_preferred_certs)}")
    if matched_industries:
        strengths.append(f"Preferred industries matched: {', '.join(matched_industries)}")
    if matched_keyword_groups:
        strengths.append(f"Keyword groups matched: {', '.join(matched_keyword_groups)}")

    if missing_required_skills:
        gaps.append(f"Missing required skills: {', '.join(missing_required_skills)}")
    if missing_required_tools:
        gaps.append(f"Missing required tools: {', '.join(missing_required_tools)}")
    if missing_required_education:
        gaps.append(f"Missing required education: {', '.join(missing_required_education)}")
    if missing_required_certs:
        gaps.append(f"Missing required certifications: {', '.join(missing_required_certs)}")
    if missing_preferred_skills:
        gaps.append(f"Missing preferred skills: {', '.join(missing_preferred_skills)}")
    if missing_preferred_tools:
        gaps.append(f"Missing preferred tools: {', '.join(missing_preferred_tools)}")
    if missing_keyword_groups:
        gaps.append(f"Missing keyword groups: {', '.join(missing_keyword_groups)}")

    total_score = round(max(0.0, min(total, 100.0)), 2)
    final_fit_label = fit_label(total_score, hard_fail)

    if hard_fail and total_score >= 85:
        summary = "Very strong overall profile, but failed required qualifications."
    elif hard_fail and total_score >= 70:
        summary = "Strong overall match, but failed required qualifications."
    elif hard_fail:
        summary = "Candidate does not meet required qualifications."
    else:
        summary = "Qualified candidate."

    explanation_json = {
        "fit_label": final_fit_label,
        "strengths": strengths,
        "gaps": gaps,
        "hard_fail_reasons": hard_fail_reasons,
        "summary": summary,
    }

    score_breakdown_json = {
        "matched_required_skills": matched_required_skills,
        "missing_required_skills": missing_required_skills,
        "matched_preferred_skills": matched_preferred_skills,
        "missing_preferred_skills": missing_preferred_skills,
        "matched_required_tools": matched_required_tools,
        "missing_required_tools": missing_required_tools,
        "matched_preferred_tools": matched_preferred_tools,
        "missing_preferred_tools": missing_preferred_tools,
        "matched_required_education": matched_required_education,
        "missing_required_education": missing_required_education,
        "matched_preferred_education": matched_preferred_education,
        "missing_preferred_education": missing_preferred_education,
        "matched_required_certifications": matched_required_certs,
        "missing_required_certifications": missing_required_certs,
        "matched_preferred_certifications": matched_preferred_certs,
        "missing_preferred_certifications": missing_preferred_certs,
        "matched_industries": matched_industries,
        "missing_industries": missing_industries,
        "matched_keyword_groups": matched_keyword_groups,
        "missing_keyword_groups": missing_keyword_groups,
        "years_experience": years,
        "minimum_years_experience": minimum_years_experience,
        "preferred_years_experience": preferred_years_experience,
        "required_skill_score": round(required_skill_score, 2),
        "preferred_skill_score": round(preferred_skill_score, 2),
        "required_tool_score": round(required_tool_score, 2),
        "preferred_tool_score": round(preferred_tool_score, 2),
        "required_education_score": round(required_education_score, 2),
        "preferred_education_score": round(preferred_education_score, 2),
        "required_certification_score": round(required_certification_score, 2),
        "preferred_certification_score": round(preferred_certification_score, 2),
        "minimum_experience_score": round(minimum_experience_score, 2),
        "preferred_experience_score": round(preferred_experience_score, 2),
        "required_clearance_score": round(required_clearance_score, 2),
        "preferred_clearance_score": round(preferred_clearance_score, 2),
        "industry_score": round(industry_score, 2),
        "keyword_group_score": round(keyword_group_score, 2),
        "fit_label": final_fit_label,
    }

    return {
        "total_score": total_score,
        "hard_fail": hard_fail,
        "score_breakdown_json": score_breakdown_json,
        "explanation_json": explanation_json,
    }