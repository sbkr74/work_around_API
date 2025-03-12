
with open(r"flaskAPI\project\Math_quiz\EXP\files\que_check.txt", "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

questions_list = []
current_question = []
current_options = []
current_answer = None

for line in lines:
    if line[0].isdigit() and "." in line[:3]:  # New question starts
        if current_question:  # Save previous question
            questions_list.append({
                "question": "\n".join(current_question),
                "options": "\n".join(current_options),
                "answer": current_answer
            })
        # Reset for new question
        current_question = [line]  
        current_options = []
        current_answer = None
    elif line.startswith("(A)"):  # Options start
        current_options.append(line)
    elif line.startswith("Answer:"):
        current_answer = line.split("Answer:")[-1].strip()
    else:
        current_question.append(line)

# Append the last question
if current_question:
    questions_list.append({
        "question": "\n".join(current_question),
        "options": "\n".join(current_options),
        "answer": current_answer
    })

# Print results
for i, q in enumerate(questions_list, 1):
    print(f"Question {i}:\n{q['question']}\n")
    print(f"Options:\n{q['options']}\n")
    print(f"Answer: {q['answer']}\n{'-'*50}\n")

