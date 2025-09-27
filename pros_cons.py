# pros_cons.py
import streamlit as st

def pros_cons_page():
    st.markdown("""
    **Pros:**  
    - Fast skill-based job matching  
    - Easy to customize and expand  
    - Detects skills from resumes  

    **Cons:**  
    - Depends on dataset quality  
    - Simple TF-IDF scoring  
    - Limited to uploaded resume content  
    """)