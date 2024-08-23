import requests
import time
import csv
from datetime import datetime, timedelta

GITHUB_TOKEN = 'Your Token'
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

GITHUB_API_URL = 'https://api.github.com'
SEARCH_REPOS_URL = f'{GITHUB_API_URL}/search/repositories'

RESULTS_CSV = 'github_repos_results.csv'
ERRORS_CSV = 'github_repos_errors.csv'

def fetch_total_repositories_count(query):
    """Récupère le nombre total de dépôts GitHub correspondant à la requête sur toute la période."""
    params = {
        'q': query,
        'per_page': 1,  # On ne récupère qu'un seul résultat, on veut juste le total_count
    }

    try:
        response = requests.get(SEARCH_REPOS_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        total_count = data.get('total_count', 0)
        return total_count
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du nombre total de dépôts : {e}")
        return 0

def fetch_repositories(query, start_date, end_date, per_page=100):
    """Récupère les dépôts GitHub correspondant à la requête dans la plage de dates."""
    repos = []
    page = 1
    params = {
        'q': f'{query} created:{start_date}..{end_date}',
        'per_page': per_page,
        'page': page
    }

    while True:
        try:
            response = requests.get(SEARCH_REPOS_URL, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des dépôts (page {page}) : {e}")
            time.sleep(5)
            continue

        if not data.get('items'):
            print(f"Toutes les pages disponibles ont été récupérées pour la période {start_date} à {end_date}.")
            break

        repos.extend(data['items'])
        print(f"Page {page}: {len(data['items'])} projets récupérés.")
        
        page += 1
        params['page'] = page
        time.sleep(1)

    return repos

def get_default_branch(repo_full_name):
    """Récupère la branche par défaut d'un dépôt."""
    repo_url = f"{GITHUB_API_URL}/repos/{repo_full_name}"
    try:
        response = requests.get(repo_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json().get('default_branch', 'main')
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Impossible de récupérer la branche par défaut pour {repo_full_name}: {e}")

def count_files_in_repo(repo_full_name, default_branch):
    """Compte le nombre total de fichiers et de fichiers C# dans un dépôt."""
    tree_url = f"{GITHUB_API_URL}/repos/{repo_full_name}/git/trees/{default_branch}?recursive=1"
    try:
        response = requests.get(tree_url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        tree = response.json().get('tree', [])
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur lors de la récupération de l'arborescence pour {repo_full_name}: {e}")

    files_count = len(tree)
    csharp_files_count = sum(1 for file in tree if file['type'] == 'blob' and file['path'].endswith('.cs'))
    
    print(f"Dépôt: {repo_full_name} - Total fichiers: {files_count}, Fichiers C#: {csharp_files_count}")
    return files_count, csharp_files_count

def extract_repo_info(repo):
    """Extrait les informations d'un dépôt et compte les fichiers C#."""
    try:
        default_branch = get_default_branch(repo['full_name'])
        files_count, csharp_files_count = count_files_in_repo(repo['full_name'], default_branch)
    except RuntimeError as e:
        return None, str(e)

    if csharp_files_count == 0:
        print(f"Pas de fichiers C# trouvés dans {repo['full_name']}, ignoré.")
        return None, None

    repo_info = {
        'Name': repo['name'],
        'URL': repo['html_url'],
        'forks': repo['forks_count'],
        'watchers': repo['watchers_count'],
        'stars_count': repo['stargazers_count'],
        'created_at': repo['created_at'],
        'updated_at': repo['updated_at'],
        'fork': repo['fork'],
        'size': repo['size'],
        'commit_count': repo['open_issues_count'],  # Utilisation des "open_issues_count" comme proxy pour les commits
        'files_count': files_count,
        'C#_files_count': csharp_files_count
    }
    return repo_info, None

def save_to_csv(filename, data, fieldnames):
    """Enregistre les données dans un fichier CSV."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            if row:  # Vérifier que la ligne n'est pas None
                writer.writerow(row)

def daterange(start_date, end_date, delta):
    """Génère une série de dates pour créer des sous-périodes de recherche."""
    current_date = start_date
    while current_date < end_date:
        next_date = current_date + delta
        yield current_date, min(next_date, end_date)
        current_date = next_date

def main():
    # Saisie des dates, du langage, du nombre d'étoiles, et de la technologie par l'utilisateur
    start_date_input = input("Entrez la date de début (YYYY-MM-DD) : ")
    end_date_input = input("Entrez la date de fin (YYYY-MM-DD) : ")
    language = input("Entrez le langage de programmation (par exemple, C#) : ")
    stars = input("Entrez le nombre minimum d'étoiles : ")

    filter_technology = input("Voulez-vous filtrer par une technologie spécifique (par exemple, ASP.NET, ASP.NET Core, .NET) ? (oui/non) : ").strip().lower()
    
    if filter_technology == "oui":
        technology = input("Entrez la technologie spécifique : ")
    else:
        technology = ""  # Pas de filtre sur la technologie

    start_date = datetime.strptime(start_date_input, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_input, '%Y-%m-%d')

    # Requête globale pour toute la période
    global_query = f'language:{language} stars:>{stars} {technology} created:{start_date_input}..{end_date_input}'
    total_repos_count = fetch_total_repositories_count(global_query)
    print(f"Nombre total de dépôts trouvés pour la période {start_date_input} à {end_date_input} avec le filtre '{technology}': {total_repos_count}")

    delta = timedelta(days=365)  # Changer cela pour une période plus courte si nécessaire (ex: 6 mois ou 3 mois)
    
    repo_data = []
    error_data = []

    fieldnames = ['Name', 'URL', 'forks', 'watchers', 'stars_count', 'created_at', 'updated_at', 'fork', 'size', 'commit_count', 'files_count', 'C#_files_count']

    for start, end in daterange(start_date, end_date, delta):
        query = f'language:{language} stars:>{stars} {technology}'
        repos = fetch_repositories(query, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        
        for repo in repos:
            repo_info, error = extract_repo_info(repo)
            if repo_info:
                repo_data.append(repo_info)
            elif error:
                print(f"Erreur lors de l'analyse du dépôt {repo['name']}: {error}")
                error_data.append({'Name': repo['name'], 'URL': repo['html_url'], 'Error': error})

    save_to_csv(RESULTS_CSV, repo_data, fieldnames)
    save_to_csv(ERRORS_CSV, error_data, ['Name', 'URL', 'Error'])

    print(f"Analyse terminée. Résultats enregistrés dans {RESULTS_CSV}. Erreurs enregistrées dans {ERRORS_CSV}.")

if __name__ == '__main__':
    main()
