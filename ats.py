import streamlit as st
import time
from main import extract_text_from_resume

# ATS score calculation
def calculate_ats_score(resume_text):
    skills = ["Python", "SQL", "Java", "Data Science", "Machine Learning", "Communication", "Teamwork"]
    experience_keywords = ["project", "lead", "manager", "data analysis", "engineer", "developer", "consultant"]
    education_keywords = ["degree", "university", "masters", "bachelor's", "certification"]

    skill_match = sum(1 for skill in skills if skill.lower() in resume_text.lower())
    experience_match = sum(1 for word in experience_keywords if word.lower() in resume_text.lower())
    education_match = sum(1 for word in education_keywords if word.lower() in resume_text.lower())

    ats_score = min((skill_match + experience_match + education_match) * 10, 100)

    suggestions = []

    if ats_score < 50:
        suggestions.append("🔴 **Low Score**: Add more skills, experiences, and education details.")
    elif ats_score < 80:
        suggestions.append("🟡 **Average Score**: Add certifications and strong project experiences.")
    else:
        suggestions.append("🟢 **Good Score**: Fine-tune keywords for specific job roles.")

    if skill_match == 0:
        suggestions.append("⚡ **Skills**: Add technical skills like Python, SQL, Machine Learning.")
    if experience_match == 0:
        suggestions.append("⚡ **Experience**: Mention clear projects or leadership roles.")
    if education_match == 0:
        suggestions.append("⚡ **Education**: Include degrees, certifications, or trainings.")

    suggestions.append("💡 Use strong action verbs like 'Led', 'Designed', 'Implemented'.")
    suggestions.append("💡 Keep formatting simple for better ATS parsing.")

    return ats_score, suggestions


# Main ATS checker
def ats_resume_score():
    # Custom CSS
    st.markdown("""
        <style>
        body {
            background-color: #0d0d0d;
            font-family: 'Poppins', sans-serif;
        }
        .fixed-header {
            font-size: 2.5rem;
            font-weight: 600;
            color: #ff4b5c;
            text-align: center;
            margin-bottom: 2rem;
        }
        .main-content {
            padding: 2rem;
        }
        .glass-card {
    background: rgba(255, 255, 255, 0.05);  /* faint transparent background */
    border-radius: 16px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25); /* neutral dark shadow */
    margin-top: 2rem;
    text-align: center;
}
        .score-heading {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .low { color: #ff4b5c; }
        .avg { color: #f4a261; }
        .good { color: #2ecc71; }
        .suggestions-heading {
            font-size: 1.5rem;
            font-weight: 600;
            color: #ff4b5c;
            margin-bottom: 1rem;
        }
        .suggestions-list {
            list-style: none;
            padding-left: 0;
            text-align: left;
            color: #f0f0f0;
            font-size: 1.1rem;
            margin-top: 1rem;
        }
        .suggestions-list li {
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<div class="fixed-header">🚀 ATS Score Checker</div>', unsafe_allow_html=True)

    # Main content
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # Sidebar upload
    st.sidebar.header("Upload Your Resume")
    resume_file = st.sidebar.file_uploader("📄 Upload Resume", type=["pdf", "docx"])

    if resume_file is not None:
        resume_text = extract_text_from_resume(resume_file)

        if resume_text:
            st.success("✅ Resume uploaded successfully. Analyzing...")

            with st.spinner("⏳ Calculating your ATS score..."):
                ats_score, suggestions = calculate_ats_score(resume_text)
                time.sleep(1)

            # Decide color class
            if ats_score < 50:
                score_class = "low"
                status = "Low"
            elif ats_score < 80:
                score_class = "avg"
                status = "Average"
            else:
                score_class = "good"
                status = "Good"

            # Animated Score Counter
            score_placeholder = st.empty()
            for i in range(1, ats_score + 1):
                score_placeholder.markdown(
                    f"""
                    <div class="glass-card">
                        <div class="score-heading {score_class}">📊 Your ATS Score: {i}%</div>
                        <div style="color:#bbb;font-size:1.2rem;">Status: {status}</div>
                    </div>
                    """, unsafe_allow_html=True
                )
                time.sleep(0.02)  # speed of animation

            # Suggestions Card
            suggestions_html = "<ul class='suggestions-list'>"
            for suggestion in suggestions:
                suggestions_html += f"<li>✅ {suggestion}</li>"
            suggestions_html += "</ul>"

            st.markdown(f"""
                <div class="glass-card">
                    <div class="suggestions-heading">📋 Suggestions to Improve</div>
                    {suggestions_html}
                </div>
            """, unsafe_allow_html=True)

        else:
            st.warning("⚠️ Could not extract text from the uploaded resume.")
    else:
        st.info("📤 Please upload a resume to continue.")

    st.markdown('</div>', unsafe_allow_html=True)
