import pandas as pd
import os

def load_data(file_path):
    """Charge les données à partir d'un fichier CSV."""
    data = pd.read_csv(file_path)
    return data

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
        # Nombre de fois que l'odeur est détectée
        count = detected_smells.get(smell, 0)  # Si non détectée, le compte est 0

        # Nombre de projets affectés
        projects_with_smell = data[data['Smell'] == smell]['Project'].nunique() if count > 0 else 0
        percent_in_projects = (projects_with_smell / total_projects) * 100 if total_projects > 0 else 0

        # Nombre de fichiers affectés
        files_with_smell = data[data['Smell'] == smell]['File'].nunique() if count > 0 else 0
        files_smelly = data['File'].nunique()
        percent_in_smelly_files = (files_with_smell / files_smelly) * 100 if files_smelly > 0 else 0

        # Ajouter les données au résumé
        summary['Smell'].append(smell)
        summary['% in projects'].append(round(percent_in_projects, 2))
        summary['% in smelly files/modules'].append(round(percent_in_smelly_files, 2))
        summary['% of total smells'].append(round((count / total_smells) * 100, 2) if total_smells > 0 else 0)

    # Créer un DataFrame à partir du résumé
    summary_df = pd.DataFrame(summary)

    # Trier les résultats en ordre décroissant par la colonne '% of total smells'
    summary_df = summary_df.sort_values(by='% of total smells', ascending=False)

    return summary_df

def export_to_csv(summary_df, output_file):
    """Exporte le DataFrame vers un fichier CSV."""
    summary_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Liste complète des odeurs de code attendues (telles que dans l'image)
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

    # Charger les données depuis le fichier CSV
    file_path = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\RawData\CompleteDataSet.csv'
    
    if os.path.exists(file_path):
        data = load_data(file_path)

        # Calculer les statistiques incluant toutes les odeurs de code possibles
        summary_df = calculate_statistics(data, all_smells)

        # Afficher les résultats
        print("\nStatistiques des Odeurs de Code (triées de manière décroissante)")
        print(summary_df.to_string(index=False))

        # Exporter les résultats vers un fichier CSV
        output_file = r'C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ1\code_smell_statistics_sorted.csv'
        export_to_csv(summary_df, output_file)

        print(f"\nLes statistiques triées ont été exportées vers {output_file}")
    else:
        print(f"Le fichier {file_path} n'existe pas.")
