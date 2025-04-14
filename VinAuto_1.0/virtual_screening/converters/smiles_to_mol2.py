import os
import re
import subprocess
import logging
import pandas as pd

def clean_smiles(smiles: str) -> str:
    """
    Remove any parts after a '.' in the SMILES string.
    """
    return re.sub(r'\..*$', '', smiles)

def convert_smiles_to_mol2(smiles: str, name: str, output_dir: str, obabel_cmd: str = "obabel") -> str:
    """
    Convert a given SMILES string to a MOL2 file using the OpenBabel command line tool.
    
    Args:
        smiles: The raw SMILES string.
        name: Identifier used to name the output file.
        output_dir: Directory where the MOL2 file will be saved.
        obabel_cmd: Command for OpenBabel, can be modified if needed.
    
    Returns:
        The path to the generated MOL2 file.
    """
    # Clean the SMILES
    cleaned_smiles = clean_smiles(smiles)
    
    # Sanitize the name to avoid invalid characters in file names
    sanitized_name = str(name).strip().replace('/', '_').replace('\\', '_').replace(':', '_')
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the output filename based on the sanitized name and the output directory
    output_filename = os.path.join(output_dir, f"{sanitized_name}.mol2")
    
    # Prepare the obabel command to generate the MOL2 file with 3D coordinates
    command = f'{obabel_cmd} -:"{cleaned_smiles}" --gen3D -O "{output_filename}"'
    
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True)
        logging.info(f"Converted and saved: {output_filename}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting SMILES {smiles} for {name}. Command: {command}\nError: {e}")
        raise e
    
    return output_filename

def convert_from_excel(file_path: str,
                       smiles_column_index: int = 1,
                       name_column_index: int = 0,
                       output_dir: str = 'mol2_files',
                       obabel_cmd: str = "obabel") -> list:
    """
    Read an Excel file, extract the SMILES and names, and convert them to MOL2 files.
    
    Args:
        file_path: Path to the input Excel file.
        smiles_column_index: Zero-based index of the column containing SMILES.
        name_column_index: Zero-based index of the column containing molecule names.
        output_dir: Directory where MOL2 files will be stored.
        obabel_cmd: Command to invoke OpenBabel.
    
    Returns:
        A list of paths to the generated MOL2 files.
    """
    df = pd.read_excel(file_path)
    mol2_files = []
    
    for index, row in df.iterrows():
        # Extract the SMILES string and molecule name
        smiles = str(row[smiles_column_index]).strip()
        name = row[name_column_index]
        
        # Skip rows with missing or invalid data
        if pd.isna(smiles) or pd.isna(name) or not smiles or not name:
            logging.warning(f"Invalid data at row {index}: SMILES='{smiles}', Name='{name}'")
            continue
        
        logging.debug(f"Row {index} - SMILES: {smiles}, Name: {name}")
        
        try:
            output_file = convert_smiles_to_mol2(smiles, name, output_dir, obabel_cmd)
            mol2_files.append(output_file)
        except Exception as e:
            logging.error(f"Failed to convert row {index}: {e}")
    
    return mol2_files

if __name__ == '__main__':
    import argparse

    # Set up command-line argument parsing for testing or standalone runs
    parser = argparse.ArgumentParser(description="Convert SMILES from an Excel file to MOL2 files.")
    parser.add_argument("--file_path", required=True, help="Path to the Excel file containing SMILES strings.")
    parser.add_argument("--smiles_col", type=int, default=5, help="Column index for SMILES strings (0-indexed).")
    parser.add_argument("--name_col", type=int, default=0, help="Column index for molecule names (0-indexed).")
    parser.add_argument("--output_dir", default="mol2_files", help="Directory for saving generated MOL2 files.")
    parser.add_argument("--obabel_cmd", default="obabel", help="Command for invoking OpenBabel.")
    args = parser.parse_args()

    # Set up basic logging configuration
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")
    
    # Run the conversion process
    files_generated = convert_from_excel(args.file_path,
                                         smiles_column_index=args.smiles_col,
                                         name_column_index=args.name_col,
                                         output_dir=args.output_dir,
                                         obabel_cmd=args.obabel_cmd)
    
    logging.info(f"Conversion complete. Generated files: {files_generated}")
