# virtual_screening/pipeline.py

import logging
import argparse
import os

# Import the various modules of our package
from virtual_screening import data_io, docking, utils, dock_box
from virtual_screening.converters import smiles_to_mol2, pdb_to_pdbqt, mol2_to_pdbqt, clean_pdbqt, normalize_format

def run_pipeline(input_csv, receptor_file, output_dir, num_poses, exhaust, padding):
    # Set up logging for the whole pipeline
    utils.setup_logging()
    logging.info("Starting virtual screening pipeline.")

    # Step 1: Load SMILES data from the CSV file
    # smiles_data is a pandas dataframe
    logging.info("Loading SMILES data from CSV.")
    smiles_data = data_io.load_smiles(input_csv)

    # Step 2: Convert SMILES to mol2 format files
    logging.info("Converting SMILES to mol2 files.")

    # Loop over the rows (or use any DataFrame operations) (smiles data is a pd dataframe)
    # the dir of the mol2 files is created in the current dir
    mol2_dir = os.path.join(str(output_dir), "mol2_files")
    for index, row in smiles_data.iterrows():
        print(f"Molecule: {row['name']}, SMILES: {row['smiles']}")
        smile = row['smiles']
        name = row['name']
        cleaned_smile = smiles_to_mol2.clean_smiles(smile)
        mol2file = smiles_to_mol2.convert_smiles_to_mol2(cleaned_smile, name, mol2_dir,  "obabel")


    # Step 3: Convert the mol2 files to pdbqt format (for docking)
    logging.info("Converting mol2 files to pdbqt format.")
    cmdline = ["obabel", "-imol2", "-opdbqt"]
    ligands_pdbqt = os.path.join(str(output_dir), "ligands_pdbqt")
    pdbqt_files = mol2_to_pdbqt.convert_mol2_to_pdbqt(mol2_dir, ligands_pdbqt, cmdline)

    # Step 3bis: convert the pdbqt files into Vina-compatible files
    for file in pdbqt_files:
        clean_pdbqt.rename_ligand_residue(file)

    #Step 4: Convert the pdb file into a pdbqt file
    logging.info("converting pdb protein to pdbqt")
    out_rec = os.path.join(str(output_dir), "protein_conversion")
    receptor_pdbqt = pdb_to_pdbqt.convert_pdb_to_pdbqt(receptor_file, out_rec, "obabel", None)

    # Step 5: Run docking for each pdbqt file using VINA
    from virtual_screening import docking

    log = os.path.join(str(output_dir), "docking_global_log.log")
    o_fold = os.path.join(str(output_dir), "docking_results")

    # 10 is the padding (extra box space in angrstong)
    box = dock_box.calculate_docking_box(receptor_pdbqt, padding)
    print("Calculated Docking Box:")
    print(f"Center (x, y, z): {box['center_x']:.3f}, {box['center_y']:.3f}, {box['center_z']:.3f}")
    print(f"Dimensions (x, y, z): {box['size_x']:.3f}, {box['size_y']:.3f}, {box['size_z']:.3f}")
    
    docking_results = docking.run_docking(
        receptor=receptor_pdbqt,
        center_x=box['center_x'],
        center_y=box['center_y'],
        center_z=box['center_z'],
        size_x=box['size_x'],
        size_y=box['size_y'],
        size_z=box['size_z'],
        num_modes=num_poses,
        exhaustiveness=exhaust,
        spacing=0.375,
        ligand_folder = ligands_pdbqt,
        out_folder = o_fold,
        log_file = log,
        vina_exe=r"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina_1.2.5_win.exe"
    )

    #data_io.save_results(docking_results, output_dir)
    logging.info("Pipeline finished successfully.")

    # Step 6: Convert pdbqt results to a more Windows-friendly format
    for file_name in os.listdir(o_fold):
        file_path = os.path.join(o_fold, file_name)
        # Optionally, check the file extension (e.g., only normalize .pdbqt files)
        if file_name.lower().endswith(".pdbqt"):
            normalize_format.normalize_pdbqt_format(file_path)
            print(f"Normalized: {file_path}")
            

if __name__ == "__main__":
    # Provide a command-line interface to the pipeline
    parser = argparse.ArgumentParser(description="Virtual Screening Pipeline using VINA")
    parser.add_argument("--input_csv", required=True,
                        help="Path to the CSV file containing SMILES strings.")
    parser.add_argument("--receptor_path", required=True,
                        help = "Path to the prepared pdbqt file of the receptor")
    parser.add_argument("--output_dir", default="results",
                        help="Output directory for intermediate and final results.")

    args = parser.parse_args()

    run_pipeline(args.input_csv, args.receptor_path, args.output_dir)

