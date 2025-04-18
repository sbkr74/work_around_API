from flask import Flask,render_template,redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__,template_folder="../templates",static_folder="../static")
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(100),nullable=False)
    complete = db.Column(db.Integer,default=0)
    created = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self):
        return f"Task {self.id}"

# creating databases     
with app.app_context():
    db.create_all()

@app.route("/",methods =["GET","POST"])
def home_page():
    # Add Task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = Task(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error:{e}")
            return f"ERROR:{e}"
    # see all current task
    else:
        tasks = Task.query.order_by(Task.created).all()
        return render_template("index.html",tasks=tasks)

# delete task
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = Task.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error:{e}")
        return f"ERROR:{e}"

# edit task
@app.route("/update/<int:id>", methods = ["GET","POST"])
def edit(id:int):
    edit_task = Task.query.get_or_404(id)
    if request.method == "POST":
        edit_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template("edit.html",task=edit_task)

if __name__ == "__main__":
    app.run(debug=True)