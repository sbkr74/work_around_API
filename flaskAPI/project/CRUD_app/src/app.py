from flask import Flask,render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder="../templates",static_folder="../static")

@app.route("/")
def home_page():
    return render_template("./index.html")


if __name__ == "__main__":
    app.run(debug=True)