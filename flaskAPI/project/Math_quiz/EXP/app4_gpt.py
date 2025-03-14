from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Global variables to track quiz state
score = 0
asked_questions = []
remaining_questions = []

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

questions = read_questions()

def reset_quiz():
    """Resets the quiz to its initial state."""
    global score, asked_questions, remaining_questions
    score = 0
    asked_questions = []
    remaining_questions = random.sample(questions, len(questions))  # Shuffle questions

reset_quiz()  # Initialize the quiz at the start

@app.route('/')
def get_question():
    global remaining_questions, asked_questions

    # If all questions have been answered, redirect to final score page
    if len(asked_questions) == len(questions):
        return redirect(url_for('final_score'))

    # Get the next question randomly but without repetition
    selected_question = remaining_questions.pop(0)  # Remove from the list
    asked_questions.append(selected_question['id'])  # Track asked question IDs
    
    return render_template("app4_index.html", question=selected_question)

@app.route('/submit', methods=['POST'])
def submit():
    global score

    selected_answer = request.form.get("answer", "")
    correct_answer = request.form.get("correct_answer", "")
    print(selected_answer)
    print(correct_answer)


    if selected_answer == correct_answer:
        score += 1  # Increase score if the answer is correct

    return get_question()  # Show the next question or final score

@app.route('/final_score')
def final_score():
    global score

    score_message = f"Quiz completed! Your final score is {score}/{len(questions)}"
    
    # Reset the quiz when the final score is viewed
    reset_quiz()

    return render_template("app4_final_score.html", score_message=score_message)

if __name__ == "__main__":
    app.run(debug=True)
