# CodeSmells\Common_Scripts

Ce répertoire contient trois scripts Python utiles pour l'analyse de code et de données associées aux "code smells" ou à l'analyse de dépôts GitHub. Chaque script est décrit ci-dessous avec ses fonctionnalités principales.

---

## `collect_csharp_files_from_project.py`

### Description
Ce script parcourt un répertoire donné pour :
1. Identifier tous les fichiers C# (`.cs`).
2. Compter le nombre de lignes dans chaque fichier.
3. Enregistrer les résultats dans un fichier CSV.

### Fonctionnalités principales
- **Exploration récursive** : Parcourt tous les sous-dossiers d'un répertoire.
- **Comptage des lignes** : Compte les lignes dans chaque fichier `.cs`.
- **Export CSV** : Sauvegarde les chemins des fichiers et les comptes de lignes dans un fichier CSV.


---

## `github_repository_analyzer.py`

### Description
Ce script analyse les dépôts GitHub en fonction de critères spécifiques comme le langage, le nombre d'étoiles ou des technologies particulières. Il collecte et sauvegarde des informations détaillées sur les dépôts dans un fichier CSV.

### Fonctionnalités principales
- **Analyse des dépôts** : Recherche des dépôts en utilisant l'API GitHub avec des filtres comme langage, étoiles, ou période de création.
- **Collecte de métriques** : Extrait des informations telles que le nombre de fichiers, de commits, d'observateurs et les fichiers C#.
- **Gestion des limites d'API** : Utilise plusieurs tokens et divise les périodes de requêtes si nécessaire.



---

## `replace_smell_headers.py`

### Description
Ce script transforme les en-têtes d'un fichier CSV contenant des données sur les "code smells" en abréviations compactes.

### Fonctionnalités principales
- **Mapping des en-têtes** : Remplace les noms complets des "code smells" par des abréviations prédéfinies.
- **Manipulation CSV** : Charge le fichier CSV original et enregistre un nouveau fichier avec les en-têtes modifiés.


---

## Organisation des fichiers
Voici l'arborescence du répertoire :
```
CodeSmells\Common_Scripts
│
├── find_csharp_files.py
├── github_repository_analyzer.py
└── replace_smell_headers.py

