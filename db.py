import sqlite3

conn = sqlite3.connect("hr.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    name TEXT,
    skills TEXT,
    ml_score REAL,
    skill_score REAL,
    final_score REAL
)
""")
conn.commit()

def save_data(name, skills, ml, skill, final):
    cursor.execute("""
    INSERT INTO candidates VALUES (?, ?, ?, ?, ?)
    """, (name, ", ".join(skills), ml, skill, final))
    conn.commit()

def get_all():
    cursor.execute("SELECT * FROM candidates")
    return cursor.fetchall()