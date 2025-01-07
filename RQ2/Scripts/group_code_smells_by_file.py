import pandas as pd

# 1.1 Charger le fichier CSV (modifie le chemin vers ton fichier si nécessaire)
data_path = 'C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/RawData/CompleteDataSet.csv'  # Remplace par le bon chemin
df = pd.read_csv(data_path)

# 1.2 Afficher les premières lignes pour vérifier l'importation
print("Aperçu des premières lignes du fichier d'entrée :")
print(df.head())

# 1.3 Grouper les odeurs de code par fichier
grouped_df = df.groupby('File')['Smell'].apply(list).reset_index()

# 1.4 Afficher un aperçu du regroupement
print("\nAperçu des fichiers avec les odeurs de code groupées :")
print(grouped_df.head())

# Optionnel : Sauvegarder les données groupées dans un nouveau fichier CSV pour usage ultérieur
output_path = 'C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ2/grouped_smells_per_file.csv'  # Remplace par le bon chemin si nécessaire
grouped_df.to_csv(output_path, index=False)

print(f"\nLes données groupées ont été sauvegardées sous : {output_path}")
