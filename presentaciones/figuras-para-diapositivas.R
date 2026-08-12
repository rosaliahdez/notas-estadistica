# ============================================================
#  Genera las figuras de R que usan las diapositivas.
#  Ejecutar desde el proyecto de RStudio:  source("presentaciones/figuras-para-diapositivas.R")
#
#  Las guarda en presentaciones/figuras/ con el mismo nombre que espera el .tex.
#  Ventaja de tener esto como script: las diapositivas son reproducibles.
#  Si cambian los datos o el estilo, se regeneran todas con una línea.
# ============================================================

library(tidyverse)
library(palmerpenguins)

destino <- file.path("presentaciones", "figuras")
dir.create(destino, recursive = TRUE, showWarnings = FALSE)

# Estilo común: fondo transparente y tipografía grande, para que se lea proyectado
tema_diapo <- theme_minimal(base_size = 15) +
  theme(panel.grid.minor = element_blank(),
        plot.background  = element_rect(fill = "transparent", color = NA),
        panel.background = element_rect(fill = "transparent", color = NA))

guardar <- function(nombre, grafica, ancho = 6.5, alto = 4) {
  ggsave(file.path(destino, nombre), grafica,
         width = ancho, height = alto, dpi = 300, bg = "transparent")
  cat("  generada:", nombre, "\n")
}

azul <- "#1F4E79"

cat("Generando figuras para las diapositivas...\n")

# ---- 1. Barras: cuántos pingüinos por especie (variable categórica) ----
g1 <- ggplot(penguins, aes(x = species)) +
  geom_bar(fill = azul) +
  labs(x = "Especie", y = "Cantidad") +
  tema_diapo
guardar("r-barras-especie.png", g1)

# ---- 2. Histograma de la masa corporal (variable cuantitativa) ----
g2 <- ggplot(penguins, aes(x = body_mass_g)) +
  geom_histogram(binwidth = 250, fill = azul, color = "white") +
  labs(x = "Masa corporal (g)", y = "Cantidad") +
  tema_diapo
guardar("r-histograma-masa.png", g2)

# ---- 3. El mismo histograma separado por especie: de dónde viene la bimodalidad ----
g3 <- ggplot(penguins, aes(x = body_mass_g, fill = species)) +
  geom_histogram(binwidth = 250, alpha = 0.75, position = "identity") +
  labs(x = "Masa corporal (g)", y = "Cantidad", fill = "Especie") +
  tema_diapo
guardar("r-histograma-especie.png", g3, ancho = 7)

# ---- 4. El ancho de clase cambia la historia: tres versiones, una por archivo ----
# Se guardan por separado para poder mostrarlas una tras otra en la clase.
for (a in c(100, 250, 800)) {
  g <- ggplot(drop_na(penguins, body_mass_g), aes(x = body_mass_g)) +
    geom_histogram(binwidth = a, fill = azul, color = "white") +
    labs(title = paste("ancho de clase =", a, "g"),
         x = "Masa corporal (g)", y = "Cantidad") +
    tema_diapo
  guardar(paste0("r-ancho-", a, ".png"), g, ancho = 5.2, alto = 3.6)
}

# ---- 5. Mapa del archipiélago Palmer con las coordenadas publicadas ----
# Coordenadas tomadas de Gorman, Williams y Fraser (2014), PLoS ONE 9(3):e90081,
# sección Field methods. Se convierten de grados y minutos a grados decimales.
gm <- function(g, m) g + m/60          # devuelve grados decimales

naranja <- "#E8871E"   # para la estación, que debe distinguirse de las islas

# Torgersen y la estación Palmer están a menos de un kilómetro una de otra,
# así que sus etiquetas se dirigen en sentidos opuestos para que no se traslapen.
sitios <- data.frame(
  nombre = c("Biscoe", "Torgersen", "Dream", "Estación Palmer"),
  lat    = -c(gm(64,48), gm(64,46), gm(64,43), gm(64,46)),   # sur = negativo
  lon    = -c(gm(63,46), gm(64, 4), gm(64,13), gm(64, 3)),   # oeste = negativo
  tipo   = c("Isla de estudio", "Isla de estudio", "Isla de estudio", "Estación Palmer"),
  etiq   = c("Biscoe\n(Juanito y Adelia)", "Torgersen\n(Adelia)",
             "Dream\n(Barbijo y Adelia)", "Estación Palmer\n(isla Anvers)"),
  dx     = c( 0.000, -0.015,  0.000,  0.022),   # desplazamiento de la etiqueta
  dy     = c( 0.016, -0.022,  0.016,  0.020),
  hj     = c( 0.5,    1.0,    0.5,    0.0)      # alineación horizontal
)

g6 <- ggplot(sitios, aes(x = lon, y = lat)) +
  # línea que une la estación con Torgersen, para que se lea que están juntas
  annotate("segment", x = -gm(64,4), xend = -gm(64,3),
           y = -gm(64,46), yend = -gm(64,46),
           color = "#B4B2A9", linewidth = 0.4) +
  geom_point(aes(color = tipo, shape = tipo, size = tipo)) +
  geom_text(aes(x = lon + dx, y = lat + dy, label = etiq, hjust = hj, color = tipo),
            size = 3.3, lineheight = 0.95, show.legend = FALSE) +
  scale_color_manual(values = c("Isla de estudio" = azul, "Estación Palmer" = naranja)) +
  scale_shape_manual(values = c("Isla de estudio" = 16, "Estación Palmer" = 17)) +
  scale_size_manual(values = c("Isla de estudio" = 4, "Estación Palmer" = 5)) +
  scale_x_continuous(labels = function(x) sprintf("%.1f°O", abs(x))) +
  scale_y_continuous(labels = function(y) sprintf("%.2f°S", abs(y))) +
  coord_cartesian(xlim = c(-64.34, -63.66), ylim = c(-64.84, -64.66), clip = "off") +
  labs(x = "Longitud oeste", y = "Latitud sur",
       color = NULL, shape = NULL, size = NULL) +
  tema_diapo +
  theme(legend.position = "bottom",
        legend.margin = margin(t = -4, b = 0),
        plot.margin = margin(t = 6, r = 14, b = 2, l = 6))
# --- Recuadro de ubicación con el continente antártico ---------------------
# A la escala del mapa principal (unos 30 km de ancho) la Península Antártica
# no cabe: si se aleja lo suficiente para verla, las islas se vuelven un punto.
# La solución es un recuadro de ubicación. Requiere dos paquetes:
#     install.packages(c("sf", "rnaturalearth"))
# Si no están instalados, se guarda el mapa sin recuadro y no pasa nada.

hay_mapas <- requireNamespace("sf", quietly = TRUE) &&
             requireNamespace("rnaturalearth", quietly = TRUE)

if (hay_mapas) {
  suppressPackageStartupMessages({library(sf); library(rnaturalearth)})
  antartida <- ne_countries(continent = "Antarctica", scale = "medium",
                            returnclass = "sf")

  ubicacion <- ggplot() +
    geom_sf(data = antartida, fill = "#EDEAE3", color = "#9A9A9A", linewidth = 0.25) +
    annotate("point", x = -64.05, y = -64.77, color = naranja, size = 2.6) +
    annotate("text", x = -64.05, y = -70.5, label = "zona de\nestudio",
             color = naranja, size = 2.5, lineheight = 0.9) +
    coord_sf(expand = FALSE) +
    theme_void() +
    theme(panel.background = element_rect(fill = "#F7FAFD", color = "#B4B2A9",
                                          linewidth = 0.4),
          plot.background = element_rect(fill = "transparent", color = NA))

  g6b <- g6 + annotation_custom(ggplotGrob(ubicacion),
                                xmin = -64.34, xmax = -64.14,
                                ymin = -64.845, ymax = -64.755)
  guardar("r-mapa-palmer.png", g6b, ancho = 8.2, alto = 4.2)
  cat("  (con recuadro de ubicación del continente)\n")
} else {
  guardar("r-mapa-palmer.png", g6, ancho = 8.2, alto = 4.2)
  cat("  (sin recuadro: para añadirlo, install.packages(c('sf','rnaturalearth')))\n")
}

# ---- 6. Boxplot comparativo, para la sesión 2 ----
g5 <- ggplot(drop_na(penguins, body_mass_g),
             aes(x = species, y = body_mass_g, fill = species)) +
  geom_boxplot() +
  labs(x = "Especie", y = "Masa corporal (g)") +
  tema_diapo + theme(legend.position = "none")
guardar("r-boxplot-especie.png", g5)

cat("\nListo. Las figuras están en", destino, "\n")
cat("Las diapositivas las usan automáticamente si están presentes.\n")
