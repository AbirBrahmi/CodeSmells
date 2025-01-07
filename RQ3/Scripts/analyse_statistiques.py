import pandas as pd
from scipy.stats import mannwhitneyu
import cliffs_delta  # Assurez-vous d'avoir installé cette bibliothèque : pip install cliffs-delta
import os

# Chemin du fichier enrichi
file_path = r'C:\Users\Brahm\Documents\CodeSmells\Common_Raw_Data\historique_commits_with_indicators.csv'

# Charger les données
print("Chargement du fichier...")
data = pd.read_csv(file_path, sep=',')

# Vérification et ajout des colonnes nécessaires
if 'Project' not in data.columns:
    raise ValueError("La colonne 'Project' est manquante dans le fichier de données.")
if 'Taille' not in data.columns:
    print("Ajout de la colonne 'Taille'...")
    data['Taille'] = pd.cut(
        data['Churn'],
        bins=[-float('inf'), 50, 500, float('inf')],
        labels=['Petite', 'Moyenne', 'Grande']
    )

# Vérification des colonnes nécessaires
required_columns = ['Project', 'Smelly', 'Change Frequency', 'Churn', 'Taille']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise ValueError(f"Colonnes manquantes : {', '.join(missing_columns)}")

# Fonction pour calculer les statistiques descriptives
def calculer_statistiques_descriptives(group_data, metric):
    return {
        'Metric': metric,
        'Group': group_data.name if hasattr(group_data, 'name') else None,
        'Mean': group_data[metric].mean(),
        'Median': group_data[metric].median(),
        'Std Dev': group_data[metric].std(),
        'Min': group_data[metric].min(),
        'Max': group_data[metric].max()
    }

# Fonction pour effectuer les tests statistiques
def effectuer_tests_statistiques(smelly_data, non_smelly_data, metric):
    if not smelly_data.empty and not non_smelly_data.empty:
        u_stat, p_value = mannwhitneyu(smelly_data, non_smelly_data, alternative='two-sided')
        delta, magnitude = cliffs_delta.cliffs_delta(smelly_data, non_smelly_data)
        # Ajouter une interprétation des p-values
        if p_value < 1e-100:
            p_interpretation = '< 1e-100'
        elif p_value < 0.001:
            p_interpretation = '< 0.001'
        elif p_value < 0.01:
            p_interpretation = '< 0.01'
        elif p_value < 0.05:
            p_interpretation = '< 0.05'
        else:
            p_interpretation = '> 0.05'

        return {
            'U-Statistic': u_stat,
            'P-Value': p_value,
            'Cliff\'s Delta': delta,
            'Effect Size': magnitude,
            'P-Value Interpretation': p_interpretation
        }
    else:
        return {
            'U-Statistic': None,
            'P-Value': None,
            'Cliff\'s Delta': None,
            'Effect Size': None,
            'P-Value Interpretation': None
        }

# ============================
# Analyses globales
# ============================
print("Calcul des statistiques descriptives globales et des tests statistiques globaux...")
global_stats = []
global_tests = []

for metric in ['Change Frequency', 'Churn']:
    smelly = data[data['Smelly'] == 1]
    non_smelly = data[data['Smelly'] == 0]
    
    # Statistiques descriptives
    for group, group_data in [('Smelly', smelly), ('Non-Smelly', non_smelly)]:
        stats = calculer_statistiques_descriptives(group_data, metric)
        stats.update({'Metric': metric, 'Group': group})
        global_stats.append(stats)
    
    # Tests statistiques
    tests = effectuer_tests_statistiques(smelly[metric], non_smelly[metric], metric)
    tests.update({'Metric': metric, 'Test': 'Mann-Whitney U'})
    global_tests.append(tests)

global_stats_df = pd.DataFrame(global_stats)
global_tests_df = pd.DataFrame(global_tests)

# Réorganiser les colonnes pour que les titres soient à gauche
global_stats_df = global_stats_df[['Metric', 'Group', 'Mean', 'Median', 'Std Dev', 'Min', 'Max']]
global_tests_df = global_tests_df[['Metric', 'Test', 'U-Statistic', 'P-Value', 'Cliff\'s Delta', 'Effect Size', 'P-Value Interpretation']]

# Arrondir les colonnes sauf P-Value
global_stats_df = global_stats_df.round(2)
global_tests_df[['U-Statistic', 'Cliff\'s Delta', 'Effect Size']] = global_tests_df[['U-Statistic', 'Cliff\'s Delta', 'Effect Size']].round(4)

# ============================
# Analyses par taille
# ============================
print("Calcul des statistiques descriptives et des tests statistiques par taille...")
size_stats = []
size_tests = []

for size in ['Petite', 'Moyenne', 'Grande']:
    size_data = data[data['Taille'] == size]
    smelly = size_data[size_data['Smelly'] == 1]
    non_smelly = size_data[size_data['Smelly'] == 0]
    
    for metric in ['Change Frequency', 'Churn']:
        # Statistiques descriptives
        for group, group_data in [('Smelly', smelly), ('Non-Smelly', non_smelly)]:
            stats = calculer_statistiques_descriptives(group_data, metric)
            stats.update({'Size': size, 'Metric': metric, 'Group': group})
            size_stats.append(stats)
        
        # Tests statistiques
        tests = effectuer_tests_statistiques(smelly[metric], non_smelly[metric], metric)
        tests.update({'Size': size, 'Metric': metric, 'Test': 'Mann-Whitney U'})
        size_tests.append(tests)

size_stats_df = pd.DataFrame(size_stats)
size_tests_df = pd.DataFrame(size_tests)

# Réorganiser les colonnes pour que les titres soient à gauche
size_stats_df = size_stats_df[['Size', 'Metric', 'Group', 'Mean', 'Median', 'Std Dev', 'Min', 'Max']]
size_tests_df = size_tests_df[['Size', 'Metric', 'Test', 'U-Statistic', 'P-Value', 'Cliff\'s Delta', 'Effect Size', 'P-Value Interpretation']]

# Arrondir les colonnes sauf P-Value
size_stats_df = size_stats_df.round(2)
size_tests_df[['U-Statistic', 'Cliff\'s Delta', 'Effect Size']] = size_tests_df[['U-Statistic', 'Cliff\'s Delta', 'Effect Size']].round(4)

# ============================
# Analyses par projet
# ============================
print("Calcul des statistiques descriptives et des tests statistiques par projet...")
project_stats = []
project_tests = []

for project in data['Project'].unique():
    project_data = data[data['Project'] == project]
    smelly = project_data[project_data['Smelly'] == 1]
    non_smelly = project_data[project_data['Smelly'] == 0]
    
    for metric in ['Change Frequency', 'Churn']:
        # Statistiques descriptives
        for group, group_data in [('Smelly', smelly), ('Non-Smelly', non_smelly)]:
            stats = calculer_statistiques_descriptives(group_data, metric)
            stats.update({'Project': project, 'Metric': metric, 'Group': group})
            project_stats.append(stats)
        
        # Tests statistiques
        tests = effectuer_tests_statistiques(smelly[metric], non_smelly[metric], metric)
        tests.update({'Project': project, 'Metric': metric, 'Test': 'Mann-Whitney U'})
        project_tests.append(tests)

project_stats_df = pd.DataFrame(project_stats)
project_tests_df = pd.DataFrame(project_tests)

# Réorganiser les colonnes pour que les titres soient à gauche
project_stats_df = project_stats_df[['Project', 'Metric', 'Group', 'Mean', 'Median', 'Std Dev', 'Min', 'Max']]
project_tests_df = project_tests_df[['Project', 'Metric', 'Test', 'U-Statistic', 'P-Value', 'Cliff\'s Delta', 'Effect Size', 'P-Value Interpretation']]

# Arrondir les colonnes sauf P-Value
project_stats_df = project_stats_df.round(2)
project_tests_df[['U-Statistic', 'Cliff\'s Delta', 'Effect Size']] = project_tests_df[['U-Statistic', 'Cliff\'s Delta', 'Effect Size']].round(4)

# ============================
# Sauvegarde des résultats
# ============================
output_dir = r'C:\Users\Brahm\Documents\CodeSmells\RQ3\data'
os.makedirs(output_dir, exist_ok=True)


global_stats_path = os.path.join(output_dir, 'global_statistics.csv')
global_tests_path = os.path.join(output_dir, 'global_tests.csv')
size_stats_path = os.path.join(output_dir, 'size_statistics.csv')
size_tests_path = os.path.join(output_dir, 'size_tests.csv')
project_stats_path = os.path.join(output_dir, 'project_statistics.csv')
project_tests_path = os.path.join(output_dir, 'project_tests.csv')

global_stats_df.to_csv(global_stats_path, index=False)
global_tests_df.to_csv(global_tests_path, index=False)
size_stats_df.to_csv(size_stats_path, index=False)
size_tests_df.to_csv(size_tests_path, index=False)
project_stats_df.to_csv(project_stats_path, index=False)
project_tests_df.to_csv(project_tests_path, index=False)

print(f"Statistiques globales sauvegardées dans : {global_stats_path}")
