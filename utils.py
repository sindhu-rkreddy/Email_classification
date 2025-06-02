import re

def mask_pii(text: str):
    """
    Detects and masks PII entities in the input text using regular expressions.
    Returns the masked text and a list of detected entities.
    """
    masked_entities = []
    masked_text = text

    # Define PII patterns and their corresponding entity types
    pii_patterns = {
        "full_name": r"\b[A-Z][a-z]+(?: [A-Z][a-z]+)+\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone_number": r"(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "dob": r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b",
        # Placeholder for Aadhar, Credit/Debit Card, CVV, Expiry - these require
        # more specific patterns or external validation for robust detection.
        # For demonstration, we'll use generic number patterns that might need refinement.
        "aadhar_num": r"\b\d{4}[-.\s]?\d{4}[-.\s]?\d{4}\b", # Example: XXXX XXXX XXXX
        "credit_debit_no": r"\b(?:\d{4}[-.\s]?){3}\d{4}\b", # Example: XXXX XXXX XXXX XXXX
        "cvv_no": r"\b\d{3,4}\b", # 3 or 4 digits
        "expiry_no": r"\b(?:0[1-9]|1[0-2])[-/.]\d{2,4}\b" # MM/YY or MM/YYYY
    }

    # Iterate through patterns and mask PII
    for entity_type, pattern in pii_patterns.items():
        for match in re.finditer(pattern, masked_text):
            original_entity = match.group(0)
            start, end = match.span()

            # Store the masked entity information
            masked_entities.append({
                "position": [start, end],
                "classification": entity_type,
                "entity": original_entity
            })

            # Replace the original entity with its masked form
            masked_text = masked_text[:start] + f"[{entity_type}]" + masked_text[end:]

            # Adjust subsequent positions due to the change in string length
            # This is a simplified adjustment and might need more robust handling for
            # complex masking scenarios where multiple entities are close together.
            for i in range(len(masked_entities) - 1):
                if masked_entities[i]["position"][0] > start:
                    diff = len(f"[{entity_type}]") - len(original_entity)
                    masked_entities[i]["position"][0] += diff
                    masked_entities[i]["position"][1] += diff


    return masked_text, masked_entities

def demask_email(masked_email: str, masked_entities: list):
    """
    Restores the original email from the masked email and masked entities list.
    """
    demasked_email = masked_email
    # Sort entities by their original start position in descending order
    # to avoid issues when replacing substrings as the string length changes.
    masked_entities.sort(key=lambda x: x['position'][0], reverse=True)

    for entity_info in masked_entities:
        original_start, original_end = entity_info['position']
        original_entity = entity_info['entity']
        entity_type = entity_info['classification']
        masked_placeholder = f"[{entity_type}]"

        # Find the masked placeholder in the current demasked_email string
        # This assumes that the placeholders are unique and correctly placed
        # after the initial masking.
        # A more robust approach might involve storing the exact start/end indices
        # within the *masked* string during the masking process.
        placeholder_index = demasked_email.find(masked_placeholder)

        if placeholder_index != -1:
            demasked_email = (demasked_email[:placeholder_index] +
                              original_entity +
                              demasked_email[placeholder_index + len(masked_placeholder):])
    return demasked_email

# Example Usage (for testing)
if __name__ == "__main__":
    test_email = "Hello, my name is John Doe, and my email is johndoe@example.com. My phone number is 123-456-7890. My DOB is 01/15/1985. My credit card is 1234-5678-9012-3456 and CVV is 123. Expiry is 12/26. My Aadhar is 1234 5678 9012."
    masked_text, masked_entities = mask_pii(test_email)

    print("Original Email:", test_email)
    print("Masked Email:", masked_text)
    print("Masked Entities:", masked_entities)

    demasked_text = demask_email(masked_text, masked_entities)
    print("Demasked Email:", demasked_text)

    # Test with special characters in email
    test_email_2 = "Contact me at alice.smith+alias@example.co.uk regarding issue 123-ABC. My name is Alice Smith."
    masked_text_2, masked_entities_2 = mask_pii(test_email_2)
    print("\nOriginal Email 2:", test_email_2)
    print("Masked Email 2:", masked_text_2)
    print("Masked Entities 2:", masked_entities_2)
    demasked_text_2 = demask_email(masked_text_2, masked_entities_2)
    print("Demasked Email 2:", demasked_text_2)