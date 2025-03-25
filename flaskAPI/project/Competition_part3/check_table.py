import sqlite3

DATABASE = r"flaskAPI/project/Competition_part3/files/quiz.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    # cursor = conn.cursor()
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# table = cursor.fetchall()
# print(table)
# if table:
#     print("Table 'questions' exists.")
# else:
#     print("Table 'questions' does NOT exist.")

def fetch_question():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions;")
    questions = cursor.fetchall()
    conn.close()
    return [dict(q) for q in questions]

que = fetch_question()
print(que)


# conn.close()
