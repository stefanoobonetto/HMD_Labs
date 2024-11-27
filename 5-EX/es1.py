import subprocess
import os
import re
import json
import time

def run_bash_script(script_path, file1, file2):
    try:
        result = subprocess.run(['bash', script_path, file1, file2], check=True, text=True, capture_output=True)
        print("Script output:")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the script: {e}")
        print("Script error output:")
        print(e.stderr)

def extract_dict_from_file(file_path, interval=2):
    while True:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                print("Checking file content...")
                print(content)
                
                # Match the JSON structure without recursion
                match = re.search(
                    r'\{\s*"NLU"\s*:\s*\{\s*"intent"\s*:\s*".*?"\s*,\s*"slots"\s*:\s*\{.*?\}\s*\}\s*\}',
                    content,
                    re.DOTALL
                )
                
                if match:
                    print("Found potential dictionary:\n", match.group(0))
                    dict_str = match.group(0)
                    
                    # Try to parse the matched string as JSON
                    parsed_dict = json.loads(dict_str)
                    return parsed_dict
        except json.JSONDecodeError as e:
            print(f"Found potential dictionary but could not parse: {e}")
        except Exception as e:
            print(f"Error reading the file: {e}")

        time.sleep(interval)
    return None

# Paths
bash_script_path = os.path.join(os.path.dirname(__file__), 'run.sh')
prompt_path = os.path.join(os.path.dirname(__file__), 'prompt_NLU.txt')
input_path = os.path.join(os.path.dirname(__file__), 'input.txt')

# Read input files
with open(prompt_path, 'r') as f:
    prompt = f.read()
    print(prompt)

with open(input_path, 'r') as f:
    input_text = f.read()
    print(input_text)

# Run the bash script
# output = run_bash_script(bash_script_path, prompt_path, input_path)
output = 1
# print("\n\n", output)
# if output:
#     match = re.search(r'Submitted batch job (\d+)', output)
#     if match:
# job_number = match.group(1)
job_number = 935321
print(f"Extracted Job Number: {job_number}")
path_output = os.path.join(os.path.dirname(__file__), f'hmd_example-{job_number}.out')

# Check and parse dictionary structure in a loop
parsed_dict = extract_dict_from_file(path_output, interval=5)
if parsed_dict:
    print("Parsed Dictionary:")
    print(parsed_dict)
    prompt_DM = "" 
    }
else:
    print("Dictionary not found within the timeout.")
    # else:
    #     print("Job number could not be extracted.")
