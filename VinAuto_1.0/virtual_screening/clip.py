import argparse
from virtual_screening.pipeline import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="Virtual Screening using VINA")
    parser.add_argument("-i", "--input-csv", required=True, help="CSV file containing SMILES")
    parser.add_argument("-r", "--input-receptor", required=True, help = "pdb receptor")
    parser.add_argument("-o", "--output-dir", default="./results", help="Directory for output files")
    parser.add_argument("-n", "--num-poses", default=20, help="Number of docking poses for each ligand (default = 20)")
    parser.add_argument("-e", "--exhaustivness", default=10, help="exhaustivness (default = 10) the higher the better, but increases computational time")
    parser.add_argument("-p", "--padding", default=10, help="The extra space you wish to add to the calculated protein box (default = 10 Angstrom)")

    args = parser.parse_args()
    run_pipeline(args.input_csv, args.input_receptor, args.output_dir, args.num_poses, args.exhaustivness, args.padding)
    
if __name__ == "__main__":
    main()
