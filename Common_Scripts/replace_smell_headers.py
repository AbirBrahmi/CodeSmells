# replace_smell_headers.py

import pandas as pd

def replace_headers_with_abbreviations(file_path, output_path):
    # Mapping des noms complets des smells vers les nouvelles abréviations
    column_mapping = {
        "Virtual Method Call from Constructor": "I-VMCC", 
        "Complex Conditional": "I-CC", 
        "Complex Method": "I-CM", 
        "Empty Catch Block": "I-ECB", 
        "Long Identifier": "I-LI", 
        "Long Method": "I-LM", 
        "Long Parameter List": "I-LPL", 
        "Long Statement": "I-LS", 
        "Magic Number": "I-MN", 
        "Missing Default": "I-MD", 
        "Duplicate Code": "I-DC",
        "Imperative Abstraction": "D-IA", 
        "Unnecessary Abstraction": "D-UA", 
        "Multifaceted Abstraction": "D-MA", 
        "Unutilized Abstraction": "D-UA2", 
        "Duplicate Abstraction": "D-DA", 
        "Feature Envy": "D-FE", 
        "Deficient Encapsulation": "D-DE", 
        "Unexploited Encapsulation": "D-UE", 
        "Broken Modularization": "D-BM", 
        "Insufficient Modularization": "D-IM", 
        "Hub-like Modularization": "D-HM", 
        "Cyclically-dependent Modularization": "D-CDM", 
        "Wide Hierarchy": "D-WH", 
        "Deep Hierarchy": "D-DH", 
        "Multipath Hierarchy": "D-MH", 
        "Cyclic Hierarchy": "D-CH", 
        "Unfactored Hierarchy": "D-UH", 
        "Rebellious Hierarchy": "D-RH", 
        "Missing Hierarchy": "D-MH2", 
        "Broken Hierarchy": "D-BH"
    }

    # Charger le fichier CSV
    df = pd.read_csv(file_path)

    # Remplacer les noms des colonnes par leurs abréviations
    df = df.rename(columns=column_mapping)

    # Sauvegarder le fichier transformé en tant que CSV
    df.to_csv(output_path, index=False)
    print(f"Fichier sauvegardé à : {output_path}")

# Exécution
if __name__ == "__main__":
    file_path = r'C:\Users\Brahm\Documents\CodeSmells\RQ1\data\density_counts_per_file.csv'
    output_path = r'C:\Users\Brahm\Documents\CodeSmells\RQ1\data\density_counts_per_file_with_abbr.csv'
    replace_headers_with_abbreviations(file_path, output_path)
