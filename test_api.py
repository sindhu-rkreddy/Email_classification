import requests
import json

api_url = "https://chittisvr-email-classifier.hf.space/classify"

# Example 1: Basic test
email_body_1 = "Subject: Urgent issue, my name is John Doe and my email is john.doe@example.com. Please help with my account."
payload_1 = {"input_email_body": email_body_1}

print("--- Test Case 1 ---")
response_1 = requests.post(api_url, json=payload_1)
print(f"Status Code: {response_1.status_code}")
print(f"Response JSON: {json.dumps(response_1.json(), indent=2)}")
print("-" * 20)

# Example 2: Another test case
email_body_2 = "Hello, I need to reset my password for my account at example.com. My phone number is 123-456-7890."
payload_2 = {"input_email_body": email_body_2}

print("--- Test Case 2 ---")
response_2 = requests.post(api_url, json=payload_2)
print(f"Status Code: {response_2.status_code}")
print(f"Response JSON: {json.dumps(response_2.json(), indent=2)}")
print("-" * 20)