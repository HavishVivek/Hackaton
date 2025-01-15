import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import string

# File path to the dataset downloaded on your computer
file_path = "../data/SMSSpamCollection"  # Update this with the actual path to the file

# Load dataset with proper encoding
df = pd.read_csv(file_path, sep='\t', header=None, names=["label", "message"], encoding='latin-1')

# Debug: Check dataset shape and contents
print(df.head())
print(f"Dataset shape before preprocessing: {df.shape}")

# Handle missing values (drop rows with NaN values in the 'message' column)
df.dropna(subset=['message'], inplace=True)

# Debug: Check shape after dropping NaN values
print(f"Shape after dropping NaN: {df.shape}")

# Data Preprocessing: Remove punctuation and convert to lowercase
df['message'] = df['message'].apply(
    lambda x: x.translate(str.maketrans('', '', string.punctuation)).lower() if isinstance(x, str) else x
)

# Debug: Check for empty or invalid messages
print(f"Number of empty messages: {(df['message'].str.strip() == '').sum()}")
df = df[df['message'].str.strip() != '']  # Remove empty messages

# Debug: Check shape after removing empty strings
print(f"Shape after removing empty strings: {df.shape}")

# Split dataset into features and labels
X = df['message']
y = df['label']

# Encode labels (ham = 0, spam = 1)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Train-test split (80% train, 20% test)
if len(X) == 0 or len(y) == 0:
    print("Error: Dataset is empty after preprocessing.")
else:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Vectorize the text messages using CountVectorizer
    vectorizer = CountVectorizer(stop_words='english')
    X_train_vect = vectorizer.fit_transform(X_train)
    X_test_vect = vectorizer.transform(X_test)

    # Display confirmation
    print("Data preprocessing complete!")
    print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")