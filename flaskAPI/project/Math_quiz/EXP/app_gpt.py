from flask import Flask, render_template

app = Flask(__name__)


def read_questions():
    questions = []
    with open(r"flaskAPI\project\Math_quiz\EXP\files\questions.txt","r") as f:
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
            answer = line.strip(": ")[1]

@app.route('/')
def get_questions():
    questions = read_questions()
    return render_template("index.html",questions=questions)

if __name__=="__main__":
    app.run(debug=True)
