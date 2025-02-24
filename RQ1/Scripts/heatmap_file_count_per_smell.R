# Installer les bibliothèques nécessaires
if (!require(ggplot2)) install.packages("ggplot2")
if (!require(reshape2)) install.packages("reshape2")
if (!require(dplyr)) install.packages("dplyr")

# Charger les bibliothèques
library(ggplot2)
library(reshape2)
library(dplyr)

# Charger les données du nombre de fichiers par code smell
file_path <- "C:/Users/Brahm/Documents/CodeSmells/RQ1/data/file_count_per_smell.csv"
data <- read.csv(file_path, stringsAsFactors = FALSE)

# Nettoyage des données
colnames(data)[1] <- "Odeur"  # Renommer la première colonne
data <- data %>% 
  mutate(across(-Odeur, ~ as.numeric(.)))  # Convertir les colonnes en valeurs numériques

# Calcul de la médiane pour chaque projet (nombre de fichiers)
medians <- sapply(data[-1], median, na.rm = TRUE)

# Ajustement des données pour commencer la coloration à la médiane
data_color <- data
for (col in names(medians)) {
  median_value <- medians[col]
  data_color[[col]] <- ifelse(data[[col]] >= median_value, data[[col]], NA)  # Conserver les valeurs >= médiane
}

# Transformer les données au format long
heatmap_data <- melt(data, id.vars = "Odeur")  # Données originales pour les textes
heatmap_color_data <- melt(data_color, id.vars = "Odeur")  # Données colorées
colnames(heatmap_data) <- c("Odeur", "Projet", "Nombre_Fichiers")
colnames(heatmap_color_data) <- c("Odeur", "Projet", "Nombre_Fichiers_Color")

# Fusionner les données pour conserver les valeurs originales et colorer conditionnellement
heatmap_combined <- merge(heatmap_data, heatmap_color_data, by = c("Odeur", "Projet"))

# Création de la Heatmap avec Nombre de Fichiers (avec tailles ajustées)
heatmap_plot <- ggplot(heatmap_combined, aes(x = Projet, y = Odeur, fill = Nombre_Fichiers_Color)) +
  geom_tile(color = "white") +
  scale_fill_gradient(low = "white", high = "steelblue", na.value = "white", guide = guide_colorbar(position = "bottom")) +  # Dégradé avec échelle en bas
  geom_text(aes(label = ifelse(!is.na(Nombre_Fichiers), round(Nombre_Fichiers, 0), "")), 
            color = "black", size = 3.6) +  # Texte ajusté à 3.6
  theme_minimal() +
  labs(title = "Nombre de Fichiers par Odeur de Code (par Projet)",
       x = "Projets",
       y = "Odeurs de Code",
       fill = "Nombre de Fichiers") +
  theme(axis.text.x = element_text(angle = 0, hjust = 0.5, size = 11),  # Texte des noms des projets ajusté à 11
        axis.text.y = element_text(size = 11),  # Texte des noms des odeurs ajusté à 11
        legend.position = "bottom",
        legend.key.width = unit(2, "cm"))  # Largeur de la légende

# Afficher le graphique
print(heatmap_plot)
