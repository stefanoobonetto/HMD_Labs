import json
from utils import check_response_dict

class DictManager:
    """Manages operations on the dictionary status."""
    
    def __init__(self, initial_dict=None):
        self.dict_status = initial_dict or {}

    def validate_dict(self, response):
        """Validate and update dict_status with a new response."""
        parsed_response = check_response_dict(response)  # Assuming this validates and parses the response
        self.dict_status.update(parsed_response)
        return self.dict_status

    def update_slot(self, slot_name, slot_value):
        """Update a specific slot in the dictionary."""
        if "NLU" not in self.dict_status:
            self.dict_status["NLU"] = {"slots": {}}
        self.dict_status["NLU"]["slots"][slot_name] = slot_value

    def get_next_best_action(self):
        """Retrieve the next best action from the dictionary."""
        return self.dict_status.get("DM", {}).get("next_best_action", "No action available")

    def get_slot_value(self, slot_name):
        """Get the value of a specific slot."""
        return self.dict_status.get("NLU", {}).get("slots", {}).get(slot_name)

    def to_json(self):
        """Return the dictionary as a JSON string."""
        return json.dumps(self.dict_status, indent=2)
