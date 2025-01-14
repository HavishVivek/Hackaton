from flask import Flask, request, jsonify
import joblib

# Load the trained spam detection model
model = joblib.load("spam_detector.pkl")

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the message from the incoming request
        data = request.get_json()
        message = data.get('message', '')

        # Check if message is provided
        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Predict whether the message is spam or not
        prediction = model.predict([message])[0]

        # Return the result as a JSON response
        return jsonify({"spam": bool(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)