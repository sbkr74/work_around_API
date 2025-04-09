from flask import Flask, render_template, session, redirect, url_for, request
import sqlite3, random
import html
import os
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = os.urandom(24)   # Needed for session

DATABASE = r'flaskAPI\project\Competition(GPT)\data\quiz1.db'
csv_path = r'flaskAPI\project\Competition(GPT)\files\jpsc_gs.csv'

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
        SELECT question_number, question_text, option_a, option_b, option_c, option_d, correct_option
        FROM questions WHERE id = ?
    """, (q_id,))
    row = cur.fetchone()
    conn.close()
    return row

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/start')
def start_quiz():
    # session.clear()         # ... rest of the quiz start logic
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

    if not question_ids or question_index < 0 or question_index >= len(question_ids):
        return redirect(url_for('start_quiz'))

    qid = question_ids[question_index]
    question = get_question_by_id(qid)

    selected_option = responses.get(str(qid))

    if request.method == 'POST':
        selected_option = request.form.get('option')

        if selected_option != "":
            responses[str(qid)] = selected_option
        else:
            responses.pop(str(qid), None)

        session['responses'] = responses

        # Check if the user came from review page
        return_to_review = request.args.get('from_review')
        action = request.form['action']

        if return_to_review == '1':
            return redirect(url_for('review'))

        if action == 'next':
            return redirect(url_for('show_question', question_index=question_index + 1))
        elif action == 'prev':
            return redirect(url_for('show_question', question_index=question_index - 1))
        elif action == 'review':
            return redirect(url_for('review'))
        elif action == 'finish':
            return redirect(url_for('final_score'))

    return render_template('quiz.html',
                           question=question,
                           index=question_index,
                           total=len(question_ids),
                           selected=selected_option)


@app.route('/review')
def review():
    question_ids = session.get('question_ids')
    responses = session.get('responses', {})

    if not question_ids:
        return redirect(url_for('start_quiz'))

    review_data = []

    for idx, qid in enumerate(question_ids):
        question = get_question_by_id(qid)
        selected = responses.get(str(qid))
        review_data.append({
            'index': idx,           # <- for edit button
            'number': idx + 1,
            'question': question[1],
            'options': {
                'A': question[2],
                'B': question[3],
                'C': question[4],
                'D': question[5],
            },
            'selected': selected
        })

    return render_template('review.html', review_data=review_data)

@app.route('/final_score')
def final_score():
    question_ids = session.get('question_ids')
    responses = session.get('responses', {})

    if not question_ids:
        return redirect(url_for('start_quiz'))

    review_data = []
    score = 0.0  # Make it float for fractional deductions

    for idx, qid in enumerate(question_ids):
        question = get_question_by_id(qid)
        selected = responses.get(str(qid))
        correct = question[6]

        if selected == correct:
            is_correct = True
            score += 1
        elif selected is None or selected == "":
            is_correct = None  # Skipped
        else:
            is_correct = False
            score -= 0.25

        review_data.append({
            'index': idx,
            'question': question[1],
            'options': {
                'A': question[2],
                'B': question[3],
                'C': question[4],
                'D': question[5],
            },
            'correct': correct,
            'selected': selected,
            'is_correct': is_correct,
        })

    total = len(question_ids)
    percentage = max((score / total) * 100, 0)

    # Performance based on percentage
    if percentage == 100:
        performance = "Outstanding"
    elif percentage >= 80:
        performance = "Excellent"
    elif percentage >= 60:
        performance = "Good"
    elif percentage >= 40:
        performance = "Needs Improvement"
    else:
        performance = "Try Again"

    return render_template('final_score.html',
                           review_data=review_data,
                           score=round(score, 2),
                           total=total,
                           percentage=round(percentage, 2),
                           performance=performance)



if __name__ == "__main__":
    app.run(debug=True)
