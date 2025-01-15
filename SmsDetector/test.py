import joblib

# Step 1: Load the Trained Model and Vectorizer
model_path = "spam_detector_model.pkl"
vectorizer_path = "vectorizer.pkl"

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

# Step 2: Define a Function for Testing
def predict_message(message):
    """
    Predict whether a message is spam or ham.

    Parameters:
        message (str): The input message to classify.

    Returns:
        str: 'spam' or 'ham' based on the prediction.
    """
    # Preprocess the message (lowercase and remove punctuation)
    import string
    message_cleaned = message.translate(str.maketrans('', '', string.punctuation)).lower()
    
    # Transform the message into a vector
    message_vect = vectorizer.transform([message_cleaned])
    
    # Predict using the trained model
    prediction = model.predict(message_vect)[0]
    
    # Return the label ('ham' or 'spam')
    return 'spam' if prediction == 1 else 'ham'

# Step 3: Test with New Messages
while True:
    print("\nEnter a message to classify (or type 'exit' to quit):")
    input_message = input("Message: ").strip()
    
    if input_message.lower() == "exit":
        print("Exiting the test application.")
        break
    
    result = predict_message(input_message)
    print(f"The message is classified as: {result}")