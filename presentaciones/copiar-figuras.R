# ============================================================
#  Copia las ilustraciones de palmerpenguins a presentaciones/figuras/
#  Ejecutar una sola vez, desde el proyecto de RStudio.
#
#  Las ilustraciones son de Allison Horst y su uso para enseñanza está
#  permitido con el crédito: "Artwork by @allison_horst".
#  Fuente: https://allisonhorst.github.io/palmerpenguins/articles/art.html
# ============================================================

if (!requireNamespace("palmerpenguins", quietly = TRUE)) {
  stop("Primero instalar el paquete:  install.packages('palmerpenguins')")
}

destino <- file.path("presentaciones", "figuras")
dir.create(destino, recursive = TRUE, showWarnings = FALSE)

# Buscar todas las imágenes que trae el paquete instalado
raiz <- system.file(package = "palmerpenguins")
imagenes <- list.files(raiz, pattern = "\\.(png|jpg)$",
                       recursive = TRUE, full.names = TRUE)

if (length(imagenes) == 0) {
  cat("No se encontraron imágenes dentro del paquete instalado.\n",
      "Descargarlas manualmente desde:\n",
      "  https://github.com/allisonhorst/palmerpenguins/tree/main/man/figures\n",
      "y guardarlas en", destino, "\n")
} else {
  file.copy(imagenes, destino, overwrite = TRUE)
  cat("Copiadas", length(imagenes), "imágenes a", destino, "\n\n")
  print(basename(imagenes))
  cat("\nLas que usan las diapositivas son:\n",
      "  lter_penguins.png   (las tres especies)\n",
      "  culmen_depth.png    (dimensiones del pico)\n",
      "  palmerpenguins.png  (logotipo)\n")
}

# Si alguna faltara, se puede descargar directamente así:
#
# base <- "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/man/figures/"
# for (f in c("lter_penguins.png", "culmen_depth.png", "palmerpenguins.png")) {
#   download.file(paste0(base, f), file.path(destino, f), mode = "wb")
# }
