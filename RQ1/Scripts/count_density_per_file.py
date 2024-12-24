import pandas as pd

# Chemin d'accès à votre fichier CSV d'entrée
input_file_path = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\RawData\CompleteDataSet.csv'

# Charger les données à partir du fichier CSV
data = pd.read_csv(input_file_path)

# Calculer le nombre de code smells pour chaque projet et chaque type de smell
smell_counts = data.groupby(['Project', 'Smell']).size().unstack(fill_value=0)

# Sauvegarder les résultats dans un fichier CSV
smell_counts.to_csv(r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ1\smell_count_per_project.csv')

# Calculer le nombre de fichiers affectés par chaque type de smell pour chaque projet
file_counts = data.groupby(['Project', 'Smell'])['File'].nunique().unstack(fill_value=0)

# Sauvegarder les résultats dans un fichier CSV
file_counts.to_csv(r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\RawData\project_affected_file_counts.csv')

# Compter le nombre de smells pour chaque fichier et type de smell
smell_counts_per_file = data.groupby(['Project', 'File', 'Smell']).size().reset_index(name='Smell Count')

# Joindre les comptes de smells avec les tailles de fichiers
smell_counts_per_file = smell_counts_per_file.merge(data[['Project', 'File', 'Line Count']], on=['Project', 'File'])

# Calculer la densité pour chaque type de smell
smell_counts_per_file['Density'] = (smell_counts_per_file['Smell Count'] / smell_counts_per_file['Line Count']) * 1000

# Réorganiser pour avoir les types de smells en colonnes
density_pivot = smell_counts_per_file.pivot_table(index=['Project', 'File'], columns='Smell', values='Density', fill_value=0)

# Sauvegarder les résultats dans un fichier CSV
density_pivot.to_csv(r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ1\density_counts_per_file.csv')

print("Les fichiers de résultats ont été générés avec succès.")
