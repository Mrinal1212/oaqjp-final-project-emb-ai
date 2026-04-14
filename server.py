"""
Flask server for Emotion Detection application.
Provides a web interface and API endpoint to analyze emotions in text.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """
    Render the index.html page for user input.
    """
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    """
    Detect emotions from user-provided text.
    Handles both GET (query parameter) and POST (JSON or form) requests.
    Returns formatted response or error message for blank input.
    """
    if request.method == 'GET':
        text_to_analyze = request.args.get("textToAnalyze", "")
    else:
        if request.is_json:
            data = request.get_json()
            text_to_analyze = data.get("text", "")
        else:
            text_to_analyze = request.form.get("text", "")

    result = emotion_detector(text_to_analyze)

    if result["dominant_emotion"] is None:
        return jsonify({"response": "Invalid text! Please try again!"})

    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
