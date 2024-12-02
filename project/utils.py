import os
import re
import json

USER_INPUT = os.path.join(os.path.dirname(__file__), "user_input.txt")
PROMPT_NLU = os.path.join(os.path.dirname(__file__), "prompt_NLU.txt")
PROMPT_DM = os.path.join(os.path.dirname(__file__), "prompt_DM.txt")
PROMPT_NLG = os.path.join(os.path.dirname(__file__), "prompt_NLG.txt")

def extract_json(response):
    """Extract and parse the JSON part from a response string."""
    try:
        # Find the JSON-like part by looking for the first opening brace '{'
        start = response.find('{')
        if start != -1:
            json_part = response[start:]

            # Replace single quotes with double quotes
            json_part = re.sub(r"'", r'"', json_part)

            # Replace Python literals with JSON-compliant literals
            json_part = re.sub(r'\bNone\b', 'null', json_part)  # Replace None with null
            json_part = re.sub(r'\bTrue\b', 'true', json_part)  # Replace True with true
            json_part = re.sub(r'\bFalse\b', 'false', json_part)  # Replace False with false

            # Attempt to load the sanitized JSON
            return json.loads(json_part)
        else:
            raise ValueError("No JSON object found in the response.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")

def check_response_dict(response):
    """Check if the response is a dictionary."""
    if isinstance(response, str):
        try:
            dict_status = extract_json(response)
        except ValueError as e:
            raise ValueError(f"Response is not valid JSON: {e}")
    elif not isinstance(response, dict):
        raise ValueError(f"Expected a dictionary but got {type(response)}")
    else:
        dict_status = response  # Already a dictionary

    # print("\n\nValidated response (as dictionary):\n\n", dict_status)
    return dict_status

def update_dict_status(existing_status, new_status):
    """Recursively update the existing dictionary with new data."""
    for key, value in new_status.items():
        if isinstance(value, dict) and key in existing_status:
            # Recursively update nested dictionaries
            update_dict_status(existing_status[key], value)
        else:
            # Overwrite or add new keys
            existing_status[key] = value
