import pandas as pd
import re

# Chemin du fichier d'entrée
file_path = r"C:\Users\Brahm\Documents\CodeSmells\Common_Raw_Data\historique_commits_with_smelly.csv"

# Charger les données
data = pd.read_csv(file_path)

# Liste des mots-clés pour identifier les Defect-Fixing Commits
keywords = ["error", "bug", "fix", "issu", "mistak", "incorrect", "fault",
            "defect", "flaw", "crash", "patch", "fail", "problem"]

# Étape 1 : Ajouter une colonne pour marquer les DFCs
data['Is_DFC'] = data['Commit Message'].str.contains('|'.join(keywords), case=False, na=False).astype(int)

# Étape 2 : Exclure les commits de tests et d'exemples
def has_only_examples_tests_files_changed(file_paths):
    """
    Vérifie si seuls des fichiers de test ou d'exemple ont été modifiés dans le commit.
    """
    for path in file_paths.split(';'):  # Les chemins des fichiers sont séparés par des ';'
        if not re.search(r'test|exampl', path, re.IGNORECASE):
            return False  # Si un fichier n'est pas un test/exemple, on garde le commit
    return True  # Si tous les fichiers sont des tests/exemples, on exclut le commit

# Ajouter une colonne pour indiquer si le DFC est pertinent
data['Relevant_DFC'] = data.apply(
    lambda row: 0 if has_only_examples_tests_files_changed(row['File Path']) else 1, axis=1
)

# Étape 3 : Filtrer uniquement les commits pertinents
relevant_dfcs = data[(data['Is_DFC'] == 1) & (data['Relevant_DFC'] == 1)]

# Sauvegarder les résultats dans un nouveau fichier
output_path = r"C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\filtered_relevant_dfcs.csv"
relevant_dfcs.to_csv(output_path, index=False)

# Étape 4 : Statistiques
num_total_commits = len(data)
num_dfcs = data['Is_DFC'].sum()
num_relevant_dfcs = len(relevant_dfcs)

print(f"Nombre total de commits : {num_total_commits}")
print(f"Nombre de Defect-Fixing Commits (DFCs) identifiés : {num_dfcs}")
print(f"Nombre de DFCs pertinents (non liés aux tests ou exemples) : {num_relevant_dfcs}")
print(f"Les résultats ont été sauvegardés dans : {output_path}")
