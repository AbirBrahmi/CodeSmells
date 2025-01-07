import os
import pandas as pd

# Chemins des répertoires source et destination
source_dir = r"C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\DesigniteResults\SimplCommerce\Analyse"
destination_file = r"C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\DesigniteResults\SimplCommerce\Combined_Smells.csv"

# Liste pour stocker les DataFrames
df_list = []

# Liste des fichiers d'entrée
input_files = []

# Parcourir tous les fichiers dans le répertoire source
for filename in os.listdir(source_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(source_dir, filename)
        input_files.append(file_path)
        # Lire le fichier CSV et exclure les colonnes 'Cause', 'Method', 'Description'
        df = pd.read_csv(file_path)
        df = df.drop(columns=["Cause", "Method", "Description"], errors="ignore")
        df_list.append(df)

# Vérifier si des fichiers ont été ajoutés
if not df_list:
    print("Aucun fichier .csv trouvé dans le répertoire source.")
else:
    # Fusionner tous les DataFrames dans un seul DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)

    # Sauvegarder le DataFrame fusionné dans un fichier CSV
    combined_df.to_csv(destination_file, index=False)

    # Afficher les fichiers d'entrée traités
    print("Fichiers d'entrée traités :")
    for file in input_files:
        print(file)

    print(f"\nFichier fusionné enregistré sous : {destination_file}")
