from flask import Flask, session, redirect, url_for, render_template, request
import random

app = Flask(__name__,template_folder="../templates")
app.secret_key = 'your_secret_key'  # Required for session management

# Example questions (replace with your actual data)
questions = [
    {"id": 1, "question": "What is 2 + 2?", "answers": ["3", "4", "5"], "correct_answer": "4"},
    {"id": 2, "question": "What is the capital of France?", "answers": ["Paris", "London", "Berlin"], "correct_answer": "Paris"},
    {"id": 3, "question": "What is the largest planet?", "answers": ["Earth", "Jupiter", "Saturn"], "correct_answer": "Jupiter"},
]

def reset_quiz():
    """
    Reset the quiz by clearing the score and asked questions.
    """
    session['score'] = 0
    session['asked_questions'] = []

@app.route('/')
def get_question():
    """
    Display a random question that hasn't been asked yet.
    """
    # Initialize session variables if they don't exist
    if 'score' not in session:
        session['score'] = 0
    if 'asked_questions' not in session:
        session['asked_questions'] = []

    # Select a random question that hasn't been asked
    available_questions = [q for q in questions if q['id'] not in session['asked_questions']]

    if not available_questions:
        # No more questions, redirect to final score
        return redirect(url_for('final_score'))

    selected_question = random.choice(available_questions)
    session['asked_questions'].append(selected_question['id'])
    session.modified = True  # Ensure the session is saved

    return render_template("app_ch_index.html", question=selected_question, score=session['score'])

@app.route('/submit', methods=['POST'])
def submit():
    """
    Handle the user's answer and update the score.
    """
    selected_answer = request.form.get("answer", "")
    correct_answer = request.form.get("correct_answer", "")

    if selected_answer == correct_answer:
        session['score'] += 1  # Increase score if the answer is correct

    return redirect(url_for('get_question'))  # Redirect to the next question

@app.route('/final_score')
def final_score():
    """
    Display the final score and reset the quiz.
    """
    score_message = f"Quiz completed! Your final score is {session['score']}/{len(questions)}"

    # Reset the quiz when the final score is viewed
    reset_quiz()

    return render_template("app_ch_final_score.html", score_message=score_message)

if __name__ == '__main__':
    app.run(debug=True)