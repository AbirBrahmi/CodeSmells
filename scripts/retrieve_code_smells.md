# Retrieve Code Smells Script

## Introduction
Ce script Python permet de récupérer les "code smells" depuis le serveur SonarQube, de les exporter dans un fichier JSON, puis de convertir ces données en un fichier CSV. Le script prend comme paramètre la clé de projet (par exemple "OrchardCore") et le token d'authentification de SonarQube pour accéder aux rapports. Ce script se lance après l'analyse du projet sur SonarQube.

## Fonctionnalités Principales
- Récupération des "code smells" depuis SonarQube
- Exportation des données dans un fichier JSON
- Conversion des données JSON en fichier CSV

## Utilisation
Pour exécuter ce script, utilisez la commande suivante avec les paramètres nécessaires :
```sh
python retrieve_code_smells.py --project_key "votre_clé_de_projet" --auth_token "votre_token_sonarqube"
