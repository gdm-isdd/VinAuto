def rename_ligand_residue(input_file: str, output_file: str = None, old_res: str = "UNL", new_res: str = "LIG") -> str:
    """
    Rename the residue in a PDBQT file from old_res to new_res. 
    (this is necessary because openbabel uses a naming incompatible with Vina)
    
    Args:
        input_file (str): Path to the original PDBQT file.
        output_file (str): Path to save the modified PDBQT file.
                           If not provided, the original file is overwritten.
        old_res (str): The residue name to replace (default "UNL").
        new_res (str): The new residue name (default "LIG").
    
    Returns:
        str: The path to the modified PDBQT file.
    """
    if output_file is None:
        output_file = input_file  # Overwrite in-place if no output file is provided

    new_lines = []
    with open(input_file, "r") as infile:
        for line in infile:
            # Process ATOM and HETATM lines
            if line.startswith("ATOM") or line.startswith("HETATM"):
                # In PDBQT format, the residue name is typically in columns 18-20 (1-indexed)
                # Python string slicing (0-indexed): line[17:20]
                residue = line[17:20]
                if residue.strip() == old_res:
                    # Replace with new_res, formatted to 3 characters wide, right-aligned
                    new_line = line[:17] + f"{new_res:>3}" + line[20:]
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

    with open(output_file, "w") as outfile:
        outfile.writelines(new_lines)

    return output_file

# Example:
# Suppose your generated file is "ligand.pdbqt". To rename the residue:
# rename_ligand_residue("ligand.pdbqt")
