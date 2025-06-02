import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib # For saving/loading models
import os

class EmailClassifier:
    def __init__(self, model_path='email_classifier_model.joblib',
                 vectorizer_path='tfidf_vectorizer.joblib'):
        self.model = None
        self.vectorizer = None
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path

    def train(self, emails: pd.Series, labels: pd.Series):
        """
        Trains the email classification model.
        Args:
            emails (pd.Series): Series of email texts (masked).
            labels (pd.Series): Series of corresponding email categories.
        """
        X_train, X_test, y_train, y_test = train_test_split(
            emails, labels, test_size=0.2, random_state=42, stratify=labels
        )

        # Initialize TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        # Initialize and train RandomForestClassifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_vec, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test_vec)
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        # Save the trained model and vectorizer
        self._save_model()

    def predict(self, email_text: str):
        """
        Predicts the category of a single email text.
        Args:
            email_text (str): The masked email text to classify.
        Returns:
            str: Predicted category.
        """
        if self.model is None or self.vectorizer is None:
            self.load_model()
            if self.model is None or self.vectorizer is None:
                raise Exception("Model or vectorizer not loaded. Please train the model first.")

        email_vec = self.vectorizer.transform([email_text])
        prediction = self.model.predict(email_vec)
        return prediction[0]

    def _save_model(self):
        """Saves the trained model and vectorizer to disk."""
        if self.model and self.vectorizer:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            print(f"Model saved to {self.model_path}")
            print(f"Vectorizer saved to {self.vectorizer_path}")
        else:
            print("No model or vectorizer to save.")

    def load_model(self):
        """Loads the trained model and vectorizer from disk."""
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            print("Model and vectorizer loaded successfully.")
        else:
            print("Model or vectorizer files not found. Please train the model first.")

# Example Usage (for training)
if __name__ == "__main__":
    # Assuming 'combined_emails_with_natural_pii.csv' is available
    df = pd.read_csv('combined_emails_with_natural_pii.csv')

    # Apply PII masking to the 'email' column
    # Note: For training, you should use the masked emails.
    # We will perform the actual masking in the API endpoint.
    # For simplicity in this example, we'll just use the raw emails for training TFIDF,
    # but in a real scenario, you'd mask them first before training the classifier on masked data.
    # A more robust approach would be to mask all emails in the dataset for training.
    # For now, let's proceed with an assumption that the 'email' column will be masked before
    # being fed to the classifier during inference. For training, we can simplify this if
    # the PII doesn't significantly alter the core content for classification.

    # Let's create a masked email column for training for consistency.
    from utils import mask_pii
    masked_emails = []
    for email_text in df['email']:
        masked_text, _ = mask_pii(email_text)
        masked_emails.append(masked_text)
    df['masked_email'] = masked_emails


    classifier = EmailClassifier()
    classifier.train(df['masked_email'], df['type'])

    # Test prediction
    test_email_masked = "Subject: Need help with my account [full_name]. I can't log in."
    predicted_category = classifier.predict(test_email_masked)
    print(f"\nPredicted category for '{test_email_masked}': {predicted_category}")