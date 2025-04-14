import re

def normalize_pdbqt_format(input_file: str, output_file: str = None) -> str:
    """
    Read a Unix-formatted PDBQT file and rewrite it with Windows CRLF newlines,
    remove non-printable characters, and trim extra leading spaces on critical lines.
    (this is necessary, otherwise you would need to opend the pdbqt files of the docking results
    with the notepad and save the file with ctrl-s, in order to visualize the different conformations
    on software like pymol, probably because of openbabel's formatting)
    
    Args:
        input_file (str): Path to the original PDBQT file.
        output_file (str): If provided, path to save the normalized file.
                           Otherwise, overwrites the input file.
    
    Returns:
        str: The path to the normalized file.
    """
    if output_file is None:
        output_file = input_file

    # Read the file as binary and decode (this helps remove any problematic BOMs or hidden bytes)
    with open(input_file, 'rb') as f:
        content = f.read()

    # Decode using UTF-8, ignoring any errors
    text = content.decode('utf-8', errors='ignore')

    # Remove non-printable characters except for newline (\n) and carriage-return (\r)
    # This regex keeps characters in the range space (0x20) to tilde (0x7E), plus \r and \n.
    text = re.sub(r'[^\x20-\x7E\r\n]', '', text)

    # Process each line:
    cleaned_lines = []
    for line in text.splitlines():
        # Remove extra leading whitespace for lines starting with "MODEL" or "ENDMDL"
        if line.lstrip().startswith("MODEL") or line.lstrip().startswith("ENDMDL"):
            line = line.lstrip()
        # Remove trailing whitespace as well
        cleaned_lines.append(line.rstrip())

    # Join lines with Windows-style CRLF newlines
    new_text = "\r\n".join(cleaned_lines) + "\r\n"

    # Write back with Windows newlines
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        f.write(new_text)

    return output_file

# Example:
# normalized_file = normalize_pdbqt_format("path/to/docking_results.pdbqt")


