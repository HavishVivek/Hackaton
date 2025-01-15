from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import string

# Load the trained model and vectorizer
model = joblib.load("spam_detector_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for Flutter integration

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data.get("message", "")
    
    # Preprocess the message
    message_cleaned = message.translate(str.maketrans('', '', string.punctuation)).lower()
    
    # Vectorize the message
    message_vect = vectorizer.transform([message_cleaned])
    
    # Predict using the trained model
    prediction = model.predict(message_vect)[0]
    
    # Return the result
    result = "spam" if prediction == 1 else "ham"
    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)