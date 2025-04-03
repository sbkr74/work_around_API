from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for session management

DATABASE = r"flaskAPI/project/Competition_part3/files/quiz.db"

# Database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Initialize database (Run only once)
def init_db():
    conn = get_db()
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
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    db.close()
    return [dict(q) for q in questions]  # Convert to list of dictionaries

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('quiz'))

def reset_quiz():
    """Resets the quiz session when a new user logs in."""
    session['score'] = 0
    session["history"] = []
    session["current_index"] = 0

# User Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Username already exists! Try a different one."
        finally:
            conn.close()

    return render_template("signup.html")

# User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = username
            reset_quiz()
            session["questions"] = fetch_questions()  # Load questions
            random.shuffle(session["questions"])  # Shuffle for randomness
            return redirect(url_for("quiz"))
        else:
            msg = "Invalid username or password!"

    return render_template("login.html",msg=msg)

# Logout
@app.route("/logout")
def logout():
    session.clear()  # Clears all session data
    return redirect(url_for("login"))

# Quiz logic with Previous and Next buttons
@app.route("/quiz")
def quiz():
    if "user" not in session:
        return redirect(url_for("login"))  # Redirect if not logged in
    
    if 'score' not in session:
        session['score'] = 0  # Initialize score

    if "questions" not in session or not session["questions"]:
        return redirect(url_for("final_score"))

    # Fix: Start at index 0 instead of popping a question immediately
    # Ensure at least one question is in history before accessing index 0
    if not session["history"] and session["questions"]:
        session["history"].append(session["questions"][0])  # Add the first question
    
    if "total_questions" not in session:  # Store total questions count
        session["total_questions"] = len(session["history"])-1 + len(session["questions"])

    # Prevent IndexError
    if session["current_index"] >= len(session["history"]):
        return redirect(url_for("final_score"))

    question = session["history"][session["current_index"]]
    
    return render_template("quiz.html", question=question, score=session['score'],total_questions=session["total_questions"])

@app.route("/next", methods=["POST"])
def next_question():
    if session["current_index"] < len(session["history"]) - 1:
        session["current_index"] += 1
    elif session["questions"]:
        # Store the last popped question to allow restoring in prev_question()
        session["last_popped"] = session["questions"][-1]
        question = session["questions"].pop()
        session["history"].append(question)
        session["current_index"] = len(session["history"]) - 1
    else:
        return redirect(url_for("final_score"))

    session.modified = True
    return redirect(url_for("quiz"))

@app.route("/prev", methods=["POST"])
def prev_question():
    if session["current_index"] > 0:
        # Restore the last popped question if we moved forward previously
        if "last_popped" in session:
            session["questions"].append(session["last_popped"])
            session["history"].pop()  # Remove last added question from history
            del session["last_popped"]  # Remove the stored question reference
        
        session["current_index"] -= 1

    session.modified = True
    return redirect(url_for("quiz"))

@app.route("/submit", methods=["POST"])
def submit():
    if session["current_index"] < len(session["history"]) - 1:
        session["current_index"] += 1
    elif session["questions"]:
        question = session["questions"].pop()
        session["history"].append(question)
        session["current_index"] = len(session["history"]) - 1
    else:
        return redirect(url_for("final_score"))
    
    selected_answer = request.form.get("answer", "")
    correct_answer = request.form.get("correct_answer", "")

    if selected_answer == correct_answer:
        session['score'] += 1 
    session.modified = True
    return redirect(url_for("quiz"))

# Final Score
@app.route("/final_score")
def final_score():
    score = session.get("score")
    total_questions = len(session.get("history", []))
    # session.clear()  # Reset session after quiz ends
    if 'user' not in session:
        return redirect(url_for('login'))

    # Reset the quiz when the final score is viewed
    reset_quiz()
    return render_template("final_score.html", score=score, total_questions=total_questions-1)

# Run the app
if __name__ == "__main__":
    
    app.run(debug=True)
