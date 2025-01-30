
def questions(quest_path):
    with open(quest_path,"r") as f:
        data = f.readlines()
        return data
    

if __name__ == '__main__':
    quest_path = r"flaskAPI\project\Math_quiz\EXP\files\equations.txt"
    ans_path = r"flaskAPI\project\Math_quiz\EXP\files\answers.txt"
    quiz = questions(quest_path)
    answer = questions(ans_path)
    sol = []
    ans = []
    for quest in quiz:
        print(quest.strip())
        x = eval(quest.strip())
        sol.append(x)
    for val in answer:
        ans.append(val.strip())
    comparison = [a == float(b) for a, b in zip(sol, ans)]
    print(comparison)  
        