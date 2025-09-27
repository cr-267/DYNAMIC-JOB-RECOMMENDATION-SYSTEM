# main.py

import pandas as pd
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1) Load dataset
def load_data(csv_path="job_recommendation_dataset.csv"):
    return pd.read_csv(csv_path)

# 2) Extract text from resume (PDF or DOCX)
def extract_text_from_resume(uploaded_file):
    if uploaded_file is None:
        return ""
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join(page.extract_text() or "" for page in pdf_reader.pages)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return docx2txt.process(uploaded_file)
        else:
            return ""
    except Exception:
        return ""

# 3) Preprocess dataset and extract skills
def preprocess_data(df):
    df["combined_features"] = (
        df["Job Title"].fillna('') + " " +
        df["Industry"].fillna('') + " " +
        df["Required Skills"].fillna('') + " " +
        df["Experience Level"].fillna('')
    )
    all_skills = sorted({
        skill.strip()
        for skills in df["Required Skills"].dropna()
        for skill in skills.split(",")
    })
    return df, all_skills

# 4) TF-IDF matrix
def get_tfidf_matrix(df, vectorizer=None):
    if vectorizer is None:
        vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["combined_features"])
    return tfidf_matrix, vectorizer

# 5) Get top N job recommendations
def get_recommendations(user_skills, user_industry, user_experience, min_salary, top_n, df, vectorizer, tfidf_matrix):
    profile_str = " ".join(user_skills + [user_industry, user_experience])
    user_vec = vectorizer.transform([profile_str])
    df["similarity"] = cosine_similarity(user_vec, tfidf_matrix).flatten()
    lb = max(min_salary - 200000, 0)
    ub = min_salary + 300000
    candidates = df[(df["Salary"] >= lb) & (df["Salary"] <= ub) & (df["similarity"] >= 0.4)]
    return candidates.sort_values(by="similarity", ascending=False).head(top_n)