# Charger les bibliothèques nécessaires
library(ggplot2)
library(reshape2)

# Lire les données à partir du fichier CSV avec la nouvelle structure
data <- read.csv("C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ1/file_count_per_smell.csv", header = TRUE)

# Transformer les données pour qu'elles soient utilisables pour les graphiques
data_melted <- melt(data, id.vars = c("Project"))

# Créer un violin plot avec un boxplot superposé pour montrer la distribution des smells par projet sans échelle logarithmique
ggplot(data_melted, aes(x = variable, y = value)) +
  geom_violin(trim = TRUE, scale = "width", fill = "#0073C2", color = "black", adjust = 1, width = 0.9) +  # Violon plot
  geom_boxplot(width = 0.1, color = "black", outlier.size = 1, alpha = 0.5) +  # Boxplot superposé pour médiane et quartiles
  geom_jitter(color = "black", size = 0.5, alpha = 0.3) +  # Ajout de points pour montrer les valeurs individuelles
  scale_y_continuous(breaks = seq(0, max(data_melted$value, na.rm = TRUE), by = 10)) +  # Ajustement des valeurs sur l'axe Y
  labs(title = "Distribution des fichiers impactés par type de code smell", 
       x = "Type de smell", 
       y = "Nombre de fichiers") +  # Titre et labels mis à jour
  theme_minimal() +  # Utilisation d'un thème minimal
  theme(
    axis.text.x = element_text(angle = 0, vjust = 0.5, hjust = 0.5, margin = margin(t = 10), size = 10),  # Étiquettes de l'axe X horizontales
    axis.line = element_line(color = "black")  # Ligne d'axe noire
  )
