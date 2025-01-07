import pandas as pd

# Chargement des fichiers CSV contenant les données de fréquence et de prévalence
file_frequency_path = r"C:\Users\Brahm\Documents\CodeSmells\RQ1\data\frequency_by_project.csv"
file_prevalence_path = r"C:\Users\Brahm\Documents\CodeSmells\RQ1\data\prevalence_by_project.csv"

# Lire les fichiers CSV dans des DataFrames pandas
df_frequency = pd.read_csv(file_frequency_path)
df_prevalence = pd.read_csv(file_prevalence_path)

# Conversion des pourcentages en valeurs numériques (en enlevant le signe '%' et en divisant par 100)
def convert_percentage_to_numeric(df):
    for column in df.columns[1:]:  # Ignorer la première colonne 'Smell'
        df[column] = df[column].replace('%', '', regex=True).astype(float) / 100
    return df

# Convertir les pourcentages pour les deux DataFrames
df_frequency = convert_percentage_to_numeric(df_frequency)
df_prevalence = convert_percentage_to_numeric(df_prevalence)

# Fonction pour classer les odeurs de code dans l'une des 4 catégories avec abréviations
def classify_smell_by_project(row, project, median_freq, median_prev):
    # Utiliser les valeurs spécifiques de 'Frequency' et 'Prevalence' pour le projet donné
    frequency = row[project + '_Frequency']  # Accéder à la valeur de fréquence pour ce projet
    prevalence = row[project + '_Prevalence']  # Accéder à la valeur de prévalence pour ce projet
    
    if frequency >= median_freq and prevalence >= median_prev:
        return 'HPHF'  # High Prevalence & High Frequency
    elif frequency < median_freq and prevalence >= median_prev:
        return 'HPLF'  # High Prevalence & Low Frequency
    elif frequency >= median_freq and prevalence < median_prev:
        return 'LPHF'  # Low Prevalence & High Frequency
    else:
        return 'LPLF'  # Low Prevalence & Low Frequency

# Créer un DataFrame pour stocker les résultats classifiés
df_classified = pd.DataFrame()

# Ajouter la colonne 'Smell' pour les odeurs de code
df_classified['Smell'] = df_frequency['Smell']

# Analyser chaque projet séparément et ajouter le seuil dans le nom de la colonne
for project in df_frequency.columns[1:]:  # Supposons que la première colonne est 'Smell'
    # Calculer les médianes de fréquence et prévalence pour chaque projet
    median_frequency = df_frequency[project].median()
    median_prevalence = df_prevalence[project].median()

    # Appliquer un seuil minimum pour la médiane
    if median_frequency < 0.01:
        median_frequency = 0.01
    if median_prevalence < 0.01:
        median_prevalence = 0.01

    # Créer des colonnes temporaires pour "Frequency" et "Prevalence" par projet
    df_classified[project + '_Frequency'] = df_frequency[project]
    df_classified[project + '_Prevalence'] = df_prevalence[project]
    
    # Classifier chaque odeur de code pour ce projet
    df_classified[project] = df_classified.apply(
        lambda row: classify_smell_by_project(row, project, median_frequency, median_prevalence), axis=1)

    # Renommer les colonnes pour inclure les seuils dans l'en-tête sous forme de pourcentage
    df_classified.rename(columns={project: f"{project} (Freq: {median_frequency*100:.2f}%, Prev: {median_prevalence*100:.2f}%)"}, inplace=True)

# Supprimer les colonnes de fréquence et prévalence temporaires
df_classified.drop(columns=[col for col in df_classified.columns if '_Frequency' in col or '_Prevalence' in col], inplace=True)

# Réorganiser le DataFrame en plaçant la colonne 'Smell' en premier
df_classified = df_classified[['Smell'] + [col for col in df_classified.columns if col != 'Smell']]

# Afficher les résultats classifiés pour chaque projet
print(df_classified)

# Sauvegarder les résultats dans un fichier CSV
output_path = r"C:\Users\Brahm\Documents\CodeSmells\RQ1\data\classified_smells_per_project_median.csv"
df_classified.to_csv(output_path, index=False)
