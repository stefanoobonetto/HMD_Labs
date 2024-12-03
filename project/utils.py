import os
import re
import json
from argparse import Namespace
from typing import Tuple

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BatchEncoding,
    PreTrainedTokenizer,
    PreTrainedModel,
)

USER_INPUT = os.path.join(os.path.dirname(__file__), "user_input.txt")
PROMPT_NLU = os.path.join(os.path.dirname(__file__), "prompt_NLU.txt")
PROMPT_DM = os.path.join(os.path.dirname(__file__), "prompt_DM.txt")
PROMPT_NLG = os.path.join(os.path.dirname(__file__), "prompt_NLG.txt")

MODELS = {
    "llama2": "meta-llama/Llama-2-7b-chat-hf",
    "llama3": "meta-llama/Meta-Llama-3-8B-Instruct",
}

TEMPLATES = {
    "llama2": "<s>[INST] <<SYS>>\n{}\n<</SYS>>\n\n{} [/INST]",
    "llama3": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
}

PROMPTS = {
    "NLU": """You are the NLU component.
Identify the user intent from this list: [ramen_ordering, pizza_ordering, pizza_delivery, flight_booking, drink_ordering]
If the intent is ramen_ordering, extract the slots from the input of the user.
The slots are: [broth, spaghetti_type, egg, seaweed] and the values can be:

broth : {null, "none", "pork", "chicken"}
spaghetti_type : {null, "rice_noodles", "weath_noodles"},
egg : {null, "no", "yes"},
seaweed : {null, "yes", "no"}

If no values are present in the user input you have to put null as the value, pay attention to this, don't hallucinate, if you're not sure, please write null.
Output them as a json in the following manner (no other phrases just the json):

{
    "NLU": {
        "intent": "ramen_ordering",
        "slots": {
            "broth": ...,
            "spaghetti_type": ...,
            "egg": ...,
            "seaweed": ...
        }
    }
}

""",

    "DM": """You are the Dialogue Manager.
Given the input json of the NLU component, you should generate the best action to take from this list:
- request_info(slot), if a slot value is missing (null value)
- confirmation(intent), if all slots have been filled with a value (notice that "none" may be an accepted slot value)

return your response updating the json file, adding an entry "DM" : { "next_best_action" : "request_info(<slot_name>)"} 
for in the first case, or confirmation(intent) if in the second case.

The final result will be something like the following dictionary, without any other introduction phrases and other stuff:

{
    "NLU": {
        "intent": "ramen_ordering",
        "slots": { ... }
    },
    "DM": {
        "next_best_action": ...
    }
}

where the NLU entry is the same as the input one and the DM one is the one you have to update.
""",

    "NLG": """You are the NLG component, 
Given the best action classified by the DM Component (you'll find it as a JSON input entry), you should generate a lexicalized response for the user.
Possible next best actions are:
- request_info(slot_name): you have to ask to the user to provide informations to fill the slot    
- confirmation(intent), confirm the task has been completed and the ramen has been ordered

Please return only the question enclosed in quotation marks.


You will receive a json file like the following:

{
    "NLU": {
        "intent": "ramen_ordering",
        "slots": { ... }
    },
    "DM": {
        "next_best_action": ...
    }
}

Consider the following values for the slots:

broth : {null, "none", "pork", "chicken"}
spaghetti_type : {null, "rice_noodles", "weath_noodles", "bucatini", "udon"},
egg : {null, "no", "yes"},
seaweed : {null, "yes", "no"}

Lexicalize the next_best_action given by the DM component taking into account the possible values of the slots.

"""
}


def load_model(args: Namespace) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        device_map="auto" if args.parallel else args.device, 
        torch_dtype=torch.float32 if args.dtype == "f32" else torch.bfloat16,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    return model, tokenizer  # type: ignore


def generate(
    model: PreTrainedModel,
    inputs: BatchEncoding,
    tokenizer: PreTrainedTokenizer,
    args: Namespace,
) -> str:
    output = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=args.max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(
        output[0][len(inputs.input_ids[0]) :], skip_special_tokens=True
    )


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
