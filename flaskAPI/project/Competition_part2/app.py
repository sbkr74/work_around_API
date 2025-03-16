from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for session management

DATABASE = "flaskAPI/project/Competition_part2/files/quiz.db"

# Database initialization
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)''')
        conn.commit()

init_db()  # Initialize database on startup

def read_questions():
    file_path = r"flaskAPI\project\Competition_part2\files\test_1.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines() if line.strip()]
    
    questions = []
    question = []
    options = []
    answer = None

    options_start = False

    for line in data:
        if re.match(r"^\d+\.", line):               # Detect question number (e.g., "1.")
            if question and options and answer:
                full_question = "\n".join(question)
                # Remove question number using regex
                clean_question = re.sub(r"^\d+\.\s*", "", full_question)
                questions.append({
                    "id": len(questions) + 1,
                    "question": clean_question,
                    "options": options,
                    "answer": answer
                })
            question = [line]
            options = []
            answer = None
            options_start = False
        
        elif line.startswith("(A)"):
            options_start = True
            options.append(line)
        
        elif options_start and line.startswith(("(B)", "(C)", "(D)")):
            options.append(line)
        
        elif line.startswith("Answer:"):
            answer = line.split("Answer: ")[-1].strip()
        
        else:
            question.append(line)

    if question and options and answer:
        full_question = "\n".join(question)
        clean_question = re.sub(r"^\d+\.\s*","",full_question)
        questions.append({
            "id": len(questions) + 1,
            "question": clean_question,
            "options": options,
            "answer": answer
        })

    return questions

questions = read_questions()

def reset_quiz():
    """Resets the quiz session when a new user logs in."""
    session['score'] = 0
    session['asked_questions'] = []
    session['remaining_questions'] = random.sample(questions, len(questions))

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('get_question'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return "Username already exists. Try a different one."

    return render_template('signup.html')

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
                reset_quiz()  # Reset quiz for the new user
                return redirect(url_for('get_question'))
            else:
                return "Invalid username or password. Try again."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('login'))

@app.route('/quiz')
def get_question():
    if 'user' not in session:
        return redirect(url_for('login'))

    if 'score' not in session:
        session['score'] = 0  # Initialize score
    if 'asked_questions' not in session:
        session['asked_questions'] = []  # Track asked questions
    
    total_questions = len(questions) + 1  # Get the total number of questions
    # Select a random question that hasn't been asked
    available_questions = [q for q in questions if q['id'] not in session['asked_questions']]
    k = total_questions - len(available_questions)  # Dynamically calculate k

    if not available_questions:
        return redirect(url_for('final_score'))

    selected_question = random.choice(available_questions)
    session['asked_questions'].append(selected_question['id'])
    session.modified = True  # Ensure the session is saved   
    
    return render_template("index.html", question=selected_question, score=session['score'],k=k)

@app.route('/submit', methods=['POST'])
def submit():
    if 'user' not in session:
        return redirect(url_for('login'))

    selected_answer = request.form.get("answer", "")
    correct_answer = request.form.get("correct_answer", "")

    if selected_answer == correct_answer:
        session['score'] += 1

    return redirect(url_for('get_question')) 

@app.route('/final_score')
def final_score():
    if 'user' not in session:
        return redirect(url_for('login'))

    score_message = f"Quiz completed! Your final score is {session['score']}/{len(questions)}"
    return render_template("final_score.html", score_message=score_message)

if __name__ == "__main__":
    app.run(debug=True)
