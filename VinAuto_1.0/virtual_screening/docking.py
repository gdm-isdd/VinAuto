import os
import subprocess
import logging

def run_docking(
    receptor: str,
    center_x: float,
    center_y: float,
    center_z: float,
    size_x: float,
    size_y: float,
    size_z: float,
    num_modes: int,
    exhaustiveness: int,
    spacing: float,
    ligand_folder: str,
    out_folder: str,
    log_file: str,
    vina_exe: str
) -> list:
    """
    Perform docking using Vina on all ligand files in a specified folder.

    Args:
        receptor: Path to the receptor file in PDBQT format.
        center_x, center_y, center_z: Coordinates of the grid center.
        size_x, size_y, size_z: Dimensions of the docking grid.
        num_modes: Maximum number of docking modes to generate.
        exhaustiveness: Search exhaustiveness parameter.
        spacing: Grid spacing.
        ligand_folder: Folder containing ligand files in PDBQT format.
        out_folder: Folder where docking results will be stored.
        log_file: Path to the global log file for summarizing binding energies.
        vina_exe: Path to the Vina executable.

    Returns:
        A list of dictionaries summarizing results (each with 'ligand' and 'binding_energy').
    """
    # Create the output directory if necessary
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    docking_results = []

    # Open the global log file to record summary results
    with open(log_file, "w", encoding="utf-8") as summary_log:
        summary_log.write("Ligand\tBinding Energy (kcal/mol)\n")

        # Process each ligand file in the folder
        for ligand_file in os.listdir(ligand_folder):
            if ligand_file.lower().endswith(".pdbqt"):
                ligand_path = os.path.join(ligand_folder, ligand_file)
                base_name = os.path.splitext(ligand_file)[0]
                output_file = os.path.join(out_folder, f"docking_{base_name}.pdbqt")
                vina_log_file = os.path.join(out_folder, f"docking_{base_name}.log")

                # Build the Vina command
                vina_command = [
                    vina_exe,
                    "--receptor", receptor,
                    "--ligand", ligand_path,
                    "--out", output_file,
                    "--center_x", str(center_x),
                    "--center_y", str(center_y),
                    "--center_z", str(center_z),
                    "--size_x", str(size_x),
                    "--size_y", str(size_y),
                    "--size_z", str(size_z),
                    "--num_modes", str(num_modes),
                    "--exhaustiveness", str(exhaustiveness),
                    "--spacing", str(spacing)
                ]

                logging.info(f"Running command: {' '.join(vina_command)}")

                try:
                    result = subprocess.run(
                        vina_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        check=False
                    )
                    if result.returncode != 0:
                        logging.error(f"Vina failed for ligand {ligand_file} with error: {result.stderr}")
                        continue

                    # Write the detailed Vina log for this ligand
                    with open(vina_log_file, "w", encoding="utf-8") as f_log:
                        f_log.write(result.stdout)

                    logging.info(f"Docking completed for ligand {ligand_file}")
                except Exception as e:
                    logging.error(f"Exception while running Vina for {ligand_file}: {e}")
                    continue

                # Extract binding energy from the Vina log
                binding_energy = None
                if os.path.exists(vina_log_file) and os.path.getsize(vina_log_file) > 0:
                    try:
                        with open(vina_log_file, "r", encoding="utf-8") as f_log:
                            for line in f_log:
                                if line.startswith("REMARK VINA RESULT:"):
                                    parts = line.split()
                                    if len(parts) >= 4:
                                        binding_energy = parts[3]
                                    break
                    except Exception as e:
                        logging.error(f"Error reading {vina_log_file}: {e}")
                else:
                    logging.warning(f"Log file {vina_log_file} is empty or missing.")

                if binding_energy is not None:
                    summary_log.write(f"{ligand_file}\t{binding_energy}\n")
                    docking_results.append({"ligand": ligand_file, "binding_energy": binding_energy})
    logging.info(f"Docking completed. Results saved in: {out_folder}")
    return docking_results

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run docking with Vina on a set of ligand files.")
    parser.add_argument("--receptor", required=True, help="Path to receptor file in PDBQT format.")
    parser.add_argument("--center_x", type=float, required=True, help="X coordinate of grid center.")
    parser.add_argument("--center_y", type=float, required=True, help="Y coordinate of grid center.")
    parser.add_argument("--center_z", type=float, required=True, help="Z coordinate of grid center.")
    parser.add_argument("--size_x", type=float, required=True, help="Grid size along the X-axis.")
    parser.add_argument("--size_y", type=float, required=True, help="Grid size along the Y-axis.")
    parser.add_argument("--size_z", type=float, required=True, help="Grid size along the Z-axis.")
    parser.add_argument("--num_modes", type=int, required=True, help="Maximum number of docking modes.")
    parser.add_argument("--exhaustiveness", type=int, required=True, help="Search exhaustiveness.")
    parser.add_argument("--spacing", type=float, default=0.375, help="Grid spacing (default: 0.375).")
    parser.add_argument("--ligand_folder", required=True, help="Folder containing ligand files in PDBQT format.")
    parser.add_argument("--out_folder", required=True, help="Folder to store docking results.")
    parser.add_argument("--log_file", required=True, help="Path to global log file for summary results.")
    parser.add_argument("--vina_exe", required=True, help="Path to the Vina executable.")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    run_docking(
        receptor=args.receptor,
        center_x=args.center_x,
        center_y=args.center_y,
        center_z=args.center_z,
        size_x=args.size_x,
        size_y=args.size_y,
        size_z=args.size_z,
        num_modes=args.num_modes,
        exhaustiveness=args.exhaustiveness,
        spacing=args.spacing,
        ligand_folder=args.ligand_folder,
        out_folder=args.out_folder,
        log_file=args.log_file,
        vina_exe=args.vina_exe
    )
