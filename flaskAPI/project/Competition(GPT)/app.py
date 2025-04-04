from flask import Flask, render_template
import sqlite3
import html
from markupsafe import Markup

app = Flask(__name__)

DATABASE = r'flaskAPI\project\Competition(GPT)\data\quiz.db'
# Custom filter to escape HTML and add <br> for newlines
def safe_nl2br(value):
    escaped = html.escape(value)          # Escapes <, >, ", etc.
    with_br = escaped.replace("\n", "<br>")
    return Markup(with_br)                # Only <br> is rendered as HTML

# Register the filter
app.jinja_env.filters['safe_nl2br'] = safe_nl2br

# Fetch questions
def get_questions():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT question_number, question_text, option_a, option_b, option_c, option_d FROM questions")
    questions = cursor.fetchall()
    conn.close()
    return questions

@app.route("/")
def show_questions():
    questions = get_questions()
    return render_template("questions.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
