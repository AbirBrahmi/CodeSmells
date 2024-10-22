import pandas as pd

# Chemin vers le fichier d'entrée et le fichier de sortie
input_file = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\RawData\CompleteDataSet.csv'
output_file = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ1\smell_count_per_file.csv'

# Liste des types de code smells
smells_list = [
    'Unutilized Abstraction', 'Unnecessary Abstraction', 'Duplicate Abstraction', 'Feature Envy', 
    'Deficient Encapsulation', 'Wide Hierarchy', 'Broken Hierarchy', 'Rebellious Hierarchy', 
    'Unfactored Hierarchy', 'Long Method', 'Complex Method', 'Long Parameter List', 
    'Long Statement', 'Empty Catch Block', 'Magic Number', 'Missing Default', 
    'Complex Conditional', 'Broken Modularization', 'Insufficient Modularization', 
    'Cyclically-dependent Modularization', 'Cyclic Hierarchy', 'Multipath Hierarchy', 
    'Long Identifier', 'Virtual Method Call from Constructor', 'Hub-like Modularization', 
    'Imperative Abstraction', 'Duplicate Code', 'Multifaceted Abstraction', 
    'Unexploited Encapsulation', 'Missing Hierarchy'
]

# Lire le fichier CSV en DataFrame
try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Le fichier {input_file} n'a pas été trouvé. Vérifiez le chemin et le nom du fichier.")
    exit(1)

# Créer un DataFrame vide pour stocker les résultats
columns = ['Project', 'URL', 'Namespace', 'File', 'Line Count'] + smells_list
result_df = pd.DataFrame(columns=columns)

# Grouper par projet et fichier pour compter les smells
grouped = df.groupby(['Project', 'File'])

# Liste pour stocker les nouvelles lignes
rows = []

# Compter les occurrences des smells par fichier
for (project, file), group in grouped:
    smell_counts = {smell: 0 for smell in smells_list}
    
    # Récupérer les informations supplémentaires (une seule ligne suffit, elles sont les mêmes pour chaque groupe)
    url = group['URL'].iloc[0]
    namespace = group['Namespace'].iloc[0]
    line_count = group['Line Count'].iloc[0]
    
    # Parcourir chaque ligne pour compter les occurrences des smells
    for smell in group['Smell']:
        if smell in smell_counts:
            smell_counts[smell] += 1
    
    # Créer une nouvelle ligne avec les données du projet, fichier et les comptes de smells
    new_row = {
        'Project': project, 
        'URL': url, 
        'Namespace': namespace, 
        'File': file, 
        'Line Count': line_count
    }
    new_row.update(smell_counts)
    rows.append(new_row)

# Convertir la liste en DataFrame
result_df = pd.concat([result_df, pd.DataFrame(rows)], ignore_index=True)

# Sauvegarder le résultat dans un fichier CSV
result_df.to_csv(output_file, index=False)

print(f"Les résultats ont été exportés dans le fichier : {output_file}")
