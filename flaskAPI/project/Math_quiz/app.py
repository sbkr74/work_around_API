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

        # Validation: Check if both values are numbers and not empty
        if x1 is None or x2 is None:
            return "Error: Missing input values!", 400  # Bad Request

        # Additional check (example: both values must be positive)
        if x1 <= 0 or x2 <= 0:
            return "Error: Both numbers must be positive!", 400

        return f"Received values: x1 = {x1}, x2 = {x2}"

    except ValueError:
        return "Invalid input! Please enter numbers.", 400

if __name__ == '__main__':
    app.run(debug=True)