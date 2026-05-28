import sys
import os

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import tempfile
import os

# Import all pipeline modules
from src.parser import parse_from_uploaded_file
from src.cleaner import clean_resume, clean_job_description
from src.extractor import extract_skills, extract_all_skills_flat
from src.similarity import compute_match_score
from src.gap_analyzer import run_full_gap_analysis
from src.ai_feedback import generate_full_feedback

from app.ui_components import (
    render_score_card,
    render_score_breakdown,
    render_skill_chips,
    render_gap_item,
    render_coverage_bar,
    render_feedback_section
)

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="NLP Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global Styles ──────────────────────────────────────────────
st.markdown("""
    <style>
        .stApp { background-color: #0F172A; }
        .stTextArea textarea {
            background-color: #1E293B;
            color: #F1F5F9;
            border: 1px solid #334155;
        }
        .stFileUploader {
            background-color: #1E293B;
        }
        h1, h2, h3, h4 { color: #F1F5F9; }
        .stButton>button {
            background-color: #6366F1;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 32px;
            font-size: 16px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #4F46E5;
        }
    </style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────
st.markdown("""
    <div style="text-align: center; padding: 32px 0 16px 0;">
        <h1 style="font-size: 42px; color: #F1F5F9;">
            📄 NLP Resume Screener
        </h1>
        <p style="color: #94A3B8; font-size: 16px;">
            Upload your resume, paste a job description,
            and get AI-powered match analysis instantly.
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ── Input Section ──────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📎 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Supported formats: PDF, DOCX, TXT",
        type=["pdf", "docx", "txt"]
    )

with col_right:
    st.markdown("### 📋 Paste Job Description")
    jd_input = st.text_area(
        "Paste the full job description here",
        height=200,
        placeholder="We are looking for a Data Scientist..."
    )
    job_title = st.text_input(
        "Job Title (optional)",
        placeholder="e.g. Data Scientist, ML Engineer"
    )

st.divider()

# ── Analyze Button ─────────────────────────────────────────────
analyze_clicked = st.button("🔍 Analyze Resume")

# ── Pipeline ───────────────────────────────────────────────────
if analyze_clicked:
    if not uploaded_file:
        st.error("Please upload a resume file.")
        st.stop()
    if not jd_input.strip():
        st.error("Please paste a job description.")
        st.stop()

    with st.spinner("Parsing and analyzing your resume..."):

        # Step 1 — Parse
        resume_raw = parse_from_uploaded_file(uploaded_file)

        # Step 2 — Clean
        resume_clean = clean_resume(resume_raw)
        jd_clean     = clean_job_description(jd_input)

        # Step 3 — Extract
        resume_skills      = extract_skills(resume_clean)
        jd_skills          = extract_skills(jd_clean)
        resume_skills_flat = extract_all_skills_flat(resume_clean)
        jd_skills_flat     = extract_all_skills_flat(jd_clean)

        # Step 4 — Similarity
        similarity_result = compute_match_score(
            resume_clean, jd_clean,
            resume_skills_flat, jd_skills_flat
        )

        # Step 5 — Gap Analysis
        gap_analysis = run_full_gap_analysis(
            resume_skills, jd_skills
        )

        # Step 6 — AI Feedback
        feedback = generate_full_feedback(
            similarity_result=similarity_result,
            gap_analysis=gap_analysis,
            job_title=job_title or "the target role"
        )

    st.success("Analysis complete!")
    st.divider()

    # ── Results: Match Score ───────────────────────────────────
    st.markdown("## 🎯 Match Score")
    render_score_card(
        similarity_result["final_score"],
        similarity_result["match_label"]
    )
    render_score_breakdown(
        similarity_result["tfidf_score"],
        similarity_result["semantic_score"],
        similarity_result["skill_score"]
    )

    st.divider()

    # ── Results: Skills ────────────────────────────────────────
    st.markdown("## 🛠 Skill Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ Skills You Have")
        matched = gap_analysis["gap_report"]["matched"]
        all_matched = []
        for skills in matched.values():
            all_matched.extend(skills)

        if all_matched:
            render_skill_chips(all_matched, color="#10B981")
        else:
            st.info("No matched skills detected.")

    with col2:
        st.markdown("#### ❌ Skills You're Missing")
        missing = gap_analysis["gap_report"]["missing"]
        all_missing = []
        for skills in missing.values():
            all_missing.extend(skills)

        if all_missing:
            render_skill_chips(all_missing, color="#EF4444")
        else:
            st.success("No skill gaps detected!")

    st.divider()

    # ── Results: Gap Priority ──────────────────────────────────
    st.markdown("## 🚨 Priority Gaps")
    st.markdown(
        f"<p style='color:#94A3B8'>{gap_analysis['summary']}</p>",
        unsafe_allow_html=True
    )

    if gap_analysis["prioritized_gaps"]:
        for gap in gap_analysis["prioritized_gaps"]:
            render_gap_item(gap)
    else:
        st.success("No gaps found — strong match!")

    st.divider()

    # ── Results: Coverage Bars ─────────────────────────────────
    st.markdown("## 📊 Skill Category Coverage")
    for cat in gap_analysis["coverage"]:
        render_coverage_bar(
            cat["category"],
            cat["coverage_pct"],
            cat["label"]
        )

    st.divider()

    # ── Results: AI Feedback ───────────────────────────────────
    st.markdown("## 🤖 AI Career Feedback")
    sections = feedback["parsed_sections"]

    render_feedback_section(
        "Overall Assessment",
        sections["overall_assessment"],
        "📌"
    )
    render_feedback_section(
        "Strengths To Highlight",
        sections["strengths"],
        "💪"
    )
    render_feedback_section(
        "Critical Action Plan",
        sections["action_plan"],
        "🎯"
    )
    render_feedback_section(
        "Quick Wins",
        sections["quick_wins"],
        "⚡"
    )
    render_feedback_section(
        "Honest Advice",
        sections["honest_advice"],
        "🧠"
    )

    st.divider()

    # ── Raw Feedback Expander ──────────────────────────────────
    with st.expander("View Full Raw AI Feedback"):
        st.markdown(
            f"<div style='color:#F1F5F9'>{feedback['raw_feedback']}</div>",
            unsafe_allow_html=True
        )