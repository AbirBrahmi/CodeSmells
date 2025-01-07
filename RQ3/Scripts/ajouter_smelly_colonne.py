import pandas as pd
import os
import glob

def ajouter_colonne_smelly_par_commit():
    print("=== Ajout de la colonne 'Smelly' (0 ou 1) avec vérification par commit ===")

    # Répertoires des fichiers
    smells_dir = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\AllCombinedsmells'
    commits_path = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\historique_commits_all_projects.csv'
    output_path = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\historique_commits_with_smelly.csv'

    # Vérifiez que le répertoire et le fichier existent
    if not os.path.exists(smells_dir):
        raise FileNotFoundError(f"Le répertoire {smells_dir} est introuvable.")
    if not os.path.exists(commits_path):
        raise FileNotFoundError(f"Le fichier {commits_path} est introuvable.")

    # Charger tous les fichiers de smells
    print("Chargement des fichiers de smells...")
    all_smelly_records = []
    for filepath in glob.glob(os.path.join(smells_dir, '*.csv')):
        print(f"Traitement du fichier : {os.path.basename(filepath)}")
        smells_df = pd.read_csv(filepath, sep=',', on_bad_lines='skip')  # Séparateur adapté

        # Nettoyer les noms de colonnes
        smells_df.columns = smells_df.columns.str.strip()

        # Vérifiez si 'File' et 'Commit' existent
        if 'File' not in smells_df.columns or 'Commit' not in smells_df.columns:
            raise ValueError(f"Le fichier {filepath} ne contient pas les colonnes 'File' ou 'Commit'. Vérifiez sa structure.")

        # Ajouter les enregistrements smelly (File, Commit) à la liste
        smelly_records = smells_df[['File', 'Commit']].drop_duplicates()
        all_smelly_records.append(smelly_records)

    # Combiner tous les enregistrements smelly en un seul DataFrame
    all_smelly_df = pd.concat(all_smelly_records).drop_duplicates()
    print(f"Nombre total de fichiers smelly avec commits trouvés : {len(all_smelly_df)}")

    # Charger le fichier des commits
    print("Chargement du fichier des commits...")
    commits_df = pd.read_csv(commits_path, sep=',', on_bad_lines='skip')  # Séparateur adapté pour les commits

    # Vérifiez si 'File Path' et 'Commit Hash' existent
    if 'File Path' not in commits_df.columns or 'Commit Hash' not in commits_df.columns:
        raise ValueError("Le fichier des commits ne contient pas les colonnes 'File Path' ou 'Commit Hash'. Vérifiez sa structure.")

    # Ajouter la colonne 'Smelly' en vérifiant (File Path, Commit Hash)
    print("Ajout de la colonne 'Smelly'...")
    smelly_set = set(zip(all_smelly_df['File'], all_smelly_df['Commit']))
    commits_df['Smelly'] = commits_df.apply(
        lambda row: 1 if (row['File Path'], row['Commit Hash']) in smelly_set else 0, axis=1
    )

    # Sauvegarder le fichier avec la nouvelle colonne
    print(f"Sauvegarde du nouveau fichier dans : {output_path}")
    commits_df.to_csv(output_path, index=False, sep=',')

    print("=== Ajout de la colonne 'Smelly' terminé ===")


if __name__ == "__main__":
    try:
        ajouter_colonne_smelly_par_commit()
        print("=== Script terminé avec succès ===")
    except Exception as e:
        print(f"Erreur : {e}")
