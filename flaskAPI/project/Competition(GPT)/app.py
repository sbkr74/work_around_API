from flask import Flask, render_template, session, redirect, url_for, request
import sqlite3, random
import html
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for session

DATABASE = r'flaskAPI\project\Competition(GPT)\data\quiz.db'
# Custom filter to escape HTML and add <br> for newlines
def safe_nl2br(value):
    escaped = html.escape(value)          # Escapes <, >, ", etc.
    with_br = escaped.replace("\n", "<br>")
    return Markup(with_br)                # Only <br> is rendered as HTML

# Register the filter
app.jinja_env.filters['safe_nl2br'] = safe_nl2br

# Utility: Fetch all question IDs
def get_all_question_ids():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT id FROM questions")
    ids = [row[0] for row in cur.fetchall()]
    conn.close()
    return ids

# Utility: Fetch a single question by ID
def get_question_by_id(q_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
        SELECT question_number, question_text, option_a, option_b, option_c, option_d
        FROM questions WHERE id = ?
    """, (q_id,))
    row = cur.fetchone()
    conn.close()
    return row

@app.route('/start')
def start_quiz():
    # Get all question IDs and shuffle
    question_ids = get_all_question_ids()
    random.shuffle(question_ids)

    # Initialize session
    session['question_ids'] = question_ids
    session['responses'] = {}  # track answers
    return redirect(url_for('show_question', question_index=0))

@app.route('/quiz/<int:question_index>', methods=['GET', 'POST'])
def show_question(question_index):
    question_ids = session.get('question_ids')
    responses = session.get('responses', {})

    if question_ids is None:
        return redirect(url_for('start_quiz'))

    if request.method == 'POST':
        selected_option = request.form.get('option')
        qid = question_ids[question_index]
        responses[str(qid)] = selected_option  # Only latest answer retained
        session['responses'] = responses

    if question_index < 0 or question_index >= len(question_ids):
        return redirect(url_for('final_score'))  # or a 404

    qid = question_ids[question_index]
    question = get_question_by_id(qid)

    return render_template('quiz.html',
        question=question,
        index=question_index,
        total=len(question_ids),
        selected=responses.get(str(qid)),
    )

@app.route('/final')
def final_score():
    return "<h2>Final score coming soon...</h2>"  # Will be updated later

if __name__ == "__main__":
    app.run(debug=True)
