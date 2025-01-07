# Méthodologie de l'étude RQ3

## Objectif
Analyser l’impact des odeurs de code sur la fréquence des modifications (*Change Frequency*) et le volume des changements (*Churn*) dans les fichiers C# en comparant les fichiers affectés par des odeurs de code (*Smelly Files*) à ceux qui ne le sont pas (*Non-Smelly Files*).

---

## Étapes de la Méthodologie

### Collecte des Données

1. **Extraction de l’historique des commits**
   - Script : 
     ```
     CodeSmells\RQ3\Scripts\extract_commit_history_change_proneness.py
     ```
   - Fonctionnalités : Analyse de la branche principale d'un dépôt Git pour identifier les fichiers modifiés, calculer les lignes ajoutées/supprimées et exporter les résultats dans un fichier CSV.
   - Résultat : 10 fichiers consolidés (équivalent à 1 fichier par projet).
   - Emplacement : `C:\Users\Brahm\Documents\CodeSmells\RQ3\data\Historique Commit`

2. **Analyse des odeurs de code par commit**
   - Script : 
     ```
     CodeSmells\RQ3\Scripts\analyze_code_smells_by_commit.py
     ```
   - Fonctionnalités : Utilisation de DesigniteConsole pour détecter les odeurs de code dans chaque commit et les combiner en un seul fichier consolidé.
   - Emplacement des fichiers : `C:\Users\Brahm\Documents\CodeSmells\RQ3\data\AllCombinedsmells`

3. **Fusion des résultats Designite**
   - Script : 
     ```
     CodeSmells\RQ3\Scripts\merge_designite_reports.py
     ```
   - Fonctionnalités : Fusion des fichiers CSV contenant des "Code Smells" par projet en excluant des colonnes inutiles.
   - Résultat : Fichiers consolidés par projet.
   - Emplacement : `C:\Users\Brahm\Documents\CodeSmells\data\StudyCodeSmells\ProcessedData\RQ3\DesigniteResults\SimplCommerce\Combined_Smells.csv`

4. **Fusion des fichiers consolidés**
   - Script : 
     ```
     CodeSmells\RQ3\Scripts\fusionner_fichiers.py
     ```
   - Fonctionnalités : Fusion des fichiers de "Code Smells" et d'historique des commits pour tous les projets.
   
5. **Ajout de colonnes "Smelly"**
   - Script : 
     ```
     CodeSmells\RQ3\Scripts\ajouter_smelly_colonne.py
     ```
   - Fonctionnalités : Ajout d’un indicateur binaire indiquant si un fichier est affecté par une odeur de code.

6. **Calcul des indicateurs clefs**
   - Script : 
     ```
     CodeSmells\RQ3\Scripts\calcul_indicateurs.py
     ```
   - Fonctionnalités : Calcul des indicateurs "Change Frequency" et "Churn" basés sur les données fusionnées.

---

## Jeu de Données Final

**Structure des Données**

- **Project** : Nom du projet auquel appartient le fichier.
- **File Path** : Chemin du fichier modifié dans le projet.
- **Commit Hash** : Identifiant unique du commit.
- **Date** : Date du commit.
- **Commit Message** : Description des modifications.
- **Files Modified** : Nombre de fichiers modifiés dans le commit.
- **Lines Added** : Nombre de lignes ajoutées.
- **Lines Deleted** : Nombre de lignes supprimées.
- **Smelly** : Indicateur binaire (1 : fichier Smelly, 0 : fichier Non-Smelly).
- **Change Frequency** : Nombre total de modifications d’un fichier.
- **Churn** : Volume total des modifications (lignes ajoutées + supprimées).

---

## Analyse Statistique

### Préparation des Données

- **Classification des fichiers selon leur taille** :
  - Petite : ≤ 50 lignes
  - Moyenne : 51-500 lignes
  - Grande : > 500 lignes

### Analyses

1. **Approche Globale**
   - Comparaison des fichiers Smelly et Non-Smelly pour *Change Frequency* et *Churn*.
   - Tests :
     - **Mann-Whitney U** : Différences significatives
     - **Cliff’s Delta** : Taille des effets (petit, moyen, grand)

2. **Par Taille**
   - Comparaison des métriques par catégorie (Petite, Moyenne, Grande).

3. **Par Projet**
   - Comparaison des fichiers Smelly et Non-Smelly pour chaque projet.

---

## Visualisation des Données

- **Graphique 1 : Distribution de la Fréquence des Modifications (*Change Frequency*)**
  - Axe des x : Taille et type de fichier (Smelly ou Non-Smelly)
  - Axe des y : Fréquence des modifications (logarithmique)

- **Graphique 2 : Distribution du *Churn***
  - Axe des x : Taille et type de fichier (Smelly ou Non-Smelly)
  - Axe des y : Volume des modifications (logarithmique)

**Représentations graphiques**
  - *Violin plots* : Distribution des données
  - *Boxplots* : Indicateurs statistiques (médiane, quartiles)
  - *Points individuels (jitter)* : Visualisation granulaire

---

## Références
- **Documentation des questions de recherche** :
  - [README_ProjectOverview](./README_ProjectOverview.md)
  - [Common_Raw_Data Documentation](./Common_Raw_Data/README_CommonRawData)
  - [Common_Scripts Documentation](./Common_Scripts/README_CommonScripts)
  - [GitHub_Total_Extraction Documentation](./GitHub_Total_Extraction/README_GitHub_Total_Extraction.md)
  - [RQ1 Documentation](./RQ1/README_RQ1.md)
  - [RQ2 Documentation](./RQ2/README_RQ2.md)
  - [RQ3 Documentation](./RQ3/README_RQ3.md)
  - [RQ4 Documentation](./RQ4/README_RQ4.md)

---