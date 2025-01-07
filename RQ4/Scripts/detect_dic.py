import pandas as pd
import os
import subprocess
import shutil
import tempfile

# Chemin des fichiers d'entrée et de sortie
dfcs_file = r"C:\Users\AT09490\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ4\filtered_dfcs.csv"
output_file = r"C:\Users\AT09490\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ4\dic_results.csv"

# Charger le fichier DFCs
df = pd.read_csv(dfcs_file)

# Liste pour stocker les résultats des DICs
dic_list = []

# Vérification des colonnes nécessaires
df.columns = df.columns.str.strip()
required_columns = ['Depot local', 'Date', 'File Path', 'Commit Hash']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Colonne requise absente : {col}")

# Fonction pour exécuter une commande système
def run_command(command, cwd=None):
    try:
        result = subprocess.check_output(command, shell=True, text=True, cwd=cwd, encoding='utf-8', errors='ignore')
        return result.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erreur avec la commande : {command}")
        return None

# Analyse des DFCs pour identifier tous les DICs
for index, row in df.iterrows():
    project = row['Project']
    depot_local = row['Depot local']
    file_path = row['File Path']
    commit_hash = row['Commit Hash']
    dfc_date = row['Date']

    if not os.path.exists(depot_local):
        print(f"Le dépôt Git est introuvable : {depot_local}")
        continue

    print(f"Analyse : Projet {project}, Dépôt {depot_local}, Fichier {file_path}, Commit {commit_hash}")

    # Utiliser git diff pour identifier les lignes modifiées
    diff_command = f"git diff {commit_hash}~1 {commit_hash} -- {file_path}"
    diff_output = run_command(diff_command, cwd=depot_local)

    if diff_output:
        lines_modified = []
        for line in diff_output.splitlines():
            if line.startswith("@@"):
                # Identifier les lignes modifiées
                parts = line.split(' ')
                old_range = parts[1]
                old_start_line = int(old_range.split(',')[0].replace('-', ''))
                lines_modified.append(old_start_line)

        # Blamer chaque ligne modifiée
        for line in lines_modified:
            blame_command = f"git blame --porcelain -L {line},{line} {file_path} {commit_hash}"
            blame_output = run_command(blame_command, cwd=depot_local)

            if blame_output:
                blame_commit_hash = blame_output.splitlines()[0].split(' ')[0]

                # Créer un dossier temporaire pour effectuer le checkout
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Cloner une copie du dépôt dans le dossier temporaire
                    clone_command = f"git clone {depot_local} {temp_dir}"
                    run_command(clone_command)

                    # Effectuer un checkout sur le commit DIC
                    checkout_command = f"git checkout {blame_commit_hash}"
                    run_command(checkout_command, cwd=temp_dir)

                    # Vérifier si le fichier existe et récupérer son chemin relatif
                    dic_file_path = None
                    for root, _, files in os.walk(temp_dir):
                        for f in files:
                            abs_path = os.path.join(root, f)
                            if os.path.basename(abs_path) == os.path.basename(file_path):
                                dic_file_path = os.path.relpath(abs_path, temp_dir)
                                break
                        if dic_file_path:
                            break

                # Récupérer la date et l'heure du commit DIC
                show_date_command = f"git show -s --format=%ci {blame_commit_hash}"
                commit_date_output = run_command(show_date_command, cwd=depot_local)

                dic_date = None
                if commit_date_output:
                    dic_date_parts = commit_date_output.split(' ')
                    dic_date = f"{dic_date_parts[0]} {dic_date_parts[1]}"

                # Ajouter les résultats
                dic_list.append({
                    "DFC Commit": commit_hash,
                    "DFC File Path": file_path,
                    "DFC Date": dfc_date,
                    "DIC Commit": blame_commit_hash,
                    "DIC File Path": dic_file_path if dic_file_path else "Non trouvé",
                    "DIC Date": dic_date,
                    "Depot local": depot_local,
                    "Line": line
                })
            else:
                print(f"Aucune information trouvée pour la ligne {line} dans {file_path}")
    else:
        print(f"Aucune modification trouvée pour le commit : {commit_hash}")
        continue

# Sauvegarder les résultats dans un fichier CSV
dic_df = pd.DataFrame(dic_list)
dic_df.to_csv(output_file, index=False)

print(f"Analyse terminée. Les résultats sont enregistrés dans '{output_file}'.")
