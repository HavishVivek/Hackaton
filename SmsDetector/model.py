import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import string
import joblib

# Step 1: Load the Dataset
file_path = "../data/SMSSpamCollection"
df = pd.read_csv(file_path, sep='\t', header=None, names=["label", "message"])

# Step 2: Data Preprocessing
df['message'] = df['message'].dropna().apply(
    lambda x: x.translate(str.maketrans('', '', string.punctuation)).lower()
)

# Split dataset into features (X) and labels (y)
X = df['message']
y = df['label']

# Encode labels (ham -> 0, spam -> 1)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Step 3: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Vectorize the Text Data
vectorizer = CountVectorizer(stop_words='english')
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Step 5: Train the Naive Bayes Classifier
model = MultinomialNB()
model.fit(X_train_vect, y_train)

# Step 6: Evaluate the Model
y_pred = model.predict(X_test_vect)

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['ham', 'spam']))

# Step 7: Save the Model and Vectorizer
model_path = "spam_detector_model.pkl"
vectorizer_path = "vectorizer.pkl"

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print(f"Model saved to {model_path}")
print(f"Vectorizer saved to {vectorizer_path}")