import pandas as pd
from scipy.stats import mannwhitneyu
import cliffs_delta
import os

# Chemin du fichier enrichi
file_path = r'C:\Users\Brahm\Documents\CodeSmells\Common_Raw_Data\historique_commits_with_indicators.csv'

# Charger les données
print("Chargement du fichier...")
data = pd.read_csv(file_path, sep=',')

# Vérification des colonnes nécessaires
required_columns = ['Project', 'File Path', 'Commit Hash', 'Smelly', 'Churn']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise ValueError(f"Colonnes manquantes : {', '.join(missing_columns)}")

# Ajouter une colonne temporaire pour identifier l'état par fichier et commit
data['File_Commit'] = data['File Path'] + '_' + data['Commit Hash']

# Ajouter une colonne 'Taille' pour classer les fichiers par leur churn
if 'Taille' not in data.columns:
    print("Ajout de la colonne 'Taille'...")
    data['Taille'] = pd.cut(
        data['Churn'],
        bins=[-float('inf'), 50, 500, float('inf')],
        labels=['Petite', 'Moyenne', 'Grande']
    )

# ============================
# Fonctions pour analyses
# ============================

# Fonction pour calculer des statistiques descriptives
def calculer_statistiques(data, metric):
    return {
        'Mean': data.mean(),
        'Median': data.median(),
        'Std Dev': data.std(),
        'Min': data.min(),
        'Max': data.max(),
        'Total': data.sum()
    }

# Fonction pour afficher les fichiers correspondant à la valeur maximale
def afficher_fichiers_max(data, metric, group_name):
    max_value = data.max()
    fichiers_max = data[data == max_value].index.tolist()
    print(f"Fichiers avec la valeur maximale pour {metric} ({group_name}):")
    for fichier in fichiers_max:
        print(f"  - {fichier} : {max_value}")

# Fonction pour effectuer des tests statistiques
def effectuer_tests_statistiques(smelly_data, non_smelly_data, metric_name):
    if not smelly_data.empty and not non_smelly_data.empty:
        u_stat, p_value = mannwhitneyu(smelly_data, non_smelly_data, alternative='two-sided')
        delta, magnitude = cliffs_delta.cliffs_delta(smelly_data, non_smelly_data)
        return {
            'Metric': metric_name,
            'U-Statistic': u_stat,
            'P-Value': p_value,
            'Cliff\'s Delta': delta,
            'Effect Size': magnitude
        }
    else:
        return {key: None for key in ['Metric', 'U-Statistic', 'P-Value', 'Cliff\'s Delta', 'Effect Size']}

# Fonction pour effectuer une analyse (globale, par taille ou par projet)
def analyser_par_groupe(data, grouping_column=None):
    stats_list = []
    tests_list = []
    
    # Si une colonne de regroupement est spécifiée, grouper les données
    groups = [('', data)] if grouping_column is None else data.groupby(grouping_column, observed=True)
    
    for group_name, group_data in groups:
        smelly = group_data[group_data['Smelly'] == 1]
        non_smelly = group_data[group_data['Smelly'] == 0]
        
        # Traiter Change Frequency en premier
        for metric in ['Commit Hash', 'Churn']:
            if metric == 'Commit Hash':
                smelly_metric = smelly.groupby('File Path')['Commit Hash'].nunique()
                non_smelly_metric = non_smelly.groupby('File Path')['Commit Hash'].nunique()
                metric_name = 'Change Frequency'
            else:
                smelly_metric = smelly.groupby('File Path')[metric].sum()
                non_smelly_metric = non_smelly.groupby('File Path')[metric].sum()
                metric_name = 'Churn'
            
            # Statistiques descriptives
            smelly_stats = calculer_statistiques(smelly_metric, metric_name)
            non_smelly_stats = calculer_statistiques(non_smelly_metric, metric_name)
            
            smelly_stats.update({'Group': 'Smelly', 'Metric': metric_name, grouping_column: group_name})
            non_smelly_stats.update({'Group': 'Non-Smelly', 'Metric': metric_name, grouping_column: group_name})
            stats_list.extend([smelly_stats, non_smelly_stats])
            
            # Afficher les fichiers avec la valeur maximale
            afficher_fichiers_max(smelly_metric, metric_name, 'Smelly')
            afficher_fichiers_max(non_smelly_metric, metric_name, 'Non-Smelly')
            
            # Tests statistiques
            tests = effectuer_tests_statistiques(smelly_metric, non_smelly_metric, metric_name)
            tests.update({grouping_column: group_name, 'Metric': metric_name})
            tests_list.append(tests)
    
    stats_df = pd.DataFrame(stats_list)
    tests_df = pd.DataFrame(tests_list)

    # Réorganiser les colonnes pour que les titres soient à gauche
    stats_columns = ['Group', 'Metric', grouping_column, 'Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Total']
    tests_columns = [grouping_column, 'Metric', 'U-Statistic', 'P-Value', 'Cliff\'s Delta', 'Effect Size']
    
    if grouping_column is None:
        stats_columns.remove(grouping_column)
        tests_columns.remove(grouping_column)
    
    stats_df = stats_df[stats_columns]
    tests_df = tests_df[tests_columns]

    return stats_df, tests_df

# ============================
# Analyses globales
# ============================
print("Analyse globale...")
global_stats_df, global_tests_df = analyser_par_groupe(data)

# ============================
# Analyses par taille
# ============================
print("Analyse par taille...")
size_stats_df, size_tests_df = analyser_par_groupe(data, grouping_column='Taille')

# ============================
# Analyses par projet
# ============================
print("Analyse par projet...")
project_stats_df, project_tests_df = analyser_par_groupe(data, grouping_column='Project')

# ============================
# Sauvegarde des résultats
# ============================
output_dir = r'C:\Users\Brahm\Documents\CodeSmells\RQ3\data'
os.makedirs(output_dir, exist_ok=True)

def sauvegarder_resultats(stats_df, tests_df, prefix):
    stats_path = os.path.join(output_dir, f'{prefix}_statistics.csv')
    tests_path = os.path.join(output_dir, f'{prefix}_tests.csv')
    stats_df.to_csv(stats_path, index=False)
    tests_df.to_csv(tests_path, index=False)
    print(f"Résultats sauvegardés pour {prefix}.")

sauvegarder_resultats(global_stats_df, global_tests_df, 'global')
sauvegarder_resultats(size_stats_df, size_tests_df, 'size')
sauvegarder_resultats(project_stats_df, project_tests_df, 'project')

print("Analyses terminées avec succès.")
