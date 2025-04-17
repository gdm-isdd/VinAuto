# OVERVIEW
VinAuto is a software, that using Vina v1.2.5 [1,2], and Obabel [3,4] allows you dock a database of molecules in a fully automatized way, with only one command line, on a protein. You only need a csv containing the SMILES, and the pdb file of the monomer you wish to study. With just one line of command you can launch a fully automatized docking experiment, you will obtain the results in a pdbqt format for inspection, and log files that will show the score for each conformation.  

# REQUIRED PYTHON PACKAGES

**Pandas** >= 1.5.0 reccomended
**setuptools** >= 72.1.0 recommended
**wheel** >= 0.45.1 recommended
**openpyxl** >= 3.0.0 recommended

# REQUIRED EXTERNAL DEPENDECIES

**Vina** (recommended v1.2.5) ( installation guide and files: https://github.com/ccsb-scripps/AutoDock-Vina/releases/tag/v1.2.5 )

**Obabel** (3.1.1 recommended) ( installation guide and files: https://github.com/openbabel/openbabel/releases )


A conda environment containing all the requirements (except Vina and Obabel) is also provided in the folder called "env". You can install it in this way:

```batch
cd env
conda env create -f vinauto_env.yml
conda activate vinauto_env
```

# AUTOMATED DOCKING PIPELINE

- Converts SMILES to MOL2 with 3D conformer generation (obabel).

- Converts MOL2 files to PDBQT format for ligands and receptors (obabel).

- Automatically calculates the docking box by determining the protein’s center, and adding the possibility of a user-defined padding.

- Runs docking experiments using AutoDock Vina (v1.2.5) with customizable parameters (number of poses and exhaustiveness).

- Produces output files for each step (MOL2, PDBQT, docking result logs and docking results PDBQT conformers) for easy inspection and further analysis.

- Provides a single command-line interface to trigger the entire workflow.

# INSTALLATION GUIDE

This software is currently available only for Windows. The majority of the test have been conducted on Windows 11. To install it, first download the "VinAuto_1.0" folder, then activate the "vinauto_env" environment, or the custom environment you decided to use, then go into the main directory:

```batch
cd VinAuto_1.0
```

Execute the python installer:

```batch
python setup.py install
```

You are now ready to use VinAuto


# USER GUIDE

Within the environment you chose for the installation, you will only need the csv file containing the SMILES of the molecule you wish to dock, and a cleaned pdb file for the monomer (no waters, no ions, just the protein). 

## Required input formats:

#### CSV File:

The file should contain 2 column, the first with the molecules' names and the seconds with their SMILES strings. Please clean the SMILES strings before submitting it to VinAuto (e.g. remove salts, and separate ion couples) because VinAuto will just remove everything that occures after a dot occuring in a SMILES string.

Example row:

MoleculeName, C/C=C(/C)\C(=O)OC1CCN2C1C(=CC2)COC(=O)/C(=C/C)/CO

Example csv file:

name,SMILES
first_molecule,CCO
second_molecule,CCN
third_molecule,CCF
fourth_mol,CN(C)CCOC(C1=CC=CC=C1)C1=CC=CC=C1
fifth_mol,C/C=C(/C)\C(=O)OC1CCN2C1C(=CC2)COC(=O)/C(=C/C)/CO

#### Protein PDB File:

The pdb structure should be a monomer, without water molecules, ligands or ions


## Basic execution:

```batch
vinauto --input-csv your_file.csv --receptor-file your_protein.pdb
```
or 

```batch
vinauto -i your_file.csv -r your_protein.pdb
```

This way, vinauto will create a folder in the current directory, called "results", that will contain another folder called "docking_results", there you will find the log files containing the binding energies of the conformers different ligands, along with a pdbqt file, for each ligand, containing the conformations. You can infact open the resulting pdbqt file in a software like Pymol [5], and visualize the poses of each ligand on the protein, by opening the protein in the same session.

In the "results" folder you will also find the intermediate generated files, such as mol2 and pdbqt files.

However, there are many more parameters that can be chosen for the automatized docking:

## More detailed execution

```batch
vinauto -i your_file.csv -r your_protein.pdb -o output_folder -n number_of_poses -e exhaustivness -p padding
```

-o or --output-dir, is a dir, to create the results folder (default is the current dir)

-n or --num-poses, is an integer, that determines the number of poses for each ligand (default is 20)

-e or -exhaustiveness, is an integer, that defines how deeply the conformational space is explored (default is 10)

-p or --padding, is an integer, that defines the additional space you want to add to the docking box, in Angstrong (default is 10)


## Example of real execution:

```batch
vinauto -i your_file.csv -r your_protein.pdb -o output_folder -n 100 -e 8 -p 15
```

# TROUBLESHOOTING AND FAQs
### Problem: Vina is not found

This can happen if you did not install Vina in its defaul installation directory (C:\Program Files (x86)\The Scripps Research Institute\Vina\vina_1.2.5_win.exe). To solve this, you will need to uninstall VinAuto:
```batch
pip uninstall VinAuto
```
And open the file "pipeline.py", and substitute the path to the vina executable with yours, in line 76.
Once this is done, save the file, and install VinAuto as shown in the installation guide.

### Problem: No MOL2 files generated with specific SMILES

Solution: Check SMILES formatting and ensure that OpenBabel is installed and in your PATH.

### Problem: Docking results not showing expected number of poses in PyMOL

Solution: Verify that you are loading the multi-state PDBQT file with the correct settings, such as using multi=1 in PyMOL.

### Problem: Output directory specified but files are not being saved there

Solution: Ensure that you are supplying absolute paths or properly escaped paths for Windows (e.g., using raw strings).

### Problem: Unable to visualize the different conformations in Pymol

Solution: Open the pdbqt file resulting from the docking experiment, on the notepad, and press ctrl+s, then close it and open it in Pymol


# CURRENT LIMITATIONS

The charge assignment is set to the gasteiger method, but can be changed prior to installation, by substituting "gasteiger" in line 49 of pdbqt of converters/pdb_to_pdbqt.py with another obabel-compatible method, and in line 37 of converters/mol2_to_pdbqt.py (the functioning is not guaranteed with the other methods)


# ACKNOWLEDGMENTS

Developed by Gabriele De Marco

# REFERENCES

[1] J. Eberhardt, D. Santos-Martins, A. F. Tillack, and S. Forli. AutoDock Vina 1.2.0: New Docking Methods, Expanded Force Field, and Python Bindings. Journal of Chemical Information and Modeling (2021).

[2] O. Trott, A. J. Olson, AutoDock Vina: improving the speed and accuracy of docking with a new scoring function, efficient optimization and multithreading, Journal of Computational Chemistry 31 (2010) 455-461

[3] O’Boyle, Noel M, et al., Open Babel: An Open Chemical Toolbox, Journal of Cheminformatics, vol. 3, no. 1, 7 Oct. 2011

[4] Yoshikawa, Naruki, and Geoffrey R. Hutchison, Fast, Efficient Fragment-Based Coordinate Generation for Open Babel, Journal of Cheminformatics, vol. 11, no. 1, 1 Aug. (2019)

[5] The PyMOL Molecular Graphics System, Version 3.0 Schrödinger, LLC






