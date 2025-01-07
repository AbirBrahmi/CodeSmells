
## Introduction
Ce projet vise à analyser les odeurs de code (« code smells ») dans des projets logiciels .NET en utilisant différentes méthodes analytiques. La structure des fichiers et répertoires ci-dessous permet de répondre à plusieurs questions de recherche (RQ) et d'organiser les données et scripts associés.

---

## Structure du Projet

### [Common_Raw_Data](./Common_Raw_Data)
Ce répertoire contient les fichiers de données brutes (« RawData ») utilisés dans le projet. Les données couvrent :
- Les analyses des odeurs de code.
- Les caractéristiques des fichiers C#.
- L'historique des commits des projets.

#### Fichiers Clés
- [README](Common_Raw_Data/README.md) : Décrit le contenu des données brutes et leur organisation.

---

### [Common_Scripts](./Common_Scripts)
Contient des scripts Python communs utiles pour :
- L'analyse des odeurs de code.
- L'analyse des dépôts GitHub.

#### Fichiers Clés
- [README](Common_Scripts/README.md) : Fournit des détails sur chaque script, ses fonctionnalités et son utilisation.

---

### [GitHub_Total_Extraction](./GitHub_Total_Extraction)
Ce répertoire contient les projets extraits de GitHub pour analyse.

#### Contenu Principal
1. **github_csharp_repos_2015-01-01_to_2024-09-06_Extraction.csv** :
   - Liste tous les projets extraits selon des critères spécifiques (C#, .NET, etc.).

2. **Final_Selection.csv** :
   - Contient uniquement les projets sélectionnés pour l'étude après filtrage.

#### Fichiers Clés
- [README_GitHub_Total_Extraction.md](GitHub_Total_Extraction/README.md) : Explique l'organisation et les critères de sélection des projets.

---

### [RQ1](./RQ1)
Analyse la prévalence des odeurs de code dans les projets .NET.

#### Sous-Répertoires
- **data** : Contient les données utilisées pour l'analyse.
- **Scripts** : Contient les scripts nécessaires pour cette étude.

#### Fichiers Clés
- [README](RQ1/README.md) : Explique la méthodologie et les objectifs de cette étude.

---

### [RQ2](./RQ2)
Explore les relations entre différentes odeurs de code dans les fichiers C#.

#### Sous-Répertoires
- **data** : Contient les données associées à l'étude.
- **Scripts** : Contient les scripts nécessaires pour cette étude..

#### Fichiers Clés
- [README](RQ2/README.md) : Fournit des détails sur l'utilisation des algorithmes Apriori et des tests statistiques.

---

### [RQ3](./RQ3)
Analyse l'impact des odeurs de code sur la fréquence et le volume des modifications (« churn »).

#### Sous-Répertoires
- **data** : Contient les données pour cette étude.
- **Scripts** : Contient les scripts nécessaires pour cette étude..

#### Fichiers Clés
- [README](RQ3/README.md) : Explique la méthodologie et les résultats attendus.

---

### [RQ4](./RQ4)
Analyse l'impact des odeurs de code sur la propension des projets .NET à accumuler des défauts.

#### Sous-Répertoires
- **data** : Données utilisées pour l'analyse.
- **Scripts** : Contient les scripts nécessaires pour cette étude..

#### Fichiers Clés
- [README](RQ4/README.md) : Décrit la méthodologie de cette étude.

---

## Conclusion
Cette organisation structurée permet une analyse approfondie des odeurs de code dans les projets .NET. Chaque répertoire est spécifiquement conçu pour répondre à une question de recherche ou pour fournir des données/soutiens techniques nécessaires à ces études.


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