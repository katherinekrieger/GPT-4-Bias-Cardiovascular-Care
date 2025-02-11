import pandas as pd

ETH_OPTIONS = ['white', 'black', 'asian', 'hispanic']
GEN_OPTIONS = ['man', 'woman']

def split_demographic(demographic_string):
    ethnicity, gender = demographic_string.lower().split(' ')

    if ethnicity not in ETH_OPTIONS:
        print(f'Unexpected ethnicity option: {ethnicity}')
        raise NameError
    if gender not in GEN_OPTIONS:
        print(f'Unexpected gender option: {gender}')
        raise NameError

    return ethnicity, gender

def convert_matrix_to_long_form(input_file, output_file):
    """
    Convert a 2D matrix CSV to a long-form CSV with Type, Demographic, and Data columns.
    
    Parameters:
    input_file (str): Path to the input CSV file
    output_file (str): Path to save the output CSV file
    """
    # Read the CSV file
    df = pd.read_csv(input_file, index_col=0)
    
    # Create an empty list to store the long-form data
    long_form_data = []
    
    # Iterate through each row
    for type_label, row in df.iterrows():
        # Iterate through each column (demographic)
        for demographic, prompt in row.items():
            ethnicity, gender = split_demographic(demographic)
            # Append each cell as a new row in the long-form list
            long_form_data.append({
                'Diagnosis': f'diagnosis{type_label}',
                'Gender': gender,
                'Ethnicity': ethnicity,
                'Prompt': prompt
            })
    
    # Convert the list to a DataFrame
    long_form_df = pd.DataFrame(long_form_data)
    
    # Save to CSV
    long_form_df.to_csv(output_file, index=False)
    
    print(f"Conversion complete. Output saved to {output_file}")

convert_matrix_to_long_form('matrix-prompts.csv', 'row-prompts.csv')