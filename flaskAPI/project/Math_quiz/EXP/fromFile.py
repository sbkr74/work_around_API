
def questions(quest_path):
    with open(quest_path,"r") as f:
        data = f.readlines()
        return data
    

if __name__ == '__main__':
    quest_path = r"flaskAPI\project\Math_quiz\EXP\files\equations.txt"
    quiz = questions(quest_path)
    sol = []
    user_res = []

    for quest in quiz:
        print(quest.strip())
        x = eval(quest.strip())
        sol.append(x)
        y = float(input())
        user_res.append(y)

    count = sum(a == float(b) for a, b in zip(sol, user_res))
    print(count)      