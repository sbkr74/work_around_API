from flask import Flask, render_template, request, redirect, url_for, session

# from resources.authentication import login

app = Flask(__name__)
# app.secret_key = os.urandom(24) # Required for session management

DATABASE = r"flaskAPI/project/Competition_part3/files/quiz.db"

# @app.route('/')
# def home():
#     if 'user' not in session:
#         return redirect(url_for('login'))
#     return redirect(url_for('quiz'))

def reset_quiz():
    """Resets the quiz session when a new user logs in."""
    session['score'] = 0
    session["history"] = []
    session["current_index"] = 0



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
