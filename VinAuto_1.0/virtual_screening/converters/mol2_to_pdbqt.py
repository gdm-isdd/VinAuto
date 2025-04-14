import os
import subprocess
import logging

def convert_mol2_to_pdbqt(input_folder: str,
                          output_folder: str,
                          prepare_ligand_cmd: list) -> list:
    """
    Convert all MOL2 files in the specified input folder into PDBQT files using the 
    provided ligand preparation command with obabel.
    
    Args:
        input_folder (str): Directory containing the .mol2 files.
        output_folder (str): Directory where .pdbqt files will be stored.
        prepare_ligand_cmd (list): Command list for ligand preparation. This should
                                   include the interpreter and the full path to prepare_ligand4.py
                                   if necessary.
    
    Returns:
        list: A list of paths to the generated .pdbqt files.
    """
    os.makedirs(output_folder, exist_ok=True)
    pdbqt_files = []

    # Process each MOL2 file in the input folder
    for mol2_file in os.listdir(input_folder):
        if mol2_file.lower().endswith(".mol2"):
            mol2_path = os.path.join(input_folder, mol2_file)
            base_name = os.path.splitext(mol2_file)[0]
            pdbqt_path = os.path.join(output_folder, f"{base_name}.pdbqt")

            # obabel first_molecule.mol2 -opdbqt -O first_molecule.pdbqt --partialcharge gasteiger
            command = prepare_ligand_cmd + [
                mol2_path,
                "-opdbqt",
                "-O", pdbqt_path,
                "--partialcharge gasteiger",
                "--addHs"
            ]
            

            try:
                subprocess.run(command, check=True, capture_output=True)
                logging.info(f"PDBQT generated for {base_name}")
                pdbqt_files.append(pdbqt_path)
            except subprocess.CalledProcessError as e:
                logging.error(f"Error converting {base_name}: {e}")

    return pdbqt_files

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert MOL2 files to PDBQT format.")
    parser.add_argument("--input_folder", default="mol2_files", help="Folder containing MOL2 files.")
    parser.add_argument("--output_folder", default="pdbqt_files", help="Folder to store generated PDBQT files.")
    
    # Instead of a fixed default, you can require the user to provide the full command,
    # or set a reasonable default if known. Here, we assume users might need to supply
    # a full command including the interpreter and path to prepare_ligand4.py.
    parser.add_argument("--prepare_ligand_cmd", default="", 
                        help="Full command to run the ligand preparation script. For example:\n"
                             '"python C:\\Path\\to\\AutoDockTools\\Utilities24\\prepare_ligand4.py"')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    if not args.prepare_ligand_cmd:
        logging.error("You must supply the full command for the ligand preparation script using --prepare_ligand_cmd")
        exit(1)
    
    # Split the command string into a list; if you're on Windows, ensure the path is quoted correctly.
    prepare_ligand_cmd = args.prepare_ligand_cmd.split()

    logging.info("Starting the MOL2 to PDBQT conversion process.")
    converted_files = convert_mol2_to_pdbqt(args.input_folder, args.output_folder, prepare_ligand_cmd)
    logging.info(f"Conversion complete. Generated files: {converted_files}")
