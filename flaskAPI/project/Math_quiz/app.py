from flask import Flask,request,redirect,render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/submit/', methods=['POST'])
def submit():
    try:
        # Get values from the form
        x1 = request.form.get("x1", type=float)  # Convert to float (or int if you want)
        x2 = request.form.get("x2", type=float)

        ans1 = 3
        ans2 = 2

        if (x1 == ans1 or x1 == ans2) and (x2 == ans1 or x2 == ans2) and (x1!=x2):
            return f"Correct: {x1} and {x2} "
        
        else:
            return f"incorrect:{x1} or {x2}"


    except ValueError:
        return "Invalid input! Please enter numbers.", 400

if __name__ == '__main__':
    app.run(debug=True)