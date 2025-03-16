from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for session management
DATABASE = "flaskAPI/project/Competition_part2/files/quiz.db"


def get_db():
    """Connects to SQLite database."""
    conn = sqlite3.connect(DATABASE)
    # conn.row_factory = sqlite3.Row  # Enables dictionary-like access
    return conn


def init_db():
    """Creates the questions table in SQLite."""
    # conn = sqlite3.connect(DATABASE)
    conn = get_db()
    cursor = conn.cursor()

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
        ("What is 5 + 3?", "6", "7", "8", "9", "8"),
        ("What is 10 - 4?", "5", "6", "7", "8", "6"),
        ("What is 2 * 6?", "10", "11", "12", "13", "12"),
        ("What is 15 / 3?", "3", "4", "5", "6", "5"),
        ("What is 9 + 1?", "8", "9", "10", "11", "10"),
    ]

    cursor.executemany("""
        INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_questions)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Run the function once to set up the database
init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

            if user:
                session['user'] = username  # Start new session
                # reset_quiz()  # Reset quiz for the new user
                return redirect(url_for('quiz'))
            else:
                return "Invalid username or password. Try again."

    return render_template('login.html')

def fetch_questions():
    """Fetch all questions from the database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    db.close()
    return list(questions)


@app.route("/")
def home():
    """Redirects to quiz if user is logged in, otherwise to login."""
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("quiz"))


@app.route("/quiz")
def quiz():
    if "questions" not in session:
        session["questions"] = fetch_questions()
        random.shuffle(session["questions"])
        session["history"] = []
        session["current_index"] = -1

    # Ensure a question is popped before accessing history
    if session["current_index"] == -1:
        question = session["questions"].pop(0)
        session["history"].append(question)
        session["current_index"] = 0  # Move to first question
    else:
        # Ensure current index is valid
        if session["current_index"] < 0 or session["current_index"] >= len(session["history"]):
            session["current_index"] = len(session["history"]) - 1  # Reset to last valid index
        
        question = session["history"][session["current_index"]]

    return render_template("index.html", question=question)

@app.route("/logout")
def logout():
    """Logs out the user and clears session."""
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
