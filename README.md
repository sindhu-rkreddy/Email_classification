---
title: Email Classification API
emoji: 📧
colorFrom: purple
colorTo: indigo
sdk: docker
app_file: main.py
pinned: false
---

# Title: Secure Email Management System with PII Masking.
Secure Email Management System with PII Masking
## 1. Project Overview
This project implements a FastAPI for email classification and PII masking, utilizing machine learning models. Containerized with Docker, the API is deployed on Hugging Face Spaces, offering public access and interactive testing. It efficiently classifies emails, masks sensitive data, and facilitates demasking.

## 2. Problem Statement
Given an incoming email text, the system should:

Accurately classify the email into one of several predefined categories (e.g., Sales, HR, Marketing).

Detect and mask any personally identifiable information (PII) present within the email content.

Provide functionality to demask previously masked PII using a provided mapping.

Return all processing results (e.g., masked text, classification, extracted PII) in a well-defined JSON format.

## 3. Model Details
Overall Approach: Employs a two-pronged machine learning strategy for distinct tasks.

### Email Classification:

### Feature Extraction
Uses a TF-IDF Vectorizer to transform text into numerical features, capturing word importance.

### Classifier
Employs a supervised machine learning classifier (e.g., Logistic Regression or similar scikit-learn model, based on your training choice) trained on categorized email datasets.

### PII Detection

### Library Used
Utilizes the spaCy library.

### Specific Model
Leverages spaCy's pre-trained statistical model, en_core_web_sm, for Named Entity Recognition (NER).

### Functionality
Identifies various PII types including names, phone numbers, email addresses, and locations.

## 4. System Pipeline
### Input: Accepts JSON payload containing the email text (e.g., in an input_email_body field) for processing.

### Text Preprocessing
The raw input text undergoes cleaning, including lowercasing, removal of punctuation, special characters, and digits, and elimination of common stopwords.

### PII Detection & Masking
Utilizes spaCy's NER model to identify and then mask sensitive PII (e.g., names, phone numbers) within the cleaned text using designated placeholders.

### Text Vectorization: For classification purposes, the (potentially masked) text is transformed into numerical features using the pre-trained TF-IDF Vectorizer.

### Email Classification
The vectorized text is fed into the trained machine learning model to predict the email's category.

### Output Generation
Assembles the processed results, including the masked text, identified PII mapping (if applicable), and the predicted email category.

### Output
Returns a structured JSON response containing the processed information.

## 5. PII Detection & Masking
Types of PII detected include:

Phone Numbers

Email Addresses

Aadhar Numbers

Dates

Expiry Numbers

Each entity is replaced with a corresponding placeholder like [phone], [aadhar_num], etc., and recorded in a list with position, classification, and original text.

## 6. API Endpoints
GET /
Description: Health check endpoint.

Response:

{"detail":"Not Found"}

(Note: This is the default FastAPI response for the root path if no specific GET endpoint is defined. Your API is fully functional at /classify.)

POST /classify
Description: Accepts email content and returns classification with PII masking.

Request Body:

{
  "input_email_body": "Subject: Important: KYC Update, my Aadhar number is 1234-5678-9123."
}

Response:

{
  "input_email_body": "Subject: Important: KYC Update, my Aadhar number is 1234-5678-9123.",
  "list_of_masked_entities": [
    {
      "position": [45, 60],
      "classification": "aadhar_num",
      "entity": "1234-5678-9123"
    }
  ],
  "masked_email": "Subject: Important: KYC Update, my Aadhar number is [aadhar_num].",
  "category_of_the_email": "Request"
}

(Note: The category_of_the_email will be one of "Incident", "Request", "Change", or "Problem".)

## 7. Sample Testing via curl
Using curl (for Linux, macOS, or Git Bash on Windows):

curl -X POST "[https://chittisvr-email-classifier.hf.space/classify](https://chittisvr-email-classifier.hf.space/classify)" \
     -H "Content-Type: application/json" \
     -d '{
           "input_email_body": "Subject: Urgent issue, my name is John Doe and my email is john.doe@example.com. Please help with my account."
         }'

Using PowerShell (Invoke-RestMethod):

Invoke-RestMethod -Uri "[https://chittisvr-email-classifier.hf.space/classify](https://chittisvr-email-classifier.hf.space/classify)" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{ "input_email_body": "Subject: Urgent issue, my name is John Doe and my email is john.doe@example.com. Please help with my account." }' | ConvertTo-Json -Depth 4

Using FastAPI's Interactive Docs (Recommended for easy testing):
Visit https://chittisvr-email-classifier.hf.space/docs in your web browser, expand the /classify endpoint, click "Try it out", and then "Execute".

## Observatioins
Terminal output with a classification report for an email model, including precision, recall, f1-score, and accuracy metrics for different categories like Change, Incident, Problem, and Request.
![Image](https://github.com/user-attachments/assets/fce1df6a-f9e6-45d7-99e3-5f2f61b3b14d)

![Image](https://github.com/user-attachments/assets/9907914e-b27a-4e8d-96fd-e01ebd491c45)

 A JSON request body for the email classification API.     
![Image](https://github.com/user-attachments/assets/651a3ca1-2724-4075-9f3d-26ab71277406)

A successful JSON response from the email classification API, displaying the input_email_body, an empty list_of_masked_entities, the masked_email, and the category_of_the_email as "Incident". It also shows response headers.
![Image](https://github.com/user-attachments/assets/67ecd8cc-f8df-4c0e-a809-81ab4836067e)

## 8. Deployment & Source Code Links
Hugging Face Deployment: https://huggingface.co/spaces/chittisvr/email-classifier

GitHub Repository:https://github.com/sindhu-rkreddy/Email_classification

# Designed and executed by : R SINDHU
