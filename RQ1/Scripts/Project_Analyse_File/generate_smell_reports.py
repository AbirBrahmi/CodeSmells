import pandas as pd
import os

def generate_report(input_file, project_name, smell_name, output_dir):
    # Chargement des données
    data = pd.read_csv(input_file)
    
    # Filtrer les données en fonction du projet et du smell spécifiés
    filtered_data = data[(data['Project'] == project_name) & (data['Smell'] == smell_name)]
    
    # Vérifier si des données ont été filtrées
    if filtered_data.empty:
        print(f"Aucune donnée trouvée pour le projet '{project_name}' et le smell '{smell_name}'.")
        return
    
    # Calculer le nombre d'occurrences par classe
    class_count = filtered_data.groupby(['Class']).size().reset_index(name='Repetition Count')
    
    # Trier par nombre de répétitions en ordre décroissant
    class_count = class_count.sort_values(by='Repetition Count', ascending=False)
    
    # Assurer que le répertoire de sortie existe
    os.makedirs(output_dir, exist_ok=True)

    # Créer un fichier Excel pour chaque classe et son nombre de répétitions
    class_count_output = os.path.join(output_dir, f"{project_name}_{smell_name}_class_count.xlsx")
    class_count.to_excel(class_count_output, index=False)

    # Calculer le nombre d'occurrences par fichier
    file_count = filtered_data.groupby('File').size().reset_index(name='Repetition Count')
    
    # Trier par nombre de répétitions en ordre décroissant
    file_count = file_count.sort_values(by='Repetition Count', ascending=False)
    
    # Créer un fichier Excel pour chaque fichier et son nombre de répétitions
    file_count_output = os.path.join(output_dir, f"{project_name}_{smell_name}_file_count.xlsx")
    file_count.to_excel(file_count_output, index=False)
    
    print(f"Rapports générés :\n - {class_count_output}\n - {file_count_output}")

# Chemin du fichier CSV (à remplacer par le chemin réel)
input_file = r"C:\Users\Brahm\Documents\CodeSmells\Common_Raw_Data\CompleteDataSet.csv"

# Répertoire de sortie
output_dir = r"C:\Users\Brahm\Documents\CodeSmells\RQ1\data\Projet_Analyse_per_file"

# Demander les entrées à l'utilisateur
project_name = input("Entrez le nom du projet : ")
smell_name = input("Entrez le nom du smell : ")

# Appeler la fonction pour générer les rapports
generate_report(input_file, project_name, smell_name, output_dir)
