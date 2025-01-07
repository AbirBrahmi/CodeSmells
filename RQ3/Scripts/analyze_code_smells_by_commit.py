import os
import pandas as pd
import subprocess
import time
import shutil  # Pour la compression des dossiers

# Chemin vers DesigniteConsole
designite_console_path = r'C:\Users\AT09490\Documents\DesigniteConsole\DesigniteConsole_4_2_0_0\DesigniteConsole.exe'

# Chemin du fichier CSV contenant les numéros de commit et projets
commit_file = r'C:\Users\AT09490\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\DesigniteResults\SimplCommerce\historique_commits_gitpython.csv'

# Chemin où cloner le projet (une seule fois)
clone_directory = r'C:\Users\AT09490\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\Clone'
output_dir = r'C:\Users\AT09490\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\DesigniteResults\SimplCommerce\Analyse'

# Lire le fichier des commits (projet et commit spécifiés par ligne)
commits_df = pd.read_csv(commit_file)

# Fonction pour extraire les chemins des projets d'un fichier .sln
def extract_solution_file(project_path):
    solution_file = None
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".sln"):
                solution_file = os.path.join(root, file)
                return solution_file
    return solution_file

# Fonction pour filtrer les projets de test
def is_test_project(project_name):
    return "Test" in project_name or "Tests" in project_name

# Fonction pour exécuter DesigniteConsole sur une solution spécifique
def analyze_with_designite(solution_file, project_name, commit_hash, output_dir):
    if is_test_project(project_name):
        print(f"Skipping test project: {project_name}")
        return False

    output_file_project_commit = os.path.join(output_dir, f"{project_name}_{commit_hash}")
   
    if not os.path.exists(output_file_project_commit):
        print(f"Creating output directory: {output_file_project_commit}")
        os.makedirs(output_file_project_commit)

    print(f"Analyzing project {project_name} at commit {commit_hash}...")
    print(f"Using solution file: {solution_file}")
    print(f"Results will be saved in: {output_file_project_commit}")

    command = [
        designite_console_path,
        '-i', solution_file,
        '-o', output_file_project_commit,
        '-c'
    ]

    print(f"Running DesigniteConsole command: {' '.join(command)}")

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f'Analysis completed for {project_name} at commit {commit_hash}. Results saved in {output_file_project_commit}')
        print(f"Command output: {result.stdout}")

        time.sleep(3)

        if not any(file.endswith('_DesignSmells.csv') or file.endswith('_ImpSmells.csv') for file in os.listdir(output_file_project_commit)):
            print(f"Warning: No results found for commit {commit_hash}. Please check the solution file and the analysis tool.")
            return False
    except subprocess.CalledProcessError as e:
        print(f'Error during analysis of {project_name} at commit {commit_hash}: {e}')
        print(f"Command output: {e.output}")
        print(f"Command error: {e.stderr}")
        return False

    return True

# Fonction pour fusionner les fichiers Design Smells et Implementation Smells pour un seul commit
def filter_and_combine_smells(output_dir, project_name, commit_hash):
    combined_data = []
   
    project_dir = os.path.join(output_dir, f"{project_name}_{commit_hash}")
    for file in os.listdir(project_dir):
        if file.endswith('_DesignSmells.csv') or file.endswith('_ImpSmells.csv'):
            file_path = os.path.join(project_dir, file)
           
            print(f"Reading file: {file_path}")
            df = pd.read_csv(file_path)
            df['Commit'] = commit_hash
           
            if 'Design smell' in df.columns:
                df = df.rename(columns={'Design smell': 'Code Smells'})
            elif 'Implementation smell' in df.columns:
                df = df.rename(columns={'Implementation smell': 'Code Smells'})
           
            if 'Method' not in df.columns:
                df['Method'] = None
            if 'Description' not in df.columns:
                df['Description'] = None
           
            combined_data.append(df)

    if combined_data:
        print(f"Combining smells for commit {commit_hash}...")
        return pd.concat(combined_data, ignore_index=True)
    else:
        print(f"No smell data found for commit {commit_hash}")
        return pd.DataFrame()

# Fonction pour compresser un répertoire et supprimer le répertoire original
def compress_and_remove_directory(directory_path):
    zip_file = f"{directory_path}.zip"
    print(f"Compressing directory {directory_path} to {zip_file}...")
   
    shutil.make_archive(directory_path, 'zip', directory_path)
    shutil.rmtree(directory_path)
    print(f"Directory {directory_path} has been compressed and removed.")

# Fonction pour supprimer le fichier compressé après fusion
def delete_zip_file(zip_file):
    if os.path.exists(zip_file):
        os.remove(zip_file)
        print(f"Compressed file {zip_file} has been deleted.")

# Cloner le projet une seule fois
project_name = commits_df['Project'].iloc[0]
repo_link = commits_df['Lien Github'].iloc[0]

project_path = os.path.join(clone_directory, project_name)

if not os.path.exists(project_path):
    print(f"Cloning repository for {project_name} with full history...")
    subprocess.run(['git', 'clone', repo_link, project_path], check=True)

# Boucle principale de traitement des commits
for index, row in commits_df.iterrows():
    commit_hash = row['Commit Hash']
   
    print(f"\nProcessing commit {commit_hash} ({index + 1}/{len(commits_df)})...")
   
    subprocess.run(['git', '-C', project_path, 'checkout', commit_hash], check=True)
   
    current_commit = subprocess.run(['git', '-C', project_path, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    if current_commit != commit_hash:
        print(f"Failed to checkout to the correct commit: {commit_hash}")
        continue

    solution_file = extract_solution_file(project_path)
   
    if not solution_file:
        print(f"No .sln file found for project {project_name}")
        continue

    if not analyze_with_designite(solution_file, project_name, commit_hash, output_dir):
        print(f"Skipping commit {commit_hash} due to analysis issues or test project.")
        continue

    combined_df_commit = filter_and_combine_smells(output_dir, project_name, commit_hash)
   
    output_file_combined = os.path.join(output_dir, f"{project_name}_{commit_hash}_Combined_Smells.csv")
   
    if not combined_df_commit.empty:
        combined_df_commit.to_csv(output_file_combined, mode='w', header=True, index=False)
        print(f"Combined smells saved to {output_file_combined}")
    else:
        print(f"No data found for commit {commit_hash}")

    # Compresser et supprimer le répertoire d'analyse
    compress_and_remove_directory(os.path.join(output_dir, f"{project_name}_{commit_hash}"))

    # Supprimer le fichier compressé après fusion
    zip_file = os.path.join(output_dir, f"{project_name}_{commit_hash}.zip")
    delete_zip_file(zip_file)

print(f"\nAnalysis completed for all commits. Individual results are saved in {output_dir}")
