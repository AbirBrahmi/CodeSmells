import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 2.1 Charger les données groupées (produites à l'étape 1)
data_path = 'C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ2/grouped_smells_per_file.csv'
grouped_df = pd.read_csv(data_path)

# 2.2 Conversion des odeurs de code en une liste de transactions (par fichier)
transactions = grouped_df['Smell'].apply(eval).tolist()  # eval est utilisé pour transformer la chaîne en liste

# 2.3 Encoder les transactions (conversion en format binaire)
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

# 2.4 Appliquer l'algorithme Apriori
frequent_itemsets = apriori(df_encoded, min_support=0.1, use_colnames=True)

# 2.5 Générer les règles d'association
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

# 2.6 Afficher les règles trouvées avec les mesures Support, Confidence et Lift
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# Optionnel : Sauvegarder les résultats des règles dans un fichier CSV pour une analyse ultérieure
output_path = 'C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ2/apriori_rules.csv'
rules.to_csv(output_path, index=False)
print(f"Les règles d'association ont été sauvegardées sous : {output_path}")
