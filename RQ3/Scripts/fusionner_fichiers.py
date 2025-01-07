import os
import pandas as pd

# Chemin du répertoire contenant les fichiers
repertoire = r"C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\DesigniteResults\AllCombinedsmells"

# Chemin pour enregistrer le fichier de sortie
repertoire_sortie = r"C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3"
fichier_sortie = os.path.join(repertoire_sortie, "combined_file.csv")

# Ouvrir le fichier de sortie en mode écriture
with open(fichier_sortie, 'w', encoding='utf-8', newline='') as f_out:
    premier_fichier = True  # Indicateur pour inclure l'en-tête uniquement pour le premier fichier
    for fichier in os.listdir(repertoire):
        chemin_fichier = os.path.join(repertoire, fichier)
        if os.path.isfile(chemin_fichier) and fichier.endswith('.csv'):
            try:
                # Lecture par blocs (chunks)
                for chunk in pd.read_csv(chemin_fichier, chunksize=10000):
                    if premier_fichier:
                        # Inclure l'en-tête pour le premier fichier
                        chunk.to_csv(f_out, index=False, header=True, mode='a')
                        premier_fichier = False
                    else:
                        # Pas d'en-tête pour les fichiers suivants
                        chunk.to_csv(f_out, index=False, header=False, mode='a')
            except Exception as e:
                print(f"Erreur lors de la lecture de {fichier} : {e}")

print(f"Fichier combiné enregistré avec succès : {fichier_sortie}")
