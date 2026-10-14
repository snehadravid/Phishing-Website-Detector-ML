import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from feature_extraction import extract_features


# Load dataset
df = pd.read_csv("dataset/PhiUSIIL_Phishing_URL_Dataset.csv")

print("Dataset loaded!")
print("Total rows:", len(df))


# Extract URL-based features
X = df["URL"].apply(extract_features).apply(pd.Series)

# Target
y = df["label"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("Training model...")


# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# Train
model.fit(X_train, y_train)


# Predict
predictions = model.predict(X_test)


# Accuracy
accuracy = accuracy_score(y_test, predictions)

print()
print("Model Accuracy:", accuracy)

print()
print("Classification Report:")
print(classification_report(y_test, predictions))


# Save model
joblib.dump(model, "models/phishing_model.pkl")

print()
print("Model saved successfully!")