import csv

UNSORTED_FOLDER = 'batch-csvs'
SORTED_FOLDER = 'sorted-batch-csvs'

def sort_csv(input_file, output_file):
    # Read the rows from the input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # Read the header row
        rows = list(reader)  # Read all the remaining rows
        
    # Sort the rows first by 'Prompt Number' and then by 'Trial Number'
    rows.sort(key=lambda row: (int(row[1]), int(row[2])))  # Sorting by columns: Prompt Number (index 1), Trial Number (index 2)
    
    # Write the sorted rows to the output CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)  # Write the header first
        writer.writerows(rows)    # Write the sorted rows

for i in range(1, 11):
    input_file = f'{UNSORTED_FOLDER}/diagnosis{i}.csv'
    output_file = f'{SORTED_FOLDER}/diagnosis{i}_sorted.csv'
    sort_csv(input_file, output_file)

