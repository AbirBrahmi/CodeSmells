import pandas as pd
from tabulate import tabulate

# Chemin du répertoire pour les fichiers d'entrée et de sortie
base_dir = r"C:\Users\Brahm\Documents\CodeSmells\RQ4\data"
file_path = f"{base_dir}\\dfcs_dics_enrichi_final.csv"

# Charger les données
data = pd.read_csv(file_path)

# Vérification des colonnes nécessaires
required_columns = ['DFC_LOC', 'Smelly_Flag_DFC', 'Churn_DFC', 'Churn_DIC', 'Defect_Propagation_Time']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise KeyError(f"Les colonnes suivantes sont manquantes dans le fichier d'entrée : {missing_columns}")

# ------------------------------
# Analyse par Smelly/Non-Smelly
# ------------------------------
def analyse_smelly(data):
    # Séparer les données Smelly/Non-Smelly
    smelly_data = data[data['Smelly_Flag_DFC'] == 1]
    non_smelly_data = data[data['Smelly_Flag_DFC'] == 0]

    # Calculer les statistiques
    stats_smelly = smelly_data[metrics].agg(['mean', 'median', 'std']).round(2)
    stats_non_smelly = non_smelly_data[metrics].agg(['mean', 'median', 'std']).round(2)

    # Ajouter une colonne pour identifier le groupe
    stats_smelly['Type'] = 'Smelly'
    stats_non_smelly['Type'] = 'Non-Smelly'

    # Combiner les résultats
    combined_stats = pd.concat([stats_smelly, stats_non_smelly])

    return combined_stats

# ----------------------------
# Analyse par Taille de Fichier et Smelly/Non-Smelly
# ----------------------------
def analyse_file_size_and_smelly(data):
    # Calculer les percentiles pour les tailles
    loc_33 = data['DFC_LOC'].quantile(0.33)
    loc_66 = data['DFC_LOC'].quantile(0.66)

    # Ajouter la catégorie de taille
    data['File_Size_Category'] = pd.cut(
        data['DFC_LOC'],
        bins=[-1, loc_33, loc_66, data['DFC_LOC'].max()],
        labels=['Small', 'Medium', 'Large']
    )

    # Séparer les données en Smelly/Non-Smelly
    smelly_data = data[data['Smelly_Flag_DFC'] == 1]
    non_smelly_data = data[data['Smelly_Flag_DFC'] == 0]

    # Calculer les statistiques par catégorie de taille pour Smelly
    stats_smelly_size = smelly_data.groupby('File_Size_Category')[metrics].agg(['mean', 'median', 'std']).round(2)
    stats_smelly_size['Type'] = 'Smelly'

    # Calculer les statistiques par catégorie de taille pour Non-Smelly
    stats_non_smelly_size = non_smelly_data.groupby('File_Size_Category')[metrics].agg(['mean', 'median', 'std']).round(2)
    stats_non_smelly_size['Type'] = 'Non-Smelly'

    # Combiner les deux analyses
    combined_stats = pd.concat([stats_smelly_size, stats_non_smelly_size])

    return combined_stats

# ------------------------------
# Exécution des analyses
# ------------------------------
metrics = ['Churn_DFC', 'Churn_DIC', 'Defect_Propagation_Time']

# Analyse par Smelly/Non-Smelly
stats_smelly_non_smelly = analyse_smelly(data)

# Analyse combinée par Taille de Fichier et Smelly/Non-Smelly
stats_size_smelly = analyse_file_size_and_smelly(data)

# ------------------------------
# Export des résultats
# ------------------------------
# Exporter les statistiques Smelly/Non-Smelly
output_path_smelly = f"{base_dir}\\stats_smelly.csv"
stats_smelly_non_smelly.to_csv(output_path_smelly, index=True)

# Exporter les statistiques combinées par Taille de Fichier et Smelly/Non-Smelly
output_path_size_smelly = f"{base_dir}\\stats_file_size_smelly.csv"
stats_size_smelly.to_csv(output_path_size_smelly, index=True)

# ------------------------------
# Affichage des résultats
# ------------------------------
print("\nStatistiques par Smelly/Non-Smelly :")
print(tabulate(stats_smelly_non_smelly, headers="keys", tablefmt="fancy_grid"))

print("\nStatistiques par Taille de Fichier et Smelly/Non-Smelly :")
print(tabulate(stats_size_smelly, headers="keys", tablefmt="fancy_grid"))

print(f"\nLes résultats par Smelly/Non-Smelly ont été exportés dans : {output_path_smelly}")
print(f"Les résultats par Taille de Fichier et Smelly/Non-Smelly ont été exportés dans : {output_path_size_smelly}")
