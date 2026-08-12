# ============================================================
#  Generador de datos simulados - Curso de Estadistica (LCC)
#  Universidad de Sonora
#
#  Modelo generativo de las bases de respaldo del curso. Al correrlo
#  en R produce una realizacion equivalente (misma estructura y mismos
#  resultados esperados) a los CSV incluidos. Ajusta los parametros de
#  cada bloque para adaptar dificultad, tamanos o efectos.
#
#  Uso:  source("generar_datos.R")   # crea la carpeta ./datos_simulados
#  Analisis sugerido de cada base: ver DICCIONARIO_DATOS.md
# ============================================================

set.seed(2026)
dir.create("datos_simulados", showWarnings = FALSE)
clamp <- function(x, lo, hi) pmin(pmax(x, lo), hi)

# ---------- 1. GALLETAS: ANOVA de un factor (cata a ciegas) ----------
marcas <- c("Oreo", "Chokis", "Lors", "GreatValue")
base   <- c(Oreo = 7.3, Chokis = 6.6, Lors = 5.8, GreatValue = 5.4)
nj <- 25
galletas <- do.call(rbind, lapply(1:nj, function(j) {
  juez_eff <- rnorm(1, 0, 0.6)                 # unos jueces califican mas alto
  orden    <- sample(marcas)                   # orden de cata balanceado por juez
  data.frame(
    juez  = j,
    orden = 1:4,
    marca = orden,
    agrado = sapply(1:4, function(pos) {
      fatiga <- -0.12 * (pos - 1)              # cansancio de paladar
      val <- base[[orden[pos]]] + juez_eff + fatiga + rnorm(1, 0, 1.0)
      as.integer(clamp(round(val), 1, 9))
    })
  )
}))
write.csv(galletas, "datos_simulados/galletas.csv", row.names = FALSE)
# Analisis:  aov(agrado ~ marca, galletas); TukeyHSD(...); shapiro/leveneTest

# ---------- 2. LAGARTIJAS: comparacion de dos grupos ----------
lz <- function(n, hab, temp, s_temp, masa, s_masa, lhc, s_lhc, fc, s_fc) {
  data.frame(
    id            = sprintf("%s%02d", toupper(substr(hab, 1, 1)), 1:n),
    habitat       = hab,
    temp_corporal = round(rnorm(n, temp, s_temp), 1),
    masa_g        = round(rnorm(n, masa, s_masa), 1),
    lhc_mm        = round(rnorm(n, lhc,  s_lhc), 1),
    frec_cardiaca = as.integer(round(rnorm(n, fc, s_fc)))
  )
}
lagartijas <- rbind(
  lz(32, "urbana", 35.3, 1.4, 14.5, 3.0, 62, 5.0, 88, 10),  # urbana: mas calida y variable
  lz(30, "campo",  33.9, 1.2, 12.8, 2.6, 62, 5.0, 80,  9)
)
write.csv(lagartijas, "datos_simulados/lagartijas.csv", row.names = FALSE)
# Analisis:  t.test(temp_corporal ~ habitat); t.test(lhc_mm ~ habitat) [no difiere];
#            var.test(temp_corporal ~ habitat)  [complemento MCD]

# ---------- 3. RICKETTSIOSIS: proporciones y ji-cuadrada ----------
expit <- function(x) 1 / (1 + exp(-x))
zonas <- sample(c(rep("urbana_marginada", 180), rep("urbana", 140), rep("rural", 100)))
p_perro <- c(urbana_marginada = 0.75, urbana = 0.50, rural = 0.80)
contacto   <- runif(length(zonas)) < p_perro[zonas]
garrapatas <- runif(length(zonas)) < ifelse(contacto, 0.55, 0.20)
lin <- -2.6 + 1.1 * contacto + 1.0 * garrapatas + 0.5 * (zonas == "urbana_marginada")
positivo <- runif(length(zonas)) < expit(lin)
rickettsiosis <- data.frame(
  id = sprintf("P%03d", seq_along(zonas)),
  zona = zonas,
  contacto_perro = ifelse(contacto, "si", "no"),
  garrapatas     = ifelse(garrapatas, "si", "no"),
  resultado      = ifelse(positivo, "positivo", "negativo")
)
write.csv(rickettsiosis, "datos_simulados/rickettsiosis.csv", row.names = FALSE)
# Analisis:  chisq.test(table(contacto_perro, resultado));
#            prop.test(...) diferencia de proporciones por zona

# ---------- 4a. ALGORITMOS - REGRESION (tiempo ~ tamano) ----------
sizes <- rep(seq(1000, 10000, by = 1000), each = 5)     # 10 tamanos x 5 replicas
par_ent <- list(Mac = c(1.5, 0.00170, 1.5), Windows = c(2.2, 0.00195, 1.7))
alg <- do.call(rbind, lapply(names(par_ent), function(ent) {
  p <- par_ent[[ent]]
  data.frame(entorno = ent, n = as.integer(sizes),
             tiempo_ms = round(pmax(p[1] + p[2]*sizes + 1e-8*sizes^2 + rnorm(length(sizes), 0, p[3]), 0.1), 2))
}))
write.csv(alg, "datos_simulados/algoritmos_regresion.csv", row.names = FALSE)
# Analisis:  lm(tiempo_ms ~ n, subset = entorno=="Mac"); plot de residuales

# ---------- 4b. ALGORITMOS - A/B (dos muestras, n fijo = 5000) ----------
ab <- do.call(rbind, lapply(names(par_ent), function(ent) {
  p <- par_ent[[ent]]
  data.frame(entorno = ent, corrida = 1:30,
             tiempo_ms = round(pmax(p[1] + p[2]*5000 + 1e-8*5000^2 + rnorm(30, 0, p[3]), 0.1), 2))
}))
write.csv(ab, "datos_simulados/algoritmos_ab.csv", row.names = FALSE)
# Analisis:  t.test(tiempo_ms ~ entorno, ab)   # prueba A/B

# ---------- 5. HONGOS / SUSTRATO: ANOVA + ji-cuadrada ----------
sus <- list(paja_trigo = c(88, 8, 21, 0.04), pulpa_cafe = c(80, 8, 24, 0.24),
            olote_maiz = c(66, 8, 27, 0.12), aserrin    = c(52, 12, 30, 0.48))
hongos <- do.call(rbind, lapply(names(sus), function(s) {
  p <- sus[[s]]
  data.frame(
    id = sprintf("%s%02d", substr(s, 1, 3), 1:25),
    sustrato = s,
    eficiencia_biologica = round(pmax(rnorm(25, p[1], p[2]), 1), 1),
    dias_cosecha = as.integer(round(rnorm(25, p[3], 2.5))),
    contaminado = ifelse(runif(25) < p[4], "si", "no")
  )
}))
write.csv(hongos, "datos_simulados/hongos_sustrato.csv", row.names = FALSE)
# Analisis:  aov(eficiencia_biologica ~ sustrato); bartlett.test(...) [varianzas];
#            chisq.test(table(sustrato, contaminado))

cat("Listo: 6 archivos en ./datos_simulados/\n")
cat("Pinguinos (laboratorio de ensenanza): install.packages('palmerpenguins'); data(penguins)\n")
