import pandas as pd
from scipy.stats import mannwhitneyu

# Chemin du fichier source
file_path = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\historique_commits_with_smelly.csv'

# Charger les données
print("Chargement du fichier...")
data = pd.read_csv(file_path, sep=',')  # Assurez-vous que le séparateur est ','
print("Aperçu des données chargées :")
print(data.head())

# Calcul simultané de la fréquence des modifications (Change Frequency) et du churn (Lines Added + Lines Deleted)
print("Calcul des indicateurs (Change Frequency et Churn)...")
data['Change Frequency'] = data.groupby('File Path')['Commit Hash'].transform('count')
data['Churn'] = data['Lines Added'] + data['Lines Deleted']

# Aperçu des données après ajout des indicateurs
print("Aperçu des données après calcul des indicateurs :")
print(data[['File Path', 'Change Frequency', 'Churn']].drop_duplicates().head())

# Séparer les groupes Smelly et Non-Smelly
print("Séparation des groupes Smelly et Non-Smelly...")
smelly = data[data['Smelly'] == 1]
non_smelly = data[data['Smelly'] == 0]

# Calcul des statistiques descriptives
print("Calcul des statistiques descriptives...")
stats = {
    'Smelly': {
        'Change Frequency Mean': smelly['Change Frequency'].mean(),
        'Change Frequency Median': smelly['Change Frequency'].median(),
        'Churn Mean': smelly['Churn'].mean(),
        'Churn Median': smelly['Churn'].median(),
    },
    'Non-Smelly': {
        'Change Frequency Mean': non_smelly['Change Frequency'].mean(),
        'Change Frequency Median': non_smelly['Change Frequency'].median(),
        'Churn Mean': non_smelly['Churn'].mean(),
        'Churn Median': non_smelly['Churn'].median(),
    }
}
print("Statistiques descriptives :")
print(stats)

# Tests statistiques : Mann-Whitney U
print("Tests statistiques...")
u_stat_cf, p_value_cf = mannwhitneyu(smelly['Change Frequency'], non_smelly['Change Frequency'], alternative='two-sided')
u_stat_churn, p_value_churn = mannwhitneyu(smelly['Churn'], non_smelly['Churn'], alternative='two-sided')

# Afficher les résultats des tests statistiques
print(f"Mann-Whitney U Test pour Change Frequency : U={u_stat_cf}, p={p_value_cf}")
print(f"Mann-Whitney U Test pour Churn : U={u_stat_churn}, p={p_value_churn}")

# Sauvegarder les données enrichies
output_path = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\historique_commits_with_indicators.csv'
print(f"Sauvegarde des données enrichies dans : {output_path}")
data.to_csv(output_path, index=False, sep=',')

# Sauvegarder les résultats statistiques dans un fichier texte structuré
output_stats_path = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\statistiques_resultats.csv'
print(f"Sauvegarde des résultats statistiques dans : {output_stats_path}")
with open(output_stats_path, 'w') as f:
    f.write("Statistiques Descriptives\n")
    for group, values in stats.items():
        f.write(f"\n{group}:\n")
        for metric, value in values.items():
            f.write(f"{metric}: {value}\n")

    f.write("\nTests Statistiques\n")
    f.write(f"Change Frequency:\nU-Statistic: {u_stat_cf}\nP-Value: {p_value_cf}\n")
    f.write(f"Churn:\nU-Statistic: {u_stat_churn}\nP-Value: {p_value_churn}\n")

# Sauvegarder les résultats statistiques dans un CSV tabulaire
output_stats_csv_path = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\statistiques_resultats_tabulaire.csv'
print(f"Sauvegarde des résultats statistiques tabulaires dans : {output_stats_csv_path}")

# Préparer les données pour le CSV tabulaire
stats_data = [
    ['Metric', 'Group', 'Mean', 'Median'],
    ['Change Frequency', 'Smelly', smelly['Change Frequency'].mean(), smelly['Change Frequency'].median()],
    ['Change Frequency', 'Non-Smelly', non_smelly['Change Frequency'].mean(), non_smelly['Change Frequency'].median()],
    ['Churn', 'Smelly', smelly['Churn'].mean(), smelly['Churn'].median()],
    ['Churn', 'Non-Smelly', non_smelly['Churn'].mean(), non_smelly['Churn'].median()],
    ['Metric', 'Statistic', 'U-Statistic', 'P-Value'],
    ['Change Frequency', 'Mann-Whitney U', u_stat_cf, p_value_cf],
    ['Churn', 'Mann-Whitney U', u_stat_churn, p_value_churn],
]

# Créer un DataFrame pour l'écriture
stats_df = pd.DataFrame(stats_data[1:], columns=stats_data[0])
stats_df.to_csv(output_stats_csv_path, index=False)

print("=== Étape terminée : Indicateurs calculés et résultats statistiques sauvegardés. ===")
