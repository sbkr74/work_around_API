from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session tracking

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
        session['asked_questions'] = []  # Track asked question IDs
    
    if 'remaining_questions' not in session or not session['remaining_questions']:
        # Shuffle and store all questions at the start
        session['remaining_questions'] = random.sample(questions, len(questions))

    # Stop the quiz only when ALL questions have been asked once
    if len(session['asked_questions']) == len(questions):
        final_score = f"Quiz completed! Your final score is {session['score']}/{len(questions)}"
        session.clear()  # Clear session after quiz completion
        return final_score  # Display final score

    # Get the next question randomly but without repetition
    selected_question = session['remaining_questions'].pop(0)  # Remove from list
    session['asked_questions'].append(selected_question['id'])  # Track asked question IDs
    
    return render_template("index.html", question=selected_question, score=session['score'])

@app.route('/submit', methods=['POST'])
def submit():
    selected_answer = request.form.get("answer", "")
    correct_answer = request.form.get("correct_answer", "")

    if selected_answer == correct_answer:
        session['score'] += 1  # Increase score if the answer is correct

    return get_question()  # Show the next question or final score

if __name__ == "__main__":
    app.run(debug=True)
