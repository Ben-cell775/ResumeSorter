import os
import copy
import json
import re
import shutil
from datetime import datetime, date

import pandas as pd
import streamlit as st

from import_applicants import import_applicants
from pdf_import import import_pdfs
from db import supabase
from job_roles import JOB_ROLES
from scoring import score_applicant


st.set_page_config(
    page_title="HireFlow AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --bg-main: #eef6f2;
            --bg-card: #ffffff;
            --bg-soft: #f8fcf9;
            --bg-green-soft: #e8f7e7;
            --bg-blue-soft: #eef6ff;
            --bg-yellow-soft: #fff5dc;
            --bg-red-soft: #fff0f2;

            --text-main: #253746;
            --text-soft: #637a71;
            --text-muted: #7e8f98;
            --text-green: #2c6d40;
            --text-blue: #3f6290;
            --text-red: #b24652;
            --text-yellow: #946a12;

            --border: #d7e4db;
            --border-strong: #bfd4c5;
            --shadow: 0 10px 24px rgba(76, 110, 90, 0.07);
            --shadow-soft: 0 6px 18px rgba(76, 110, 90, 0.05);
        }

        html, body, [class*="css"] {
            color: var(--text-main);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(192, 242, 197, 0.30) 0%, rgba(192, 242, 197, 0) 26%),
                radial-gradient(circle at top right, rgba(183, 229, 255, 0.25) 0%, rgba(183, 229, 255, 0) 25%),
                linear-gradient(180deg, #f4faf6 0%, #edf5f1 55%, #edf4fb 100%);
        }

        .block-container {
            max-width: 1460px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        [data-testid="stHeader"] {
            background: rgba(255,255,255,0) !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f9fcfa 0%, #f3f8f5 42%, #edf4fb 100%) !important;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            color: var(--text-main) !important;
        }

        .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
        .stAlert, .stAlert *, .stCaption, .stCaption * {
            color: var(--text-main) !important;
        }

        h1, h2, h3, h4, h5 {
            color: var(--text-main) !important;
        }

        div[data-testid="stWidgetLabel"],
        div[data-testid="stWidgetLabel"] *,
        .stSelectbox label,
        .stTextInput label,
        .stTextArea label,
        .stNumberInput label,
        .stSlider label {
            color: var(--text-main) !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }

        .field-label {
            color: var(--text-main) !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.32rem !important;
            margin-top: 0.2rem !important;
            opacity: 1 !important;
            line-height: 1.2 !important;
        }

        .hero-wrap {
            background: linear-gradient(135deg, #ffffff 0%, #f7fcf8 45%, #eef8f2 100%);
            border: 1px solid var(--border);
            border-radius: 32px;
            padding: 1.25rem 1.45rem 1.15rem 1.45rem;
            box-shadow: var(--shadow);
            margin-bottom: 1.15rem;
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--text-main);
            margin: 0;
            line-height: 1.05;
        }

        .hero-subtitle {
            margin-top: 0.35rem;
            color: var(--text-soft);
            font-size: 0.98rem;
        }

        .hero-chip-wrap {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
        }

        .hero-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.38rem;
            background: linear-gradient(180deg, #d8efcf 0%, #c8e7bb 100%);
            color: #285d39 !important;
            border: 1px solid #b8d7ab;
            border-radius: 16px;
            padding: 0.45rem 0.8rem;
            font-weight: 700;
            font-size: 0.8rem;
            box-shadow: 0 4px 10px rgba(101, 145, 90, 0.08);
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 1.16rem;
            font-weight: 800;
            color: var(--text-main);
            margin-top: 0.35rem;
            margin-bottom: 0.8rem;
        }

        .section-icon {
            display: inline-flex;
            width: 1.75rem;
            height: 1.75rem;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            background: linear-gradient(180deg, #d8efcf 0%, #c6e3ba 100%);
            border: 1px solid #b7d8b0;
            color: #25673d !important;
            font-size: 0.96rem;
        }

        .metric-card, .status-card, .summary-box, .candidate-card, .panel {
            background: linear-gradient(180deg, #ffffff 0%, #fbfdfb 100%);
            border: 1px solid var(--border);
            box-shadow: var(--shadow-soft);
        }

        .metric-card {
            border-radius: 24px;
            min-height: 118px;
            padding: 1rem;
        }

        .status-card {
            border-radius: 22px;
            min-height: 110px;
            padding: 1rem;
        }

        .summary-box {
            border-radius: 20px;
            padding: 1rem;
            margin-bottom: 0.9rem;
        }

        .candidate-card {
            border-radius: 24px;
            padding: 1rem 1.05rem;
            margin-bottom: 0.85rem;
        }

        .panel {
            border-radius: 24px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .metric-label, .small-label {
            color: #6d8377 !important;
            font-size: 0.88rem;
            font-weight: 700;
            margin-bottom: 0.42rem;
        }

        .metric-value {
            color: var(--text-main) !important;
            font-size: 1.55rem;
            font-weight: 800;
            line-height: 1.1;
        }

        .metric-sub, .helper-text {
            color: var(--text-soft) !important;
            font-size: 0.84rem;
        }

        .big-value {
            color: var(--text-main) !important;
            font-size: 1.15rem;
            font-weight: 800;
        }

        .candidate-name {
            font-size: 1.06rem;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 0.12rem;
        }

        .candidate-meta {
            color: var(--text-soft);
            font-size: 0.92rem;
            margin-bottom: 0.12rem;
        }

        .candidate-score {
            text-align: right;
        }

        .candidate-score-main {
            font-size: 1.7rem;
            font-weight: 800;
            color: #2b4264;
            line-height: 1;
        }

        .candidate-score-sub {
            color: var(--text-soft);
            font-size: 0.92rem;
            margin-top: 0.35rem;
        }

        .experience-item {
            background: linear-gradient(180deg, #ffffff 0%, #fcfefd 100%);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 0.85rem 0.95rem;
            margin-bottom: 0.7rem;
        }

        .experience-company {
            color: var(--text-main) !important;
            font-size: 0.98rem;
            font-weight: 800;
            margin-bottom: 0.12rem;
        }

        .experience-role {
            color: #5e766d !important;
            font-size: 0.91rem;
            margin-bottom: 0.15rem;
        }

        .experience-dates {
            color: var(--text-muted) !important;
            font-size: 0.83rem;
        }

        .soft-info-box {
            background: linear-gradient(180deg, #edf5ff 0%, #e8f3ff 100%);
            border: 1px solid #bfd8f1;
            border-radius: 18px;
            padding: 0.9rem 1rem;
            margin-bottom: 1rem;
        }

        .soft-info-title {
            color: #2c67ad !important;
            font-weight: 800;
            font-size: 0.92rem;
            margin-bottom: 0.45rem;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.38rem 0.75rem;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.8rem;
            border: 1px solid transparent;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
        }

        .pill-green {
            background: var(--bg-green-soft);
            color: var(--text-green) !important;
            border-color: #bcdcbc;
        }

        .pill-blue {
            background: var(--bg-blue-soft);
            color: var(--text-blue) !important;
            border-color: #c9daef;
        }

        .pill-yellow {
            background: var(--bg-yellow-soft);
            color: var(--text-yellow) !important;
            border-color: #ecd897;
        }

        .pill-red {
            background: var(--bg-red-soft);
            color: var(--text-red) !important;
            border-color: #f0c6cf;
        }

        .tag-chip {
            display: inline-block;
            padding: 0.22rem 0.58rem;
            border-radius: 999px;
            background: #eef6ff;
            border: 1px solid #cadef1;
            color: #3868a6 !important;
            font-size: 0.74rem;
            margin-right: 0.28rem;
            margin-bottom: 0.35rem;
            font-weight: 600;
        }

        .bullet-card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 0.85rem;
            margin-top: 0.35rem;
        }

        .bullet-card {
            border-radius: 18px;
            padding: 0.95rem 1rem;
            border: 1px solid var(--border);
            background: #ffffff;
        }

        .bullet-card-title {
            font-size: 0.9rem;
            font-weight: 800;
            margin-bottom: 0.45rem;
        }

        .bullet-card ul {
            margin: 0;
            padding-left: 1.1rem;
        }

        .bullet-card li {
            margin-bottom: 0.25rem;
            color: var(--text-main) !important;
        }

        .bullet-card-strong {
            background: #edf8ef;
            border-color: #c7e1ca;
        }

        .bullet-card-strong .bullet-card-title {
            color: #2e6f43 !important;
        }

        .bullet-card-gap {
            background: #fff9ea;
            border-color: #eadca7;
        }

        .bullet-card-gap .bullet-card-title {
            color: #8a6a17 !important;
        }

        .bullet-card-risk {
            background: #fff2f3;
            border-color: #efc8cf;
        }

        .bullet-card-risk .bullet-card-title {
            color: #a34753 !important;
        }

        .bullet-card-rec {
            background: #eef5ff;
            border-color: #cdddf3;
        }

        .bullet-card-rec .bullet-card-title {
            color: #3e6392 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.55rem;
            background: transparent !important;
        }

        .stTabs [data-baseweb="tab"] {
            background: linear-gradient(180deg, #f2f7f3 0%, #edf3ee 100%) !important;
            color: #415a50 !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            padding: 0.62rem 1.1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 3px 8px rgba(76, 110, 90, 0.04);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(180deg, #edf6ef 0%, #e7f1e9 100%) !important;
            color: #305842 !important;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(180deg, #c7e3a8 0%, #b8d992 100%) !important;
            color: #2c4e35 !important;
            border: 1px solid #a8c981 !important;
            box-shadow: 0 6px 14px rgba(110, 154, 83, 0.12);
        }

        .stTabs [data-baseweb="tab-highlight"] {
            background: transparent !important;
            height: 0 !important;
        }

        button[data-baseweb="tab"]::after,
        button[role="tab"]::after,
        button[role="tab"]::before {
            display: none !important;
        }

        .stTextInput > div > div,
        .stTextArea > div > div,
        .stNumberInput > div,
        div[data-baseweb="input"],
        div[data-baseweb="base-input"],
        div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] {
            background: #ffffff !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            box-shadow: none !important;
            color: var(--text-main) !important;
        }

        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea,
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea,
        div[data-baseweb="select"] input {
            background: #ffffff !important;
            color: var(--text-main) !important;
            -webkit-text-fill-color: var(--text-main) !important;
            border: none !important;
            box-shadow: none !important;
        }

        .stTextInput input::placeholder,
        .stNumberInput input::placeholder,
        .stTextArea textarea::placeholder,
        div[data-baseweb="input"] input::placeholder,
        div[data-baseweb="textarea"] textarea::placeholder,
        div[data-baseweb="select"] input::placeholder {
            color: #97a6ad !important;
            -webkit-text-fill-color: #97a6ad !important;
            opacity: 1 !important;
        }

        .stTextInput > div > div:focus-within,
        .stTextArea > div > div:focus-within,
        .stNumberInput > div:focus-within,
        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="base-input"]:focus-within,
        div[data-baseweb="select"] > div:focus-within,
        div[data-baseweb="textarea"]:focus-within {
            border: 1px solid #9fcf9d !important;
            box-shadow: 0 0 0 3px rgba(114, 204, 113, 0.12) !important;
        }

        button[data-testid="stNumberInputStepUp"],
        button[data-testid="stNumberInputStepDown"] {
            background: #f8fcf9 !important;
            color: #335046 !important;
            border: none !important;
            box-shadow: none !important;
        }

        button[data-testid="stNumberInputStepUp"]:hover,
        button[data-testid="stNumberInputStepDown"]:hover {
            background: #eef6f0 !important;
            color: #244a34 !important;
        }

        div[data-baseweb="popover"] {
            background: transparent !important;
        }

        [role="listbox"],
        ul[role="listbox"],
        div[data-baseweb="menu"] {
            background: #ffffff !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            box-shadow: 0 12px 28px rgba(40, 60, 50, 0.12) !important;
            padding: 0.35rem !important;
        }

        [role="option"],
        li[role="option"],
        div[data-baseweb="menu"] li,
        div[data-baseweb="menu"] div {
            background: #ffffff !important;
            color: var(--text-main) !important;
            border-radius: 12px !important;
        }

        [role="option"] *,
        li[role="option"] *,
        div[data-baseweb="menu"] * {
            color: var(--text-main) !important;
            -webkit-text-fill-color: var(--text-main) !important;
        }

        [role="option"]:hover,
        li[role="option"]:hover,
        div[data-baseweb="menu"] li:hover {
            background: #f2f8f3 !important;
        }

        [role="option"][aria-selected="true"],
        li[role="option"][aria-selected="true"] {
            background: #e8f6e8 !important;
            color: #24583a !important;
            font-weight: 700 !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            border-radius: 16px !important;
            border: 1px solid var(--border-strong) !important;
            background: linear-gradient(180deg, #ffffff 0%, #f6faf7 100%) !important;
            color: #335046 !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 10px rgba(76, 110, 90, 0.05) !important;
            transition: all 0.18s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-1px);
            border-color: #b0ccb8 !important;
            background: linear-gradient(180deg, #fbfefc 0%, #f1f8f3 100%) !important;
        }

        .stButton > button[kind="primary"],
        div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(180deg, #46a85d 0%, #319652 100%) !important;
            color: white !important;
            border: 1px solid #2f8d4d !important;
            box-shadow: 0 8px 18px rgba(45, 140, 77, 0.18) !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: linear-gradient(180deg, #fbfefc 0%, #f2f8f4 100%) !important;
            border: 1.5px dashed #bfd7c5 !important;
            border-radius: 20px !important;
        }

        [data-testid="stFileUploaderDropzone"] * {
            color: #557066 !important;
        }

        [data-testid="stFileUploaderDropzone"] button {
            border-radius: 14px !important;
            background: linear-gradient(180deg, #ffffff 0%, #f5faf7 100%) !important;
            color: #2f5a44 !important;
            border: 1px solid #bfd7c5 !important;
            font-weight: 700 !important;
        }

        div[data-testid="stExpander"] {
            background: #ffffff !important;
            border: 1px solid var(--border) !important;
            border-radius: 20px !important;
            overflow: hidden !important;
            box-shadow: var(--shadow-soft);
        }

        div[data-testid="stExpander"] summary {
            background: #ffffff !important;
            color: var(--text-main) !important;
        }

        div[data-testid="stExpander"] summary *,
        div[data-testid="stExpanderDetails"] *,
        div[data-testid="stExpander"] .stMarkdown *,
        div[data-testid="stExpander"] p,
        div[data-testid="stExpander"] li,
        div[data-testid="stExpander"] span,
        div[data-testid="stExpander"] label {
            color: var(--text-main) !important;
            -webkit-text-fill-color: var(--text-main) !important;
        }

        div[data-testid="stForm"] {
            background: linear-gradient(180deg, #ffffff 0%, #fbfdfb 100%) !important;
            border: 1px solid var(--border) !important;
            border-radius: 24px !important;
            padding: 1rem !important;
            box-shadow: var(--shadow-soft);
        }

        div[data-testid="stTable"] table,
        div[data-testid="stTable"] th,
        div[data-testid="stTable"] td,
        div[data-testid="stDataFrame"] table,
        div[data-testid="stDataFrame"] th,
        div[data-testid="stDataFrame"] td,
        div[data-testid="stDataEditor"] table,
        div[data-testid="stDataEditor"] th,
        div[data-testid="stDataEditor"] td {
            background: #ffffff !important;
            color: var(--text-main) !important;
            border-color: var(--border) !important;
        }

        div[data-testid="stDataFrame"] *,
        div[data-testid="stDataEditor"] * {
            color: var(--text-main) !important;
        }

        .muted-note {
            color: var(--text-soft);
            font-size: 0.84rem;
        }

        .divider-space {
            height: 0.35rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

PDF_FOLDER = "incoming_resumes"
CSV_FILE = "applicants.csv"


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


def parse_comma_list(text):
    if not text:
        return []
    return [x.strip() for x in text.split(",") if x.strip()]


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
        "green": "pill pill-green",
        "red": "pill pill-red",
        "yellow": "pill pill-yellow",
        "blue": "pill pill-blue",
    }.get(kind, "pill pill-blue")
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


def safe_json_loads(value):
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        return {"root": value}
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return {}
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
            if isinstance(parsed, list):
                return {"root": parsed}
        except Exception:
            return {}
    return {}


def normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    return str(value).strip()


def pick_first_nonempty(item, keys):
    for key in keys:
        value = item.get(key)
        if isinstance(value, list):
            value = ", ".join([str(v).strip() for v in value if str(v).strip()])
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def parse_resume_date(value):
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    lowered = text.lower().strip()
    if lowered in {"present", "current", "now", "today"}:
        today = date.today()
        return date(today.year, today.month, 1)

    text = re.sub(r"\s+", " ", text)
    text = text.replace(".", "")
    text = text.replace("Sept", "Sep")

    formats = [
        "%b %Y",
        "%B %Y",
        "%m/%Y",
        "%m-%Y",
        "%Y-%m",
        "%Y/%m",
        "%Y",
        "%m/%d/%Y",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            if fmt == "%Y":
                return date(dt.year, 1, 1)
            return date(dt.year, dt.month, 1)
        except Exception:
            pass

    month_match = re.search(
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})",
        lowered,
    )
    if month_match:
        month_map = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
        }
        return date(int(month_match.group(2)), month_map[month_match.group(1)], 1)

    year_match = re.fullmatch(r"\d{4}", lowered)
    if year_match:
        return date(int(lowered), 1, 1)

    return None


def months_between(start_date, end_date):
    if not start_date or not end_date:
        return None
    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    return max(0, months)


def format_months(months):
    if months is None:
        return "Unknown duration"

    years = months // 12
    remaining_months = months % 12

    if years > 0 and remaining_months > 0:
        return f"{years} yr {remaining_months} mo"
    if years > 0:
        return f"{years} yr" if years == 1 else f"{years} yrs"
    if remaining_months > 0:
        return f"{remaining_months} mo"
    return "Less than 1 mo"


def format_date_label(value):
    parsed = parse_resume_date(value)
    if parsed:
        return parsed.strftime("%b %Y")

    text = normalize_text(value)
    return text if text else "Unknown"


def clean_date_range_text(start_value, end_value):
    start_label = format_date_label(start_value)
    end_label = format_date_label(end_value)

    end_lower = normalize_text(end_value).lower()
    if end_lower in {"present", "current", "now", "today"}:
        end_label = "Present"

    return f"{start_label} - {end_label}"


def infer_duration_from_entry(entry):
    start_value = pick_first_nonempty(entry, ["start_date", "start", "from", "date_start"])
    end_value = pick_first_nonempty(entry, ["end_date", "end", "to", "date_end"])

    if not end_value:
        end_value = "Present"

    start_dt = parse_resume_date(start_value)
    end_dt = parse_resume_date(end_value)

    if end_value.lower() in {"present", "current", "now", "today"}:
        today = date.today()
        end_dt = date(today.year, today.month, 1)

    months = months_between(start_dt, end_dt)
    return months, start_value, end_value


def try_extract_experience_section(parsed_resume):
    if not isinstance(parsed_resume, dict):
        return []

    candidate_keys = [
        "professional_experience",
        "work_experience",
        "experience",
        "employment_history",
        "employment",
        "career_history",
        "positions",
        "jobs",
        "work_history",
    ]

    for key in candidate_keys:
        section = parsed_resume.get(key)
        if isinstance(section, list) and section:
            return section

    root = parsed_resume.get("root")
    if isinstance(root, list):
        for item in root:
            if isinstance(item, dict):
                maybe_entries = try_extract_experience_section(item)
                if maybe_entries:
                    return maybe_entries

    return []


def normalize_experience_entries(raw_entries):
    normalized = []

    for entry in raw_entries:
        if not isinstance(entry, dict):
            continue

        company = pick_first_nonempty(
            entry,
            ["company", "company_name", "employer", "organization", "org", "client"]
        )
        title = pick_first_nonempty(
            entry,
            ["title", "job_title", "role", "position", "designation"]
        )

        months, start_value, end_value = infer_duration_from_entry(entry)

        if not company and not title and not start_value and not end_value:
            continue

        normalized.append(
            {
                "company": company or "Unknown Company",
                "title": title or "Unknown Title",
                "start": start_value,
                "end": end_value if end_value else "Present",
                "months": months,
                "duration_label": format_months(months),
                "date_range_label": clean_date_range_text(start_value, end_value if end_value else "Present"),
                "description": pick_first_nonempty(
                    entry,
                    ["summary", "description", "details", "highlights"]
                ),
            }
        )

    normalized.sort(
        key=lambda x: parse_resume_date(x["end"]) or date(1900, 1, 1),
        reverse=True
    )

    return normalized


def fallback_experience_from_text(resume_text):
    text = normalize_text(resume_text)
    if not text:
        return []

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    experience_entries = []

    date_range_pattern = re.compile(
        r"(?i)"
        r"((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{4}|\d{4})"
        r"\s*[-–—to]+\s*"
        r"((?:present|current|now|today|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{4}|\d{4}))"
    )

    for i, line in enumerate(lines):
        if date_range_pattern.search(line):
            company = ""
            title = ""

            if i > 0:
                previous = lines[i - 1]
                if " at " in previous.lower():
                    parts = re.split(r"(?i)\s+at\s+", previous, maxsplit=1)
                    if len(parts) == 2:
                        title = parts[0].strip()
                        company = parts[1].strip()
                    else:
                        title = previous
                else:
                    title = previous

            if i > 1 and not company:
                maybe_company = lines[i - 2]
                if len(maybe_company) < 80:
                    company = maybe_company

            match = date_range_pattern.search(line)
            start_val = match.group(1) if match else ""
            end_val = match.group(2) if match else "Present"

            entry = {
                "company": company or "Unknown Company",
                "title": title or "Unknown Title",
                "start_date": start_val,
                "end_date": end_val,
            }
            experience_entries.append(entry)

    return normalize_experience_entries(experience_entries)


def extract_experience_data(applicant):
    parsed_resume = safe_json_loads(applicant.get("parsed_resume_json"))
    resume_text = applicant.get("resume_text", "")

    raw_entries = try_extract_experience_section(parsed_resume)
    normalized = normalize_experience_entries(raw_entries)

    if not normalized:
        normalized = fallback_experience_from_text(resume_text)

    total_known_months = sum(item["months"] for item in normalized if item["months"] is not None)
    total_known_years = round(total_known_months / 12, 1) if total_known_months else 0

    if normalized:
        short_parts = []
        for item in normalized[:4]:
            short_parts.append(
                f"{item['title']} - {item['company']} ({item['duration_label']})"
            )
        experience_summary = "; ".join(short_parts)
    else:
        experience_summary = "No structured professional experience found."

    return {
        "entries": normalized,
        "total_months": total_known_months,
        "total_years": total_known_years,
        "summary": experience_summary,
    }


def normalize_bullet_list(items, fallback="None clearly identified"):
    cleaned = []
    for item in items or []:
        text = normalize_text(item)
        if text:
            cleaned.append(text)
    return cleaned if cleaned else [fallback]


def build_upgraded_explanation(row):
    strengths = normalize_bullet_list(row.get("strengths", []), fallback="No major strengths clearly identified")
    gaps = normalize_bullet_list(row.get("gaps", []), fallback="No major gaps clearly identified")
    hard_fail_reasons = normalize_bullet_list(row.get("hard_fail_reasons", []), fallback="No major risk flags")

    score = row.get("score", 0)
    hard_fail = row.get("hard_fail", False)
    fit = row.get("fit_label", "")
    experience_years = row.get("experience_total_years", 0)
    role = row.get("job_title", "selected role")

    strengths_short = ", ".join(strengths[:3])
    gaps_short = ", ".join(gaps[:2])

    if hard_fail:
        if score >= 85:
            recommendation = (
                f"Strong profile overall, but not currently recommended for {role} until the missing requirement(s) are clarified or addressed."
            )
        else:
            recommendation = (
                f"Not recommended for {role} in its current form. Best use is manual review only if this candidate brings a special background or adjacent fit."
            )
    else:
        if score >= 85:
            recommendation = (
                f"Strong recommendation to move forward for {role}. Candidate appears to meet the core profile with solid alignment."
            )
        elif score >= 70:
            recommendation = (
                f"Recommended to move forward for {role}, with interview time focused on validating the weaker areas."
            )
        elif score >= 50:
            recommendation = (
                f"Possible fit for {role}, but should be reviewed carefully before advancing."
            )
        else:
            recommendation = (
                f"Limited match for {role}. Move forward only if the talent pool is thin or the role requirements are flexible."
            )

    concise_summary = (
        f"{fit or 'Candidate'} with {experience_years} years of identified experience. "
        f"Strong on {strengths_short.lower()}. "
        f"Main concern areas: {gaps_short.lower()}."
    )

    return {
        "summary": concise_summary,
        "strong_on": strengths,
        "missing_weaker_on": gaps,
        "risk": hard_fail_reasons if hard_fail_reasons[0] != "No major risk flags" else gaps,
        "recommendation": recommendation,
    }


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


def icon_title(icon, text):
    return f'<div class="section-title"><span class="section-icon">{icon}</span>{text}</div>'


def render_template_chips(title, items):
    st.markdown(f"**{title}**")
    if items:
        chips = "".join([f'<span class="tag-chip">{str(item)}</span>' for item in items])
        st.markdown(chips, unsafe_allow_html=True)
    else:
        st.write("None")


def build_ranked_summary_df(filtered_results):
    rows = []
    for row in filtered_results:
        upgraded = row.get("upgraded_explanation", {})
        summary = upgraded.get("summary", row.get("summary", "")) or ""
        if len(summary) > 95:
            summary = summary[:95] + "..."

        rows.append({
            "Name": row.get("full_name", ""),
            "Role": row.get("job_title", ""),
            "Score": f"{row.get('score', 0):.1f}",
            "Experience": f"{row.get('experience_total_years', 0)} yrs",
            "Fit": row.get("fit_label", ""),
            "Status": format_status(row.get("hard_fail", False), row.get("fit_label", "")),
            "Recommendation": summary,
        })
    return pd.DataFrame(rows)


def score_one_candidate_against_all_roles(applicant):
    role_matches = []

    for role_name, role_config in JOB_ROLES.items():
        try:
            result = score_applicant(applicant, role_config)
            explanation = result.get("explanation_json", {})

            temp_row = {
                "job_title": role_name,
                "score": result.get("total_score", 0),
                "hard_fail": result.get("hard_fail", False),
                "fit_label": explanation.get("fit_label", ""),
                "summary": explanation.get("summary", ""),
                "strengths": explanation.get("strengths", []),
                "gaps": explanation.get("gaps", []),
                "hard_fail_reasons": explanation.get("hard_fail_reasons", []),
                "experience_total_years": 0,
            }

            upgraded = build_upgraded_explanation(temp_row)

            role_matches.append(
                {
                    "role_name": role_name,
                    "score": result.get("total_score", 0),
                    "hard_fail": result.get("hard_fail", False),
                    "fit_label": explanation.get("fit_label", ""),
                    "summary": explanation.get("summary", ""),
                    "strengths": explanation.get("strengths", []),
                    "gaps": explanation.get("gaps", []),
                    "hard_fail_reasons": explanation.get("hard_fail_reasons", []),
                    "upgraded_explanation": upgraded,
                }
            )
        except Exception:
            continue

    role_matches.sort(key=lambda x: (x["hard_fail"], -x["score"]))
    return role_matches


def build_multi_role_summary(applicants):
    rows = []

    for applicant in applicants:
        role_matches = score_one_candidate_against_all_roles(applicant)
        if not role_matches:
            continue

        best = role_matches[0]
        best_summary = best.get("upgraded_explanation", {}).get("summary", best.get("summary", ""))

        rows.append(
            {
                "Candidate": applicant.get("full_name", "Unnamed Candidate"),
                "Email": applicant.get("email", ""),
                "Best Role Match": best.get("role_name", ""),
                "Best Score": best.get("score", 0),
                "Best Fit Label": best.get("fit_label", ""),
                "Status": format_status(best.get("hard_fail", False), best.get("fit_label", "")),
                "Recommendation": best_summary,
            }
        )

    return pd.DataFrame(rows)


def score_all_applicants_with_config(role_config):
    applicants = get_current_applicants()
    clear_existing_scores()

    ranked_results = []
    selected_role_name = role_config.get("title", "Custom Role")

    for applicant in applicants:
        result = score_applicant(applicant, role_config)
        explanation = result.get("explanation_json", {})
        experience_data = extract_experience_data(applicant)

        row = {
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
            "experience_summary": experience_data["summary"],
            "experience_entries": experience_data["entries"],
            "experience_total_years": experience_data["total_years"],
            "experience_total_months": experience_data["total_months"],
        }

        row["upgraded_explanation"] = build_upgraded_explanation(row)

        save_score_to_db(
            applicant_id=applicant["id"],
            selected_role=selected_role_name,
            result=result,
        )

        ranked_results.append(row)

    ranked_results.sort(key=lambda x: (x["hard_fail"], -x["score"]))
    return ranked_results


def render_recruiter_summary_cards(upgraded):
    strong_on_items = upgraded.get("strong_on", [])
    weaker_on_items = upgraded.get("missing_weaker_on", [])
    risk_items = upgraded.get("risk", [])
    recommendation_text = upgraded.get("recommendation", "No recommendation available.")

    strong_on_html = "".join([f"<li>{item}</li>" for item in strong_on_items]) if strong_on_items else "<li>None clearly identified</li>"
    weaker_on_html = "".join([f"<li>{item}</li>" for item in weaker_on_items]) if weaker_on_items else "<li>None clearly identified</li>"
    risk_html = "".join([f"<li>{item}</li>" for item in risk_items]) if risk_items else "<li>No major risk flags</li>"

    st.markdown(
        f"""
        <div class="summary-box">
            <div class="small-label">Recruiter Summary</div>
            <div class="bullet-card-grid">
                <div class="bullet-card bullet-card-strong">
                    <div class="bullet-card-title">✅ Strong On</div>
                    <ul>{strong_on_html}</ul>
                </div>
                <div class="bullet-card bullet-card-gap">
                    <div class="bullet-card-title">🟡 Missing / Weaker On</div>
                    <ul>{weaker_on_html}</ul>
                </div>
                <div class="bullet-card bullet-card-risk">
                    <div class="bullet-card-title">⚠ Risk</div>
                    <ul>{risk_html}</ul>
                </div>
                <div class="bullet-card bullet-card-rec">
                    <div class="bullet-card-title">📌 Recommendation</div>
                    <ul><li>{recommendation_text}</li></ul>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-title">🌿 HireFlow AI</div>
        <div class="hero-subtitle">
            Bright, recruiter-friendly candidate review with role-based scoring, clean summaries, and professional experience timelines.
        </div>
        <div class="hero-chip-wrap">
            <span class="hero-chip">✅ Resume Ranking</span>
            <span class="hero-chip">⚙️ Template-Based Scoring</span>
            <span class="hero-chip">🧾 Professional Experience View</span>
            <span class="hero-chip">📄 PDF + CSV Imports</span>
            <span class="hero-chip">🤝 Recruiter-Friendly Review</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Control Center")
    st.markdown(
        '<div class="helper-text">Upload data, import applicants, score resumes, and reset the workspace.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
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

    st.markdown("---")
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

    st.markdown("---")
    st.markdown("### Danger Zone")
    st.caption("Deletes all applicants, scores, and uploaded files.")

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


st.markdown(icon_title("📋", "Role Template"), unsafe_allow_html=True)

st.markdown('<div class="field-label">Choose template role</div>', unsafe_allow_html=True)
selected_template = st.selectbox(
    "Choose template role",
    list(JOB_ROLES.keys()),
    key="template_role_selector",
    label_visibility="collapsed",
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
    st.markdown('<div class="soft-info-box">', unsafe_allow_html=True)
    st.markdown('<div class="soft-info-title">📘 Template Summary</div>', unsafe_allow_html=True)
    st.write(active_role_config.get("summary", "No summary available."))
    st.markdown("</div>", unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    with left_col:
        render_template_chips("Required Skills", active_role_config.get("required_skills", []))
        render_template_chips("Required Tools", active_role_config.get("required_tools", []))
        render_template_chips("Required Education", active_role_config.get("required_education", []))
        render_template_chips("Required Certifications", active_role_config.get("required_certifications", []))

    with right_col:
        render_template_chips("Preferred Skills", active_role_config.get("preferred_skills", []))
        render_template_chips("Preferred Tools", active_role_config.get("preferred_tools", []))
        render_template_chips("Preferred Industries", active_role_config.get("preferred_industries", []))
        render_template_chips("Preferred Certifications", active_role_config.get("preferred_certifications", []))

with role_tab2:
    st.markdown(
        '<div class="helper-text">Edit the selected template, preview it, then use Start Scoring below.</div>',
        unsafe_allow_html=True,
    )

    with st.form("edit_template_form"):
        current_config = get_active_role_config(selected_template, base)

        st.markdown('<div class="field-label">Role Title</div>', unsafe_allow_html=True)
        title = st.text_input("Role Title", value=current_config.get("title", base.get("title", "")), label_visibility="collapsed")

        st.markdown('<div class="field-label">Department</div>', unsafe_allow_html=True)
        department = st.text_input("Department", value=current_config.get("department", base.get("department", "")), label_visibility="collapsed")

        st.markdown('<div class="field-label">Seniority</div>', unsafe_allow_html=True)
        seniority = st.text_input("Seniority", value=current_config.get("seniority", base.get("seniority", "")), label_visibility="collapsed")

        st.markdown('<div class="field-label">Employment Type</div>', unsafe_allow_html=True)
        employment_type = st.text_input("Employment Type", value=current_config.get("employment_type", base.get("employment_type", "")), label_visibility="collapsed")

        st.markdown('<div class="field-label">Summary</div>', unsafe_allow_html=True)
        summary = st.text_area(
            "Summary",
            value=current_config.get("summary", base.get("summary", "")),
            height=110,
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Required Skills (comma separated)</div>', unsafe_allow_html=True)
        required_skills_text = st.text_area(
            "Required Skills (comma separated)",
            value=", ".join(current_config.get("required_skills", base.get("required_skills", []))),
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Preferred Skills (comma separated)</div>', unsafe_allow_html=True)
        preferred_skills_text = st.text_area(
            "Preferred Skills (comma separated)",
            value=", ".join(current_config.get("preferred_skills", base.get("preferred_skills", []))),
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Required Tools (comma separated)</div>', unsafe_allow_html=True)
        required_tools_text = st.text_area(
            "Required Tools (comma separated)",
            value=", ".join(current_config.get("required_tools", base.get("required_tools", []))),
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Preferred Tools (comma separated)</div>', unsafe_allow_html=True)
        preferred_tools_text = st.text_area(
            "Preferred Tools (comma separated)",
            value=", ".join(current_config.get("preferred_tools", base.get("preferred_tools", []))),
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Required Education (comma separated)</div>', unsafe_allow_html=True)
        required_education_text = st.text_area(
            "Required Education (comma separated)",
            value=", ".join(current_config.get("required_education", base.get("required_education", []))),
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Preferred Education (comma separated)</div>', unsafe_allow_html=True)
        preferred_education_text = st.text_area(
            "Preferred Education (comma separated)",
            value=", ".join(current_config.get("preferred_education", base.get("preferred_education", []))),
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Required Certifications (comma separated)</div>', unsafe_allow_html=True)
        required_certifications_text = st.text_area(
            "Required Certifications (comma separated)",
            value=", ".join(current_config.get("required_certifications", base.get("required_certifications", []))),
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Preferred Certifications (comma separated)</div>', unsafe_allow_html=True)
        preferred_certifications_text = st.text_area(
            "Preferred Certifications (comma separated)",
            value=", ".join(current_config.get("preferred_certifications", base.get("preferred_certifications", []))),
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Preferred Industries (comma separated)</div>', unsafe_allow_html=True)
        preferred_industries_text = st.text_area(
            "Preferred Industries (comma separated)",
            value=", ".join(current_config.get("preferred_industries", base.get("preferred_industries", []))),
            label_visibility="collapsed",
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="field-label">Minimum Years Experience</div>', unsafe_allow_html=True)
            minimum_years_experience = st.number_input(
                "Minimum Years Experience",
                min_value=0.0,
                value=float(current_config.get("minimum_years_experience", base.get("minimum_years_experience", 0))),
                label_visibility="collapsed",
            )

            st.markdown('<div class="field-label">Required Clearance</div>', unsafe_allow_html=True)
            required_clearance = st.selectbox(
                "Required Clearance",
                ["None", "confidential", "secret", "top secret", "ts/sci"],
                index=clearance_index(current_config.get("required_clearance", base.get("required_clearance"))),
                label_visibility="collapsed",
            )

        with c2:
            st.markdown('<div class="field-label">Preferred Years Experience</div>', unsafe_allow_html=True)
            preferred_years_experience = st.number_input(
                "Preferred Years Experience",
                min_value=0.0,
                value=float(current_config.get("preferred_years_experience", base.get("preferred_years_experience", 0))),
                label_visibility="collapsed",
            )

            st.markdown('<div class="field-label">Preferred Clearance</div>', unsafe_allow_html=True)
            preferred_clearance = st.selectbox(
                "Preferred Clearance",
                ["None", "confidential", "secret", "top secret", "ts/sci"],
                index=clearance_index(current_config.get("preferred_clearance", base.get("preferred_clearance"))),
                label_visibility="collapsed",
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


st.markdown(icon_title("⚡", "Scoring"), unsafe_allow_html=True)

score_col1, score_col2 = st.columns([1.15, 1])

with score_col1:
    if st.button("🚀 Start Scoring", type="primary", use_container_width=True):
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

    st.markdown('<div class="muted-note">Score all applicants against this role template</div>', unsafe_allow_html=True)

with score_col2:
    live_role_config = st.session_state.get("live_role_config")
    expected_job_id = f"live_{selected_template.lower().replace(' ', '_')}"
    using_preview = bool(live_role_config and live_role_config.get("job_id") == expected_job_id)

    source_label = "Edited template preview" if using_preview else "Base template"
    st.markdown(
        f"""
        <div class="soft-info-box" style="height:100%;">
            <div class="soft-info-title">ℹ Scoring Source</div>
            <div class="big-value">{source_label}</div>
            <div class="helper-text">The current scoring run will use this version of the job template.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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

st.markdown(icon_title("📊", "Dashboard Overview"), unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    show_metric_card("👥 Applicants in DB", len(applicants_now), "Imported candidate records")
with m2:
    show_metric_card("📚 Scores in DB", len(scores_now), "Saved evaluation records")
with m3:
    show_metric_card("✅ Passing Candidates", pass_count, "Currently qualified")
with m4:
    show_metric_card("⭐ Average Score", avg_score if avg_score else "—", f"⚠ Borderline: {borderline_count}")


st.markdown(icon_title("🏆", "Ranked Candidates"), unsafe_allow_html=True)

results = st.session_state.get("ranked_results", [])

if results:
    filter_col1, filter_col2, filter_col3 = st.columns([1.2, 1, 1])

    with filter_col1:
        st.markdown('<div class="field-label">Candidate view</div>', unsafe_allow_html=True)
        candidate_view = st.selectbox(
            "Candidate view",
            ["All Candidates", "Passing Only", "Borderline Only", "Failed Only"],
            key="candidate_view_filter",
            label_visibility="collapsed",
        )

    with filter_col2:
        st.markdown('<div class="field-label">Minimum score</div>', unsafe_allow_html=True)
        min_score_filter = st.slider("Minimum score", 0, 100, 0, 5, label_visibility="collapsed")

    with filter_col3:
        st.markdown('<div class="field-label">Sort by</div>', unsafe_allow_html=True)
        sort_choice = st.selectbox(
            "Sort by",
            ["Best Match First", "Score Low to High"],
            key="sort_choice",
            label_visibility="collapsed",
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
        summary_df = build_ranked_summary_df(filtered_results)
        st.table(summary_df)

        csv_export = summary_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Ranked Results CSV",
            data=csv_export,
            file_name="ranked_candidates.csv",
            mime="text/csv",
        )

        st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)
        st.markdown("### Candidate Review Cards")

        for row in filtered_results:
            fit = row.get("fit_label", "")
            status = format_status(row["hard_fail"], fit)
            badge_kind = badge_kind_from_fit(fit, row["hard_fail"])
            band = score_band(row["score"], row["hard_fail"])
            total_exp_years = row.get("experience_total_years", 0)
            upgraded = row.get("upgraded_explanation", {})

            st.markdown(
                f"""
                <div class="candidate-card">
                    <div style="display:flex; justify-content:space-between; gap:1rem; align-items:flex-start; flex-wrap:wrap;">
                        <div>
                            <div class="candidate-name">{row['full_name'] or 'Unnamed Candidate'}</div>
                            <div class="candidate-meta">{row['email'] or 'No email'} • {row['phone'] or 'No phone'} • {row['job_title']}</div>
                            <div class="candidate-meta">Estimated professional experience: {total_exp_years} years</div>
                        </div>
                        <div class="candidate-score">
                            <div class="candidate-score-main">{row['score']:.1f}</div>
                            <div class="candidate-score-sub">{band}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                pill_html(fit, badge_kind) + pill_html(status, "blue"),
                unsafe_allow_html=True,
            )

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

                render_recruiter_summary_cards(upgraded)

                st.markdown(
                    f"""
                    <div class="summary-box">
                        <div class="small-label">Professional Experience Summary</div>
                        <div class="big-value" style="font-size:1rem; font-weight:650;">
                            {row.get('experience_summary', 'No professional experience found.')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="summary-box">
                        <div class="small-label">Estimated Total Professional Experience</div>
                        <div class="big-value" style="font-size:1.02rem; font-weight:780;">
                            {row.get('experience_total_years', 0)} years
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("**Professional Experience Timeline**")
                experience_entries = row.get("experience_entries", [])

                if experience_entries:
                    for exp in experience_entries:
                        st.markdown(
                            f"""
                            <div class="experience-item">
                                <div class="experience-company">{exp.get('company', 'Unknown Company')}</div>
                                <div class="experience-role">{exp.get('title', 'Unknown Title')}</div>
                                <div class="experience-dates">
                                    {exp.get('date_range_label', 'Unknown dates')} • {exp.get('duration_label', 'Unknown duration')}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.write("No professional experience entries were found in the parsed resume.")

                with st.expander("View Raw Score Breakdown"):
                    st.json(row["score_breakdown_json"])
    else:
        st.info("No candidates match the current filters.")
else:
    st.info("No scoring results yet. Import applicants, optionally edit the template, then click Start Scoring.")


st.markdown(icon_title("🧠", "Multi-Role Candidate Matching"), unsafe_allow_html=True)
st.markdown(
    '<div class="helper-text">See which role each candidate fits best across all templates.</div>',
    unsafe_allow_html=True,
)

multi_col1, multi_col2 = st.columns([1, 2])

with multi_col1:
    run_multi_role = st.button("Run Multi-Role Scoring", use_container_width=True)

with multi_col2:
    st.markdown(
        '<div class="muted-note">This checks every candidate against every role template in your system.</div>',
        unsafe_allow_html=True,
    )

if run_multi_role:
    applicants_for_multi = get_current_applicants()

    if not applicants_for_multi:
        st.warning("No applicants found.")
    else:
        multi_role_df = build_multi_role_summary(applicants_for_multi)

        if multi_role_df.empty:
            st.info("No multi-role matches could be generated.")
        else:
            st.table(multi_role_df)

            multi_csv = multi_role_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Multi-Role Matches CSV",
                data=multi_csv,
                file_name="multi_role_candidate_matches.csv",
                mime="text/csv",
            )

            st.markdown("### Candidate-by-Candidate Role Breakdown")

            for applicant in applicants_for_multi:
                role_matches = score_one_candidate_against_all_roles(applicant)
                if not role_matches:
                    continue

                best_match = role_matches[0]

                with st.expander(
                    f"{applicant.get('full_name', 'Unnamed Candidate')} — Best Match: {best_match['role_name']} ({best_match['score']})",
                    expanded=False,
                ):
                    for match in role_matches[:5]:
                        fit = match.get("fit_label", "")
                        status = format_status(match.get("hard_fail", False), fit)
                        badge_kind = badge_kind_from_fit(fit, match.get("hard_fail", False))
                        upgraded = match.get("upgraded_explanation", {})

                        st.markdown(
                            f"""
                            <div class="summary-box">
                                <div class="small-label">{match['role_name']}</div>
                                <div class="big-value" style="font-size:1.05rem;">Score: {match['score']}</div>
                                <div style="margin-top:0.5rem;">
                                    {pill_html(fit, badge_kind)}
                                    {pill_html(status, "blue")}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        render_recruiter_summary_cards(upgraded)


st.markdown(icon_title("🛠", "Debug / Database Views"), unsafe_allow_html=True)

debug_tab1, debug_tab2 = st.tabs(["Applicants Table", "Scores Table"])

with debug_tab1:
    if st.button("Refresh Applicant List"):
        try:
            applicants = get_current_applicants()
            if applicants:
                applicants_df = pd.DataFrame(applicants)
                st.table(applicants_df)
            else:
                st.info("No applicants found in database.")
        except Exception as e:
            st.error(f"Could not load applicants: {e}")

with debug_tab2:
    if st.button("Refresh Score List"):
        try:
            scores = get_current_scores()
            if scores:
                scores_df = pd.DataFrame(scores)
                st.table(scores_df)
            else:
                st.info("No scores found in database.")
        except Exception as e:
            st.error(f"Could not load scores: {e}")