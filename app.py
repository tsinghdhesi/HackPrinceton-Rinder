import os
import sys

# Add the repository root to sys.path so that analysis.py and gemini_ai.py can be found.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from analysis import analyze_user  # Now analysis.py should be found


# Define absolute paths for templates and static folders.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
templates_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'error': 'No username provided'}), 400

    top_matches = analyze_user(username)
    return jsonify(top_matches)

# Only run locally
if __name__ == '__main__':
    app.run(debug=True)
