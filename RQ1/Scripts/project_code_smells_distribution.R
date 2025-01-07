# Charger les bibliothèques nécessaires
library(ggplot2)
library(reshape2)
library(dplyr)

# Lire les données à partir du fichier CSV avec la nouvelle structure
data <- read.csv("C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ1/smell_count_per_project.csv", header = TRUE)

# Transformer les données pour qu'elles soient utilisables pour les graphiques
data_melted <- melt(data, id.vars = c("Project"))

# 1. Violin Plot avec des boxplots à l'intérieur et échelle logarithmique, sans couleur distincte
p <- ggplot(data_melted, aes(x = variable, y = value)) +
  geom_violin(trim = TRUE, scale = "width", fill = "#0073C2", color = "black", adjust = 1, width = 0.9, drop = FALSE) +  # Violins avec couleur unie
  geom_boxplot(width = 0.1, color = "black", alpha = 0.5) +  # Ajouter un boxplot dans les violons
  geom_jitter(color = "black", size = 0.5, alpha = 0.3) +  # Ajout de points pour montrer les valeurs individuelles
  scale_y_continuous(trans = 'log10', breaks = scales::breaks_log(n = 10)) +  # Échelle logarithmique
  labs(title = "Distribution des code smells par type et nombre de fichiers (échelle logarithmique)", 
       x = "Type de smell", 
       y = "Nombre de fichiers (échelle logarithmique)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 0, hjust = 0.5))  # Étiquettes de l'axe X horizontales

# Afficher le graphique
print(p)

# Sauvegarder le graphique
ggsave("violin_plot_with_boxplots_log_scale_single_color.png", plot = p, width = 7, height = 5)
