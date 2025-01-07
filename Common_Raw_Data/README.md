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
### 4. Analyzed_Project

- **Description** : Ce dossier contient des fichiers extraits pour analyser les odeurs de code et d'autres caractéristiques associées dans les projets, pour répondre aux questions RQ1.
    
- **Utilisation** :
    
    - Fournir une base de données détaillée pour l'étude des odeurs de code à différents niveaux (fichiers, classes, etc.).
        
    - Utilisé spécifiquement pour répondre à RQ1.
        
- **Structure et contenu** :
    
    - Chaque fichier est nommé selon le projet analysé, par exemple  :
        
        - - `Designite_Blog.Core.xlsx`.
            
        - `Designite_Boleto.Net.xlsx.
            
        - `Designite_Greenshot.xlsx.
            
        - ....
            


**Exemple** :

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|File Name|Namespace|Smell Type|Severity|Date Analyzed|Smell Count|
|DbFirstController.cs|Blog.Core.Controllers|Design smell|High|2024-12-22|3|
|AccountService.cs|Blog.Core.Services|Code smell|Medium|2024-12-22|2|

- **Sous-dossiers** :
    
    - Le dossier peut contenir des sous-dossiers organisés par projet ou par type d'analyse.
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
     - [Documentation RQ1](RQ1/README.md)
     - [Documentation RQ2](RQ2/README.md)
     - [Documentation RQ3](RQ3/README.md)
     - [Documentation RQ4](RQ4/README.md)

---

## Références
- **Documentation des questions de recherche** :
- [Project Overview](/README.md)
- [Common Raw Data Documentation](/Common_Raw_Data/README.md) 
- [Common Scripts Documentation](/Common_Scripts/README.md) 
- [GitHub Total Extraction Documentation](/GitHub_Total_Extraction/README.md) 
- [RQ1 Documentation](/RQ1/README.md) 
- [RQ2 Documentation](/RQ2/README.md) 
- [RQ3 Documentation](/RQ3/README.md) 
- [RQ4 Documentation](/RQ4/README.md)

---
