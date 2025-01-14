import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("./data/spam.csv", encoding="latin-1")
data = data.rename(columns={"v1": "label", "v2": "message"})[["label", "message"]]

# Map labels to binary (0 = ham, 1 = spam)
data["label"] = data["label"].map({"ham": 0, "spam": 1})

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    data["message"], data["label"], test_size=0.2, random_state=42
)

# Vectorize text using TF-IDF
tfidf = TfidfVectorizer(stop_words="english", max_features=3000)
X_train_vectorized = tfidf.fit_transform(X_train)
X_test_vectorized = tfidf.transform(X_test)

# Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train_vectorized, y_train)

# Evaluate the model
y_pred = model.predict(X_test_vectorized)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save the model and vectorizer
joblib.dump(model, "spam_detector.pkl")
joblib.dump(tfidf, "tfidf_vectorizer.pkl")