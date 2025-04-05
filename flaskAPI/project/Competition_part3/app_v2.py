from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
DATABASE = r"flaskAPI/project/Competition_part3/files/quiz.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_questions():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    db.close()
    return [dict(q) for q in questions]

def reset_quiz():
    session['score'] = 0
    session['history'] = []
    session['current_index'] = 0
    session['answers'] = {}  # Stores user's chosen answers

def update_score(question_id, new_answer):
    correct_answer = session['answers'].get(question_id, {}).get('correct')
    prev_answer = session['answers'].get(question_id, {}).get('user')
    
    if prev_answer == correct_answer:  # If previously correct, decrease score
        session['score'] -= 1
    
    if new_answer == correct_answer:  # If now correct, increase score
        session['score'] += 1
    
    session['answers'][question_id] = {'user': new_answer, 'correct': correct_answer}

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('quiz'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["username"] = username
            reset_quiz()
            session["questions"] = fetch_questions()
            random.shuffle(session["questions"])
            for q in session["questions"]:
                session['answers'][q['id']] = {"user": None, "correct": q['answer']}
            return redirect(url_for("quiz"))
    return render_template("login.html")

@app.route("/quiz")
def quiz():
    if "username" not in session:
        return redirect(url_for("login"))
    
    if "questions" not in session or not session["questions"]:
        return redirect(url_for("final_score"))
    
    question = session["questions"][session["current_index"]]
    user_answer = session['answers'].get(question['id'], {}).get('user', None)
    return render_template("quiz.html", question=question, user_answer=user_answer, score=session['score'])

@app.route("/next", methods=["POST"])
def next_question():
    if session["current_index"] < len(session["questions"]) - 1:
        session["current_index"] += 1
    return redirect(url_for("quiz"))

@app.route("/prev", methods=["POST"])
def prev_question():
    if session["current_index"] > 0:
        session["current_index"] -= 1
    return redirect(url_for("quiz"))

@app.route("/submit", methods=["POST"])
def submit():
    question = session["questions"][session["current_index"]]
    selected_answer = request.form.get("answer", "")
    
    if selected_answer:
        update_score(question['id'], selected_answer)
    
    return redirect(url_for("next_question"))

@app.route("/final_score")
def final_score():
    score = session.get("score", 0)
    total_questions = len(session.get("questions", []))
    session.clear()
    return render_template("final_score.html", score=score, total_questions=total_questions)

if __name__ == "__main__":
    app.run(debug=True)
