import pandas as pd
import itertools
import numpy as np
from scipy.stats import chi2_contingency

# 1. Charger les données groupées
data_path = r'C:/Users/Brahm/Documents/CodeSmells/RQ2/data/grouped_smells_per_file.csv'
data = pd.read_csv(data_path)

# Charger les résultats d'Apriori
apriori_path = r'C:/Users/Brahm/Documents/CodeSmells/RQ2/data/apriori_rules_filtered.xlsx'
apriori_results = pd.read_excel(apriori_path)

# Extraire les paires de règles (antécédents et conséquents)
apriori_pairs = [
    (row['Règle'].split(" => ")[0], row['Règle'].split(" => ")[1])
    for _, row in apriori_results.iterrows()
]

# 2. Vérifier et transformer la colonne 'Smell'
if 'Smell' in data.columns:
    try:
        data['Smell'] = data['Smell'].apply(eval)  # Convertit les chaînes en listes
    except Exception as e:
        raise ValueError(f"Erreur lors de la conversion de 'Smell' : {e}")
else:
    raise ValueError("La colonne 'Smell' est absente du fichier.")

# 3. Extraire toutes les odeurs uniques
all_smells = set(itertools.chain.from_iterable(data['Smell']))
smells_list = sorted(list(all_smells))  # Tri alphabétique des odeurs

# 4. Créer des colonnes binaires pour chaque odeur
for smell in smells_list:
    data[smell] = data['Smell'].apply(lambda x: 1 if smell in x else 0)

# 5. Paramètres
min_support = 0.05  # Seuil pour le support
min_cramer_v = 0.2  # Seuil pour Cramer V

# 6. Analyser les associations entre les paires d'odeurs
results = []

for smell1, smell2 in itertools.combinations(smells_list, 2):
    # Trier les odeurs dans la paire
    sorted_smells = sorted([smell1, smell2])
    smell1, smell2 = sorted_smells[0], sorted_smells[1]

    # Calcul du support de la paire
    pair_support = (data[smell1] & data[smell2]).sum() / len(data)
    if pair_support < min_support:
        continue  # Ignorer les paires avec un support inférieur au seuil

    # Créer une table de contingence
    contingency_table = pd.crosstab(data[smell1], data[smell2])

    # Vérifier si la table est valide (au moins 2 lignes et 2 colonnes)
    if contingency_table.shape[0] < 2 or contingency_table.shape[1] < 2:
        continue

    # Calcul du Chi-carré et de Cramér's V
    try:
        chi2, p, _, _ = chi2_contingency(contingency_table)
        n = contingency_table.sum().sum()
        cramer_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))

        if cramer_v <= min_cramer_v:
            continue  # Ignorer les paires avec un Cramer V inférieur ou égal au seuil

        # Vérifier si la paire est dans Apriori
        apriori_match = any(
            smell1 in pair[0] and smell2 in pair[1] for pair in apriori_pairs
        )

        # Ajouter les résultats avec arrondi
        results.append({
            'Smell 1': smell1,
            'Smell 2': smell2,
            'Support (≥ 0.05)': round(pair_support, 3),
            'Chi-squared': round(chi2, 3),
            'p-value': "< 0.001" if p < 0.001 else round(p, 3),
            'Cramer V (> 0.2)': round(cramer_v, 3),
            'Apriori Match': 'Yes' if apriori_match else 'No'
        })
    except ValueError as e:
        print(f"Erreur lors du calcul pour {smell1} et {smell2} : {e}")

# 7. Convertir les résultats en DataFrame
results_df = pd.DataFrame(results)

# 8. Trier les résultats par colonnes significatives
results_df = results_df.sort_values(by=['Cramer V (> 0.2)', 'p-value'], ascending=[False, True])

# 9. Exporter les résultats filtrés
output_path = r'C:/Users/Brahm/Documents/CodeSmells/RQ2/data/chi2_results_filtered.xlsx'

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    results_df.to_excel(writer, index=False, sheet_name='Filtered Results')

print("Analyse terminée. Les résultats filtrés ont été sauvegardés dans :", output_path)
