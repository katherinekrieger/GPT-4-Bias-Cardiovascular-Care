import csv
import json

MODEL_NAME = "gpt-4"

INPUT_FILE = 'docs/prompts.csv'
OUTPUT_FILE = 'batch-input.jsonl'

TRIALS = 100

def read_input_csv(input_file):
  with open(input_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader, None)
    rows = [row for row in reader]
  return header, rows

def generate_prompts(input_rows):
    prompts = [[] for _ in range(15)]
    for row in input_rows:
        if len(row[0]) == 0: continue
        if row[0] == 'Completed!':
            print('Completed!')
            break

        for col in range(15): prompts[col].append(row[col+1])
    
    return prompts

def write_prompts_csv(output_file, prompts):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Prompts...']
        writer.writerow(header)

        for row in prompts:
            writer.writerow(row)

def generate_json_row(diagnosis_number, prompt_number, trial, prompt):
    id = f'diagnosis{diagnosis_number}-prompt{prompt_number}-trial{trial}'
    return ({
        "custom_id": id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": MODEL_NAME,
            "messages": [{ "role": "user", "content": prompt }]
        },
        "temperature": 0.7
    })

_, rows = read_input_csv('docs/prompts.csv')
prompts = generate_prompts(rows)

with open(OUTPUT_FILE, 'w') as f:
    diagnosis = 0
    for prompt_row in prompts:
        diagnosis += 1
        print(f'Writing for prompt number {diagnosis}')
        prompt_number = 0
        for prompt in prompt_row:
            prompt_number += 1
            for trial in range(1, TRIALS+1):
                request_item = generate_json_row(diagnosis, prompt_number, trial, prompt)
                json.dump(request_item, f)
                f.write('\n')
