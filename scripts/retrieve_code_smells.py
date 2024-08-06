import subprocess
import json
import csv

# Fonction pour récupérer les entrées de l'utilisateur
def get_user_inputs():
    print("Bienvenue ! Veuillez entrer les informations nécessaires :")
    componentKeys = input("Composant Key pour SonarQube : ")
    auth_token = input("Token d'authentification pour SonarQube : ")
    output_json_file = input("Nom du fichier de sortie JSON : ")
    csv_file = input("Nom du fichier CSV de sortie : ")
    return componentKeys, auth_token, output_json_file, csv_file

# Paramètres pour l'API SonarQube
base_url = 'http://localhost:9000/api/issues/search?componentKeys='
page_number = 1
page_size = 100

# Liste pour stocker tous les résultats de code smell
all_results = []

# Fonction pour récupérer les détails d'une règle SonarQube
def get_rule_details(rule_key, auth_token):
    rule_url = f'http://localhost:9000/api/rules/show?key={rule_key}'
    command = f'curl -u {auth_token}: "{rule_url}"'
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        rule_data = json.loads(result.stdout)
        return rule_data.get('rule', {}).get('name', 'Unknown Code Smell')
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande pour la règle {rule_key}: {e}")
        return 'Unknown Code Smell'
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON pour la règle {rule_key}: {e}")
        return 'Unknown Code Smell'

# Fonction pour récupérer les données JSON depuis SonarQube
def retrieve_code_smells(componentKeys, auth_token):
    global base_url, page_number, page_size
    base_url += componentKeys
    while True:
        command = f'curl -u {auth_token}: "{base_url}&p={page_number}&ps={page_size}"'

        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            data = json.loads(result.stdout)

            if 'issues' in data:
                # Filtrer les issues pour ne prendre que les CODE_SMELL
                code_smells = [issue for issue in data['issues'] if issue['type'] == 'CODE_SMELL']
                
                # Ajouter le nom du code smell à chaque issue
                for issue in code_smells:
                    rule = issue.get('rule')
                    issue['code_smell_name'] = get_rule_details(rule, auth_token)
                
                all_results.extend(code_smells)
            else:
                print(f"Aucune clé 'issues' trouvée dans les données : {data}")

            if len(data.get('issues', [])) < page_size:
                break

            page_number += 1

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de la commande : {e}")
            break

        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON : {e}")
            break

# Fonction pour exporter les données vers un fichier JSON
def export_to_json(output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)

    print(f"Tous les résultats de code smell ont été récupérés et écrits dans '{output_file}'.")

# Fonction pour convertir les données JSON en CSV
def convert_to_csv(json_file, csv_file):
    try:
        # Charger les données JSON depuis le fichier
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Vérifier si des données sont présentes
        if not data:
            raise ValueError(f"Le fichier JSON '{json_file}' est vide.")

        # Exporter en CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Écrire l'en-tête
            writer.writerow(data[0].keys())  # Supposons que chaque élément dans la liste a les mêmes clés

            # Écrire les lignes de données
            for entry in data:
                writer.writerow(entry.values())

        print(f"Toutes les données ont été exportées vers '{csv_file}'.")

    except FileNotFoundError:
        print(f"Le fichier JSON '{json_file}' n'a pas été trouvé.")
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

# Obtenir les entrées de l'utilisateur
componentKeys, auth_token, output_json_file, csv_file = get_user_inputs()

# Ajouter les extensions si elles ne sont pas déjà présentes
if not output_json_file.endswith('.json'):
    output_json_file += '.json'

if not csv_file.endswith('.csv'):
    csv_file += '.csv'

# Appel des fonctions pour récupérer les données et les exporter
retrieve_code_smells(componentKeys, auth_token)  # Récupérer les données depuis SonarQube
export_to_json(output_json_file)  # Exporter les données en JSON
convert_to_csv(output_json_file, csv_file)  # Convertir JSON en CSV
