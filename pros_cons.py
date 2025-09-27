# pros_cons.py
import streamlit as st

def pros_cons_page():
    st.title("📝 Pros & Cons of the System")
    st.write("""
    **Pros:**  
    - Fast Matching
    - Personalized Suggestions
    - Resume Skill Extraction

    **Cons:**  
    - Dependent on Resume Quality
    - Might miss soft skills
    """)
