# Méthodologie de l'étude RQ2

## Objectif

L'objectif principal de cette étape est de découvrir et de valider les relations entre les différentes odeurs de code dans les fichiers C# à l'aide des algorithmes d'association et des tests statistiques. Pour cela, nous avons utilisé l'algorithme Apriori pour générer des règles d'association, le test Chi-carré pour valider statistiquement ces relations, et le V de Cramér pour mesurer l'intensité des associations.

## 1. Paramètres

### Algorithme Apriori

- **Support minimum** : 0.05 (5 % des fichiers).
- **Lift minimum** : 1.5.
- **Confiance minimum** : 0.6.
- **Taille maximale des ensembles** : 4.

### Test du Chi-carré

- **Support minimum** : 0.05.
- **p-value** : < 0.05.

### Cramér’s V

- **V ≤ 0.2** : Faible.
- **0.2 < V ≤ 0.6** : Modéré.
- **V > 0.6** : Fort.

## 2. Étapes de l'analyse

### Étape 1 : Préparation des données

#### Chargement des données

- Charger les données brutes dans un format contenant les fichiers et leurs odeurs associées.

**Exemple** :

```plaintext
File        Smell
file1       ['DDE', 'DDS']
file2       ['DDE', 'DMP', 'DDS']
```

- **Script utilisé** : `CodeSmells\RQ2\Scripts\group_code_smells_by_file.py`
- **Fichier généré** : `CodeSmells\RQ2\data\grouped_smells_per_file.csv`

---

### Étape 2 : Analyse avec l’algorithme Apriori

#### Détection des ensembles fréquents

- Appliquer l’algorithme Apriori avec les paramètres suivants :
    - **Support minimum** : 0.03.
    - **Taille maximale des ensembles fréquents** : 4.

#### Génération des règles d’association

- Calculer les métriques suivantes :
    
    - **Lift** (> 1.5).
    - **Confiance** (≥ 0.6).
- Sauvegarder les résultats dans un fichier : `apriori_validated.csv`.
    
- **Script utilisé** : `CodeSmells\RQ2\Scripts\apriori_code_smell_association.py`
    
- **Fichier généré** : `CodeSmells\RQ2\data\apriori_rules_filtered.csv`
    

---

### Étape 3 : Validation avec le test du Chi-carré

#### Sélection des paires d’odeurs

- Utiliser toutes les paires d'odeurs possibles identifiées dans les données groupées.
- Les paires issues des résultats d'Apriori sont mises en évidence dans les résultats finaux pour faciliter la comparaison.

#### Calcul des métriques statistiques

- Pour chaque paire d'odeurs :
    - Créer une table de contingence.
    - Appliquer le test du Chi-carré pour calculer :
        - **p-value** : Indique la significativité statistique de la relation.
        - **Cramér’s V** : Mesure l’intensité de l’association entre les deux odeurs.

#### Filtrage des paires significatives

- Conserver uniquement les paires répondant aux critères suivants :
    - **Support** : ≥ 0.05 (5 % des fichiers analysés).
    - **Cramér’s V** : > 0.2 (association modérée ou forte).
- La p-value est incluse à titre de référence pour évaluer la significativité, mais aucun seuil n’est appliqué dans le filtre.

#### Résultats

- **Tri** : Les résultats sont triés par :
    - **Cramér’s V** (décroissant, les relations les plus fortes en premier).
    - **p-value** (croissant, les relations les plus significatives en premier).
- **Script utilisé** : `CodeSmells\RQ2\Scripts\chi_square_cramersv_code_smells.py`
- **Fichier généré** : `CodeSmells\RQ2\data\chi2_results_filtered.xlsx`

---

## 3. Résultats attendus

- Identification des relations fréquentes et significatives entre les odeurs de code.
- Évaluation de l'intensité des relations pour prioriser les problèmes les plus critiques.

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