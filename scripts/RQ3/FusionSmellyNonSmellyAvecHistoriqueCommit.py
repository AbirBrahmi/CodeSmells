import pandas as pd

# Chemins des fichiers CSV
historique_commits_file = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\historique_commits_gitpython.csv'
smelly_non_smelly_file = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\sortie_smelly_non_smelly.csv'

# Charger les données des deux fichiers CSV
historique_commits_df = pd.read_csv(historique_commits_file)
smelly_non_smelly_df = pd.read_csv(smelly_non_smelly_file)

# Normaliser les chemins de fichiers en remplaçant les séparateurs et en supprimant les espaces supplémentaires
historique_commits_df['File Path'] = historique_commits_df['File Path'].str.replace('\\', '/').str.strip()
smelly_non_smelly_df['File Path'] = smelly_non_smelly_df['File Path'].str.replace('\\', '/').str.strip()

# Fusionner les deux DataFrames sur 'File Path' avec une jointure complète (outer join)
# On ne remplit pas les valeurs manquantes dans cette étape pour laisser les champs vides
merged_df = pd.merge(smelly_non_smelly_df, historique_commits_df, on='File Path', how='outer')

# Combiner les colonnes 'Project_x' et 'Project_y' en une seule colonne 'Project'
merged_df['Project'] = merged_df['Project_x'].combine_first(merged_df['Project_y'])

# Supprimer les anciennes colonnes 'Project_x' et 'Project_y'
merged_df = merged_df.drop(columns=['Project_x', 'Project_y'])

# Laisser les champs 'Line Count', 'Smelly', 'Lines Added', et 'Lines Deleted' vides si des valeurs sont manquantes

# Exporter le fichier fusionné
output_file = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\merged_commits_smelly_corrected.csv'
merged_df.to_csv(output_file, index=False)

print(f"Fusion des fichiers terminée. Le fichier fusionné est enregistré dans {output_file}")
