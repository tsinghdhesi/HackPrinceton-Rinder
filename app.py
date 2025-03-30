from flask import Flask, render_template, request, jsonify
from analysis import analyze_user

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
