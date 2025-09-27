# app.py

import streamlit as st
import pandas as pd
from main import load_data, extract_text_from_resume, preprocess_data, get_recommendations, get_tfidf_matrix
from utils import init_tfidf_vectorizer
from ats import ats_resume_score
from pros_cons import pros_cons_page

# ─── 1) Page Config ───────────────────────────────────────────────────────
st.set_page_config(page_title="Job Recommender", layout="wide", initial_sidebar_state="expanded")

# ─── Inline CSS for Fixed Header and Main Content ─────────────────────────
st.markdown("""
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        background: linear-gradient(90deg, #232526, #414345);
        color: #fff;
        font-size: 2rem;
        font-weight: bold;
        padding: 1rem 2rem 1rem 2rem;
        z-index: 9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        text-align: left;
    }
    .main-content {
        margin-top: 80px;
    }
    .footer {
        margin-top: 40px;
        color: #888;
        text-align: center;
        font-size: 0.95rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# If you want to keep your external CSS for other styles, you can still load it:
with open('static/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Static Header ───────────────────────────────────────────────────────
st.markdown("<div class='fixed-header'>💼 Job Recommendation</div>", unsafe_allow_html=True)

# ─── 2) Sidebar Navigation ────────────────────────────────────────────────
st.sidebar.title("🔗 Navigation")
page = st.sidebar.radio("Go to", ["💼 Job Recommendation", "📄 ATS Resume Score"])

# ─── 3) Load Data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data_and_preprocess():
    df = load_data()
    return preprocess_data(df)

df, all_skills = load_data_and_preprocess()

# ─── 4) Main Content Based on Selection ────────────────────────────────────
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

if page == "💼 Job Recommendation":
    with st.sidebar:
        st.markdown("### 👤 Build Your Profile")
        resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])
        selected_skills = st.multiselect("💡 Select Skills", options=all_skills)
        custom_input = st.text_input("➕ Add Custom Skills (comma separated)")
        user_industry = st.selectbox("🏭 Choose Industry", df["Industry"].dropna().unique())
        user_experience = st.selectbox("📈 Experience Level", df["Experience Level"].dropna().unique())
        min_salary = st.slider("💰 Minimum Desired Salary (₹)", int(df["Salary"].min()), int(df["Salary"].max()), 50000, step=10000)
        top_n = st.slider("📌 How Many Jobs to Show?", 1, 10, 5)
        find_jobs = st.button("🔍 Find Matching Jobs")

    resume_text = extract_text_from_resume(resume_file)
    resume_skills = [s for s in all_skills if s.lower() in resume_text.lower()] if resume_text else []
    custom_skills = [s.strip() for s in custom_input.split(",") if s.strip()]
    user_skills = list(set(selected_skills + custom_skills + resume_skills))

    if find_jobs:
        if not user_skills:
            st.warning("⚠️ Please upload a resume or enter/select your skills.")
        else:
            vectorizer = init_tfidf_vectorizer()
            tfidf_matrix = get_tfidf_matrix(df, vectorizer)
            top_jobs = get_recommendations(user_skills, user_industry, user_experience, min_salary, top_n, df, vectorizer, tfidf_matrix)

            # Profile Summary Card
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #2a2a2e, #1a1a1d);
                        border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.4);'>
                <h3 style='color: #fff;'>👤 Your Profile Summary</h3>
                <ul style='list-style: none; padding-left: 0; color: #ccc; font-size: 0.95rem;'>
                    <li>🏭 <b>Industry</b>: {user_industry}</li>
                    <li>📈 <b>Experience</b>: {user_experience}</li>
                    <li>💰 <b>Desired Salary</b>: ₹{min_salary:,}</li>
                    <li>💡 <b>Skills</b>: {", ".join(user_skills)}</li>
                </ul>
                <p style='color: #aaa; font-size: 0.85rem;'>🎯 {len(resume_skills)} skills auto-detected from resume</p>
                <p style='color: #aaa; font-size: 0.85rem;'>🔎 {len(user_skills)} total skills used for matching</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("## 💼 Top Recommended Jobs")

            if top_jobs.empty:
                st.warning("❌ No matching jobs found. Try adjusting your salary or skills.")
            else:
                st.markdown("<div class='scrollable-container'>", unsafe_allow_html=True)
                for _, job in top_jobs.iterrows():
                    matched_skills = [s for s in user_skills if s.lower() in job["Required Skills"].lower()]
                    explanation = f"✅ Matched Skills: {', '.join(matched_skills)}" if matched_skills else "⚠️ No strong skill match."

                    st.markdown(f"""
                    <div class="job-card">
                        <div class="job-title">{job['Job Title']} at <span style="color:#ff5e62;">{job['Company']}</span></div>
                        <div class="job-info">📍 {job['Location']} | 💼 {job['Experience Level']} | 💰 ₹{job['Salary']:,}</div>
                        <div class="job-info"><b>Industry:</b> {job['Industry']}<br><b>Skills Required:</b> {job['Required Skills']}</div>
                        <div class="explanation">{explanation}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("💬 Was this recommendation helpful?"):
                feedback = st.radio("Your feedback:", ["👍 Yes", "👎 No"], horizontal=True)
                if feedback:
                    st.success("Thanks for your feedback!")
            with st.expander("📝 View Pros & Cons of Job Recommendation System"):
                pros_cons_page()

elif page == "📄 ATS Resume Score":
    ats_resume_score()

st.markdown("</div>", unsafe_allow_html=True)

# ─── 5) Footer ────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    TP Team 119 Dynamic Job Recommendation System
</div>
""", unsafe_allow_html=True)

