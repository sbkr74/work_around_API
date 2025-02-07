The given Python script is a **Flask web application** that runs a simple **math quiz**. It reads questions from a file, displays them randomly, and tracks the user's score using Flask's session management.  

### **Code Breakdown (Line by Line)**  

---

#### **Importing Required Modules**  
```python
from flask import Flask, render_template, request, session
import random
```
- **Flask**: A lightweight web framework for Python.
- **render_template**: Used to render HTML templates.
- **request**: Handles form data sent via POST requests.
- **session**: Stores user-specific data across multiple requests.
- **random**: Used to randomly select questions.

---

#### **Initialize the Flask App**
```python
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session tracking
```
- **`app = Flask(__name__)`**: Creates a Flask application instance.
- **`app.secret_key = 'your_secret_key'`**: Sets a secret key for **session management**, which is necessary for storing user-related data like scores.

---

### **Function: `read_questions()`**
Reads quiz questions from a file and structures them into a list of dictionaries.

```python
def read_questions():
    questions = []
    with open(r"flaskAPI\project\Math_quiz\EXP\files\questions.txt", "r", encoding="utf-8") as f:
        data = f.readlines()
```
- **`questions = []`**: Initializes an empty list to store questions.
- **`with open(..., "r", encoding="utf-8") as f:`**: Opens the file containing quiz questions in **read mode** (`"r"`) with UTF-8 encoding.
- **`data = f.readlines()`**: Reads all lines from the file into a list.

---

#### **Processing the File Content**
```python
    question = None
    options = []
    answer = None
```
- **`question`**: Stores the current question being processed.
- **`options`**: Stores answer choices (A, B, C, D).
- **`answer`**: Stores the correct answer.

---

#### **Reading and Parsing Each Line**
```python
    for line in data:
        line = line.strip()
```
- **Iterates** through each line in the file.
- **`.strip()`** removes leading and trailing spaces.

---

#### **Handling Different Parts of the Question**
```python
        if not line:
            continue
```
- If the line is **empty**, skip it.

```python
        if line[0].isdigit():  # If the line starts with a number, it's a new question
```
- If a line **starts with a digit** (`1. What is 2+2?`), it indicates the **start of a new question**.

```python
            if question and options and answer:
                questions.append({
                    "id": len(questions) + 1,
                    "question": question,
                    "options": options,
                    "answer": answer
                })
```
- If a question has already been processed (with options and an answer), store it in the `questions` list.

```python
            question = line.split(". ", 1)[1]  # Extracts the question text
            options = []
            answer = None
```
- Extracts the question **text** by splitting on `". "` and taking the second part.

---

#### **Processing Options (A, B, C, D)**
```python
        elif line.startswith(("A)", "B)", "C)", "D)")):
            options.append(line)
```
- If the line starts with **A), B), C), or D)**, it's an **answer choice** and gets added to `options`.

---

#### **Processing the Correct Answer**
```python
        elif line.startswith("Answer:"):
            answer = line.split("Answer: ")[-1].strip()
```
- Extracts the **correct answer** from the line that starts with `"Answer:"`.

---

#### **Adding the Last Question**
```python
    if question and options and answer:
        questions.append({
            "id": len(questions) + 1,
            "question": question,
            "options": options,
            "answer": answer
        })
```
- Ensures the **last question** in the file is also added.

```python
    return questions
```
- Returns the list of parsed questions.

---

### **Route: `get_question()`**
Handles the **home page** (`/`) where a random question is shown.

```python
@app.route('/')
def get_question():
```
- Defines the **Flask route** for the home page.

```python
    questions = read_questions()
```
- Calls `read_questions()` to **fetch questions** from the file.

---

#### **Initialize Session Variables**
```python
    if 'score' not in session:
        session['score'] = 0  # Initialize score
    if 'question_index' not in session:
        session['question_index'] = 0  # Track how many questions have been shown
    if 'asked_questions' not in session:
        session['asked_questions'] = []  # Track asked questions
```
- **Session Variables**:
  - `'score'`: Stores the user’s quiz score.
  - `'question_index'`: Tracks the number of **questions shown**.
  - `'asked_questions'`: Stores **question IDs already asked** to prevent repetition.

---

#### **Selecting a New Question**
```python
    available_questions = [q for q in questions if q['id'] not in session['asked_questions']]
```
- Filters out **questions already asked**.

```python
    if not available_questions:
        return f"Quiz completed! Your final score is {session['score']}/{len(questions)}"
```
- If **all questions are asked**, the quiz **ends** and displays the **final score**.

---

#### **Picking a Random Question**
```python
    selected_question = random.choice(available_questions)
    session['asked_questions'].append(selected_question['id'])
```
- Randomly selects an **unasked question**.
- Adds the question **ID** to `'asked_questions'`.

```python
    return render_template("index.html", question=selected_question, score=session['score'])
```
- Renders an **HTML template (`index.html`)** with:
  - `question`: Selected question.
  - `score`: User’s current score.

---

### **Route: `submit()`**
Handles the **form submission** when the user selects an answer.

```python
@app.route('/submit', methods=['POST'])
def submit():
```
- Defines the `/submit` route to **handle POST requests**.

```python
    selected_answer = request.form.get("answer", "")
    correct_answer = request.form.get("correct_answer", "")
```
- Retrieves:
  - `selected_answer`: User’s choice.
  - `correct_answer`: The correct answer (sent via form).

---

#### **Checking the Answer**
```python
    if selected_answer == correct_answer:
        session['score'] += 1  # Increase score if the answer is correct
```
- If the user’s **selected answer is correct**, the score **increases by 1**.

---

#### **Load Next Question**
```python
    return get_question()  # Redirect to the next question
```
- Calls `get_question()` to show **the next question**.

---

### **Running the Flask App**
```python
if __name__ == "__main__":
    app.run(debug=True)
```
- Runs the Flask app in **debug mode**, which:
  - Automatically **restarts** the server on code changes.
  - Shows **detailed error logs**.

---

## **Summary**
1. **Reads** questions from a file (`questions.txt`).
2. **Tracks** user's progress using Flask sessions.
3. **Randomly selects** a question that hasn't been asked.
4. **Displays** the question on the web page.
5. **Processes** user input and updates the score.
6. **Loops** until all questions are answered, then displays the final score.

This is a simple **Flask-based quiz application** with session management! 🚀