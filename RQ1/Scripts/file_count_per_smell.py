import pandas as pd

# Chemin vers le fichier d'entrée et le fichier de sortie
input_file = r'C:\Users\Brahm\Documents\CodeSmells\Common_Raw_Data\CompleteDataSet.csv'
output_file = r'C:\Users\Brahm\Documents\CodeSmells\RQ1\data\file_count_per_smell.csv'

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

# Initialiser un DataFrame pour stocker les résultats
result_df = pd.DataFrame(columns=['Project'] + smells_list)

# Grouper par projet et code smell, puis compter les fichiers affectés
grouped = df.groupby(['Project', 'Smell'])

# Dictionnaire pour stocker les comptes des fichiers affectés par projet et smell
project_smell_file_counts = {}

for (project, smell), group in grouped:
    file_count = group['File'].nunique()  # Compter les fichiers uniques affectés
    if project not in project_smell_file_counts:
        project_smell_file_counts[project] = {smell: file_count}
    else:
        project_smell_file_counts[project][smell] = file_count

# Créer les lignes du DataFrame à partir des données
for project, smell_data in project_smell_file_counts.items():
    row = {'Project': project}
    for smell in smells_list:
        row[smell] = smell_data.get(smell, 0)  # Mettre 0 si aucun fichier de ce type n'a été trouvé
    result_df = pd.concat([result_df, pd.DataFrame([row])], ignore_index=True)

# Réorganiser les données pour avoir les smells dans les lignes et les projets dans les colonnes
pivot_result = result_df.set_index('Project').T
pivot_result.index.name = 'Smell'  # Renommer l'index pour clarifier qu'il correspond aux smells

# Sauvegarder les résultats dans un fichier CSV
pivot_result.to_csv(output_file, index=True)

print(f"Les résultats ont été exportés dans le fichier (smells en lignes, projets en colonnes) : {output_file}")
