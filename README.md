<<<<<<< HEAD
# Email Classification System

This repository contains the implementation for an email classification system that categorizes incoming support emails and masks Personally Identifiable Information (PII) before processing.

## Project Structure

.
├── .gitignore
├── README.md
├── requirements.txt
├── main.py             # Entry point for the FastAPI application
├── models.py           # ML model training and inference logic
└── utils.py            # General-purpose utility functions (PII masking)


## Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone <your-repository-link>
    cd <your-repository-name>
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Place the Dataset:**
    Ensure the `combined_emails_with_natural_pii.csv` dataset is placed in the root directory of the project.

5.  **Train the Model (Optional - for initial setup or retraining):**
    The `main.py` will attempt to train the model if `email_classifier_model.joblib` and `tfidf_vectorizer.joblib` are not found. However, you can explicitly run the training script:

    ```bash
    python models.py
    ```
    This will generate `email_classifier_model.joblib` and `tfidf_vectorizer.joblib` files in the root directory after training.

## Local Usage

1.  **Run the FastAPI Application:**

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

    The API will be accessible at `http://0.0.0.0:8000`.

2.  **Test the Endpoint:**
    You can test the `/classify` endpoint using `curl`, Postman, or any API client.

    **Example POST Request (using `curl`):**

    ```bash
    curl -X POST "[http://0.0.0.0:8000/classify](http://0.0.0.0:8000/classify)" \
         -H "Content-Type: application/json" \
         -d '{
               "input_email_body": "Subject: Urgent issue, my name is John Doe and my email is john.doe@example.com. Please help with my account."
             }'
    ```

    **Expected Output Format:**

    ```json
    {
      "input_email_body": "Subject: Urgent issue, my name is John Doe and my email is john.doe@example.com. Please help with my account.",
      "list_of_masked_entities": [
        {
          "position": [40, 48],
          "classification": "full_name",
          "entity": "John Doe"
        },
        {
          "position": [69, 89],
          "classification": "email",
          "entity": "john.doe@example.com"
        }
      ],
      "masked_email": "Subject: Urgent issue, my name is [full_name] and my email is [email]. Please help with my account.",
      "category_of_the_email": "Request" # Or "Incident", "Change", "Problem"
    }
    ```

## Deployment on Hugging Face Spaces

1.  **Create a Hugging Face Space:**
    Go to [Hugging Face Spaces](https://huggingface.co/spaces) and create a new Space.
    * Choose "Docker" as the SDK (or "Gradio" if you want a UI, but the assignment specifies no frontend).
    * Select a suitable Docker image (e.g., `python-latest`).

2.  **Connect your GitHub Repository:**
    Link your Hugging Face Space to this GitHub repository. Hugging Face will automatically detect your `requirements.txt` and `main.py` (or whatever you set as the entry point) and build the application.

3.  **Ensure `combined_emails_with_natural_pii.csv` and `.joblib` files are available:**
    * **Dataset:** Make sure `combined_emails_with_natural_pii.csv` is committed to your repository.
    * **Trained Models:** It's highly recommended to train the model locally (`python models.py`) and commit the generated `email_classifier_model.joblib` and `tfidf_vectorizer.joblib` files to your repository *before* deploying to Hugging Face Spaces. This avoids the need for retraining on every deployment. If the files are not present, the `main.py` will attempt to train during startup, which might be slow.

4.  **Hugging Face Spaces `app.py` (for Docker/Custom SDK):**
    If you're using a custom Dockerfile or a generic SDK, you might need to specify the command to run your FastAPI app. For a standard Python Space, it often automatically runs `main.py` if it detects FastAPI. If not, you might need an `app.py` or `.env` file to configure the startup command for `uvicorn`.

    Example `app.py` (if `main.py` isn't picked up automatically):

    ```python
    # app.py
    from main import app
    ```
    Then, configure your Space to run `uvicorn app:app --host 0.0.0.0 --port 7860` (Hugging Face Spaces often use port 7860).

5.  **Access the API Endpoint:**
    Once deployed, your API endpoint will be available at:
    `https://<your-username>-<your-space-name>.hf.space/classify`

    **Important Note:** The evaluation system will hit this precise endpoint, so ensure it is configured correctly.

## Evaluation Criteria

Refer to the original assignment document for the detailed evaluation criteria, including API deployment, code quality, GitHub submission, test case coverage, and report detail.

---
title: Email Classifier
emoji: 📉
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: apache-2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
 b73bbda287f6d66886564890b2c8128a76484839
