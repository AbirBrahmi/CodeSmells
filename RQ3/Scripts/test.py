import pandas as pd

# Charger les données depuis votre fichier CSV
file_path = r'C:\Users\Brahm\Documents\CodeSmells\Common_Raw_Data\historique_commits_with_indicators.csv'
print("Chargement du fichier...")
data = pd.read_csv(file_path, sep=',')

# Désactiver la troncature des colonnes longues
pd.set_option('display.max_colwidth', None)

# Filtrer les groupes Smelly et Non-Smelly
smelly = data[data['Smelly'] == 1]
non_smelly = data[data['Smelly'] == 0]

# Calculer la valeur maximale pour Change Frequency et afficher les lignes correspondantes pour Smelly
max_cf_smelly = smelly['Change Frequency'].max()
rows_max_cf_smelly = smelly[smelly['Change Frequency'] == max_cf_smelly]

print("\n=== Smelly ===")
print(f"Valeur maximale pour Change Frequency (Smelly): {max_cf_smelly}")
print("Lignes correspondantes (colonnes principales) :")
print(rows_max_cf_smelly[['Project', 'File Path', 'Change Frequency', 'Churn']].head(10))  # Limiter à 10 lignes

# Calculer la valeur maximale pour Change Frequency et afficher les lignes correspondantes pour Non-Smelly
max_cf_non_smelly = non_smelly['Change Frequency'].max()
rows_max_cf_non_smelly = non_smelly[non_smelly['Change Frequency'] == max_cf_non_smelly]

print("\n=== Non-Smelly ===")
print(f"Valeur maximale pour Change Frequency (Non-Smelly): {max_cf_non_smelly}")
print("Lignes correspondantes (colonnes principales) :")
print(rows_max_cf_non_smelly[['Project', 'File Path', 'Change Frequency', 'Churn']].head(10))  # Limiter à 10 lignes
