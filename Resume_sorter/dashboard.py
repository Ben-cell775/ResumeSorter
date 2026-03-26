import os
import copy
import shutil
import pandas as pd
import streamlit as st

from import_applicants import import_applicants
from pdf_import import import_pdfs
from db import supabase
from job_roles import JOB_ROLES
from scoring import score_applicant


st.set_page_config(
    page_title="AI Resume Sorter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1450px;
        }

        [data-testid="stSidebar"] {
            background: #0b1220;
            border-right: 1px solid #1f2937;
        }

        .topbar {
            background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
            border: 1px solid #1f2937;
            border-radius: 20px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 1rem;
        }

        .topbar-title {
            font-size: 2rem;
            font-weight: 800;
            color: #f8fafc;
            margin: 0;
            line-height: 1.1;
        }

        .topbar-subtitle {
            font-size: 0.96rem;
            color: #94a3b8;
            margin-top: 0.35rem;
        }

        .hero-chip-wrap {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.85rem;
        }

        .hero-chip {
            background: rgba(59,130,246,0.12);
            color: #bfdbfe;
            border: 1px solid rgba(59,130,246,0.28);
            padding: 0.38rem 0.72rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .section-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #f8fafc;
            margin-top: 0.3rem;
            margin-bottom: 0.85rem;
        }

        .metric-card {
            background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
            border: 1px solid #1f2937;
            border-radius: 18px;
            padding: 1rem 1rem 0.9rem 1rem;
            min-height: 112px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        }

        .metric-label {
            font-size: 0.88rem;
            color: #94a3b8;
            margin-bottom: 0.45rem;
            font-weight: 500;
        }

        .metric-value {
            font-size: 1.55rem;
            font-weight: 800;
            color: #f8fafc;
            line-height: 1.1;
        }

        .metric-sub {
            margin-top: 0.45rem;
            color: #64748b;
            font-size: 0.82rem;
        }

        .panel {
            background: linear-gradient(180deg, #0f172a 0%, #0b1220 100%);
            border: 1px solid #1f2937;
            border-radius: 18px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .soft-panel {
            background: #0f172a;
            border: 1px solid #243041;
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .status-card {
            background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
            border: 1px solid #243041;
            border-radius: 18px;
            padding: 1rem;
            min-height: 108px;
        }

        .small-label {
            font-size: 0.86rem;
            color: #94a3b8;
            margin-bottom: 0.4rem;
        }

        .big-value {
            font-size: 1.22rem;
            font-weight: 750;
            color: #f8fafc;
        }

        .summary-box {
            background: #111827;
            border: 1px solid #243041;
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .candidate-card {
            background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
            border: 1px solid #243041;
            border-radius: 18px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.85rem;
        }

        .candidate-name {
            font-size: 1.05rem;
            font-weight: 750;
            color: #f8fafc;
            margin-bottom: 0.15rem;
        }

        .candidate-meta {
            font-size: 0.88rem;
            color: #94a3b8;
        }

        .score-pill {
            display: inline-block;
            padding: 0.35rem 0.68rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 700;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
        }

        .pill-green {
            background: rgba(34,197,94,0.14);
            color: #86efac;
            border: 1px solid rgba(34,197,94,0.26);
        }

        .pill-yellow {
            background: rgba(250,204,21,0.14);
            color: #fde68a;
            border: 1px solid rgba(250,204,21,0.26);
        }

        .pill-red {
            background: rgba(239,68,68,0.14);
            color: #fca5a5;
            border: 1px solid rgba(239,68,68,0.26);
        }

        .pill-blue {
            background: rgba(59,130,246,0.14);
            color: #bfdbfe;
            border: 1px solid rgba(59,130,246,0.26);
        }

        .helper-text {
            color: #94a3b8;
            font-size: 0.88rem;
            margin-top: -0.15rem;
            margin-bottom: 0.75rem;
        }

        .divider-space {
            height: 0.4rem;
        }

        .stButton > button {
            border-radius: 12px;
            font-weight: 700;
            border: 1px solid #334155;
        }

        .stDownloadButton > button {
            border-radius: 12px;
            font-weight: 700;
        }

        div[data-testid="stForm"] {
            background: #0b1220;
            border: 1px solid #1f2937;
            border-radius: 16px;
            padding: 1rem;
        }

        div[data-testid="stExpander"] {
            border: 1px solid #1f2937;
            border-radius: 14px;
            overflow: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

PDF_FOLDER = "incoming_resumes"
CSV_FILE = "applicants.csv"


# ----------------------------
# Database + File Helpers
# ----------------------------
def reset_database():
    supabase.table("applicant_scores").delete().neq("id", 0).execute()
    supabase.table("applicants").delete().neq("id", 0).execute()


def clear_existing_scores():
    supabase.table("applicant_scores").delete().neq("id", 0).execute()


def clear_local_upload_files():
    if os.path.exists(CSV_FILE):
        try:
            os.remove(CSV_FILE)
        except Exception:
            pass

    if os.path.exists(PDF_FOLDER):
        try:
            shutil.rmtree(PDF_FOLDER)
        except Exception:
            pass

    os.makedirs(PDF_FOLDER, exist_ok=True)


def get_current_applicants():
    response = supabase.table("applicants").select(
        "id,full_name,email,phone,parsed_resume_json,resume_text"
    ).execute()
    return response.data or []


def get_current_scores():
    response = supabase.table("applicant_scores").select("*").execute()
    return response.data or []


def save_score_to_db(applicant_id, selected_role, result):
    payload = {
        "applicant_id": applicant_id,
        "job_opening_id": 1,
        "scoring_profile_id": 1,
        "total_score": result["total_score"],
        "hard_fail": result["hard_fail"],
        "score_breakdown_json": result["score_breakdown_json"],
        "explanation_json": result["explanation_json"],
        "job_title": selected_role,
    }
    supabase.table("applicant_scores").insert(payload).execute()


# ----------------------------
# Utility Helpers
# ----------------------------
def parse_comma_list(text):
    if not text:
        return []
    return [x.strip() for x in text.split(",") if x.strip()]


def list_to_string(value):
    if isinstance(value, list):
        return ", ".join(value)
    return str(value) if value is not None else ""


def clearance_index(value):
    options = ["None", "confidential", "secret", "top secret", "ts/sci"]
    if not value:
        return 0
    value = str(value).lower().strip()
    return options.index(value) if value in options else 0


def format_status(hard_fail, fit_label=""):
    if hard_fail:
        if "Strong" in fit_label or "Promising" in fit_label:
            return "⚠️ Borderline"
        return "❌ Fail"
    return "✅ Pass"


def pill_html(text, kind="green"):
    klass = {
        "green": "score-pill pill-green",
        "red": "score-pill pill-red",
        "yellow": "score-pill pill-yellow",
        "blue": "score-pill pill-blue",
    }.get(kind, "score-pill pill-blue")
    return f'<span class="{klass}">{text}</span>'


def show_metric_card(label, value, subtext=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge_kind_from_fit(fit_label, hard_fail):
    if hard_fail:
        if "Strong" in fit_label or "Promising" in fit_label:
            return "yellow"
        return "red"
    if "Strong" in fit_label or "Good" in fit_label:
        return "green"
    if "Possible" in fit_label:
        return "yellow"
    return "red"


def score_band(score, hard_fail):
    if hard_fail and score >= 85:
        return "High Score / Missing Requirement"
    if hard_fail:
        return "Not Qualified"
    if score >= 85:
        return "Top Tier"
    if score >= 70:
        return "Strong"
    if score >= 50:
        return "Moderate"
    return "Weak"


def build_live_role_config(
    job_id,
    title,
    department,
    seniority,
    employment_type,
    summary,
    required_skills_text,
    preferred_skills_text,
    required_tools_text,
    preferred_tools_text,
    required_education_text,
    preferred_education_text,
    required_certifications_text,
    preferred_certifications_text,
    preferred_industries_text,
    minimum_years_experience,
    preferred_years_experience,
    required_clearance,
    preferred_clearance,
    keyword_groups,
    hard_fail_rules,
    weights,
):
    return {
        "job_id": job_id,
        "title": title,
        "department": department,
        "seniority": seniority,
        "employment_type": employment_type,
        "summary": summary,
        "required_skills": parse_comma_list(required_skills_text),
        "preferred_skills": parse_comma_list(preferred_skills_text),
        "required_tools": parse_comma_list(required_tools_text),
        "preferred_tools": parse_comma_list(preferred_tools_text),
        "required_education": parse_comma_list(required_education_text),
        "preferred_education": parse_comma_list(preferred_education_text),
        "required_certifications": parse_comma_list(required_certifications_text),
        "preferred_certifications": parse_comma_list(preferred_certifications_text),
        "preferred_industries": parse_comma_list(preferred_industries_text),
        "keyword_groups": keyword_groups or {},
        "minimum_years_experience": float(minimum_years_experience),
        "preferred_years_experience": float(preferred_years_experience),
        "required_clearance": None if required_clearance == "None" else required_clearance,
        "preferred_clearance": None if preferred_clearance == "None" else preferred_clearance,
        "hard_fail_rules": hard_fail_rules or {},
        "weights": weights or {},
    }


def get_active_role_config(selected_template, base):
    live_role_config = st.session_state.get("live_role_config")
    expected_job_id = f"live_{selected_template.lower().replace(' ', '_')}"

    if live_role_config and live_role_config.get("job_id") == expected_job_id:
        return live_role_config

    return base


# ----------------------------
# Scoring
# ----------------------------
def score_all_applicants_with_config(role_config):
    applicants = get_current_applicants()
    clear_existing_scores()

    ranked_results = []
    selected_role_name = role_config.get("title", "Custom Role")

    for applicant in applicants:
        result = score_applicant(applicant, role_config)
        explanation = result.get("explanation_json", {})

        save_score_to_db(
            applicant_id=applicant["id"],
            selected_role=selected_role_name,
            result=result,
        )

        ranked_results.append(
            {
                "applicant_id": applicant["id"],
                "full_name": applicant.get("full_name", ""),
                "email": applicant.get("email", ""),
                "phone": applicant.get("phone", ""),
                "job_title": selected_role_name,
                "score": result.get("total_score", 0),
                "hard_fail": result.get("hard_fail", False),
                "strengths": explanation.get("strengths", []),
                "gaps": explanation.get("gaps", []),
                "hard_fail_reasons": explanation.get("hard_fail_reasons", []),
                "fit_label": explanation.get("fit_label", ""),
                "summary": explanation.get("summary", ""),
                "score_breakdown_json": result.get("score_breakdown_json", {}),
            }
        )

    ranked_results.sort(key=lambda x: (x["hard_fail"], -x["score"]))
    return ranked_results


# ----------------------------
# Header
# ----------------------------
st.markdown(
    """
    <div class="topbar">
        <div class="topbar-title">AI Resume Sorter</div>
        <div class="topbar-subtitle">
            Rank candidates intelligently, surface strong matches, and flag missing requirements without losing top talent.
        </div>
        <div class="hero-chip-wrap">
            <span class="hero-chip">Resume Ranking</span>
            <span class="hero-chip">Template-Based Scoring</span>
            <span class="hero-chip">PDF + CSV Imports</span>
            <span class="hero-chip">Recruiter-Friendly Review</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("## Control Center")
    st.markdown(
        '<div class="helper-text">Upload data, import applicants, score resumes, and reset the workspace.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Upload Files")

    uploaded_csv = st.file_uploader("Upload applicants CSV", type=["csv"])
    if uploaded_csv is not None:
        with open(CSV_FILE, "wb") as f:
            f.write(uploaded_csv.getbuffer())
        st.success("CSV uploaded")

    uploaded_pdfs = st.file_uploader(
        "Upload PDF resumes",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_pdfs:
        os.makedirs(PDF_FOLDER, exist_ok=True)

        for existing_file in os.listdir(PDF_FOLDER):
            existing_path = os.path.join(PDF_FOLDER, existing_file)
            if os.path.isfile(existing_path):
                try:
                    os.remove(existing_path)
                except Exception:
                    pass

        for pdf in uploaded_pdfs:
            save_path = os.path.join(PDF_FOLDER, pdf.name)
            with open(save_path, "wb") as f:
                f.write(pdf.getbuffer())

        st.success(f"{len(uploaded_pdfs)} PDF(s) uploaded")

    st.markdown("### Import Data")

    if st.button("Import Applicants CSV", use_container_width=True):
        if not os.path.exists(CSV_FILE):
            st.error("Upload a CSV first")
        else:
            try:
                result = import_applicants(CSV_FILE)
                st.success(f"Imported {result['imported']} | Skipped {result['skipped']}")
                st.rerun()
            except Exception as e:
                st.error(f"CSV import failed: {e}")

    if st.button("Import PDF Resumes", use_container_width=True):
        try:
            result = import_pdfs(company_id=1, job_opening_id=1)
            st.success(f"Imported {result['imported']} | Skipped {result['skipped']}")
            st.rerun()
        except Exception as e:
            st.error(f"PDF import failed: {e}")

    st.markdown("### Danger Zone")
    if st.button("Reset Data", use_container_width=True, type="secondary"):
        try:
            reset_database()
            clear_local_upload_files()

            for key in ["ranked_results", "selected_role", "live_role_config"]:
                if key in st.session_state:
                    del st.session_state[key]

            st.success("Applicants, scores, and uploaded files deleted")
            st.rerun()
        except Exception as e:
            st.error(f"Reset failed: {e}")


# ----------------------------
# Template Selection
# ----------------------------
st.markdown('<div class="section-title">Role Template</div>', unsafe_allow_html=True)

selected_template = st.selectbox(
    "Choose template role",
    list(JOB_ROLES.keys()),
    key="template_role_selector",
)

base = copy.deepcopy(JOB_ROLES[selected_template])
active_role_config = get_active_role_config(selected_template, base)

overview_cols = st.columns(4)
with overview_cols[0]:
    show_metric_card("Role", active_role_config.get("title", ""), "Selected scoring profile")
with overview_cols[1]:
    show_metric_card("Department", active_role_config.get("department", ""), "Role ownership")
with overview_cols[2]:
    show_metric_card(
        "Minimum Experience",
        f"{active_role_config.get('minimum_years_experience', 0)} years",
        "Baseline requirement",
    )
with overview_cols[3]:
    show_metric_card(
        "Required Clearance",
        active_role_config.get("required_clearance") or "None",
        "Mandatory screening rule",
    )

role_tab1, role_tab2 = st.tabs(["Template Snapshot", "Edit Template"])

with role_tab1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("**Summary**")
    st.write(active_role_config.get("summary", "No summary available."))

    pc1, pc2 = st.columns(2)
    with pc1:
        st.markdown("**Required Skills**")
        st.write(", ".join(active_role_config.get("required_skills", [])) or "None")
        st.markdown("**Required Tools**")
        st.write(", ".join(active_role_config.get("required_tools", [])) or "None")
        st.markdown("**Required Education**")
        st.write(", ".join(active_role_config.get("required_education", [])) or "None")
        st.markdown("**Required Certifications**")
        st.write(", ".join(active_role_config.get("required_certifications", [])) or "None")

    with pc2:
        st.markdown("**Preferred Skills**")
        st.write(", ".join(active_role_config.get("preferred_skills", [])) or "None")
        st.markdown("**Preferred Tools**")
        st.write(", ".join(active_role_config.get("preferred_tools", [])) or "None")
        st.markdown("**Preferred Industries**")
        st.write(", ".join(active_role_config.get("preferred_industries", [])) or "None")
        st.markdown("**Preferred Certifications**")
        st.write(", ".join(active_role_config.get("preferred_certifications", [])) or "None")
    st.markdown("</div>", unsafe_allow_html=True)

with role_tab2:
    st.markdown(
        '<div class="helper-text">Edit the selected template, preview it, then use Start Scoring below.</div>',
        unsafe_allow_html=True,
    )

    with st.form("edit_template_form"):
        current_config = get_active_role_config(selected_template, base)

        title = st.text_input("Role Title", value=current_config.get("title", base.get("title", "")))
        department = st.text_input("Department", value=current_config.get("department", base.get("department", "")))
        seniority = st.text_input("Seniority", value=current_config.get("seniority", base.get("seniority", "")))
        employment_type = st.text_input("Employment Type", value=current_config.get("employment_type", base.get("employment_type", "")))
        summary = st.text_area(
            "Summary",
            value=current_config.get("summary", base.get("summary", "")),
            height=110,
        )

        required_skills_text = st.text_area(
            "Required Skills (comma separated)",
            value=", ".join(current_config.get("required_skills", base.get("required_skills", []))),
        )
        preferred_skills_text = st.text_area(
            "Preferred Skills (comma separated)",
            value=", ".join(current_config.get("preferred_skills", base.get("preferred_skills", []))),
        )
        required_tools_text = st.text_area(
            "Required Tools (comma separated)",
            value=", ".join(current_config.get("required_tools", base.get("required_tools", []))),
        )
        preferred_tools_text = st.text_area(
            "Preferred Tools (comma separated)",
            value=", ".join(current_config.get("preferred_tools", base.get("preferred_tools", []))),
        )
        required_education_text = st.text_area(
            "Required Education (comma separated)",
            value=", ".join(current_config.get("required_education", base.get("required_education", []))),
        )
        preferred_education_text = st.text_area(
            "Preferred Education (comma separated)",
            value=", ".join(current_config.get("preferred_education", base.get("preferred_education", []))),
        )
        required_certifications_text = st.text_area(
            "Required Certifications (comma separated)",
            value=", ".join(current_config.get("required_certifications", base.get("required_certifications", []))),
        )
        preferred_certifications_text = st.text_area(
            "Preferred Certifications (comma separated)",
            value=", ".join(current_config.get("preferred_certifications", base.get("preferred_certifications", []))),
        )
        preferred_industries_text = st.text_area(
            "Preferred Industries (comma separated)",
            value=", ".join(current_config.get("preferred_industries", base.get("preferred_industries", []))),
        )

        c1, c2 = st.columns(2)
        with c1:
            minimum_years_experience = st.number_input(
                "Minimum Years Experience",
                min_value=0.0,
                value=float(current_config.get("minimum_years_experience", base.get("minimum_years_experience", 0))),
            )
            required_clearance = st.selectbox(
                "Required Clearance",
                ["None", "confidential", "secret", "top secret", "ts/sci"],
                index=clearance_index(current_config.get("required_clearance", base.get("required_clearance"))),
            )

        with c2:
            preferred_years_experience = st.number_input(
                "Preferred Years Experience",
                min_value=0.0,
                value=float(current_config.get("preferred_years_experience", base.get("preferred_years_experience", 0))),
            )
            preferred_clearance = st.selectbox(
                "Preferred Clearance",
                ["None", "confidential", "secret", "top secret", "ts/sci"],
                index=clearance_index(current_config.get("preferred_clearance", base.get("preferred_clearance"))),
            )

        preview_clicked = st.form_submit_button("Preview Edited Template", use_container_width=True)

        live_role_config = build_live_role_config(
            job_id=f"live_{selected_template.lower().replace(' ', '_')}",
            title=title,
            department=department,
            seniority=seniority,
            employment_type=employment_type,
            summary=summary,
            required_skills_text=required_skills_text,
            preferred_skills_text=preferred_skills_text,
            required_tools_text=required_tools_text,
            preferred_tools_text=preferred_tools_text,
            required_education_text=required_education_text,
            preferred_education_text=preferred_education_text,
            required_certifications_text=required_certifications_text,
            preferred_certifications_text=preferred_certifications_text,
            preferred_industries_text=preferred_industries_text,
            minimum_years_experience=minimum_years_experience,
            preferred_years_experience=preferred_years_experience,
            required_clearance=required_clearance,
            preferred_clearance=preferred_clearance,
            keyword_groups=base.get("keyword_groups", {}),
            hard_fail_rules=base.get("hard_fail_rules", {}),
            weights=base.get("weights", {}),
        )

        if preview_clicked:
            st.session_state["live_role_config"] = live_role_config
            st.success("Edited template preview updated. Click Start Scoring below to use it.")
            st.rerun()


# ----------------------------
# Scoring Control Bar
# ----------------------------
st.markdown('<div class="section-title">Scoring</div>', unsafe_allow_html=True)

score_col1, score_col2 = st.columns([1.15, 1])

with score_col1:
    if st.button("Start Scoring", type="primary", use_container_width=True):
        try:
            applicants = get_current_applicants()
            if not applicants:
                st.warning("No applicants found.")
            else:
                role_to_score = get_active_role_config(selected_template, base)
                ranked_results = score_all_applicants_with_config(role_to_score)
                st.session_state["ranked_results"] = ranked_results
                st.session_state["selected_role"] = role_to_score.get("title", "")
                st.success(f"Scoring completed for {role_to_score.get('title', 'Selected Role')}.")
                st.rerun()
        except Exception as e:
            st.error(f"Scoring failed: {e}")

with score_col2:
    live_role_config = st.session_state.get("live_role_config")
    expected_job_id = f"live_{selected_template.lower().replace(' ', '_')}"
    using_preview = bool(live_role_config and live_role_config.get("job_id") == expected_job_id)

    source_label = "Edited template preview" if using_preview else "Base template"
    st.markdown(
        f"""
        <div class="status-card">
            <div class="small-label">Scoring Source</div>
            <div class="big-value">{source_label}</div>
            <div class="helper-text">The current scoring run will use this version of the job template.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------
# Dashboard Overview
# ----------------------------
applicants_now = get_current_applicants()
scores_now = get_current_scores()

pass_count = 0
avg_score = 0
borderline_count = 0

if "ranked_results" in st.session_state and st.session_state["ranked_results"]:
    current_results = st.session_state["ranked_results"]
    pass_count = sum(1 for x in current_results if not x["hard_fail"])
    borderline_count = sum(
        1 for x in current_results if x["hard_fail"] and ("Strong" in x["fit_label"] or "Promising" in x["fit_label"])
    )
    avg_score = round(sum(x["score"] for x in current_results) / len(current_results), 2)

st.markdown('<div class="section-title">Dashboard Overview</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    show_metric_card("👥 Applicants in DB", len(applicants_now), "Imported candidate records")
with m2:
    show_metric_card("📊 Scores in DB", len(scores_now), "Saved evaluation records")
with m3:
    show_metric_card("✅ Passing Candidates", pass_count, "Currently qualified")
with m4:
    show_metric_card("⭐ Average Score", avg_score if avg_score else "—", f"⚠️ Borderline: {borderline_count}")


# ----------------------------
# Ranked Candidates
# ----------------------------
st.markdown('<div class="section-title">Ranked Candidates</div>', unsafe_allow_html=True)

results = st.session_state.get("ranked_results", [])

if results:
    filter_col1, filter_col2, filter_col3 = st.columns([1.2, 1, 1])
    with filter_col1:
        candidate_view = st.selectbox(
            "Candidate view",
            ["All Candidates", "Passing Only", "Borderline Only", "Failed Only"],
            key="candidate_view_filter",
        )
    with filter_col2:
        min_score_filter = st.slider("Minimum score", 0, 100, 0, 5)
    with filter_col3:
        sort_choice = st.selectbox(
            "Sort by",
            ["Best Match First", "Score Low to High"],
            key="sort_choice",
        )

    filtered_results = results.copy()

    if candidate_view == "Passing Only":
        filtered_results = [x for x in filtered_results if not x["hard_fail"]]
    elif candidate_view == "Borderline Only":
        filtered_results = [
            x for x in filtered_results
            if x["hard_fail"] and ("Strong" in x["fit_label"] or "Promising" in x["fit_label"])
        ]
    elif candidate_view == "Failed Only":
        filtered_results = [
            x for x in filtered_results
            if x["hard_fail"] and not ("Strong" in x["fit_label"] or "Promising" in x["fit_label"])
        ]

    filtered_results = [x for x in filtered_results if x["score"] >= min_score_filter]

    if sort_choice == "Score Low to High":
        filtered_results = sorted(filtered_results, key=lambda x: x["score"])
    else:
        filtered_results = sorted(filtered_results, key=lambda x: (x["hard_fail"], -x["score"]))

    if filtered_results:
        df = pd.DataFrame(filtered_results)
        df["Status"] = df.apply(lambda x: format_status(x["hard_fail"], x["fit_label"]), axis=1)
        df["Fit"] = df["fit_label"]
        df["Summary"] = df["summary"]

        display_df = df[
            ["full_name", "email", "job_title", "score", "Fit", "Status", "Summary"]
        ].rename(
            columns={
                "full_name": "Name",
                "email": "Email",
                "job_title": "Role",
                "score": "Score",
            }
        )

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        csv_export = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Ranked Results CSV",
            data=csv_export,
            file_name="ranked_candidates.csv",
            mime="text/csv",
            use_container_width=False,
        )

        st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)
        st.markdown("### Candidate Review Cards")

        for row in filtered_results:
            fit = row.get("fit_label", "")
            status = format_status(row["hard_fail"], fit)
            badge_kind = badge_kind_from_fit(fit, row["hard_fail"])
            band = score_band(row["score"], row["hard_fail"])

            st.markdown(
                f"""
                <div class="candidate-card">
                    <div style="display:flex; justify-content:space-between; gap:1rem; align-items:flex-start; flex-wrap:wrap;">
                        <div>
                            <div class="candidate-name">{row['full_name'] or 'Unnamed Candidate'}</div>
                            <div class="candidate-meta">{row['email'] or 'No email'} • {row['phone'] or 'No phone'} • {row['job_title']}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.5rem; font-weight:800; color:#f8fafc;">{row['score']}</div>
                            <div class="candidate-meta">{band}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            pill_row = pill_html(fit, badge_kind) + pill_html(status, "blue")
            st.markdown(pill_row, unsafe_allow_html=True)

            with st.expander("Open candidate details", expanded=False):
                top1, top2, top3 = st.columns(3)
                with top1:
                    st.markdown(
                        f"""
                        <div class="status-card">
                            <div class="small-label">Score</div>
                            <div class="big-value">{row['score']}</div>
                            <div class="helper-text">Overall weighted match score</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with top2:
                    st.markdown(
                        f"""
                        <div class="status-card">
                            <div class="small-label">Fit Label</div>
                            <div class="big-value">{fit}</div>
                            <div class="helper-text">AI-generated candidate classification</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with top3:
                    st.markdown(
                        f"""
                        <div class="status-card">
                            <div class="small-label">Status</div>
                            <div class="big-value">{status}</div>
                            <div class="helper-text">Pass / borderline / fail interpretation</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"""
                    <div class="summary-box">
                        <div class="small-label">Summary</div>
                        <div class="big-value" style="font-size:1rem; font-weight:650;">
                            {row.get('summary', 'No summary available.')}
                        </div>
                        <div class="helper-text">AI-generated candidate evaluation</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                left, right = st.columns(2)

                with left:
                    st.markdown("**Strengths**")
                    if row["strengths"]:
                        for item in row["strengths"]:
                            st.write(f"- {item}")
                    else:
                        st.write("None")

                with right:
                    st.markdown("**Gaps**")
                    if row["gaps"]:
                        for item in row["gaps"]:
                            st.write(f"- {item}")
                    else:
                        st.write("None")

                st.markdown("**Hard Fail Reasons**")
                if row["hard_fail_reasons"]:
                    for item in row["hard_fail_reasons"]:
                        st.write(f"- {item}")
                else:
                    st.write("None")

                with st.expander("View Score Breakdown"):
                    st.json(row["score_breakdown_json"])
    else:
        st.info("No candidates match the current filters.")
else:
    st.info("No scoring results yet. Import applicants, optionally edit the template, then click Start Scoring.")


# ----------------------------
# Debug / Database Views
# ----------------------------
st.markdown('<div class="section-title">Debug / Database Views</div>', unsafe_allow_html=True)

debug_tab1, debug_tab2 = st.tabs(["Applicants Table", "Scores Table"])

with debug_tab1:
    if st.button("Refresh Applicant List"):
        try:
            applicants = get_current_applicants()
            if applicants:
                applicants_df = pd.DataFrame(applicants)
                st.dataframe(applicants_df, use_container_width=True)
            else:
                st.warning("No applicants found in database.")
        except Exception as e:
            st.error(f"Could not load applicants: {e}")

with debug_tab2:
    if st.button("Refresh Score List"):
        try:
            scores = get_current_scores()
            if scores:
                scores_df = pd.DataFrame(scores)
                st.dataframe(scores_df, use_container_width=True)
            else:
                st.warning("No scores found in database.")
        except Exception as e:
            st.error(f"Could not load scores: {e}")