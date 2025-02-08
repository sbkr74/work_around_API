import uuid


from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

def read_questions():
    questions = []
    with open(r"flaskAPI\project\Math_quiz\EXP\files\questions.txt", "r", encoding="utf-8") as f:
        data = f.readlines()

    question = None
    options = []
    answer = None

    for line in data:
        line = line.strip()

        if not line:
            continue

        if line[0].isdigit():  # If the line starts with a number, it's a new question
            if question and options and answer:
                questions.append({
                    "id": len(questions) + 1,
                    "question": question,
                    "options": options,
                    "answer": answer
                })
            question = line.split(". ", 1)[1]
            options = []
            answer = None

        elif line.startswith(("A)", "B)", "C)", "D)")):
            options.append(line)

        elif line.startswith("Answer:"):
            answer = line.split("Answer: ")[-1].strip()

    if question and options and answer:
        questions.append({
            "id": len(questions) + 1,
            "question": question,
            "options": options,
            "answer": answer
        })

    return questions

@app.route('/')
def get_question():
    questions = read_questions()
    
    if 'score' not in session:
        session['score'] = 0  # Initialize score
    if 'asked_questions' not in session:
        session['asked_questions'] = []  # Track asked questions
    
    # Debug: Print session data
    print("Session asked_questions:", session['asked_questions'])
    
    # Select a random question that hasn't been asked
    available_questions = [q for q in questions if q['id'] not in session['asked_questions']]
    
    # Debug: Print available questions
    print("Available questions:", [q['id'] for q in available_questions])
    
    if not available_questions:
        return f"Quiz completed! Your final score is {session['score']}/{len(questions)}"

    selected_question = random.choice(available_questions)
    session['asked_questions'].append(selected_question['id'])
    session.modified = True  # Ensure the session is saved
    
    # Debug: Print selected question
    print("Selected question ID:", selected_question['id'])
    
    return render_template("index.html", question=selected_question, score=session['score'])

@app.route('/submit', methods=['POST'])
def submit():
    selected_answer = request.form.get("answer", "")
    correct_answer = request.form.get("correct_answer", "")

    if selected_answer == correct_answer:
        session['score'] += 1  # Increase score if the answer is correct

    return get_question()  # Redirect to the next question

if __name__ == "__main__":
    app.run(debug=True)