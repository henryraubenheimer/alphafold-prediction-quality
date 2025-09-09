from Bio.PDB import PDBParser
import pandas as pd


# Test function to parse a PDB file and extract residue data
def parse_pdb(file_path: str) -> pd.Series:
    # Parse the PDB file
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('protein', file_path)

    residue_data = []
    for model in structure:
        for chain in model:
            for residue in chain:
                # Skip heteroatoms (water, ligands, etc.)
                if residue.get_id()[0] == ' ':
                    # Get CA atom (alpha carbon) for pLDDT score
                    if 'CA' in residue:
                        ca_atom = residue['CA']
                        residue_data.append(ca_atom.get_bfactor())
    return pd.Series(residue_data)


# Find the longest low confidence segment
def find_low_confidence_segments(residue_data: pd.Series, threshold=50) -> list:

    # Sort by residue number to ensure proper sequence order
    sorted = residue_data.sort_values().reset_index(drop=True)
    # Create boolean mask for low confidence residues
    is_low_confidence = sorted < threshold
    
    # Find all contiguous segments
    segments = []
    current_segment = []
    
    for idx, _ in enumerate(sorted):

        is_low = is_low_confidence.iloc[idx]
        idx += 1
        
        if is_low:
            # Check if this residue continues the current segment
            if (not current_segment or idx == current_segment[-1] + 1):
                current_segment.append(idx)

            else:
                # Gap found, save current segment and start new one
                if current_segment:
                    segments.append(current_segment)
                current_segment = [idx]

        else:
            # High confidence residue, end current segment
            if current_segment:
                segments.append(current_segment)
                current_segment = []
    
    # Don't forget the last segment
    if current_segment:
        segments.append(current_segment)

    return segments