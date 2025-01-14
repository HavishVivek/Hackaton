import joblib

# Load the saved model and vectorizer
model = joblib.load("spam_detector.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")

def test_model(message):
    # Vectorize the input message
    vector = tfidf.transform([message])
    prediction = model.predict(vector)[0]

    if prediction == 1:
        return "Spam Message"
    else:
        return "Not Spam"

# Example usage
if __name__ == "__main__":
    # Get message input from the user
    message = input("Enter an SMS message to test: ")
    result = test_model(message)
    print(f"The message is: {result}")