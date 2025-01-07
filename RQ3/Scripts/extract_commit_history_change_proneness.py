import git
import csv
import os
from datetime import datetime
from deep_translator import GoogleTranslator

# Chemin des dépôts Git à analyser
repos = [
    r'C:\Users\AT09490\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\Clone\Blog.Core'
]

# Fichier CSV de sortie
output_file = r'C:\Users\Brahm\Documents\CodeSmells\RQ3\data\historique_commits_gitpythonBlog.Corenew.csv'

# Initialiser le traducteur Google avec deep-translator
translator = GoogleTranslator(source='auto', target='en')

# Fonction pour traduire un message de commit en anglais
def translate_message(message):
    try:
        translated_text = translator.translate(message)
        return translated_text
    except Exception as e:
        print(f"Erreur de traduction : {e}")
        return message  # Retourne le message original en cas d'échec

# Ouvrir le fichier CSV pour écrire les résultats
with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Project', 'File Path', 'Commit Hash', 'Date', 'Original Message', 'Translated Message', 'Files Modified', 'Lines Added', 'Lines Deleted'])

    # Parcourir chaque dépôt Git
    for repo in repos:
        project_name = os.path.basename(repo)  # Récupérer le nom du projet
        print(f"Analyse du projet : {project_name}")

        # Ouvrir le dépôt avec GitPython
        repo_git = git.Repo(repo)

        # Déterminer la branche principale (main ou master)
        branch_name = 'main'
        try:
            repo_git.git.rev_parse('main')
        except git.exc.GitCommandError:
            branch_name = 'master'

        # Parcourir les commits de la branche principale seulement
        for commit in repo_git.iter_commits(branch_name):
            print(f"Analyse du commit : {commit.hexsha}")
            
            # Traduire le message de commit
            original_message = commit.message.strip()
            translated_message = translate_message(original_message)

            # Compter le nombre de fichiers modifiés dans le commit
            files_modified = len(commit.stats.files)

            # Parcourir les fichiers modifiés dans le commit
            for diff in commit.diff(commit.parents[0] if commit.parents else None, create_patch=True):
                if diff.a_path and diff.a_path.endswith('.cs'):  # Filtrer les fichiers C#
                    print(f"Modification trouvée dans {diff.a_path} pour le commit {commit.hexsha}")
                    
                    # Nombre de lignes ajoutées/supprimées, en ignorant les erreurs d'encodage
                    try:
                        diff_text = diff.diff.decode('utf-8', errors='ignore').splitlines()
                    except UnicodeDecodeError:
                        diff_text = diff.diff.decode('latin-1', errors='ignore').splitlines()

                    lines_added = sum(1 for line in diff_text if line.startswith('+') and not line.startswith('+++'))
                    lines_deleted = sum(1 for line in diff_text if line.startswith('-') and not line.startswith('---'))

                    # Écrire les informations dans le fichier CSV
                    writer.writerow([
                        project_name,
                        diff.a_path,
                        commit.hexsha,
                        datetime.fromtimestamp(commit.committed_date),
                        original_message,
                        translated_message,
                        files_modified,
                        lines_added,
                        lines_deleted
                    ])

print(f"Extraction des commits terminée. Les résultats sont enregistrés dans {output_file}")
