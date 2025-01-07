# Organisation du Répertoire GitHub_Total_Extraction

## Structure des Dossiers

### 1. `github_csharp_repos_2015-01-01_to_2024-09-06 Extraction.csv`
Contient tous les projets extraits de GitHub en fonction des critères de sélection définis. Ces projets incluent :
- Langage : C#
- Framework : .NET
- Projets non archivés
- Période de création : Du 1er janvier 2015 au 6 septembre 2024

---

### 2. `Final_Selection.csv`
Contient uniquement les projets sélectionnés pour l'étude des code smells après plusieurs étapes de filtrage :
- Nombre de commits >= 1000.
- Nombre de fichiers C# >= 100.
- Activité continue sur au moins 5 ans.
- Tri par étoiles (stars).

---

## Processus de Sélection
1. **Extraction initiale** :
   - Utilisation du script `github_repository_analyzer` pour collecter 345 000 projets.
   - Critères : Langage C#, framework .NET, projets non archivés.

| **Détails supplémentaires**       | **Valeur**                                                                 |
|------------------------------------|---------------------------------------------------------------------------|
| Nom du script                     | `github_repository_analyzer`                                              |
| Adresse du script                 | `CodeSmells/Common_Scripts/github_repository_analyzer`                    |
| Langage                           | C#                                                                        |
| Framework                         | .NET                                                                      |
| Période de création               | Du 1er janvier 2015 au 6 septembre 2024                                   |
| Ensemble de données               | 345 000 projets                                                           |
| Requête utilisée                  | `language:C# created:2015-01-01..2024-09-06 archived:false`               |
| Exécution du script               | Par périodes de 1 à 6 mois pour minimiser les risques d'échec et de perte |
| Fusion des fichiers               | Tous les fichiers résultants ont été fusionnés pour obtenir l'ensemble    |

---

2. **Filtrage** :
   - Étape 1 : Nombre de commits >= 1000 → 1051 projets.
   - Étape 2 : Nombre de fichiers C# >= 100 → 977 projets.
   - Étape 3 : Activité >= 5 ans → 421 projets.
   - Étape 4 : Classement par nombre d'étoiles → 420 projets sélectionnés.

| **Étape**                        | **Détail**                                                                  |
|-----------------------------------|------------------------------------------------------------------------------|
| Filtrage initial (commits >= 1000)| 1051 projets retenus                                                        |
| Sélection selon fichiers C# (>= 100)| 977 projets conservés                                                      |
| Tri par années d'activité (>= 5 ans)| 421 projets avec plus de 5 ans d'activité                                   |
| Tri par étoiles                   | 420 projets sélectionnés                                                    |

---

3. **Exclusion** :
   - Frameworks, bibliothèques, outils pour développeurs, projets d'exemples, projets expérimentaux.

4. **Inclusion** :
   - Applications .NET complètes, prêtes à être utilisées par des utilisateurs finaux.

---

## Utilisation
| **Dossier**         | **Description**                                                                 |
|---------------------|-------------------------------------------------------------------------------|
| **Total_Extraction**| Utilisé pour toute analyse ou validation des critères appliqués.              |
| **Final_Selection** | Utilisé pour l'étude approfondie des code smells et leur fréquence/proportion dans les projets retenus. |


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