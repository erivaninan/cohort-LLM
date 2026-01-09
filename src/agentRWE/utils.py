#cohort_LLM/src/agentRWE/utils.py
# Technical sanitization layer providing resilient API calling logic
# and data validation for LLM-generated outputs.

from google.api_core import exceptions
import time

def ensure_dict(data):
    """
    Ensures the input is a dictionary.
    If the AI returns a list (e.g., [ {...} ]), it extracts the first element.
    If the data is invalid, it returns an empty dictionary.
    """
    # check if it is already a dictionary
    if isinstance(data, dict):
        return data

    # check if it is a non-empty list
    if isinstance(data, list) and len(data) > 0:
        # Check if the first element of that list is a dictionary
        if isinstance(data[0], dict):
            return data[0]

    # safety fallback just in case
    return {}

def validate_scores(data, key, min_val=0, max_val=100):
    """
    Ensures numerical values (like adherence or symptoms) stay
    within scientifically plausible bounds.
    """
    # check if the key exists in the dictionary
    if key in data:
        value = data[key]

        # check if the value is a number (int or float) or a string that can be an int
        if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
            val = int(value)
            # clamp the value between min and max
            data[key] = max(min_val, min(max_val, val))
        else:
            # fallback to min_val if the type is completely unexpected
            data[key] = min_val

    return data

def safe_generate_content(model, prompt, generation_config, max_retries=3):
    """Handles API calls with exponential backoff for Rate Limits (429)."""
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt, generation_config=generation_config)
        except exceptions.ResourceExhausted:
            wait_time = (attempt + 1) * 15 # Wait a bit longer for Free Tier
            print(f"Quota exhausted. Retry {attempt + 1}/{max_retries}. Waiting {wait_time}s...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"API Error: {e}")
            return None
    return None