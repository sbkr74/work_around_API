from flask import Flask, render_template, request
import random

app = Flask(__name__)

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

# Global variables to track quiz state
questions = read_questions()
score = 0
asked_questions = []
remaining_questions = random.sample(questions, len(questions))

@app.route('/')
def get_question():
    global score, asked_questions, remaining_questions

    # Stop the quiz only when ALL questions have been asked once
    if len(asked_questions) == len(questions):
        final_score = f"Quiz completed! Your final score is {score}/{len(questions)}"
        return final_score  # Display final score

    # Get the next question randomly but without repetition
    selected_question = remaining_questions.pop(0)  # Remove from list
    asked_questions.append(selected_question['id'])  # Track asked question IDs
    
    return render_template("index.html", question=selected_question)

@app.route('/submit', methods=['POST'])
def submit():
    global score

    selected_answer = request.form.get("answer", "")
    correct_answer = request.form.get("correct_answer", "")

    if selected_answer == correct_answer:
        score += 1  # Increase score if the answer is correct

    return get_question()  # Show the next question or final score

if __name__ == "__main__":
    app.run(debug=True)
