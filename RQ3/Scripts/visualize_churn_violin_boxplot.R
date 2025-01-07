library(ggplot2)
library(dplyr)

# Charger les données
chemin_fichier <- "C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ3/historique_commits_with_indicators.csv"
data <- read.csv(chemin_fichier, header = TRUE)

# Ajouter une colonne pour catégoriser la taille (Small, Medium, Large) basée sur Churn
data$Taille <- cut(data$Churn,
                   breaks = c(-Inf, 50, 500, Inf),
                   labels = c("Petite", "Moyenne", "Grande"))

# Remplacer les zéros dans la colonne 'Churn' par une petite valeur pour éviter les problèmes log10
data <- data %>%
  mutate(Churn = ifelse(Churn <= 0, 0.1, Churn))

# Convertir la colonne Smelly en facteur pour la visualisation
data$Smelly <- factor(data$Smelly, levels = c(0, 1), labels = c("Non-Smelly", "Smelly"))

# ==========================================
# Visualisation par catégorie (Séparée)
# ==========================================

# 1. Filtrer les données pour chaque catégorie
categories <- unique(data$Taille)

for (cat in categories) {
  data_cat <- data[data$Taille == cat, ]
  
  # Créer un graphique en violon pour la catégorie
  p <- ggplot(data_cat, aes(x = Smelly, y = Churn, fill = Smelly)) +
    geom_violin(trim = TRUE, scale = "width", color = "black", adjust = 1, width = 0.9) +  # Graphique en violon
    geom_boxplot(width = 0.1, color = "black", outlier.size = 1, alpha = 0.5) +  # Boxplot superposé
    geom_jitter(color = "black", size = 0.3, alpha = 0.1, width = 0.2) +  # Points superposés
    scale_fill_manual(values = c("#0073C2", "#F39C12")) +  # Couleurs pour Non-Smelly et Smelly
    scale_y_log10(
      breaks = c(10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000),
      labels = scales::comma
    ) +  # Échelle logarithmique avec plus de valeurs
    labs(
      title = paste("Distribution du Churn pour la catégorie :", cat),
      x = "Type de fichier",
      y = "Churn (Volume de modification)",
      fill = "Type de fichier"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
      axis.title.x = element_text(size = 14),
      axis.title.y = element_text(size = 14),
      axis.text.x = element_text(size = 12, vjust = 0.5),  # Étiquettes horizontales
      axis.text.y = element_text(size = 12),
      legend.title = element_text(size = 14),
      legend.text = element_text(size = 12),
      panel.grid.minor = element_blank()  # Supprimer les grilles mineures
    )
  
  # Sauvegarder le graphique pour chaque catégorie
  chemin_sortie <- paste0("C:/Users/Brahm/Documents/CodeSmells/data/StudyCodeSmells/ProcessedData/RQ3/churn_violin_boxplot_", cat, ".png")
  ggsave(
    filename = chemin_sortie,
    plot = p,
    width = 14, height = 8
  )
  
  print(paste("Graphique sauvegardé pour la catégorie :", cat))
}
