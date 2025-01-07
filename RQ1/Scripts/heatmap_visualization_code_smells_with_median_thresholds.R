# Installer les bibliothèques nécessaires si elles ne sont pas déjà installées
if (!require(ggplot2)) install.packages("ggplot2")
if (!require(reshape2)) install.packages("reshape2")
if (!require(dplyr)) install.packages("dplyr")

# Charger les bibliothèques
library(ggplot2)
library(reshape2)
library(dplyr)

# Charger les données du fichier de sortie du script précédent (fichier CSV)
file_path <- "C:/Users/Brahm/Documents/CodeSmells/RQ1/data/classified_smells_per_project_median.csv"
data <- read.csv(file_path, stringsAsFactors = FALSE)

# Nettoyage des données : Renommer la première colonne (Odeur)
colnames(data)[1] <- "Odeur"
data <- data %>% 
  mutate(across(-Odeur, ~ as.character(.)))  # Convertir les valeurs en caractères

# Transformer les données au format long pour créer la heatmap avec 'melt'
heatmap_data <- melt(data, id.vars = "Odeur")
colnames(heatmap_data) <- c("Odeur", "Projet", "Classification")

# Définir des couleurs descriptives pour les classifications
classification_colors <- c("HPHF" = "#1f77b4",  # Bleu foncé (High Prevalence & High Frequency)
                           "HPLF" = "#ff7f0e",  # Orange (High Prevalence & Low Frequency)
                           "LPHF" = "#2ca02c",  # Vert foncé (Low Prevalence & High Frequency)
                           "LPLF" = "#7f7f7f")  # Gris clair (Low Prevalence & Low Frequency)

# Créer la heatmap avec des couleurs descriptives pour les classifications des odeurs de code
heatmap_plot <- ggplot(heatmap_data, aes(x = Projet, y = Odeur, fill = Classification)) +
  geom_tile(color = "white") +
  scale_fill_manual(values = classification_colors, na.value = "white") +  # Couleurs selon les classifications
  geom_text(aes(label = Classification), color = "black", size = 3) +  # Afficher les classifications dans chaque case
  theme_minimal() +
  labs(title = "Classification des Odeurs de Code par Projet",
       x = "Projets",
       y = "Odeurs de Code",
       fill = "Classification") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10),  # Ajuster l'angle et la taille du texte des projets
        axis.text.y = element_text(size = 10),  # Ajuster la taille du texte des odeurs
        legend.position = "top")  # Position de la légende

# Afficher la heatmap
print(heatmap_plot)
