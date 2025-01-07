import pandas as pd

# Chemin d'accès à votre fichier CSV d'entrée
input_file_path = r'C:\Users\Brahm\Documents\CodeSmells\Common_Raw_Data\CompleteDataSet.csv'

# Charger les données à partir du fichier CSV
data = pd.read_csv(input_file_path)

# Calculer le nombre de code smells pour chaque fichier et chaque type de smell
smell_counts = data.groupby(['Project', 'File', 'Smell']).size().unstack(fill_value=0).reset_index()

# Sauvegarder le nombre de code smells par fichier dans un fichier CSV
smell_counts_file_path = r'C:\Users\Brahm\Documents\CodeSmells\RQ1\data\smell_count_per_file.csv'
smell_counts.to_csv(smell_counts_file_path, index=False)

# Joindre les tailles des fichiers pour calculer les densités
smell_counts = smell_counts.merge(data[['Project', 'File', 'Line Count']].drop_duplicates(), on=['Project', 'File'])

# Calculer la densité pour chaque type de smell
for column in smell_counts.columns[2:-1]:  # Exclure les colonnes 'Project', 'File', et 'Line Count'
    smell_counts[column] = (smell_counts[column] / smell_counts['Line Count']) * 1000

# Réorganiser pour avoir les types de smells en colonnes (densité)
density_pivot = smell_counts.drop(columns=['Line Count'])

# Sauvegarder la densité des code smells par fichier dans un fichier CSV
density_file_path = r'C:\Users\Brahm\Documents\CodeSmells\RQ1\data\density_counts_per_file.csv'
density_pivot.to_csv(density_file_path, index=False)

print("Les fichiers 'smell_count_per_file.csv' et 'density_counts_per_file.csv' ont été générés avec succès.")
