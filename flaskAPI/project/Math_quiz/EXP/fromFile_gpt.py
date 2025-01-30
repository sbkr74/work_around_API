import ast

def read_questions(quest_path):
    try:
        with open(quest_path, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{quest_path}' not found.")
        return []

if __name__ == '__main__':
    quest_path = r"flaskAPI\project\Math_quiz\EXP\files\equations.txt"
    quiz = read_questions(quest_path)
    
    if not quiz:  # Exit if file is missing
        exit()

    sol = []
    user_res = []

    for quest in quiz:
        print(quest)
        try:
            y = float(input("Your answer: "))  # Handle user input safely
            user_res.append(y)
            x = ast.literal_eval(quest)  # Safer than eval()
            sol.append(x)

        except (ValueError, SyntaxError):
            print("Invalid input. Skipping...")
            user_res.append(None)

    # Compare answers
    count = sum(a == b for a, b in zip(sol, user_res) if b is not None)
    print(f"Correct answers: {count}/{len(sol)}")
