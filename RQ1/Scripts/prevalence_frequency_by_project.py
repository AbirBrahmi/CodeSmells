import pandas as pd

def load_data(file_path):
    """Charge les données à partir d'un fichier CSV."""
    return pd.read_csv(file_path)

def calculate_prevalence(smell_data, file_info_data):
    """
    Calcule la prévalence (% de fichiers affectés par type de smell)
    en utilisant les informations sur le total des fichiers par projet.
    """
    smells = smell_data['Smell'].unique()
    projects = file_info_data['Project Name'].unique()
    prevalence_df = pd.DataFrame(0.0, index=smells, columns=projects)

    grouped = smell_data.groupby(['Project', 'Smell'])['File'].nunique().reset_index(name='Affected Files')
    total_files_by_project = file_info_data.groupby('Project Name')['File Path'].nunique().to_dict()

    for _, row in grouped.iterrows():
        project = row['Project']
        smell = row['Smell']
        affected_files = row['Affected Files']
        total_files = total_files_by_project.get(project, 1)
        prevalence_df.loc[smell, project] = (affected_files / total_files) * 100

    prevalence_df = prevalence_df.map(lambda x: f"{x:.2f}%" if x > 0 else "0")
    return prevalence_df

def calculate_frequency(smell_data):
    """
    Calcule la fréquence (% des occurrences d'un type de smell par projet)
    par rapport au total des occurrences dans le projet.
    """
    smells = smell_data['Smell'].unique()
    projects = smell_data['Project'].unique()
    frequency_df = pd.DataFrame(0.0, index=smells, columns=projects)

    grouped = smell_data.groupby(['Project', 'Smell']).size().reset_index(name='Occurrences')

    for project in grouped['Project'].unique():
        project_data = grouped[grouped['Project'] == project]
        total_occurrences = project_data['Occurrences'].sum()
        for _, row in project_data.iterrows():
            smell = row['Smell']
            frequency_df.loc[smell, project] = (row['Occurrences'] / total_occurrences) * 100

    frequency_df = frequency_df.map(lambda x: f"{x:.2f}%" if x > 0 else "0")
    return frequency_df

def export_to_csv(dataframe, output_file):
    """Exporte le DataFrame vers un fichier CSV."""
    dataframe.to_csv(output_file, index=True)

if __name__ == "__main__":
    smell_input_file = r"C:\\Users\\Brahm\\Documents\\CodeSmells\\Common_Raw_Data\\CompleteDataSet.csv"
    file_info_input_file = r"C:\\Users\\Brahm\\Documents\\CodeSmells\\Common_Raw_Data\\csharp_files_info.csv"

    try:
        smell_data = load_data(smell_input_file)
        file_info_data = load_data(file_info_input_file)
    except FileNotFoundError as e:
        print(f"Fichier introuvable : {e}")
        exit(1)

    if {"Project", "Smell", "File"}.issubset(smell_data.columns) and {"Project Name", "File Path"}.issubset(file_info_data.columns):
        prevalence_df = calculate_prevalence(smell_data, file_info_data)
        frequency_df = calculate_frequency(smell_data)

        prevalence_output = r"C:\\Users\\Brahm\\Documents\\CodeSmells\\RQ1\\data\\prevalence_by_project.csv"
        frequency_output = r"C:\\Users\\Brahm\\Documents\\CodeSmells\\RQ1\\data\\frequency_by_project.csv"

        export_to_csv(prevalence_df, prevalence_output)
        export_to_csv(frequency_df, frequency_output)

        print(f"Fichier de prévalence généré avec succès : {prevalence_output}")
        print(f"Fichier de fréquence généré avec succès : {frequency_output}")
    else:
        print("Les colonnes requises ne sont pas présentes dans les données.")
