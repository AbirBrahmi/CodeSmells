import pandas as pd

# Chemin vers le fichier d'entrée et le fichier de sortie
input_file = r'C:\Users\Brahm\Documents\CodeSmells\Common_Raw_Data\CompleteDataSet.csv'
output_file = r'C:\Users\Brahm\Documents\CodeSmells\RQ1\data\smell_count_per_project.csv'

# Lire le fichier CSV en DataFrame
try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Le fichier {input_file} n'a pas été trouvé. Vérifiez le chemin et le nom du fichier.")
    exit(1)

# Grouper par projet et type de smell, puis compter les occurrences
smell_counts = df.groupby(['Project', 'Smell']).size().unstack(fill_value=0)

# Réorganiser les données pour avoir les smells dans les lignes et les projets dans les colonnes
smell_counts = smell_counts.T  # Transposer le DataFrame
smell_counts.index.name = 'Smell'  # Nommer l'index comme "Smell"
smell_counts.columns.name = 'Project'  # Nommer les colonnes comme "Project"

# Sauvegarder les résultats dans un fichier CSV
smell_counts.to_csv(output_file)

print(f"Les résultats (smells en lignes, projets en colonnes) ont été exportés dans le fichier : {output_file}")
