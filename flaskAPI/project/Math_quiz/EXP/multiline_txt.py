def read_questions():
    questions = []
    with open(r"flaskAPI\project\Math_quiz\EXP\files\que_check.txt", "r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines() if line.strip()]

    question = []
    options = []
    answer = None

    options_start = False

    for line in data:
        if line[0].isdigit() and "." in line[:3]:  # If the line starts with a number, it's a new question
            if question and options and answer:
                questions.append({
                    "id": len(questions) + 1,
                    "question": "\n".join(question),
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
        questions.append({
            "id": len(questions) + 1,
            "question": "\n".join(question),
            "options": options,
            "answer": answer
        })

    return questions

print(read_questions())
