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

    for key in CLEARANCE_LEVELS:
        if key in clearance:
            return CLEARANCE_LEVELS[key]

    return 0


def text_contains_phrase(text_lower, phrase):
    phrase = normalize_text(phrase)
    return phrase in text_lower


def build_normalized_set(items):
    return {normalize_text(x) for x in items if normalize_text(x)}


def score_ratio(matched_count, total_count, max_points):
    if total_count == 0:
        return 0
    return (matched_count / total_count) * max_points


def candidate_data(applicant):
    parsed = applicant.get("parsed_resume_json") or {}
    resume_text = applicant.get("resume_text", "") or ""
    text_lower = normalize_text(resume_text)

    return {
        "text_lower": text_lower,
        "skills": parsed.get("skills", []),
        "years_experience": float(parsed.get("years_experience", 0) or 0),
        "clearance": parsed.get("clearance"),
    }


def match_items(target_items, candidate_items, text_lower):
    matched = []
    missing = []

    for item in target_items:
        item_norm = normalize_text(item)

        if item_norm in [normalize_text(x) for x in candidate_items] or item_norm in text_lower:
            matched.append(item)
        else:
            missing.append(item)

    return matched, missing


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

    required_skills = role_config.get("required_skills", [])
    preferred_skills = role_config.get("preferred_skills", [])

    minimum_years = role_config.get("minimum_years_experience", 0)
    required_clearance = role_config.get("required_clearance")

    weights = role_config.get("weights", {})

    strengths = []
    gaps = []
    hard_fail_reasons = []
    hard_fail = False

    # --- Skill Matching ---
    matched_required, missing_required = match_items(
        required_skills, candidate["skills"], text_lower
    )
    matched_preferred, missing_preferred = match_items(
        preferred_skills, candidate["skills"], text_lower
    )

    score = 0

    score += score_ratio(len(matched_required), len(required_skills), 40)
    score += score_ratio(len(matched_preferred), len(preferred_skills), 20)

    if matched_required:
        strengths.append(f"Strong required skill coverage: {', '.join(matched_required)}")

    if missing_required:
        gaps.append(f"Missing required skills: {', '.join(missing_required)}")

    if matched_preferred:
        strengths.append(f"Has preferred skills: {', '.join(matched_preferred)}")

    # --- Experience ---
    years = candidate["years_experience"]

    if years >= minimum_years:
        score += 20
        strengths.append(f"{years} years experience meets requirement")
    else:
        gaps.append(f"Only {years} years experience (needs {minimum_years})")
        hard_fail = True
        hard_fail_reasons.append("Below minimum experience")

    # --- Clearance ---
    if required_clearance:
        if candidate.get("clearance") != required_clearance:
            hard_fail = True
            hard_fail_reasons.append("Missing required clearance")
            gaps.append("No required clearance")
        else:
            score += 10
            strengths.append("Meets clearance requirement")

    total_score = round(min(score, 100), 2)

    final_fit_label = fit_label(total_score, hard_fail)

    # --- Build Pros / Cons ---
    pros = strengths[:4]
    cons = (gaps + hard_fail_reasons)[:4]

    # --- Smart Summary ---
    if hard_fail and total_score >= 85:
        summary = (
            "Strong technical candidate with excellent skill alignment and experience. "
            "However, they are missing required qualifications, which prevents full eligibility. "
            "Could still be considered depending on flexibility."
        )
    elif hard_fail:
        summary = (
            "Candidate shows some relevant experience but does not meet key requirements. "
            "Several gaps reduce overall fit for this role."
        )
    elif total_score >= 85:
        summary = (
            "Highly qualified candidate with strong alignment across skills and experience. "
            "Demonstrates readiness to contribute immediately."
        )
    elif total_score >= 70:
        summary = (
            "Solid candidate with good alignment to the role. "
            "May require some ramp-up in certain areas."
        )
    else:
        summary = (
            "Candidate has limited alignment with the role requirements and may not be a strong fit."
        )

    return {
        "total_score": total_score,
        "hard_fail": hard_fail,
        "score_breakdown_json": {},
        "explanation_json": {
            "fit_label": final_fit_label,
            "summary": summary,
            "pros": pros,
            "cons": cons,
            "strengths": strengths,
            "gaps": gaps,
            "hard_fail_reasons": hard_fail_reasons,
        },
    }