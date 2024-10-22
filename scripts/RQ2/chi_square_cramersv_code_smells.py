import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

# Charger les données (fichier généré lors de l'étape 1)
data_path = 'C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ2/grouped_smells_per_file.csv'
df = pd.read_csv(data_path)

# Supprimer les lignes avec des valeurs nulles dans la colonne 'Smell'
df = df.dropna(subset=['Smell'])

# Résultats à sauvegarder
results = []

# Liste des odeurs à comparer (remplacer par les odeurs que tu souhaites comparer)
smell_list = ['Unutilized Abstraction', 'Unnecessary Abstraction', 'Broken Hierarchy', 
              'Magic Number', 'Long Statement', 'Wide Hierarchy', 'Empty Catch Block']

# Comparaison des paires d'odeurs de code
for i in range(len(smell_list)):
    for j in range(i + 1, len(smell_list)):
        smell_a = smell_list[i]
        smell_b = smell_list[j]
        
        # Création du tableau de contingence pour deux odeurs de code
        contingency_table = pd.crosstab(df['Smell'].apply(lambda x: smell_a in x),
                                        df['Smell'].apply(lambda x: smell_b in x))
        
        # Calcul du Chi-carré
        chi2, p, dof, expected = chi2_contingency(contingency_table)
        
        # Calcul de Cramér's V
        n = contingency_table.sum().sum()  # Nombre total d'observations
        if n == 0:
            cramer_v = 0  # Pas d'association si le tableau est vide
        else:
            cramer_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
        
        # Stocker les résultats dans une liste
        results.append([smell_a, smell_b, chi2, p, cramer_v])

# Créer un DataFrame pour les résultats
results_df = pd.DataFrame(results, columns=['Smell A', 'Smell B', 'Chi2', 'p-value', 'Cramér\'s V'])

# Sauvegarder les résultats dans un fichier CSV
output_path = 'C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ2/chi_square_cramersv_results.csv'
results_df.to_csv(output_path, index=False)

print(f"Les résultats ont été sauvegardés sous : {output_path}")
