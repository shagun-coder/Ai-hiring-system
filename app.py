import streamlit as st
import fitz
import pandas as pd

from model import extract_skills, ml_score, skill_score, final_score, feedback
from db import save_data, get_all

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Hiring System",
    layout="wide"
)

# ---------------- PDF READER ----------------
def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

# ---------------- UI ----------------
st.title("🤖 AI Hiring Intelligence System ")

name = st.text_input("Candidate Name")
file = st.file_uploader("Upload Resume (PDF)")
job = st.text_area("Job Description")

if st.button("Analyze Candidate"):

    if file and job and name:

        # TEXT EXTRACTION
        resume_text = read_pdf(file)

        # AI PROCESS
        skills = extract_skills(resume_text)
        ml = ml_score(resume_text, job)
        skill = skill_score(skills, job)
        final = final_score(ml, skill)

        # SAVE
        save_data(name, skills, ml, skill, final)

        # RESULTS
        st.subheader("📊 Analysis Result")

        col1, col2, col3 = st.columns(3)

        col1.metric("ML Score", f"{ml:.2f}")
        col2.metric("Skill Score", f"{skill:.2f}")
        col3.metric("Final Score", f"{final:.2f}")

        st.write("🧠 Skills Found:", skills)

        st.subheader("🧠 AI Feedback")
        st.info(feedback(final, skills, job))

        if final > 75:
            st.success("🔥 Strong Candidate")
        elif final > 50:
            st.warning("⚠️ Medium Candidate")
        else:
            st.error("❌ Weak Candidate")

# ---------------- DASHBOARD ----------------
st.divider()
st.subheader("📈 Candidate Dashboard")

data = get_all()

if data:

    df = pd.DataFrame(data, columns=[
        "Name", "Skills", "ML Score", "Skill Score", "Final Score"
    ])

    st.bar_chart(df.set_index("Name")["Final Score"])

    st.subheader("🏆 Ranking")

    for row in sorted(data, key=lambda x: x[4], reverse=True):
        st.write(f"👤 {row[0]} | Score: {row[4]:.2f} | Skills: {row[1]}")