import sqlite3
import sys
import os

# Get the parent directory path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from app import DATABASE as db_path

# Database connection
def get_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Initialize database (Run only once)
def init_db():
    conn = get_db(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)

    # Insert sample questions (Run once)
    sample_questions = [
        ("What is 2 + 2?", "3", "4", "5", "6", "4"),
        ("What is 3 * 3?", "6", "7", "9", "10", "9"),
        ("What is 10 / 2?", "3", "4", "5", "6", "5"),
        ("What is 5 + 3?", "6", "7", "8", "9", "8"),
        ("What is 10 - 4?", "5", "6", "7", "8", "6"),
        ("What is 2 * 6?", "10", "11", "12", "13", "12"),
        ("What is 15 / 3?", "3", "4", "5", "6", "5"),
        ("What is 9 + 1?", "8", "9", "10", "11", "10"),
    ]
    

    # Insert sample questions if the table is empty
    cursor.execute("SELECT COUNT(*) FROM questions")
    if cursor.fetchone()[0] == 0:  # ✅ Insert only if table is empty
        cursor.executemany("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer) VALUES 
            (?, ?, ?, ?, ?, ?)
        """, sample_questions)
        print("Sample questions inserted!")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")
init_db()  # Run only once to initialize database

# Fetch questions from database
def fetch_questions():
    db = get_db(db_path)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    db.close()
    return [dict(q) for q in questions]  # Convert to list of dictionaries