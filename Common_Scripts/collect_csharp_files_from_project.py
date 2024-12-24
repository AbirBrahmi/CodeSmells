import os

def find_csharp_files(directory):
    cs_files = []
    # Parcours des répertoires et des fichiers
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".cs"):
                file_path = os.path.join(root, file)
                line_count = count_lines_in_file(file_path)
                cs_files.append((file_path, line_count))
    return cs_files

def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
        return 0

def save_files_to_csv(file_list, output_csv):
    import csv
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Path", "Line Count"])
        for f, line_count in file_list:
            writer.writerow([f, line_count])

# Demander à l'utilisateur de saisir le chemin du projet et le répertoire où sauvegarder le fichier de sortie
project_directory = input("Veuillez entrer le chemin complet du projet .NET : ")
output_directory = input("Veuillez entrer le répertoire où le fichier de sortie sera enregistré : ")

# Extraire le nom du projet à partir du chemin
project_name = os.path.basename(os.path.normpath(project_directory))

# Exécute la fonction pour trouver tous les fichiers .cs et compter les lignes
csharp_files = find_csharp_files(project_directory)

# Construire le nom du fichier de sortie avec le nom du projet
output_csv = os.path.join(output_directory, f"fichiers_csharp_{project_name}.csv")

# Sauvegarde les résultats dans un fichier CSV avec le nombre de lignes
save_files_to_csv(csharp_files, output_csv)

print(f"Extraction terminée. {len(csharp_files)} fichiers C# trouvés. Résultat sauvegardé dans {output_csv}.")
