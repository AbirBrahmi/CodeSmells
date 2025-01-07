import pandas as pd

# Chemins d'accès aux fichiers
base_path = r"C:\\Users\\Brahm\\Documents\\CodeSmells\\Common_Raw_Data"
output_file = r"C:\\Users\\Brahm\\Documents\\CodeSmells\\RQ1\\data\\project_smell_summary_statistics.csv"

# Charger les fichiers d'entrée
complete_data = pd.read_csv(f"{base_path}\\CompleteDataSet.csv")
file_info = pd.read_csv(f"{base_path}\\csharp_files_info.csv")

# Calculer le nombre total d'odeurs par projet
total_odeurs = complete_data.groupby("Project")["Smell"].count().reset_index()
total_odeurs.rename(columns={"Smell": "Total Odeurs"}, inplace=True)

# Calculer le nombre de fichiers affectés
fichiers_affectes = complete_data.groupby("Project")["File"].nunique().reset_index()
fichiers_affectes.rename(columns={"File": "Fichiers Affectés"}, inplace=True)

# Calculer le nombre total de fichiers
total_fichiers = file_info.groupby("Project Name")["File Path"].nunique().reset_index()
total_fichiers.rename(columns={"File Path": "Total Fichiers", "Project Name": "Project"}, inplace=True)

# Calculer le pourcentage de fichiers affectés
fichiers_summary = pd.merge(fichiers_affectes, total_fichiers, on="Project", how="inner")
fichiers_summary["% Fichiers Affectés"] = (fichiers_summary["Fichiers Affectés"] / fichiers_summary["Total Fichiers"]) * 100

# Calculer la densité des odeurs par KLOC
complete_data["Densité Odeurs par KLOC"] = (
    complete_data.groupby("File")["Smell"].transform("count") / complete_data["Line Count"]
) * 1000

# Calculer la densité moyenne par projet
density_per_project = complete_data.groupby("Project")["Densité Odeurs par KLOC"].mean().reset_index()

# Créer le résumé global
summary = pd.merge(total_odeurs, fichiers_summary, on="Project")
summary = pd.merge(summary, density_per_project, on="Project")
summary.rename(columns={"Densité Odeurs par KLOC": "Densité Moyenne (Odeurs/KLOC)"}, inplace=True)

# Sauvegarder le fichier de sortie
summary.to_csv(output_file, index=False)

print(f"Fichier `summary_results.csv` généré avec succès : {output_file}")
