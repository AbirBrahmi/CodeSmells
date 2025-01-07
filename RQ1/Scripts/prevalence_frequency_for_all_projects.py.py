import pandas as pd
import os

# Fonction pour charger les données
def load_data(file_path):
    """Charge les données à partir d'un fichier CSV."""
    data = pd.read_csv(file_path)
    return data

# Fonction pour calculer les statistiques globales
def calculate_statistics(data, all_smells):
    """Calcule les statistiques des odeurs de code, incluant celles qui ne sont pas détectées."""
    total_projects = data['Project'].nunique()
    detected_smells = data['Smell'].value_counts()
    total_smells = detected_smells.sum()

    # Initialiser le résumé des résultats
    summary = {
        'Smell': [],
        '% in projects': [],
        '% in smelly files/modules': [],
        '% of total smells': []
    }

    # Inclure toutes les odeurs de code même celles qui ne sont pas présentes dans les données
    for smell in all_smells:
        count = detected_smells.get(smell, 0)
        projects_with_smell = data[data['Smell'] == smell]['Project'].nunique() if count > 0 else 0
        percent_in_projects = (projects_with_smell / total_projects) * 100 if total_projects > 0 else 0

        files_with_smell = data[data['Smell'] == smell]['File'].nunique() if count > 0 else 0
        files_smelly = data['File'].nunique()
        percent_in_smelly_files = (files_with_smell / files_smelly) * 100 if files_smelly > 0 else 0

        summary['Smell'].append(smell)
        summary['% in projects'].append(round(percent_in_projects, 2))
        summary['% in smelly files/modules'].append(round(percent_in_smelly_files, 2))
        summary['% of total smells'].append(round((count / total_smells) * 100, 2) if total_smells > 0 else 0)

    summary_df = pd.DataFrame(summary)
    summary_df = summary_df.sort_values(by='% of total smells', ascending=False)

    return summary_df

# Fonction pour exporter les données vers un fichier CSV
def export_to_csv(summary_df, output_file):
    """Exporte le DataFrame vers un fichier CSV."""
    summary_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Liste complète des odeurs de code
    all_smells = [
        "Virtual Method Call from Constructor",
        "Complex Conditional",
        "Complex Method",
        "Empty Catch Block",
        "Long Identifier",
        "Long Method",
        "Long Parameter List",
        "Long Statement",
        "Magic Number",
        "Missing Default",
        "Duplicate Code",
        "Imperative Abstraction",
        "Unnecessary Abstraction",
        "Multifaceted Abstraction",
        "Unutilized Abstraction",
        "Duplicate Abstraction",
        "Feature Envy",
        "Deficient Encapsulation",
        "Unexploited Encapsulation",
        "Broken Modularization",
        "Insufficient Modularization",
        "Hub-like Modularization",
        "Cyclically-dependent Modularization",
        "Wide Hierarchy",
        "Deep Hierarchy",
        "Multipath Hierarchy",
        "Cyclic Hierarchy",
        "Unfactored Hierarchy",
        "Rebellious Hierarchy",
        "Missing Hierarchy",
        "Broken Hierarchy"
    ]

    # Fichiers d'entrée et de sortie
    summary_input = r"C:\\Users\\Brahm\\Documents\\CodeSmells\\Common_Raw_Data\\CompleteDataSet.csv"
    summary_output = r"C:\\Users\\Brahm\\Documents\\CodeSmells\\RQ1\\data\\prevalence_frequency_for_all_projects.csv"

    # Charger les données pour `summary_results`
    if os.path.exists(summary_input):
        data = load_data(summary_input)

        # Calculer les statistiques globales
        summary_df = calculate_statistics(data, all_smells)

        # Exporter les résultats vers un fichier CSV
        export_to_csv(summary_df, summary_output)

        print(f"Fichier `summary_results.csv` généré avec succès : {summary_output}")
    else:
        print(f"Le fichier {summary_input} n'existe pas.")
