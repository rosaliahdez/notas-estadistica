# Bases de datos simuladas — Curso de Estadística (LCC, Unison)

Datos de respaldo para el curso, por si los expositores comparten el contexto pero no sus datos. **Todo es simulado** (semilla 2026) pero con parámetros realistas y con "imperfecciones" deliberadas —una varianza desigual aquí, una variable sin diferencias allá— para que los estudiantes tengan que verificar supuestos, no solo aplicar fórmulas.

Cada base activa una técnica concreta del temario. Los resultados esperados que se listan abajo están **verificados numéricamente** sobre los CSV incluidos.

| Archivo | Técnica principal | Unidad / semana |
|---|---|---|
| `galletas.csv` | ANOVA de un factor + post-hoc | U10 / sem. 13 (proyecto) |
| `hongos_sustrato.csv` | ANOVA de un factor + Bartlett + ji-cuadrada | U10 / sem. 13 |
| `lagartijas.csv` | Diferencia de dos medias (+ prueba de varianzas) | U8 / sem. 10 |
| `rickettsiosis.csv` | Proporciones y ji-cuadrada | U9 / sem. 11 |
| `algoritmos_regresion.csv` | Regresión lineal e inferencia | U3 y U11 / sem. 3 y 14 |
| `algoritmos_ab.csv` | Prueba A/B (dos muestras) | U8 / sem. 10 |
| *(Palmer Penguins)* | Laboratorio de enseñanza (todo) | transversal |

> Reproducibilidad: los CSV son una realización con semilla 2026. `generar_datos.R` regenera datos equivalentes en tu entorno y permite ajustar tamaños y efectos. `generar_datos.py` es el generador que produjo exactamente estos CSV (solo numpy y pandas).

---

## 1. `galletas.csv` — cata a ciegas de marcas de galletas

**Historia.** Réplica del experimento de la tesis dirigida por la Dra. Figueroa: 25 jueces evalúan a ciegas cuatro marcas (Oreo, Chokis, Lors, Great Value) en una escala hedónica de 1 a 9. El orden de cata se aleatoriza por juez y se incluyó un leve efecto de fatiga de paladar (las últimas posiciones tienden a puntuarse un poco más bajo) para poder discutir *por qué* se aleatoriza.

| Variable | Tipo | Descripción |
|---|---|---|
| `juez` | entero | Identificador del catador (1–25) |
| `orden` | entero | Posición en que probó esa marca (1–4) |
| `marca` | categórica | Oreo, Chokis, Lors, GreatValue |
| `agrado` | entero 1–9 | Calificación hedónica |

**Resultado esperado.** ANOVA `agrado ~ marca`: **F(3,96) ≈ 19.1, p ≈ 8×10⁻¹⁰**. Medias: Oreo 7.4, Chokis 6.8, Lors 5.8, Great Value 5.0. Tukey separa a las de marca de las económicas. Supuestos aceptables; buen caso para verificarlos.

```r
d <- read.csv("datos_simulados/galletas.csv")
m <- aov(agrado ~ marca, d); summary(m); TukeyHSD(m)
shapiro.test(residuals(m))            # normalidad de residuos
bartlett.test(agrado ~ marca, d)      # homogeneidad de varianzas
```

---

## 2. `hongos_sustrato.csv` — cultivo de seta sobre sustratos

**Historia.** Experimento agrícola: se cultiva seta (*Pleurotus ostreatus*) en 25 bolsas por cada uno de cuatro sustratos (paja de trigo, pulpa de café, olote de maíz, aserrín) y se mide la eficiencia biológica (%), los días a cosecha y si la bolsa se contaminó. El aserrín se diseñó con **más variabilidad** que los demás, para que la prueba de homogeneidad de varianzas tenga algo que detectar. Es el gemelo científico del experimento de galletas: mismo ANOVA, datos de laboratorio real — ideal para el expositor micólogo.

| Variable | Tipo | Descripción |
|---|---|---|
| `id` | texto | Identificador de la bolsa |
| `sustrato` | categórica | paja_trigo, pulpa_cafe, olote_maiz, aserrin |
| `eficiencia_biologica` | numérica | % (peso fresco de hongo / peso seco de sustrato) |
| `dias_cosecha` | entero | Días hasta la primera cosecha |
| `contaminado` | categórica | si / no |

**Resultado esperado.** ANOVA `eficiencia_biologica ~ sustrato`: **F(3,96) ≈ 83, p ≈ 10⁻²⁶**; medias paja 86 > pulpa 81 > olote 65 > aserrín 50. Ji-cuadrada `sustrato × contaminado`: **X² ≈ 13.6, gl 3, p ≈ 0.004** (aserrín se contamina más).

> **Nota sobre las varianzas.** El aserrín se generó con mayor dispersión (desviación 12 contra 8 de los demás), y en la muestra efectivamente es el más variable (≈ 10.5 contra 7.5–9.4). Sin embargo, **Bartlett NO rechaza** la igualdad de varianzas (p ≈ 0.32): con 25 bolsas por grupo no hay potencia suficiente para detectar esa diferencia. Es un caso didáctico útil —una diferencia real que la prueba no detecta— y así está tratado en el @sec-cap10.

```r
d <- read.csv("datos_simulados/hongos_sustrato.csv")
m <- aov(eficiencia_biologica ~ sustrato, d); summary(m); TukeyHSD(m)
bartlett.test(eficiencia_biologica ~ sustrato, d)
chisq.test(table(d$sustrato, d$contaminado))
```

---

## 3. `lagartijas.csv` — fisiología urbana vs. campo abierto

**Historia.** Comparación de lagartijas de zona urbana (n=32) contra campo abierto (n=30). La temperatura corporal es mayor y más variable en la ciudad (isla de calor urbana); la masa también difiere; **la longitud hocico–cloaca (LHC) NO difiere** —incluida a propósito para enseñar que un resultado no significativo también es un resultado.

| Variable | Tipo | Descripción |
|---|---|---|
| `id` | texto | Identificador del individuo |
| `habitat` | categórica | urbana / campo |
| `temp_corporal` | numérica | °C |
| `masa_g` | numérica | gramos |
| `lhc_mm` | numérica | longitud hocico–cloaca (mm) |
| `frec_cardiaca` | entero | latidos por minuto |

**Resultado esperado.** t de Welch `temp_corporal ~ habitat`: **t ≈ 4.0, p ≈ 0.0002** (urbana 35.4 vs campo 34.0). `masa_g`: **p ≈ 0.01**. `lhc_mm`: **p ≈ 0.25 (no significativo)**. `var.test` sobre la temperatura ilustra el complemento MCD de comparación de varianzas.

```r
d <- read.csv("datos_simulados/lagartijas.csv")
boxplot(temp_corporal ~ habitat, d)
t.test(temp_corporal ~ habitat, d)   # difiere
t.test(lhc_mm ~ habitat, d)          # NO difiere
var.test(temp_corporal ~ habitat, d) # comparacion de varianzas
```

---

## 4. `rickettsiosis.csv` — factores asociados a un resultado positivo

**Historia.** Registro de 420 personas evaluadas por rickettsiosis (endémica en Sonora), con la zona de residencia, el contacto con perros, la presencia de garrapatas y el resultado de laboratorio. El contacto con perros y las garrapatas elevan la probabilidad de resultado positivo. Base epidemiológica simulada, para tratar el tema con datos y sin exponer información real.

| Variable | Tipo | Descripción |
|---|---|---|
| `id` | texto | Identificador |
| `zona` | categórica | urbana_marginada / urbana / rural |
| `contacto_perro` | categórica | si / no |
| `garrapatas` | categórica | si / no |
| `resultado` | categórica | positivo / negativo |

**Resultado esperado.** Ji-cuadrada `contacto_perro × resultado`: **X² ≈ 29.8, gl 1, p ≈ 5×10⁻⁸**. Positividad: con contacto 33% vs sin contacto 9% (global 25%). `prop.test` compara proporciones de positivos entre zonas.

```r
d <- read.csv("datos_simulados/rickettsiosis.csv")
tab <- table(d$contacto_perro, d$resultado); tab
chisq.test(tab)
prop.test(table(d$zona, d$resultado))   # diferencia de proporciones por zona
```

---

## 5. `algoritmos_regresion.csv` — tiempo de ejecución vs. tamaño de entrada

**Historia.** Tiempos de ejecución (ms) de un algoritmo para tamaños de entrada de 1 000 a 10 000, con 5 réplicas por tamaño, en dos entornos (Mac, Windows). Contexto propio de LCC. Se incluyó una **curvatura muy leve** para que el análisis de residuales tenga algo que mostrar.

| Variable | Tipo | Descripción |
|---|---|---|
| `entorno` | categórica | Mac / Windows |
| `n` | entero | Tamaño de entrada |
| `tiempo_ms` | numérica | Tiempo de ejecución (ms) |

**Resultado esperado.** Regresión (solo Mac) `tiempo_ms ~ n`: pendiente **b ≈ 0.0018 ms/elemento, r ≈ 0.97**, prueba sobre la pendiente **t ≈ 28, p ≈ 10⁻³¹**. Los residuales insinúan la curvatura → discusión de bondad del modelo lineal.

```r
d <- read.csv("datos_simulados/algoritmos_regresion.csv")
mac <- subset(d, entorno == "Mac")
m <- lm(tiempo_ms ~ n, mac); summary(m)
plot(m, which = 1)                   # residuales vs ajustados
```

---

## 6. `algoritmos_ab.csv` — prueba A/B entre dos entornos

**Historia.** El mismo algoritmo se corre 30 veces por entorno con un tamaño fijo (n = 5 000). Es una prueba A/B clásica: ¿Windows es más lento que Mac? Vocabulario de la industria para una comparación de dos medias.

| Variable | Tipo | Descripción |
|---|---|---|
| `entorno` | categórica | Mac / Windows |
| `corrida` | entero | Número de corrida (1–30) |
| `tiempo_ms` | numérica | Tiempo de ejecución (ms) |

**Resultado esperado.** t de dos muestras `tiempo_ms ~ entorno`: **t ≈ 4.8, p < 0.0001** (Windows 12.6 ms vs Mac 10.6 ms).

```r
d <- read.csv("datos_simulados/algoritmos_ab.csv")
t.test(tiempo_ms ~ entorno, d)       # prueba A/B
```

---

## 7. Palmer Penguins — laboratorio de enseñanza

No se simula: es un conjunto real, limpio y siempre disponible, para introducir la mecánica de cada técnica antes de aplicarla a los datos de arriba.

```r
install.packages("palmerpenguins")   # una sola vez
library(palmerpenguins); data(penguins)
# ANOVA:      aov(body_mass_g ~ species, penguins)
# 2 medias:   t.test(bill_length_mm ~ sex, subset(penguins, species=="Adelie"))
# regresion:  lm(bill_depth_mm ~ bill_length_mm, penguins)
# ji-cuadrada:chisq.test(table(penguins$species, penguins$island))
# matriz de correlacion: cor(na.omit(penguins[,3:6]))
```
