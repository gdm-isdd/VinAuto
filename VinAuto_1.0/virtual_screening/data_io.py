import os
import pandas as pd
import csv
import logging

def load_smiles(csv_file: str, delimiter: str = ',', header: int = 0) -> pd.DataFrame:
    """
    Load a CSV file containing molecule names and SMILES strings and return a DataFrame.
    
    Assumes:
      - The first column has molecule names.
      - The second column has SMILES strings.
    
    Args:
        csv_file (str): Path to the CSV file.
        delimiter (str): Delimiter used in the CSV file (default is comma).
        header (int): Row number to use as the column names (default 0, meaning first row).
        
    Returns:
        pd.DataFrame: A DataFrame with two columns: 'name' and 'smiles'.
    """
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file, delimiter=delimiter, header=header)
    
    # Use only the first two columns, and rename them for clarity
    df = df.iloc[:, :2]
    df.columns = ['name', 'smiles']
    print(df)
    return df

# docking_results is a list

def save_results(docking_results, output_folder):
    """
    Save docking results into a CSV file within the specified output folder.
    
    Args:
        docking_results (list): A list of dictionaries summarizing docking results.
                                Each dictionary should include keys such as 'ligand'
                                and 'binding_energy'.
        output_folder (str): Directory where the results file will be saved.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    
    # Define the output CSV file name
    output_file = os.path.join(output_folder, "docking_results.csv")
    
    try:
        with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
            # If the results list is non-empty, use its keys as header. Otherwise, use default headers.
            if docking_results:
                fieldnames = list(docking_results[0].keys())
            else:
                fieldnames = ["ligand", "binding_energy"]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in docking_results:
                writer.writerow(result)
        
        logging.info("Docking results successfully saved to: %s", output_file)
    except Exception as e:
        logging.error("Error saving docking results: %s", e)
