import os
import subprocess
import logging

def convert_pdb_to_pdbqt(pdb_file: str, output_folder: str, obabel_exe: str = "obabel", extra_args: list = None) -> str:
    """
    Convert a monomer protein PDB file to a PDBQT file using OpenBabel.
    
    Args:
        pdb_file (str): Path to the input PDB file.
        output_folder (str): Directory where the generated PDBQT file will be saved.
        obabel_exe (str): Command or path of the OpenBabel executable (default: "obabel").
        extra_args (list): Optional list of additional command-line arguments for obabel.
    
    Returns:
        str: The path to the generated PDBQT file.
    
    Raises:
        subprocess.CalledProcessError: If the conversion command fails.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # generate charged pdb
    base_name_1 = os.path.splitext(os.path.basename(pdb_file))[0]
    base_name_2 = f"{base_name_1}_charged.pdb"
    charged_pdb = os.path.join(str(output_folder),str(base_name_2))

    # obabel 1rex.pdb -O 1rex_charged.pdb -xr -p 7.4

    # generate charged pdb
    pH = 7.4
    comm = [obabel_exe, pdb_file, "-O", charged_pdb, "-xr", "-p", str(pH) ]

    try:
        result_1 = subprocess.run(comm, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f"Conversion successful. Output saved to: {charged_pdb}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {pdb_file} to PDBQT:\n{e.stderr}")
        raise e
    
# Generate the output file name based on the input file's base name.
    base_name = os.path.splitext(os.path.basename(pdb_file))[0]
    pdbqt_file = os.path.join(output_folder, f"{base_name}.pdbqt")
    
    # Build the command: obabel input.pdb -O output.pdbqt [optional extra args]
    # Build the command including flags to reformat and add Gasteiger charges
    # e.g. obabel 1rex_charged.pdb -O 1rex.pdbqt -xr --partialcharge gasteiger
    command = [ obabel_exe, charged_pdb,"-O", pdbqt_file, "-xr", "--partialcharge", "gasteiger"]
    

    if extra_args:
        command.extend(extra_args)

        if extra_args:
            command.extend(extra_args)
        
    logging.info(f"Running OpenBabel command: {' '.join(command)}")
        
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f"Conversion successful. Output saved to: {pdbqt_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {charged_pdb} to PDBQT:\n{e.stderr}")
        raise e
        
    return pdbqt_file


