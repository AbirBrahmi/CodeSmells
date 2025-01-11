import pandas as pd

# Chemin du répertoire pour les fichiers d'entrée et de sortie
base_dir = r"C:\Users\Brahm\Documents\CodeSmells\RQ4\data"
file_path = f"{base_dir}\\dfcs_dics_enrichi_final.csv"

# Charger les données
data = pd.read_csv(file_path)

# Vérification des colonnes nécessaires
required_columns = ['Project', 'Smelly_Flag_DFC', 'Churn_DFC', 'Churn_DIC', 'Defect_Propagation_Time']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise KeyError(f"Les colonnes suivantes sont manquantes dans le fichier d'entrée : {missing_columns}")

# ------------------------------
# Analyse par Projet et Smelly
# ------------------------------
def analyse_project(data):
    results = []

    for project in data['Project'].unique():
        project_data = data[data['Project'] == project]

        for smelly_flag in [0, 1]:
            smelly_data = project_data[project_data['Smelly_Flag_DFC'] == smelly_flag]
            stats = smelly_data[metrics].agg(['mean', 'median', 'std']).round(2)

            # Ajouter les résultats horizontalement pour chaque projet et Smelly Flag
            results.append({
                'Project': project,
                'Smelly_Flag': smelly_flag,
                'Churn_DFC_Mean': stats.loc['mean', 'Churn_DFC'] if not stats.empty else None,
                'Churn_DFC_Median': stats.loc['median', 'Churn_DFC'] if not stats.empty else None,
                'Churn_DFC_Std': stats.loc['std', 'Churn_DFC'] if not stats.empty else None,
                'Churn_DIC_Mean': stats.loc['mean', 'Churn_DIC'] if not stats.empty else None,
                'Churn_DIC_Median': stats.loc['median', 'Churn_DIC'] if not stats.empty else None,
                'Churn_DIC_Std': stats.loc['std', 'Churn_DIC'] if not stats.empty else None,
                'Defect_Propagation_Time_Mean': stats.loc['mean', 'Defect_Propagation_Time'] if not stats.empty else None,
                'Defect_Propagation_Time_Median': stats.loc['median', 'Defect_Propagation_Time'] if not stats.empty else None,
                'Defect_Propagation_Time_Std': stats.loc['std', 'Defect_Propagation_Time'] if not stats.empty else None,
            })

    return pd.DataFrame(results)

# ------------------------------
# Exécution de l'analyse
# ------------------------------
metrics = ['Churn_DFC', 'Churn_DIC', 'Defect_Propagation_Time']
stats_project = analyse_project(data)

# ------------------------------
# Export et Affichage
# ------------------------------
output_path = f"{base_dir}\\stats_project_vertical.csv"
stats_project.to_csv(output_path, index=False)

# Affichage des résultats dans un tableau formaté
from tabulate import tabulate
print("\nStatistiques regroupées par projet et Smelly Flag :")
print(tabulate(stats_project.head(20), headers="keys", tablefmt="fancy_grid"))

print(f"\nLes résultats ont été exportés dans : {output_path}")
