from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from utils import mask_pii, demask_email
from models import EmailClassifier
import os

app = FastAPI()

# Load the classifier model and vectorizer when the application starts
classifier = EmailClassifier()
classifier.load_model() # This will attempt to load the pre-trained model

# If the model files don't exist (e.g., first run), train the model
# In a production environment, you would typically pre-train the model
# and ensure the joblib files are available.
if classifier.model is None or classifier.vectorizer is None:
    print("Model not found. Attempting to train the model now...")
    try:
        import pandas as pd
        df = pd.read_csv('combined_emails_with_natural_pii.csv')

        # Mask emails for training the classifier
        masked_emails = []
        for email_text in df['email']:
            masked_text, _ = mask_pii(email_text)
            masked_emails.append(masked_text)
        df['masked_email_for_training'] = masked_emails

        classifier.train(df['masked_email_for_training'], df['type'])
    except Exception as e:
        print(f"Error during initial model training: {e}")
        print("Please ensure 'combined_emails_with_natural_pii.csv' is in the root directory and contains 'email' and 'type' columns.")


class EmailInput(BaseModel):
    input_email_body: str

class MaskedEntity(BaseModel):
    position: List[int]
    classification: str
    entity: str

class EmailOutput(BaseModel):
    input_email_body: str
    list_of_masked_entities: List[MaskedEntity]
    masked_email: str
    category_of_the_email: str

@app.post("/classify", response_model=EmailOutput)
async def classify_email(email_input: EmailInput):
    """
    Receives an email, masks PII, classifies it, and returns the result.
    """
    original_email_body = email_input.input_email_body

    # 1. Mask PII
    masked_email, masked_entities_list = mask_pii(original_email_body)

    # 2. Classify the masked email
    if classifier.model is None or classifier.vectorizer is None:
        return {"error": "Model not loaded. Please ensure the model is trained and saved correctly."}

    predicted_category = classifier.predict(masked_email)

    # 3. Prepare the response
    return EmailOutput(
        input_email_body=original_email_body,
        list_of_masked_entities=masked_entities_list,
        masked_email=masked_email,
        category_of_the_email=predicted_category
    )