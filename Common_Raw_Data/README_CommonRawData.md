# Documentation des RawData

## Description Générale
Ce document présente tous les fichiers de données brutes (*RawData*) utilisés dans le projet pour répondre aux questions de recherche (RQ1, RQ2, RQ3, RQ4). Ces fichiers couvrent les analyses des odeurs de code, les caractéristiques des fichiers C#, et l'historique des commits.

---

## RawData Inclus

### 1. CompleteDataSet.csv
- **Description** : Ce fichier contient l'analyse consolidée des odeurs de code détectées dans la dernière version des 10 projets.
- **Utilisation** :
  - Répondre aux questions RQ1 et RQ2.
  - Analyser les types d'odeurs et leur répartition dans les fichiers et les projets.
- **Colonnes principales** :
  - `Project` : Nom du projet.
  - `URL` : Lien vers le dépôt GitHub du projet.
  - `Smell Type` : Catégorie d'odeur détectée (ex. : Design smell).
  - `Smell` : Nom spécifique de l'odeur (ex. : Unutilized Abstraction).
  - `Namespace` : Espace de noms où l'odeur est localisée.
  - `Class` : Nom de la classe affectée.
  - `File` : Chemin complet du fichier source.
  - `Line Count` : Nombre de lignes dans le fichier.

**Exemple** :

| Project   | URL                                  | Smell Type    | Smell               | Namespace               | Class               | File               | Line Count |
|-----------|--------------------------------------|---------------|---------------------|-------------------------|---------------------|--------------------|------------|
| Blog.Core | [GitHub](https://github.com/...)     | Design smell  | Unutilized Abstr.   | Blog.Core.Controllers  | DbFirstController   | C:\path...         | 179        |


---

### 2. csharp_files_info.csv
- **Description** : Ce fichier contient des informations sur les fichiers C# de la dernière version des projets.
- **Utilisation** :
  - Analyser les caractéristiques des fichiers (par exemple, leur taille) dans RQ1 et RQ2.
- **Colonnes principales** :
  - `Project Name` : Nom du projet.
  - `File Path` : Chemin complet du fichier source.
  - `Line Count` : Nombre de lignes dans le fichier.

**Exemple** :

| Project Name | File Path                 | Line Count |
|--------------|---------------------------|------------|
| Blog.Core    | Blog.Core/Controllers/... | 200        |

---

### 3. historique_commits_with_indicators.csv
- **Description** : Ce fichier contient l'historique des commits pour chaque projet, avec des indicateurs sur les modifications et les odeurs de code.
- **Utilisation** :
  - Explorer l'évolution des odeurs de code et les modifications dans RQ3 et RQ4.
- **Colonnes principales** :
  - `Project` : Nom du projet.
  - `File Path` : Chemin complet du fichier modifié dans le commit.
  - `Commit Hash` : Identifiant unique du commit.
  - `Date` : Date du commit.
  - `Commit Message` : Message associé au commit.
  - `Files Modified` : Nombre de fichiers modifiés.
  - `Lines Added` : Lignes ajoutées.
  - `Lines Deleted` : Lignes supprimées.
  - `Smelly` : Indique si le fichier contient une odeur après le commit (1 = oui, 0 = non).
  - `Change Frequency` : Fréquence des modifications sur le fichier.
  - `Churn` : Somme des lignes ajoutées et supprimées.

**Exemple** :

| Project   | File Path                 | Commit Hash | Date       | Commit Message    | Files Modified | Lines Added | Lines Deleted |
| --------- | ------------------------- | ----------- | ---------- | ----------------- | -------------- | ----------- | ------------- |
| Blog.Core | Blog.Core/Controllers/... | 2c1c09...   | 2024-12-24 | Adjust the method | 10             | 65          | 1             |

---

## Instructions d'Utilisation

1. **Emplacement des fichiers** :
   - Tous les fichiers de données brutes se trouvent dans le dossier `Common_RawData`.

2. **Utilisation dans les scripts** :
   - **RQ1 et RQ2** :
     - `CompleteDataSet.csv` : utilisé pour analyser la prévalence et la densité des odeurs de code.
     - `csharp_files_info.csv` : utilisé pour extraire des informations détaillées sur les fichiers C#.
   - **RQ3 et RQ4** :
     - `historique_commits_with_indicators.csv` : utilisé pour analyser les modifications dans les historiques de commits et leur impact sur les odeurs de code.

3. **Exécution des scripts** :
   - Les scripts pour chaque question de recherche se trouvent dans les sous-dossiers correspondants :
     - **RQ1** : `RQ1/`
     - **RQ2** : `RQ2/`
     - **RQ3** : `RQ3/`
     - **RQ4** : `RQ4/`
   - Consultez les fichiers spécifiques dans chaque dossier pour des instructions détaillées :
     - [Documentation RQ1](../RQ1/README_RQ1.md)
     - [Documentation RQ2](../RQ2/README_RQ2.md)
     - [Documentation RQ3](../RQ3/README_RQ3.md)
     - [Documentation RQ4](../RQ4/README_RQ4.md)

---

## Références
- **Outil utilisé pour extraire les odeurs** : [Designite](https://www.designite.io).
- **Documentation des questions de recherche** :
  - [RQ1 Documentation](../RQ1/README_RQ1.md)
  - [RQ2 Documentation](../RQ2/README_RQ2.md)
  - [RQ3 Documentation](../RQ3/README_RQ3.md)
  - [RQ4 Documentation](../RQ4/README_RQ4.md)
