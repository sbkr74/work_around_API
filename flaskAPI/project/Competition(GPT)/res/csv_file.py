import csv

# Define the questions and answers in the new format
questions_updated = [
    {
        "question_number": 1,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. Flask is a Python framework for building desktop apps.\n"
            "II. Flask uses Jinja2 for templating.\n"
            "III. Flask supports decorators for routing.\n"
            "IV. Flask comes with a built-in ORM."
        ),
        "option_a": "Only II is correct",
        "option_b": "II and III are incorrect",
        "option_c": "All are incorrect",
        "option_d": "II and III are correct",
        "correct_option": "B"
    },
    {
        "question_number": 2,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. Python lists are mutable.\n"
            "II. Tuples in Python are mutable.\n"
            "III. Sets allow duplicate elements.\n"
            "IV. Dictionaries store key-value pairs."
        ),
        "option_a": "I and IV are correct",
        "option_b": "II and III are incorrect",
        "option_c": "Only III is correct",
        "option_d": "I, II and III are correct",
        "correct_option": "B"
    },
    {
        "question_number": 3,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. SELECT * FROM table returns all columns.\n"
            "II. GROUP BY is used with aggregate functions.\n"
            "III. INNER JOIN always returns unmatched rows.\n"
            "IV. ORDER BY sorts data in SQL."
        ),
        "option_a": "Only I is correct",
        "option_b": "III is incorrect",
        "option_c": "III and IV are incorrect",
        "option_d": "All are correct",
        "correct_option": "B"
    },
    {
        "question_number": 4,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. Python supports multiple inheritance.\n"
            "II. super() is used to call a subclass method.\n"
            "III. __init__() is a constructor in Python.\n"
            "IV. self represents the instance in a class."
        ),
        "option_a": "Only II is incorrect",
        "option_b": "II and IV are correct",
        "option_c": "I, II and III are correct",
        "option_d": "All are incorrect",
        "correct_option": "A"
    },
    {
        "question_number": 5,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. Flask can only be used with SQLite.\n"
            "II. Flask apps can have multiple routes.\n"
            "III. render_template() returns an HTML page.\n"
            "IV. Flask supports JSON responses."
        ),
        "option_a": "Only I is incorrect",
        "option_b": "II and III are correct",
        "option_c": "I and III are incorrect",
        "option_d": "I, II and IV are correct",
        "correct_option": "A"
    },
    {
        "question_number": 6,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. CSV stands for Comma Separated Values.\n"
            "II. A CSV file can store only integers.\n"
            "III. Python’s csv module is used to read CSV files.\n"
            "IV. CSV files can be opened in Excel."
        ),
        "option_a": "II is incorrect",
        "option_b": "Only III is correct",
        "option_c": "I and IV are incorrect",
        "option_d": "All are incorrect",
        "correct_option": "A"
    },
    {
        "question_number": 7,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. HTML is a programming language.\n"
            "II. '<div>' is a generic container tag.\n"
            "III. '<p>' is used for paragraphs.\n"
            "IV. '<table>' is used for form elements."
        ),
        "option_a": "I and IV are incorrect",
        "option_b": "II and III are incorrect",
        "option_c": "All are correct",
        "option_d": "Only I is incorrect",
        "correct_option": "A"
    },
    {
        "question_number": 8,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. Python uses indentation to define blocks.\n"
            "II. break is used to exit a loop.\n"
            "III. continue exits the current program.\n"
            "IV. pass is a placeholder statement."
        ),
        "option_a": "I and IV are correct",
        "option_b": "III is incorrect",
        "option_c": "Only II is correct",
        "option_d": "All are correct",
        "correct_option": "B"
    },
    {
        "question_number": 9,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. pip installs Python packages.\n"
            "II. venv creates virtual environments.\n"
            "III. import is used to install packages.\n"
            "IV. requirements.txt lists dependencies."
        ),
        "option_a": "I and II are incorrect",
        "option_b": "Only III is incorrect",
        "option_c": "II and III are incorrect",
        "option_d": "III and IV are correct",
        "correct_option": "B"
    },
    {
        "question_number": 10,
        "question_text": (
            "Which of the following is not a correct statement?\n\n"
            "I. SQLite is a file-based database.\n"
            "II. SQLite supports joins and subqueries.\n"
            "III. SQLite is not part of Python's standard library.\n"
            "IV. SQLite is useful for lightweight applications."
        ),
        "option_a": "Only III is incorrect",
        "option_b": "I and II are correct",
        "option_c": "III and IV are incorrect",
        "option_d": "All are incorrect",
        "correct_option": "A"
    }
]

# Define CSV file path
csv_file_path_2 = r"flaskAPI\project\Competition(GPT)\files\quiz_statements_questions.csv"

# Write data to CSV
with open(csv_file_path_2, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["question_number","question_text", "option_a", "option_b", "option_c", "option_d", "correct_option"])
    writer.writeheader()
    for question in questions_updated:
        writer.writerow(question)


