from flask import Flask,redirect,request,url_for,render_template,session
import database as db
from app import DATABASE as db_path,reset_quiz
import sqlite3
import random
# import os

app = Flask(__name__,template_folder="../templates")
app.secret_key = "secret_key"# Required for session management

# Homepage
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('login'))

# User Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = db.get_db(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Username already exists! Try a different one."
        finally:
            conn.close()

    return render_template("signup.html")

# User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = db.get_db(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = username
            reset_quiz()
            session["questions"] = db.fetch_questions()  # Load questions
            random.shuffle(session["questions"])  # Shuffle for randomness
            return redirect(url_for("quiz"))
        else:
            msg = "Invalid username or password!"

    return render_template("login.html",msg=msg)

# Logout
@app.route("/logout")
def logout():
    session.clear()  # Clears all session data
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)