from flask import Flask, render_template, request

app = Flask(__name__)


def read_questions():
    questions = []
    with open(r"flaskAPI\project\Math_quiz\EXP\files\questions.txt","r",encoding="utf-8") as f:
        data = f.readlines()
    
    question = None
    options = []
    answer = None
    
    for line in data:
        line = line.strip()

        if line == "":
            continue

        if line[0].isdigit():
            if question:
                questions.append({"id": len(questions)+1,"question":question,"options":options,"answer":answer})
            question = line.split(". ",1)[1]
            options = []
            answer = None
        
        elif line.startswith(("A)","B)","C)","D)")):
            options.append(line)

        elif line.startswith("Answer:"):
            # answer = line.strip(": ")[1] 
            answer = line.split("Answer: ")[-1].strip()
    
    # Append the last question
    if question and options:
        questions.append({"id": len(questions) + 1, "question": question, "options": options, "answer": answer})

    return questions


@app.route('/')
def get_questions():
    questions = read_questions()
    return render_template("index.html",questions=questions)


@app.route('/submit', methods=['POST'])
def submit():
    questions = read_questions()
    score = 0
    total = len(questions)

    for q in questions:
        selected_answer = request.form.get(f"q{q['id']}", "")
        correct_answer = q["answer"][0]  # First letter (A, B, C, or D)

        if selected_answer == correct_answer:
            score += 1

    return f"Your score: {score}/{total}"


if __name__=="__main__":
    app.run(debug=True)
