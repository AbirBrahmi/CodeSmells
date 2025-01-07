# Méthodologie de l'Étude RQ4

## Objectif

Cette étape de l’étude se concentre sur l'analyse de l'impact des odeurs de code (**code smells**) et de la taille des fichiers sur la propension des projets .NET aux défauts.  
En étudiant des métriques telles que le **churn** et le temps de propagation des défauts, l'objectif est de comprendre comment ces facteurs influencent la survenue et la gestion des défauts dans le code.

---

## Étape 1 : Identification des **Defect-Fixing Commits (DFC)**

### Script utilisé :

```
CodeSmells\RQ4\scripts\identify_dfcs.py
```

- **Fonctionnalité** :
    - Analyse un fichier CSV contenant des informations sur les commits.
    - Identifie et filtre les commits de correction de défauts (**DFC**) en recherchant des mots-clés spécifiques dans les messages de commit (ex : "error", "bug", "fix").
    - Sauvegarde les DFC pertinents dans un nouveau fichier CSV pour une analyse plus ciblée.

---

## Étape 2 : Identification des **Defect-Introducing Commits (DIC)**

### Script utilisé :

```
CodeSmells\RQ4\scripts\detect_dic.py
```

- **Fonctionnalité** :
    - Identifie les commits d'introduction des défauts (**DIC**) associés aux **DFC**.
    - Analyse un fichier CSV d'entrée pour établir le lien entre DFC et DIC.

---

## Étape 3 : Classification des fichiers selon les odeurs de code

### Script utilisé :

```
CodeSmells\RQ4\scripts\detect_smelly_commits.py
```

- **Fonctionnalité** :
    - Enrichit un fichier CSV contenant des données sur les **DFC** et les **DIC**.
    - Classe les fichiers en "smelly" (avec odeurs de code) ou "non-smelly".
    - Calcule des métriques supplémentaires comme le **churn** (lignes ajoutées + supprimées).
    - Compte le nombre total de commits impactant chaque fichier.

---

## Étape 4 : Fusion et enrichissement des données

### Script utilisé :

```
CodeSmells\RQ4\scripts\fusion_enrichissement_dfcs_dics.py
```

- **Fonctionnalité** :
    - Enrichit un fichier CSV contenant les informations sur les **DFC** et les **DIC**.
    - Calcule le temps de propagation des défauts (en jours) en comparant les dates des **DFC** et des **DIC**.
    - Corrige les valeurs invalides (comme les temps négatifs).
    - Classe les fichiers en catégories de taille ("Small", "Medium", "Large") basées sur les lignes de code (**LOC**).
    - Sauvegarde les données enrichies dans un nouveau fichier CSV pour des analyses approfondies.

---

## Résultat : Structure du fichier final

Le fichier final (`dfcs_dics_enrichi_final.csv`) contient les colonnes suivantes :

|**Colonne**|**Description**|
|---|---|
|`DFC_Commit`|Identifiant du commit de correction du défaut (**Defect-Fixing Commit**).|
|`DFC_File_Path`|Chemin du fichier modifié dans le DFC.|
|`DFC_Date`|Date du commit DFC.|
|`DFC_LOC`|Nombre de lignes de code dans le fichier lié au DFC.|
|`DIC_Commit`|Identifiant du commit d'introduction du défaut (**Defect-Introducing Commit**).|
|`DIC_File_Path`|Chemin du fichier modifié dans le DIC.|
|`DIC_LOC`|Nombre de lignes de code dans le fichier lié au DIC.|
|`DIC_Date`|Date du commit DIC.|
|`Lines_Added_DFC`|Nombre de lignes ajoutées dans le DFC.|
|`Lines_Deleted_DFC`|Nombre de lignes supprimées dans le DFC.|
|`Smelly_Flag_DFC`|Indicateur binaire (1 : fichier avec odeurs de code dans le DFC, 0 : sans odeurs).|
|`Files_Modified_DIC`|Nombre de fichiers modifiés dans le DIC.|
|`Lines_Added_DIC`|Nombre de lignes ajoutées dans le DIC.|
|`Lines_Deleted_DIC`|Nombre de lignes supprimées dans le DIC.|
|`Smelly_Flag_DIC`|Indicateur binaire (1 : fichier avec odeurs de code dans le DIC, 0 : sans odeurs).|
|`Churn_DFC`|Volume total des modifications (lignes ajoutées + supprimées) dans le DFC.|
|`Churn_DIC`|Volume total des modifications (lignes ajoutées + supprimées) dans le DIC.|
|`Defect_Propagation_Time`|Temps de propagation des défauts entre le DIC et le DFC (en jours).|
|`File_Size_Category`|Catégorie de taille du fichier dans le DFC (`Small`, `Medium`, `Large`).|


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