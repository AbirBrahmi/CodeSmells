import os
import csv
import chardet

# Fonction pour détecter l'encodage d'un fichier
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))  # Lire les 10 000 premiers octets pour détecter l'encodage
        return result['encoding']

# Fonction pour compter les lignes d'un fichier avec un encodage détecté, avec une méthode de secours
def count_lines_in_file(file_path):
    try:
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            return sum(1 for _ in f)
    except (UnicodeDecodeError, LookupError) as e:
        print(f"Erreur avec l'encodage {encoding} pour le fichier {file_path}, tentative avec 'latin-1': {e}")
        try:
            # Tentative avec l'encodage latin-1
            with open(file_path, 'r', encoding='latin-1') as f:
                return sum(1 for _ in f)
        except Exception as e:
            print(f"Erreur en lisant le fichier {file_path}: {e}")
            return 0

# Fonction pour extraire les fichiers .cs d'un projet
def extract_csharp_files(project_dir):
    csharp_files = []
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".cs"):
                file_path = os.path.join(root, file)
                line_count = count_lines_in_file(file_path)
                csharp_files.append((file_path, line_count))
    return csharp_files

# Liste des chemins de vos projets
projects = [
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\Blog",
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\Blog.Core",
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\greenshot",
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\mpv.net",
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\NETworkManager",
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\piranha.core",
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\PixiEditor",
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\Seal-Report",
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\SimplCommerce",
    r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\Terminal.Gui"
]

# Chemin du fichier de sortie
output_file = r"C:\Users\Brahm\OneDrive\Desktop\MTR896\DesigniteProjects\csharp_files_info.csv"

with open(output_file, mode='w', newline='', encoding='utf8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Project', 'File Path', 'Line Count'])

    # Parcourir chaque projet
    for project_dir in projects:
        project_name = os.path.basename(project_dir)
        csharp_files = extract_csharp_files(project_dir)
        
        # Écrire les résultats pour chaque fichier C#
        for file_path, line_count in csharp_files:
            writer.writerow([project_name, file_path, line_count])

print(f"Extraction terminée. Les résultats sont enregistrés dans {output_file}")
