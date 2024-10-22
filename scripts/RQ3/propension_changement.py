import pandas as pd

# Chemin du fichier fusionné
merged_file = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\merged_commits_smelly_corrected.csv'

# Charger les données fusionnées
merged_df = pd.read_csv(merged_file)

# Remplacer les valeurs NaN dans 'Total Modifications' par 0 pour les fichiers sans modifications
merged_df['Lines Added'] = merged_df['Lines Added'].fillna(0)
merged_df['Lines Deleted'] = merged_df['Lines Deleted'].fillna(0)

# Calculer le nombre total de modifications (lignes ajoutées + lignes supprimées)
merged_df['Total Modifications'] = merged_df['Lines Added'] + merged_df['Lines Deleted']

# Remplacer les valeurs NaN dans la colonne 'Smelly' par 0 (non-smelly par défaut si absent)
merged_df['Smelly'] = merged_df['Smelly'].fillna(0)

# Remplacer les valeurs NaN dans 'Line Count' par 0 pour les fichiers sans information de ligne
merged_df['Line Count'] = merged_df['Line Count'].fillna(0)

# Calculer la propension au changement (somme des modifications) pour les fichiers smelly et non-smelly
propension_changement = merged_df.groupby('Smelly').agg({
    'Total Modifications': 'sum',  # Somme des modifications par groupe
    'File Path': 'count'           # Compte du nombre de fichiers smelly et non-smelly
}).reset_index()

# Renommer les colonnes pour plus de clarté
propension_changement.columns = ['Smelly', 'Total Modifications', 'File Count']

# Calculer la propension moyenne par fichier
propension_changement['Modifications per File'] = propension_changement['Total Modifications'] / propension_changement['File Count']

# Exporter les résultats dans un nouveau fichier CSV
output_file = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\propension_changement_final.csv'
propension_changement.to_csv(output_file, index=False)

print(f"Analyse de la propension au changement terminée. Les résultats sont enregistrés dans {output_file}")
