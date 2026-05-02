import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

SKILLS = [
    "python", "sql", "machine learning",
    "deep learning", "nlp", "pandas",
    "data analysis", "java"
]

# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    text = text.lower()
    return [s for s in SKILLS if s in text]

# ---------------- ML SCORE ----------------
def ml_score(resume, job):
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform([resume, job])
    return cosine_similarity(matrix[0], matrix[1])[0][0] * 100

# ---------------- SKILL SCORE ----------------
def skill_score(skills, job):
    job = job.lower()
    if not skills:
        return 0
    matched = [s for s in skills if s in job]
    return (len(matched) / len(skills)) * 100

# ---------------- FINAL SCORE ----------------
def final_score(ml, skill):
    return round((ml * 0.6) + (skill * 0.4), 2)

# ---------------- AI FEEDBACK ----------------
def feedback(final, skills, job):
    job = job.lower()
    missing = []

    for s in SKILLS:
        if s in job and s not in skills:
            missing.append(s)

    if final > 75:
        return "🔥 Excellent profile. Ready for job."
    elif final > 50:
        return f"⚠️ Good profile. Improve: {missing}"
    else:
        return f"❌ Weak profile. Focus on: {missing}"