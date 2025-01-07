import pandas as pd

def load_data(file_path):
    """Charge les données à partir d'un fichier CSV."""
    data = pd.read_csv(file_path)
    return data

def classify_smells(data):
    """Classe les odeurs de code en catégories basées sur leur prévalence et fréquence."""
    
    # Calcul des médianes pour la prévalence et la fréquence
    median_prevalence = data['% in smelly files/modules'].median()  # Médiane de la prévalence (basée sur les fichiers affectés)
    median_frequency = data['% in smelly files/modules'].median()  # Médiane de la fréquence (basée sur les fichiers affectés)

    # Affichage des seuils (médianes)
    print(f"Seuil de prévalence (médiane) : {median_prevalence}%")
    print(f"Seuil de fréquence (médiane) : {median_frequency}%")

    # Classification des odeurs en fonction des seuils de prévalence et fréquence
    data['Prevalence'] = data['% in smelly files/modules'].apply(lambda x: 'High' if x >= median_prevalence else 'Low')
    data['Frequency'] = data['% in smelly files/modules'].apply(lambda x: 'High' if x >= median_frequency else 'Low')

    # Création d'une colonne 'Category' pour classer les odeurs
    data['Category'] = data.apply(
        lambda row: 'High Prevalence and High Frequency' if row['Prevalence'] == 'High' and row['Frequency'] == 'High' else
                    ('High Prevalence and Low Frequency' if row['Prevalence'] == 'High' and row['Frequency'] == 'Low' else
                     ('Low Prevalence and High Frequency' if row['Prevalence'] == 'Low' and row['Frequency'] == 'High' else
                      'Low Prevalence and Low Frequency')), axis=1)

    return data

def export_to_excel(data, output_file):
    """Exporte le DataFrame vers un fichier Excel."""
    data.to_excel(output_file, index=False, sheet_name='Classified Smells')

if __name__ == "__main__":
    # Chemin vers le fichier de données généré précédemment
    input_file = r'C:\Users\Brahm\Documents\CodeSmells\RQ1\data\prevalence_frequency_for_all_projects.csv'
    
    # Charger les données
    data = load_data(input_file)
    
    # Classifier les odeurs de code
    classified_data = classify_smells(data)
    
    # Afficher les résultats
    print("\nClassification des Odeurs de Code :")
    print(classified_data[['Smell', '% in smelly files/modules', 'Category']].to_string(index=False))
    
    # Exporter les résultats vers un fichier Excel
    output_file = r'C:\Users\Brahm\Documents\CodeSmells\RQ1\data\classified_smellsnew.xlsx'
    export_to_excel(classified_data, output_file)
    
    print(f"\nLes résultats ont été exportés vers {output_file}")
