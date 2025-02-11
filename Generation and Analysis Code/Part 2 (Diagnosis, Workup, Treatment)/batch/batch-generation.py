import csv
import json
import re

MODEL_NAME = "gpt-4"

INPUT_FILE = '../prompts/row-prompts.csv'
OUTPUT_FILE = 'part2-batch-input.jsonl'

TRIALS = 25

def read_input_csv(input_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Optionally, skip the header if there is one
        header = next(reader, None)
        rows = [row for row in reader]
    return header, rows

ETH_OPTIONS = ['white', 'black', 'asian', 'hispanic']
GEN_OPTIONS = ['man', 'woman']

def parse_prompt_row(prompt_row):
    diagnosis, gender, ethnicity, prompt = prompt_row
    
    match = re.match(r"^diagnosis(\d+)$", diagnosis)
    if match:
        diagnosis_number = int(match.group(1))
    else:
        print(f'Unexpected diagnosis value: {diagnosis}')
        raise ValueError

    if ethnicity not in ETH_OPTIONS:
        print(f'Unexpected ethnicity option: {ethnicity}')
        raise ValueError
    if gender not in GEN_OPTIONS:
        print(f'Unexpected gender option: {gender}')
        raise ValueError
    if not len(prompt) > 0:
        print('Missing prompt')
        raise ValueError

    return diagnosis_number, gender, ethnicity, prompt

def generate_json_row(diagnosis, gender, ethnicity, prompt, trial):
    id = f'diagnosis:{diagnosis}-gender:{gender}-ethnicity:{ethnicity}-trial:{trial}'
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

_, prompts = read_input_csv(INPUT_FILE)

with open(OUTPUT_FILE, 'w') as f:
    for prompt_row in prompts:
        diagnosis, gender, ethnicity, prompt = parse_prompt_row(prompt_row)
        print(f'Writing for diagnosis: {diagnosis}, gender: {gender}, ethnicity: {ethnicity}')
        for trial in range(1, TRIALS+1):
            request_item = generate_json_row(diagnosis, gender, ethnicity, prompt, trial)
            json.dump(request_item, f)
            f.write('\n')
