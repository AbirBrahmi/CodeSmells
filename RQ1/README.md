# Méthodologie de l'étude RQ1

L'objectif principal de cette étape est d'analyser la prévalence des odeurs de code dans divers projets logiciels .NET. Cette analyse vise à identifier les types d'odeurs les plus courants.

## 1. Collecte des données

Les données ont été collectées à partir des rapports d'analyse générés pour chaque projet. Les éléments suivants ont été extraits :

### 1.1 Nombre total de fichiers pour chaque type d'odeur de code (par projet)

Cette mesure est cruciale pour déterminer la présence et l'étendue des odeurs de code au sein de chaque projet. En quantifiant le nombre de fichiers associés à chaque type d'odeur, il est possible d'évaluer la prévalence relative des odeurs dans les projets analysés.

- **Script lancé pour cette étape :**
  ```
  CodeSmells\scripts\RQ1\count_file_per_smell.py
  ```

- **Fichier généré :**
  ```
  CodeSmells\scripts\RQ1\file_count_per_smell.csv
  ```

**Exemple de fichier généré :**

| Smell                  | Blog.Core | NETworkMan | PixiEditor | Seal-Report | Terminal.Gui | boletonet | drywetmidi | fo-dicom | greenshot | mpv.net |
|------------------------|-----------|------------|------------|-------------|--------------|-----------|------------|----------|-----------|---------|
| Unutilized Abstraction | 134       | 9          | 7          | 31          | 2            | 15        | 51         | 44       | 26        | 19      |
| Unnecessary Abstraction| 92        | 0          | 0          | 41          | 0            | 13        | 48         | 16       | 69        | 4       |
| Duplicate Abstraction  | 17        | 4          | 1          | 14          | 0            | 32        | 30         | 19       | 39        | 4       |

---

### 1.2 Occurrences de chaque type d'odeur de code

Pour chaque fichier, les données concernant le nombre d'occurrences de chaque odeur ont été rassemblées. Cela permet d'évaluer la fréquence avec laquelle chaque odeur apparaît, fournissant ainsi un aperçu de leur impact dans les projets étudiés.

- **Script lancé pour cette étape :**
  ```
  CodeSmells\scripts\RQ1\smell_count_per_project.py
  ```

- **Fichier généré :**
  ```
  CodeSmells\RQ1\data\smell_count_per_project.csv
  ```

**Exemple de fichier généré :**

| Smell                  | Blog.Core | NETworkMan | PixiEditor | Seal-Report | Terminal.Gui | boletonet | drywetmidi | fo-dicom | greenshot | mpv.net |
|------------------------|-----------|------------|------------|-------------|--------------|-----------|------------|----------|-----------|---------|
| Broken Hierarchy       | 15        | 0          | 0          | 20          | 0            | 8         | 20         | 23       | 11        | 0       |
| Broken Modularization  | 58        | 0          | 0          | 24          | 0            | 8         | 24         | 1        | 35        | 15      |
| Complex Conditional    | 5         | 0          | 0          | 111         | 0            | 22        | 7          | 13       | 25        | 0       |

---

### 1.3 Densité des odeurs par KLOC (mille lignes de code)

Le script gère deux fichiers CSV :

- **Nombre total d'occurrences des odeurs de code par fichier**
- **Densité des odeurs par mille lignes de code (KLOC)** pour chaque fichier

Ces fichiers permettent d'analyser à la fois la fréquence des odeurs de code et leur concentration relative, facilitant ainsi l'identification des fichiers critiques nécessitant une refactorisation.

- **Formule utilisée :**

$$
\text{Densité par KLOC} = \left( \frac{\text{Nombre d'odeurs de code dans le fichier}}{\text{Taille du fichier en lignes de code}} \right) \times 1000
$$

- **Script lancé pour cette étape :**
  ```
  CodeSmells\scripts\RQ1\count_density_per_file.py
  ```

- **Fichiers générés :**
  ```
  CodeSmells\RQ1\data\smell_count_per_file.csv
  CodeSmells\RQ1\data\density_counts_per_file.csv
  ```

**Exemple de fichier généré :**

| Project   | File          | D-BH      | D-BM      | I-CC | ... | I-LPL    | I-LS     | I-MN    |
|-----------|---------------|-----------|-----------|------|-----|----------|----------|---------|
| Blog.Core | C:\Users\ATC | 0         | 0         | 0    | ... | 11.36364 | 17.98561 | 21.58273|
| Blog.Core | C:\Users\ATC | 3.5971223 | 3.5971223 | 0    | ... | 67.03910 | 38.99721 | 2.78551 |

---
### 2. Calcul des Statistiques par projet

#### 2.1 Résumé Statistique et Quantification des Odeurs de Code par Projet

Un tableau récapitulatif des métriques liées aux odeurs de code dans plusieurs projets logiciels est généré. Ces statistiques incluent :

1. **Nombre Total d'Odeurs par Projet**  
   Nombre total d'occurrences des odeurs de code dans chaque projet.

   $$
   \text{Total Odeurs} = \sum \text{Occurrences des odeurs pour chaque projet}
   $$

2. **Nombre de Fichiers Affectés par Projet**  
   Nombre unique de fichiers touchés par au moins une odeur dans chaque projet.

   $$
   \text{Fichiers Affectés} = \text{Nombre unique de fichiers contenant des odeurs}
   $$

3. **Nombre Total de Fichiers par Projet**  
   Nombre total de fichiers dans chaque projet, qu’ils soient affectés ou non par des odeurs.

   $$
   \text{Total Fichiers} = \text{Nombre unique de fichiers dans le projet}
   $$

4. **Pourcentage de Fichiers Affectés par Projet**  
   Proportion de fichiers contenant des odeurs par rapport au total des fichiers dans le projet.

   $$
   \% \text{Fichiers Affectés} = \left( \frac{\text{Fichiers Affectés}}{\text{Total Fichiers}} \right) \times 100
   $$

5. **Densité des Odeurs par KLOC (mille lignes de code)**  
   Nombre d’odeurs rapporté à 1 000 lignes de code (KLOC) pour chaque fichier. La densité est calculée au niveau des fichiers, puis la moyenne est prise par projet.

   - **Formule (par fichier) :**

     $$
     \text{Densité Odeurs par KLOC} = \left( \frac{\text{Nombre d'Odeurs}}{\text{Nombre de Lignes de Code}} \right) \times 1000
     $$

   - **Formule (par projet) :**

     $$
     \text{Densité Moyenne (par projet)} = \frac{\sum \text{Densité des fichiers du projet}}{\text{Nombre total de fichiers}}
     $$

- **Script utilisé pour générer ces métriques :**

  ```
  CodeSmells\RQ1\Scripts\generate_summary_statistics.py
  ```

- **Fichier généré :**

  ```
  CodeSmells\RQ1\data\project_smell_summary_statistics.csv
  ```

#### Exemple de Résumé des Règles

| Métrique                | Formule/Calcul                                      |
|-------------------------|-----------------------------------------------------|
| **Total Odeurs**        | Somme des occurrences des odeurs pour chaque projet |
| **Fichiers Affectés**   | Nombre unique de fichiers touchés par des odeurs    |
| **Total Fichiers**      | Nombre unique de fichiers (affectés ou non)         |
| **% Fichiers Affectés** | $(Fichiers Affectés / Total Fichiers) \times 100$   |
| **Densité Odeurs/KLOC** | $(Nombre d'Odeurs / Lignes de Code) \times 1000$   |
| **Densité Moyenne**     | Moyenne des densités des fichiers d'un projet       |

#### Exemple de Données

| Project       | Total Odeurs | Fichiers Affectés | Total Fichiers | % Fichiers Affectés | Densité Moyenne (Odeurs/KLOC) |
|---------------|--------------|-------------------|----------------|---------------------|-----------------------------|
| Blog.Core     | 1151         | 296               | 536            | 55.22               | 87.45                      |
| NETworkMan    | 33           | 8                 | 892            | 1.01                | 50.29                      |
| PixiEditor    | 12           | 7                 | 2212           | 0.31                | 33.84                      |
| Seal-Report   | 6300         | 246               | 493            | 49.89               | 233.05                     |
| Terminal.Gui  | 7            | 2                 | 710            | 0.28                | 6.92                       |
| boletonet     | 10732        | 185               | 295            | 62.71               | 307.75                     |
| drywetmidi    | 1407         | 363               | 818            | 44.38               | 57.73                      |
| fo-dicom      | 4373         | 251               | 1167           | 21.51               | 2645.51                    |
| greenshot     | 4010         | 314               | 589            | 53.31               | 394.73                     |
| mpv.net       | 204          | 32                | 220            | 14.55               | 56.25                      |
| ...           | ...          | ...               | ...            | ...                 | ...                        |

### 2.2 Prévalence relative par projet

La prévalence mesure la proportion de fichiers affectés par chaque type d'odeur par rapport au total des fichiers d'un projet.

$$
\text{Prévalence par smell (\%)} = \left( \frac{\text{Nombre de fichiers affectés par une odeur}}{\text{Nombre total de fichiers dans le projet}} \right) \times 100
$$

### 2.3 Fréquence par projet

La fréquence mesure la proportion d'occurrences d'un type de smell parmi toutes les occurrences d'odeurs de code dans un projet spécifique.

$$
\text{Fréquence (\%)} = \left( \frac{\text{Occurrences d’un smell dans un projet}}{\text{Total des occurrences de tous les smells dans ce projet}} \right) \times 100
$$

- **Script utilisé :**

  ```
  CodeSmells\RQ1\Scripts\prevalence_frequency_by_project.py
  ```

- **Fichiers de sortie :**

  ```
  CodeSmells\RQ1\data\frequency_by_project.csv
  CodeSmells\RQ1\data\prevalence_by_project.csv
  ```
### 3. Calcul des Statistiques globales entre projets

Les statistiques des odeurs de code ont été calculées en utilisant les données collectées. Les étapes suivantes ont été suivies :

#### Chargement des Données

Les données ont été importées à partir d'un fichier CSV contenant des informations sur les odeurs de code.

#### Calcul des Statistiques :

##### 3.1 Prévalence des odeurs de code

La prévalence mesure la distribution des odeurs de code dans les projets et les fichiers analysés. Elle est évaluée à l’aide de deux indicateurs :

- **% dans les projets**

  $$
  \% \text{dans les projets} = \left( \frac{\text{Nombre de projets contenant l’odeur}}{\text{Nombre total de projets analysés}} \right) \times 100
  $$

  Cet indicateur représente la proportion de projets dans lesquels une odeur de code spécifique est détectée. Cette mesure permet d’identifier les odeurs de code les plus répandues à travers les différents projets.

- **% dans les fichiers affectés**

  $$
  \% \text{dans les fichiers affectés} = \left( \frac{\text{Nombre de fichiers contenant l’odeur}}{\text{Nombre total de fichiers analysés}} \right) \times 100
  $$

  Cet indicateur correspond à la proportion de fichiers contenant une odeur spécifique par rapport à l’ensemble des fichiers analysés. La règle appliquée est :

##### 3.2 Fréquence des odeurs de code

- **% du total des odeurs**

  La fréquence mesure l’intensité des odeurs de code, c’est-à-dire le volume total d’apparitions d’une odeur par rapport à l’ensemble des odeurs détectées. Elle est calculée à l’aide de la règle suivante :

  $$
  \% \text{du total des odeurs} = \left( \frac{\text{Nombre total d’occurrences de l’odeur}}{\text{Nombre total d’occurrences de toutes les odeurs}} \right) \times 100
  $$

- **Script utilisé :**

  ```
  CodeSmells\RQ1\Scripts\prevalence_frequency_for_all_projects.py
  ```

- **Fichier de sortie :**

  ```
  CodeSmells\RQ1\data\prevalence_frequency_for_all_projects
  ```

### 4. Visualisations Graphiques

Pour faciliter l'interprétation des résultats, plusieurs types de visualisations graphiques ont été élaborés :

- **Distribution du Nombre d’Odeurs dans Tous les Projets pour Chaque Type de Smell** :

  Ce diagramme illustre la répartition du nombre total d'odeurs de code pour chaque type d'odeur à travers l'ensemble des projets.

  - **Script utilisé pour cette étape :**

    ```
    CodeSmells\scripts\RQ1\project_code_smells_distribution.R
    ```

- **Distribution du Nombre de Fichiers Affectés par Chaque Type d'Odeur** :

  Ce graphique montre combien de fichiers sont affectés par chaque type d'odeur de code.

  - **Script utilisé pour cette étape :**

    ```
    CodeSmells\scripts\RQ1\project_code_smells_file_distribution.R
    ```

- **Distribution de la Densité des Odeurs par KLOC** :

  Ce diagramme visualise la densité des odeurs de code par mille lignes de code, permettant de repérer les fichiers où la concentration d'odeurs est la plus élevée.

  - **Script utilisé pour cette étape :**

    ```
    CodeSmells\scripts\RQ1\project_code_smells_KLOC_distribution.R
    ```


---

## Références
- **Documentation des questions de recherche** :
  - [README_ProjectOverview](./README.md)
  - [Common_Raw_Data Documentation](./Common_Raw_Data/README_CommonRawData)
  - [Common_Scripts Documentation](./Common_Scripts/README_CommonScripts)
  - [GitHub_Total_Extraction Documentation](./GitHub_Total_Extraction/README.md)
  - [RQ1 Documentation](./RQ1/README.md)
  - [RQ2 Documentation](./RQ2/README.md)
  - [RQ3 Documentation](./RQ3/README.md)
  - [RQ4 Documentation](./RQ4/README.md)

---