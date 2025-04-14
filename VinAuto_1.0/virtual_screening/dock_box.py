# virtual_screening/box_calculator.py

def calculate_docking_box(pdbqt_file: str, padding: float) -> dict:
    """
    Calculate the center and dimensions of a docking box that encloses 
    the protein contained in the given PDBQT file, with extra padding (in angstroms).

    The function reads ATOM/HETATM lines, extracts the x, y, z coordinates,
    and then computes:
      - center_x, center_y, center_z: The midpoint of the min and max for each coordinate.
      - size_x, size_y, size_z: The extent (max - min) for each axis plus the extra padding.
    
    Args:
        pdbqt_file (str): Path to the input PDBQT file.
        padding (float): Additional space (in Å) to add to each dimension. 
                         (For example, if the protein spans 30 Å in x,
                          the box size in x will be 30 + padding.)
    
    Returns:
        dict: A dictionary with keys:
              'center_x', 'center_y', 'center_z', 'size_x', 'size_y', 'size_z'
    """
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')

    with open(pdbqt_file, 'r') as f:
        for line in f:
            # Only process lines that contain coordinate data.
            if line.startswith("ATOM") or line.startswith("HETATM"):
                fields = line.split()
                try:
                    # For standard PDBQT files, the coordinates are typically 
                    # in positions 7, 8, and 9 (0-indexed) after splitting.
                    # E.g., for: 
                    # "ATOM      1  C   LIG A   1      14.982   8.851  32.647  0.00  0.00    +0.034 C"
                    # fields becomes:
                    # ['ATOM', '1', 'C', 'LIG', 'A', '1', '14.982', '8.851', '32.647', ...]
                    x = float(fields[6])
                    y = float(fields[7])
                    z = float(fields[8])
                except (IndexError, ValueError):
                    continue  # Skip lines where conversion fails

                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
                if z < min_z:
                    min_z = z
                if z > max_z:
                    max_z = z

    # Ensure that at least one valid coordinate set was found.
    if min_x == float('inf'):
        raise ValueError("No valid ATOM or HETATM lines found in the file.")

    # Compute the center coordinates.
    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    center_z = (min_z + max_z) / 2.0

    # Compute the dimensions: (max - min) + padding.
    size_x = (max_x - min_x) + padding
    size_y = (max_y - min_y) + padding
    size_z = (max_z - min_z) + padding

    return {
        "center_x": center_x,
        "center_y": center_y,
        "center_z": center_z,
        "size_x": size_x,
        "size_y": size_y,
        "size_z": size_z
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate the center and box dimensions for docking, "
                    "given a protein PDBQT file. The box dimensions will "
                    "enclose the entire protein plus extra padding."
    )
    parser.add_argument("--pdbqt", required=True, help="Path to the protein PDBQT file.")
    parser.add_argument("--padding", type=float, default=10.0,
                        help="Extra padding in angstroms to add to each dimension (default 10.0 Å).")
    args = parser.parse_args()

    box = calculate_docking_box(args.pdbqt, args.padding)
    print("Calculated Docking Box:")
    print(f"Center (x, y, z): {box['center_x']:.3f}, {box['center_y']:.3f}, {box['center_z']:.3f}")
    print(f"Dimensions (x, y, z): {box['size_x']:.3f}, {box['size_y']:.3f}, {box['size_z']:.3f}")
