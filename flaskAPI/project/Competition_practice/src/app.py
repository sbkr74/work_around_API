import uuid
import re

from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__,template_folder="../templates")
app.secret_key = str(uuid.uuid4())

def read_questions():
    with open(r"flaskAPI\project\Competition_practice\files\jpsc_gs-1.txt", "r", encoding="utf-8") as f:
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
    session['score'] = 0
    session['asked_questions'] = []

@app.route('/')
def get_question():
    if 'score' not in session:
        session['score'] = 0  # Initialize score
    if 'asked_questions' not in session:
        session['asked_questions'] = []  # Track asked questions
    
    # Select a random question that hasn't been asked
    available_questions = [q for q in questions if q['id'] not in session['asked_questions']]
    
    
    if not available_questions:
        return redirect(url_for('final_score'))

    selected_question = random.choice(available_questions)
    session['asked_questions'].append(selected_question['id'])
    session.modified = True  # Ensure the session is saved   
    
    return render_template("index.html", question=selected_question, score=session['score'])

@app.route('/submit', methods=['POST'])
def submit():
    selected_answer = request.form.get("answer", "")
    correct_answer = request.form.get("correct_answer", "")

    if selected_answer == correct_answer:
        session['score'] += 1  # Increase score if the answer is correct

    return redirect(url_for('get_question'))  # Redirect to the next question

@app.route('/final_score')
def final_score():

    score_message = f"Quiz completed! Your final score is {session['score']}/{len(questions)}"
    
    # Reset the quiz when the final score is viewed
    reset_quiz()

    return render_template("final_score.html", score_message=score_message)

if __name__ == "__main__":
    app.run(debug=True)