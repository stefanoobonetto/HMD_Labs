import subprocess
import os
import re
import json
import time

def run_bash_script(script_path, file1, file2):
    try:
        result = subprocess.run(['bash', script_path, file1, file2], check=True, text=True, capture_output=True)
        # print("Script output:")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the script: {e}")
        print("Script error output:")
        print(e.stderr)

def extract_dict_from_file(file_path, interval=2): 
    while True:
        try:
            with open(file_path, 'r+') as f:
                content = f.read()
                
                match = re.search(
                    r'\{\s*"NLU"\s*:\s*\{\s*"intent"\s*:\s*".*?"\s*,\s*"slots"\s*:\s*\{.*?\}\s*\}\s*(,\s*"DM"\s*:\s*\{.*?\}\s*)?\}',
                    content,
                    re.DOTALL
                )
                
                if match:
                    # print("Found dictionary:\n", match.group(0))
                    dict_str = match.group(0)
                    
                    try:
                        parsed_dict = json.loads(dict_str)
                    except json.JSONDecodeError:
                        print("Match found but not valid JSON, skipping.")
                        continue

                    # print("Validated JSON Dictionary:")
                    # print(parsed_dict)

                    f.seek(0)
                    f.write(dict_str)
                    f.truncate()  
                    return dict_str  

        except Exception as e:
            # print(f"Error reading the file: {e}")
            pass

        time.sleep(interval)  
    return None

def search_output(output_NLU):
    if output_NLU:
        match = re.search(r'Submitted batch job (\d+)', output_NLU)
        if match:
            return match.group(1)
    return None

def extract_final_question(file_path):
    while True:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
                match = re.search(r'"([^"]*)"', content)  
                if match:
                    sentence = match.group(1)  
                    # print(f"Found sentence: {sentence}")
                    return sentence
                else:
                    # print("No sentence found between quotation marks.")
                    continue
        except Exception as e:
            # print(f"Error reading the file: {e}")
            pass

def main():
    bash_script_path = os.path.join(os.path.dirname(__file__), 'run.sh')
    NLU_prompt_path = os.path.join(os.path.dirname(__file__), 'prompt_NLU.txt')
    DM_prompt_path = os.path.join(os.path.dirname(__file__), 'prompt_DM.txt')
    NLG_prompt_path = os.path.join(os.path.dirname(__file__), 'prompt_NLG.txt')
    input_path = os.path.join(os.path.dirname(__file__), 'user_input.txt')
    
    print("Running the pipeline...")
    
    output_NLU = run_bash_script(bash_script_path, NLU_prompt_path, input_path)
    
    job_number = search_output(output_NLU) 
    
    dict_str_out_NLU = "empty"
    path_output_NLU = None  
    if job_number:
        path_output_NLU = os.path.join(os.path.dirname(__file__), f'hmd_example-{job_number}.out')
        print(f"Checking NLU component's output... (on job {job_number})")
        dict_str_out_NLU = extract_dict_from_file(path_output_NLU, interval=5)
    else:
        print("No job number found in NLU output. Exiting the pipeline.")
        return  
    
    print("\n\n----------------------------------------NLU output----------------------------------------\n")
    print(dict_str_out_NLU)
    print("\n------------------------------------------------------------------------------------------\n")

    if path_output_NLU:
        output_DM = run_bash_script(bash_script_path, DM_prompt_path, path_output_NLU)

        dict_str_out_DM = "empty"
        job_number = search_output(output_DM)
        path_output_DM = None  
        if job_number:
            path_output_DM = os.path.join(os.path.dirname(__file__), f'hmd_example-{job_number}.out')
            print(f"Checking DM component's output... (on job {job_number})")
            dict_str_out_DM = extract_dict_from_file(path_output_DM, interval=5)
        else:
            print("No job number found in DM output. Exiting the pipeline.")
            return  
        
        print("\n\n----------------------------------------DM output----------------------------------------\n")
        print(dict_str_out_DM)    
        print("\n-----------------------------------------------------------------------------------------\n")


        if path_output_DM:
            output_NLG = run_bash_script(bash_script_path, NLG_prompt_path, path_output_DM)
            job_number2 = search_output(output_NLG)
            path_output_NLG = os.path.join(os.path.dirname(__file__), f'hmd_example-{job_number2}.out')
            print(f"Checking NLG component's output... (on job {job_number2})")
            final_question = extract_final_question(path_output_NLG)

            print("\n\n----------------------------------------NLG output----------------------------------------\n")
            print(final_question)
            print("\n-----------------------------------------------------------------------------------------\n")

        else:
            print("No valid DM output to proceed with NLG.")
    else:
        print("No valid NLU output to proceed with DM.")

if __name__ == "__main__":
    main()

