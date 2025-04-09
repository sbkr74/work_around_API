import sqlite3
import csv

def data_insertion(db_path,csv_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Create the 'questions' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_number INTEGER,
        question_text TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct_option TEXT
    )
    ''')

    # Step 2: Read from the CSV file and insert into the database
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
                INSERT INTO questions (
                    question_number,
                    question_text,
                    option_a,
                    option_b,
                    option_c,
                    option_d,
                    correct_option
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                int(row['question_number']),
                row['question_text'],
                row['option_a'],
                row['option_b'],
                row['option_c'],
                row['option_d'],
                row['correct_option']
            ))

    # Commit and close connection
    conn.commit()
    conn.close()

    print("Data imported successfully into 'quiz.db'")

if __name__ == "__main__":
    # Path to SQLite DB and CSV file
    db_path = r'flaskAPI\project\Competition(GPT)\data\quiz1.db'
    csv_path = r"flaskAPI\project\Competition(GPT)\files\quiz_statements_questions.csv"
    data_insertion(db_path,csv_path)