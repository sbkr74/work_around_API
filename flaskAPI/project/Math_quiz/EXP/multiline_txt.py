import re
def read_questions():
    with open(r"flaskAPI\project\Math_quiz\EXP\files\que_check.txt", "r", encoding="utf-8") as f:
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

print(read_questions())
