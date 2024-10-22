import git
import csv
import os
from datetime import datetime

# Chemin des dépôts Git à analyser
repos = [
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\Blog',
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\Blog.Core',
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\greenshot',
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\mpv.net',
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\NETworkManager',
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\piranha.core',
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\PixiEditor',
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\Seal-Report',
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\SimplCommerce',
    r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\Terminal.Gui'
]

# Fichier CSV de sortie
output_file = r'C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\historique_commits_gitpython.csv'

# Ouvrir le fichier CSV pour écrire les résultats
with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Project', 'File Path', 'Commit Hash', 'Date', 'Lines Added', 'Lines Deleted'])

    # Parcourir chaque dépôt Git
    for repo in repos:
        project_name = os.path.basename(repo)  # Récupérer le nom du projet
        print(f"Analyse du projet : {project_name}")

        # Ouvrir le dépôt avec GitPython
        repo_git = git.Repo(repo)

        # Parcourir les commits du dépôt
        for commit in repo_git.iter_commits():
            print(f"Analyse du commit : {commit.hexsha}")

            # Parcourir les fichiers modifiés dans le commit
            for diff in commit.diff(commit.parents[0] if commit.parents else None, create_patch=True):
                if diff.a_path and diff.a_path.endswith('.cs'):  # Filtrer les fichiers C#
                    print(f"Modification trouvée dans {diff.a_path} pour le commit {commit.hexsha}")
                    
                    # Nombre de lignes ajoutées/supprimées, en ignorant les erreurs d'encodage
                    try:
                        diff_text = diff.diff.decode('utf-8', errors='ignore').splitlines()
                    except UnicodeDecodeError:
                        diff_text = diff.diff.decode('latin-1', errors='ignore').splitlines()

                    lines_added = sum(1 for line in diff_text if line.startswith('+'))
                    lines_deleted = sum(1 for line in diff_text if line.startswith('-'))

                    writer.writerow([
                        project_name,
                        diff.a_path,  # Chemin du fichier
                        commit.hexsha,  # Hash du commit
                        datetime.fromtimestamp(commit.committed_date),  # Date du commit
                        lines_added,  # Lignes ajoutées
                        lines_deleted  # Lignes supprimées
                    ])

print(f"Extraction des commits terminée. Les résultats sont enregistrés dans {output_file}")
