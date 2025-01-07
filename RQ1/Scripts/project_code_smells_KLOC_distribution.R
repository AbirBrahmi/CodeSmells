# Installer les bibliothèques nécessaires
if (!require(ggplot2)) install.packages("ggplot2")
if (!require(reshape2)) install.packages("reshape2")
if (!require(dplyr)) install.packages("dplyr")

# Charger les bibliothèques
library(ggplot2)
library(reshape2)
library(dplyr)

# Lire les données à partir du fichier CSV
file_path <- "C:/Users/Brahm/Documents/CodeSmells/RQ1/data/density_counts_per_file_with_abbr.csv"
data <- read.csv(file_path, header = TRUE)

# Transformer les données pour qu'elles soient utilisables pour les graphiques
data_melted <- melt(data, id.vars = c("Project", "File"))

# Convertir les valeurs en numériques et gérer les NA
data_melted$value <- as.numeric(as.character(data_melted$value))

# Filtrer pour garder les valeurs positives (si nécessaire)
data_melted <- data_melted %>%
  filter(value > 0)  # Garde seulement les valeurs positives

# Créer un Violin Plot avec couleur steelblue
p <- ggplot(data_melted, aes(x = variable, y = value)) +
  geom_violin(trim = TRUE, scale = "width", fill = "steelblue", color = "black", adjust = 1, width = 0.9) +  # Appliquer steelblue
  geom_boxplot(width = 0.1, color = "black", outlier.size = 1, alpha = 0.5) +  # Boxplot superposé
  geom_jitter(color = "black", size = 0.5, alpha = 0.3) +  # Points pour montrer les valeurs individuelles
  scale_y_continuous(trans = 'log10', 
                     breaks = scales::trans_breaks("log10", function(x) 10^x),
                     labels = scales::label_number(accuracy = 1),  # Affichage des valeurs comme des entiers
                     limits = c(1, NA)) +  # Forcer la limite basse à 1 pour éviter les valeurs négatives
  labs(title = "Distribution des densités de code smells par type et par KLOC (échelle logarithmique)", 
       x = "Type de smell", 
       y = "Densité par KLOC") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 0, hjust = 0.5), 
        axis.title.y = element_text(size = 12),
        axis.title.x = element_text(size = 12))

# Afficher le graphique
print(p)

# Sauvegarder le graphique
ggsave("violin_density_color_gradient.png", plot = p, width = 5.4, height = 4.39)
