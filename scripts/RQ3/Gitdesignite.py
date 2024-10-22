import os
import subprocess
import git
import pandas as pd

# Chemins locaux pour stocker les dépôts et résultats
local_repo_dir = "C:/Users/Brahm/Documents/CodeSmells/data/ClonedRepos"
designite_path = "C:/Users/Brahm/Documents/DesigniteConsole/DesigniteConsole/DesigniteConsole.exe"
output_dir = "C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ3/DesigniteResults"
combined_output_file = "C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ3/CombinedSmells.csv"

# Fonction pour cloner ou mettre à jour le dépôt
def clone_or_pull_repo(repo_url, repo_name):
    repo_path = os.path.join(local_repo_dir, repo_name)
    if os.path.exists(repo_path):
        repo = git.Repo(repo_path)
        if repo.head.is_detached:
            print(f"Dépôt {repo_name} est dans un état 'détaché'. Ignorer git pull.")
        else:
            repo.git.pull()  # Mettre à jour le dépôt si sur une branche active
    else:
        try:
            git.Repo.clone_from(repo_url, repo_path)  # Cloner le dépôt
        except Exception as e:
            print(f"Erreur lors du clonage du dépôt {repo_url} : {e}")
            return None
    return repo_path

# Fonction pour checkout un commit spécifique
def checkout_commit(repo_path, commit_hash):
    try:
        repo = git.Repo(repo_path)
        repo.git.checkout(commit_hash)
    except Exception as e:
        print(f"Erreur lors du checkout du commit {commit_hash} : {e}")

# Fonction pour trouver automatiquement le fichier de solution ou projet dans le dépôt cloné
def find_solution_or_project_file(repo_path):
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.sln') or file.endswith('.csproj'):
                return os.path.join(root, file)
    return None

# Fonction pour exécuter Designite Console sur un fichier de solution ou projet
def run_designite_console(project_file, output_dir):
    try:
        subprocess.run([designite_path, "-i", project_file, "-o", output_dir, "-c"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Designite sur {project_file} : {e}")

# Fonction pour combiner uniquement les DesignSmells et ImpSmells dans un fichier CSV
def combine_smells_files(results_dir, output_file):
    combined_smells = pd.DataFrame()  # DataFrame vide pour stocker les données combinées
    
    # Parcourir les fichiers dans le répertoire
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Filtrer uniquement les fichiers contenant 'DesignSmells' ou 'ImpSmells' dans leur nom
            if 'DesignSmells' in file or 'ImpSmells' in file:
                print(f"Traitement du fichier : {file}")
                
                # Spécifier explicitement le moteur pour lire les fichiers Excel
                try:
                    smells_data = pd.read_excel(file_path, engine='openpyxl')
                except Exception as e:
                    print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
                    continue
                
                # Ajouter une colonne pour indiquer le type de smell
                if 'DesignSmells' in file:
                    smells_data['Smell Type'] = 'Design Smell'
                elif 'ImpSmells' in file:
                    smells_data['Smell Type'] = 'Implementation Smell'
                
                # Combiner les résultats dans un seul DataFrame
                combined_smells = pd.concat([combined_smells, smells_data])
    
    # Sauvegarder le résultat combiné dans un fichier CSV
    combined_smells.to_csv(output_file, index=False)
    print(f"Fichier combiné des smells créé : {output_file}")

# Fonction principale pour lire le fichier d'entrée et analyser les commits
def analyze_project_commits(input_csv):
    try:
        df = pd.read_csv(input_csv, encoding='utf-8', sep=',').fillna('')  # Remplir les valeurs manquantes avec des chaînes vides
    except FileNotFoundError:
        print(f"Fichier CSV {input_csv} non trouvé.")
        return
    except pd.errors.ParserError:
        print(f"Erreur lors de la lecture du fichier CSV {input_csv}.")
        return

    # Extraire les informations du projet
    project = df['Project'].iloc[0]  # Supposition : Un seul projet dans le CSV
    repo_url = df['Lien Github'].iloc[0].strip()  # Supposition : Un seul dépôt pour tous les commits

    # Étape 1: Cloner ou mettre à jour le dépôt
    repo_name = repo_url.split("/")[-1]  # Extraire le nom du dépôt
    repo_path = clone_or_pull_repo(repo_url, repo_name)
    if repo_path is None:
        return  # Arrêter si le dépôt ne peut pas être cloné

    # Étape 2: Rechercher le fichier de solution ou projet
    project_file = find_solution_or_project_file(repo_path)
    if not project_file:
        print(f"Aucun fichier de solution (.sln) ou de projet (.csproj) trouvé dans {repo_path}")
        return

    # Parcourir chaque commit dans le CSV
    for index, row in df.iterrows():
        commit_hash = row['Commit Hash'].strip()

        # Étape 3: Basculement sur le commit
        checkout_commit(repo_path, commit_hash)

        # Étape 4: Analyser le projet avec Designite pour ce commit
        run_designite_console(project_file, output_dir)
        print(f"Analyse du projet {project} au commit {commit_hash} terminée.")
        
        # Étape 5: Combiner les smells dans un fichier CSV après l'analyse
        combine_smells_files(output_dir, combined_output_file)

# Lancer l'analyse à partir du fichier CSV contenant les commits
input_csv = "C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ3/historique_commits_gitpython.csv"
analyze_project_commits(input_csv)
