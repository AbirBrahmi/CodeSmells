import requests
import json
import csv

# Demander à l'utilisateur de saisir le token GitHub
token = input("Entrez votre token GitHub : ")

# Demander à l'utilisateur de saisir l'organisation ou l'utilisateur et le dépôt
owner = input("Entrez l'organisation ou l'utilisateur : ")
repo = input("Entrez le nom du dépôt : ")

# URL de l'API GitHub pour obtenir les informations du dépôt (inclut le nom de la branche par défaut)
repo_url = f'https://api.github.com/repos/{owner}/{repo}'

# En-têtes avec le token d'accès
headers = {'Authorization': f'token {token}'}

# Envoyer la requête GET pour obtenir les informations du dépôt
repo_response = requests.get(repo_url, headers=headers)

# Vérifier si la requête a réussi
if repo_response.status_code == 200:
    # Convertir la réponse en JSON
    repo_info = repo_response.json()
    
    # Obtenir le nom de la branche par défaut
    default_branch = repo_info.get('default_branch', 'main')
    
    print(f"Branche par défaut trouvée : {default_branch}")

    # URL de l'API GitHub pour les commits de la branche par défaut
    commits_url = f'https://api.github.com/repos/{owner}/{repo}/commits?sha={default_branch}'

    # Liste pour stocker tous les commits
    all_commits = []
    page = 1

    while True:
        # Envoyer la requête GET pour obtenir les commits
        response = requests.get(commits_url, headers=headers, params={'page': page, 'per_page': 100})

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Convertir la réponse en JSON
            commits = response.json()

            # Vérifier si nous avons reçu des commits
            if not commits:
                break

            # Ajouter les commits à la liste
            all_commits.extend(commits)
            
            # Passer à la page suivante
            page += 1
        else:
            print(f"Erreur lors de la requête des commits: {response.status_code}")
            break

    # Enregistrer le résultat dans un fichier JSON
    with open('commits.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_commits, json_file, indent=4)

    # Écrire les données dans un fichier CSV avec encodage UTF-8
    with open('commits.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Écrire les en-têtes (les clés du premier commit)
        if all_commits:
            headers = all_commits[0].keys()
            writer.writerow(headers)
            
            # Écrire les données des commits
            for commit in all_commits:
                row = [str(value).encode('utf-8', errors='replace').decode('utf-8') for value in commit.values()]
                writer.writerow(row)

    print("Les données ont été enregistrées dans 'commits.json' et 'commits.csv'.")
else:
    print(f"Erreur lors de la requête du dépôt: {repo_response.status_code}")
