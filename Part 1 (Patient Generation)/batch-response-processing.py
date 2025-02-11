import json
import csv
import os

BATCH_FOLDER = 'batch-csvs'

def process_jsonl_to_csv(jsonl_file):
    # Dictionary to hold file handlers for each diagnosis
    diagnosis_files = {}
    
    # Open the .jsonl file and process line by line
    with open(jsonl_file, 'r') as f:
        count = 0
        for line in f:
            count += 1
            print(f'Processing line {count}...')
            # Parse the JSON object
            data = json.loads(line)
            
            # Extract the necessary parts from the custom_id
            custom_id = data.get('custom_id', '')
            parts = custom_id.split('-')
            diagnosis_number = parts[0].replace('diagnosis', '')  # Extract the number part
            prompt_number = parts[1].replace('prompt', '')  # Extract prompt number
            trial_number = parts[2].replace('trial', '')  # Extract trial number
            
            # Extract the response message
            try:
                message_content = data['response']['body']['choices'][0]['message']['content']
            except KeyError:
                message_content = '[FILTERED OUT]'  # Default message if 'content' key is missing
            
            # Prepare the row for the CSV
            row = [
                diagnosis_number,  # Diagnosis number
                prompt_number,     # Prompt number
                trial_number,      # Trial number
                custom_id,         # The full custom_id
                message_content.replace('"', '""').replace('\n', ' ').replace(',', ' ')  # Escaping quotes, new lines and commas for CSV
            ]
            
            # If a file for this diagnosis doesn't exist yet, create it
            if diagnosis_number not in diagnosis_files:
                # Create CSV file with headers
                filename = f'{BATCH_FOLDER}/diagnosis{diagnosis_number}.csv'
                diagnosis_files[diagnosis_number] = open(filename, 'w', newline='', encoding='utf-8')
                writer = csv.writer(diagnosis_files[diagnosis_number])
                writer.writerow(['Diagnosis Number', 'Prompt Number', 'Trial Number', 'Custom ID', 'Response Message'])
            
            # Write the row to the corresponding CSV file
            writer = csv.writer(diagnosis_files[diagnosis_number])
            writer.writerow(row)
    
    # Close all the CSV files
    for f in diagnosis_files.values():
        f.close()

# Usage example
jsonl_file = 'batch-jsons/batch-output.jsonl'  # Replace with the path to your .jsonl file
process_jsonl_to_csv(jsonl_file)
