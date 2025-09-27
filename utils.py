# utils.py

from sklearn.feature_extraction.text import TfidfVectorizer

# This can be expanded with any helper functions if needed later
def init_tfidf_vectorizer():
    return TfidfVectorizer(stop_words="english")
