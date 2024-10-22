import pandas as pd

# Charger les fichiers CSV
all_files = pd.read_csv(r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\RawData\csharp_files_info.csv')  # Remplacez par le nom réel du fichier
smelly_files = pd.read_csv(r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\RawData\CompleteDataSet.csv')  # Remplacez par le nom réel du fichier

# Assurez-vous que les colonnes à comparer sont les mêmes (par exemple, "File Path" dans les deux fichiers)
# Si nécessaire, ajustez les noms de colonnes pour les rendre compatibles
all_files['Smelly'] = all_files['File Path'].apply(lambda x: 1 if x in smelly_files['File Path'].values else 0)

# Sauvegarder les résultats dans un nouveau fichier CSV
output_file = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\RawData\sortie_smelly_non_smelly.csv'
all_files.to_csv(output_file, index=False)

print(f"Fichier généré avec les fichiers smelly et non-smelly : {output_file}")
