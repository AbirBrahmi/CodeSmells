import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 1. Charger les données groupées
data_path = 'C:/Users/Brahm/Documents/CodeSmells/RQ2/data/grouped_smells_per_file.csv'
grouped_df = pd.read_csv(data_path)

# 2. Conversion des odeurs de code en une liste de transactions
# Assurez-vous que la colonne 'Smell' est au bon format
grouped_df['Smell'] = grouped_df['Smell'].apply(eval)  # Transforme les chaînes en listes
transactions = grouped_df['Smell'].tolist()

# 3. Encoder les transactions en format binaire
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

# 4. Appliquer l'algorithme Apriori avec des paramètres ajustés
# Ajuster le support minimum et la taille maximale des ensembles fréquents
min_support = 0.03  # Support minimum ajusté pour inclure des ensembles plus rares
max_len = 4         # Taille maximale des ensembles fréquents

frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True, max_len=max_len)

# 5. Générer les règles d'association
# Choisissez une métrique et ajustez le seuil minimum
metric = "lift"            # Vous pouvez changer en "confidence" ou "leverage"
min_threshold = 1.5        # Seulement les règles avec un lift supérieur à 1.5

rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)

# Filtrer les règles pour un support et une confiance significatifs
support_threshold = 0.05   # Inclure uniquement les règles avec un support minimum de 0.05
confidence_threshold = 0.6 # Inclure uniquement les règles avec une confiance minimum de 0.6

filtered_rules = rules[
    (rules['support'] >= support_threshold) &
    (rules['confidence'] >= confidence_threshold)
]

# Arrondir toutes les valeurs numériques pour un affichage plus lisible
filtered_rules_rounded = filtered_rules.copy()
for column in filtered_rules_rounded.select_dtypes(include=['float']):
    filtered_rules_rounded[column] = filtered_rules_rounded[column].round(3)

# Convertir la colonne 'confidence' en pourcentage
filtered_rules_rounded['confidence'] = (filtered_rules_rounded['confidence'] * 100).round(1)  # Convertir en % avec 1 décimale

# Convertir les ensembles en texte lisible pour affichage avant de renommer
filtered_rules_rounded['Règle'] = filtered_rules_rounded['antecedents'].apply(lambda x: ', '.join(list(x))) + ' => ' + filtered_rules_rounded['consequents'].apply(lambda x: ', '.join(list(x)))

# Ajouter les seuils dans les en-têtes de colonnes
filtered_rules_rounded.rename(columns={
    'antecedents': 'Éléments déclencheurs',
    'consequents': 'Éléments associés',
    'support': f'Fréquence relative (≥ {support_threshold})',
    'confidence': f'Confiance (%) (≥ {confidence_threshold * 100:.1f})',
    'lift': f'Corrélation (Lift) (≥ {min_threshold})'
}, inplace=True)

# Réorganiser les colonnes pour afficher la règle au début
filtered_rules_rounded = filtered_rules_rounded[['Règle', 'Fréquence relative (≥ 0.05)', 'Confiance (%) (≥ 60.0)', 'Corrélation (Lift) (≥ 1.5)', 'Éléments déclencheurs', 'Éléments associés']]

# Sauvegarder les règles dans un fichier Excel
output_excel_path = 'C:/Users/Brahm/Documents/CodeSmells/RQ2/data/apriori_rules_filtered.xlsx'
filtered_rules_rounded.to_excel(output_excel_path, index=False)

# 6. Afficher les résultats
print("Règles d'association filtrées :")
print(filtered_rules_rounded[['Règle', 'Fréquence relative (≥ 0.05)', 'Confiance (%) (≥ 60.0)', 'Corrélation (Lift) (≥ 1.5)']])
print(f"Le tableau formaté a été enregistré sous : {output_excel_path}")
