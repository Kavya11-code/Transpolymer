from pubchempy import get_compounds

def polymer_name_to_smiles(polymer_name: str):
    compounds = get_compounds(polymer_name, 'name')
    if compounds:
        return compounds[0].canonical_smiles
    return None
