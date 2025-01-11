from flask import Flask, jsonify, render_template
import json

# Step 1: Generate Multi-Level JSON Data
stories_data = {
    "stories": [
        {
            "id": 1,
            "genre": "Mystery",
            "author": "John Doe",
            "publish_date": "2025-01-01",
            "title": "The Hidden Path",
            "short_story": {
                "introduction": "It was a dark and stormy night when Sarah stumbled upon the hidden path in the woods.",
                "main_content": [
                    "She hesitated before stepping forward, her flashlight flickering in the wind.",
                    "The path twisted and turned, leading her deeper into the unknown.",
                    "Strange noises surrounded her, but curiosity pushed her onward."
                ],
                "conclusion": "At the end of the path, Sarah found an ancient chest, its contents changing her life forever."
            }
        },
        {
            "id": 2,
            "genre": "Fantasy",
            "author": "Jane Smith",
            "publish_date": "2024-12-15",
            "title": "The Enchanted Forest",
            "short_story": {
                "introduction": "In a world where magic was fading, Elara ventured into the enchanted forest to find a cure for her people.",
                "main_content": [
                    "The trees shimmered with an ethereal glow, and whispers filled the air.",
                    "Elara encountered mystical creatures who guided her with cryptic clues.",
                    "Her journey tested her courage, wisdom, and compassion."
                ],
                "conclusion": "Elara discovered a magical fountain, and with its waters, she restored magic to her world."
            }
        },
        {
            "id": 3,
            "genre": "Science Fiction",
            "author": "Alan Turing",
            "publish_date": "2023-08-10",
            "title": "Beyond the Stars",
            "short_story": {
                "introduction": "Captain Vega and her crew embarked on a mission to explore the uncharted regions of the galaxy.",
                "main_content": [
                    "Their spacecraft, the Horizon, encountered a mysterious anomaly.",
                    "The crew faced challenges from alien species and their own fears.",
                    "A discovery was made that could alter humanity's destiny."
                ],
                "conclusion": "They returned to Earth with knowledge that united planets across the galaxy."
            }
        }
    ]
}

filepath = 'flaskAPI/story/files/stories_data.json'

# Save the JSON data to a file
with open(filepath, 'w') as json_file:
    json.dump(stories_data, json_file, indent=4)

# Step 2: Create a Flask API
app = Flask(__name__)
@app.route('/', methods=['GET'])
def show_home():
    return render_template('index.html')

@app.route('/stories', methods=['GET'])
def get_stories():
    """API endpoint to fetch and display all stories."""
    try:
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "Stories data not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
