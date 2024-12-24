import requests
import time
import csv
from datetime import datetime

GITHUB_TOKENS = [
    'Token 1',
    'Token 2',
    'Token 3',
    'Token 4'
]

CURRENT_TOKEN_INDEX = 0
HEADERS = {'Authorization': f'token {GITHUB_TOKENS[CURRENT_TOKEN_INDEX]}'}

GITHUB_API_URL = 'https://api.github.com'
SEARCH_REPOS_URL = f'{GITHUB_API_URL}/search/repositories'

def switch_token():
    """Bascule vers le prochain token disponible."""
    global CURRENT_TOKEN_INDEX
    CURRENT_TOKEN_INDEX = (CURRENT_TOKEN_INDEX + 1) % len(GITHUB_TOKENS)
    HEADERS['Authorization'] = f'token {GITHUB_TOKENS[CURRENT_TOKEN_INDEX]}'
    print(f"Basculement vers le token {CURRENT_TOKEN_INDEX + 1}")

def check_rate_limit(headers):
    """Vérifie les limites de taux de l'API GitHub."""
    remaining = headers.get('X-RateLimit-Remaining')
    reset_time = headers.get('X-RateLimit-Reset')

    if remaining and int(remaining) == 0:
        reset_timestamp = int(reset_time)
        reset_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_timestamp))
        print(f"Limite d'API atteinte. La limite sera réinitialisée à {reset_time_str}.")
        switch_token()
        return False
    return True

def make_github_request(url, params=None):
    """Fait une requête à l'API GitHub en vérifiant les limites de taux."""
    while True:
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()

            # Vérifiez les limites de taux
            if not check_rate_limit(response.headers):
                continue
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête GitHub : {e}")
            return None

def fetch_total_repositories_count(query):
    """Récupère le nombre total de dépôts GitHub correspondant à la requête sur toute la période."""
    params = {
        'q': query,
        'per_page': 1,
    }

    response = make_github_request(SEARCH_REPOS_URL, params=params)
    if response:
        return response.json().get('total_count', 0)
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
        response = make_github_request(SEARCH_REPOS_URL, params=params)
        
        if not response or not response.json().get('items'):
            print(f"Aucun dépôt trouvé pour la période {start_date} à {end_date}.")
            break

        total_count = response.json().get('total_count', 0)
        if total_count > 1000:
            print(f"Plus de 1000 résultats trouvés pour la période {start_date} à {end_date}. Division de la période...")
            mid_date = datetime.strptime(start_date, '%Y-%m-%d') + (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')) / 2
            mid_date_str = mid_date.strftime('%Y-%m-%d')
            repos += fetch_repositories(query, start_date, mid_date_str, per_page)
            repos += fetch_repositories(query, mid_date_str, end_date, per_page)
            return repos

        repos.extend(response.json()['items'])
        print(f"Page {page}: {len(response.json()['items'])} projets récupérés.")
        
        if len(response.json()['items']) < per_page:
            break

        page += 1
        params['page'] = page
        time.sleep(1)  # Délai ajouté pour éviter de dépasser les limites d'API

    return repos

def get_default_branch(repo_full_name):
    """Récupère la branche par défaut d'un dépôt."""
    repo_url = f"{GITHUB_API_URL}/repos/{repo_full_name}"
    response = make_github_request(repo_url)
    if response:
        return response.json().get('default_branch', 'main')
    return None

def count_commits_in_repo(repo_full_name, default_branch):
    """Compte le nombre total de commits dans un dépôt."""
    commits_url = f"{GITHUB_API_URL}/repos/{repo_full_name}/commits"
    params = {'sha': default_branch, 'per_page': 1}
    
    try:
        response = requests.get(commits_url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        
        # Vérifiez les limites de taux
        if not check_rate_limit(response.headers):
            return 0

        if 'Link' in response.headers:
            return int(response.headers['Link'].split(',')[1].split(';')[0].split('&page=')[-1].split('>')[0])
        else:
            data = response.json()
            return len(data)  # Retourne le nombre de commits si 'Link' n'est pas dans les en-têtes
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du comptage des commits pour {repo_full_name} : {e}")
        return 0

def get_watchers_count(repo_full_name):
    """Récupère le nombre correct de watchers pour un dépôt."""
    repo_url = f"{GITHUB_API_URL}/repos/{repo_full_name}"
    response = make_github_request(repo_url)
    if response:
        return response.json().get('subscribers_count', 0)
    return 0

def count_files_in_repo(repo_full_name, default_branch):
    """Compte le nombre total de fichiers et de fichiers C# dans un dépôt."""
    tree_url = f"{GITHUB_API_URL}/repos/{repo_full_name}/git/trees/{default_branch}?recursive=1"
    response = make_github_request(tree_url)
    if response:
        tree = response.json().get('tree', [])
        files_count = len(tree)
        csharp_files_count = sum(1 for file in tree if file['type'] == 'blob' and file['path'].endswith('.cs'))
        print(f"Dépôt: {repo_full_name} - Total fichiers: {files_count}, Fichiers C#: {csharp_files_count}")
        return files_count, csharp_files_count
    return 0, 0

def extract_repo_info(repo):
    """Extrait les informations d'un dépôt et compte les fichiers C#."""
    try:
        default_branch = get_default_branch(repo['full_name'])
        if default_branch is None:
            return None, None
        files_count, csharp_files_count = count_files_in_repo(repo['full_name'], default_branch)
        commit_count = count_commits_in_repo(repo['full_name'], default_branch)
        watchers_count = get_watchers_count(repo['full_name'])
    except RuntimeError as e:
        return None, str(e)

    if csharp_files_count == 0:
        print(f"Pas de fichiers C# trouvés dans {repo['full_name']}, ignoré.")
        return None, None

    repo_info = {
        'Name': repo['name'],
        'URL': repo['html_url'],
        'forks': repo['forks_count'],
        'watchers': watchers_count,
        'stars_count': repo['stargazers_count'],
        'created_at': repo['created_at'],
        'updated_at': repo['updated_at'],
        'fork': repo['fork'],
        'size': repo['size'],
        'commit_count': commit_count,
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
            if row:
                writer.writerow(row)

def main():
    start_date_input = input("Entrez la date de début (YYYY-MM-DD) : ")
    end_date_input = input("Entrez la date de fin (YYYY-MM-DD) : ")
    language = input("Entrez le langage de programmation (par exemple, C#) : ")

    filter_stars = input("Voulez-vous filtrer par le nombre d'étoiles ? (oui/non) : ").strip().lower()
    stars = input("Entrez le nombre minimum d'étoiles : ") if filter_stars == "oui" else ""

    filter_technology = input("Voulez-vous filtrer par une technologie spécifique (par exemple, ASP.NET, ASP.NET Core, .NET) ? (oui/non) : ").strip().lower()
    technology = input("Entrez la technologie spécifique : ") if filter_technology == "oui" else ""

    start_date = start_date_input
    end_date = end_date_input

    stars_filter = f'stars:>{stars}' if stars else ''
    query = f'language:{language} {stars_filter} {technology} archived:false'

    total_repos_count = fetch_total_repositories_count(f'{query} created:{start_date}..{end_date}')
    print(f"Nombre total de dépôts trouvés pour la période {start_date} à {end_date} avec les filtres : {total_repos_count}")

    repo_data = []
    global error_data
    error_data = []

    fieldnames = ['Name', 'URL', 'forks', 'watchers', 'stars_count', 'created_at', 'updated_at', 'fork', 'size', 'commit_count', 'files_count', 'C#_files_count']

    RESULTS_CSV = f'github_csharp_repos_{start_date}_to_{end_date}.csv'
    ERRORS_CSV = f'github_csharp_repos_errors_{start_date}_to_{end_date}.csv'

    print(f"Lancement de la requête pour la période {start_date} à {end_date}")
    repos = fetch_repositories(query, start_date, end_date)
    
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
