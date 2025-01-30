import sympy as sp

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
        print(f"Question: {quest}")
        try:
            # Safely evaluate the mathematical expression using sympy
            x = sp.sympify(quest)  # sympify can handle expressions like '12 + 8 - 5 * 2 / 2'
            sol.append(x)

            y = int(input("Your answer: "))  # Handle user input safely
            user_res.append(y)
        except (ValueError, SyntaxError, sp.SympifyError):
            print("Invalid input. Skipping...")
            user_res.append(None)

    
    # Compare answers
    count = sum(a == b for a, b in zip(sol, user_res) if b is not None)
    print(f"Correct answers: {count}/{len(sol)}")
    print(f"Percentage: {count/len(sol)*100}")
