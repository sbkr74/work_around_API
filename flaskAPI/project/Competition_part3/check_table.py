import sqlite3

DATABASE = r"flaskAPI/project/Competition_part3/files/quiz.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table = cursor.fetchall()
print(table)
if table:
    print("Table 'questions' exists.")
else:
    print("Table 'questions' does NOT exist.")

conn.close()
