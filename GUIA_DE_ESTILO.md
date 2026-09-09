# Guía de estilo del libro

Bitácora de decisiones sobre voz, vocabulario y notación. Sirve para que el libro suene parejo de principio a fin, y para que las presentaciones Beamer salgan con el mismo tono.

**Cómo usarla:** ir anotando aquí lo que se decida durante la revisión. No hace falta que sea prolijo; con una línea basta.

---

## Decisiones ya aplicadas

### Trato al lector: impersonal ✔

Todo el libro está en registro **impersonal**. Se eliminó el tuteo por completo (verificado con búsqueda exhaustiva). Las formas adoptadas:

| En vez de | Se usa |
|---|---|
| "Mueve el deslizador y observa…" | "Al mover el deslizador se observa…" |
| "Fíjate en que…" | "Nótese que…" / "Obsérvese que…" |
| "Calcula la media" (ejercicios) | "Calcular la media" (infinitivo) |
| "Puedes ver" | "Puede verse" |
| "Recuerda que" | "Conviene recordar que" |
| "tu muestra", "tus datos" | "la muestra", "los datos" |
| "¿Ves algún patrón?" | "¿Se observa algún patrón?" |

**Se conservó el "nosotros" de autor** ("ya sabemos explorar datos", "usaremos el registro"), porque es la norma en textos matemáticos en español y no constituye tuteo. Si se prefiere eliminarlo también, se puede hacer en una segunda pasada.

### Títulos de los recuadros ✔

| Antes | Ahora |
|---|---|
| "Al terminar este capítulo podrás" | **"Objetivos del capítulo"** |
| "Interpreta" | **"Interpretación"** |
| "¿Qué técnica uso?" | **"¿Qué técnica usar?"** |
| "Experimenta" | **"Experimento sugerido"** |

Sin cambio: "Soluciones y retroalimentación".

### Sin referencias a estudios de posgrado ✔

Se eliminaron todas las menciones explícitas a la Maestría en Ciencia de Datos y a cursos posteriores concretos. Los temas complementarios se presentan por su propio valor:

- "Complemento para el examen de la MCD" → **"Tema complementario"**, justificado por su uso en la práctica.
- "que se verá en la Maestría en Ciencia de Datos" → "que queda fuera del alcance de este curso".
- "Cuando en su curso de Aprendizaje Automático evalúen un modelo" → "Al evaluar cualquier modelo predictivo".

### Software y datos ✔

- El software eje es **R**; Python aparece solo como material complementario.
- Los datos aplicados son **simulados** y así se declara en el diccionario de datos.
- Estructura de cada tema: pregunta real → técnica → supuestos → cómputo en R → interpretación.

### Toda salida lleva su interpretación ✔ *(regla permanente, agosto 2026)*

**Después de cada resumen gráfico o numérico va, por escrito, qué significa.** Sin
excepción, en el libro y en las diapositivas. Una tabla, una caja, un histograma o una
línea de R que devuelve un número no se dejan solos.

La razón es de evaluación: interpretar resultados es una de las cuatro competencias que
se les pide en el examen, junto con elegir la técnica, verificar supuestos y calcular en
bases pequeñas. Si el material nunca modela la interpretación, no hay de dónde la
aprendan.

Forma adoptada: un párrafo que empieza con **Interpretación.** en negritas, dentro de la
`\destaca` que acompaña a la figura o al bloque de código. En el libro, el recuadro
`::: {.callout-note title="Interpretación"}`.

**Cuándo va "Interpretación." y cuándo "Observación."** *(acuerdo de septiembre 2026)*
La palabra **Interpretación** se reserva para cuando se aplica una herramienta a **datos de
un caso**, que es la competencia que se evalúa: qué se le contestaría a quien trajo esos
datos. Cuando la figura es solo **ilustrativa**, hecha para explicar un concepto y no para
analizar un conjunto real, el párrafo empieza con **Observación.**

### Sin referencias temporales en el material ✔ *(septiembre 2026)*

Nada de "en la sesión pasada", "el viernes", "la semana pasada". El calendario real se
mueve y el material queda mintiendo. Se remite al **contenido**, no al día: "al justificar
el 1.5 de las barreras", "en la unidad 3", "en la diapositiva siguiente". La excepción son
los avisos que de verdad hablan del calendario, como el de la semana sin clases.

### Ningún concepto se usa antes de definirlo ✔ *(septiembre 2026)*

Regla que salió de dos errores reales. El coeficiente $r$ del Q-Q plot estaba en la
Unidad 2, tres semanas antes de que se definiera la correlación; se recorrió a la Unidad 3.
Y los cuartiles de una distribución se usaban al justificar el 1.5 sin haberlos presentado.
Antes de cerrar un bloque conviene recorrerlo preguntando, de cada símbolo y de cada
palabra técnica, dónde se definió.

### Los ejemplos a mano son transversales ✔ *(regla permanente, septiembre 2026)*

Un conjunto chico de datos no se inventa para una diapositiva y se abandona: se
**reutiliza a lo largo del parcial**. Las diez masas de pingüino sirvieron en la unidad 1
para el histograma a mano, en la unidad 2 para media, mediana y moda, después para los
cuartiles y las barreras del boxplot, y al final para construir el Q-Q plot y su recta.

La ventaja es pedagógica y es la razón de ser de los proyectos ancla. Cuando llega una
técnica nueva, los estudiantes ya se saben los datos, ya calcularon algunas de sus
medidas, y toda su atención queda libre para el concepto. Además hace visible que las
distintas medidas describen **el mismo conjunto** desde ángulos distintos, que es lo que
un resumen de centro, dispersión y forma quiere decir.

De ahí dos consecuencias prácticas. La primera, que los ejemplos a mano salen de los
**proyectos ancla** y no de contextos sueltos. La segunda, que cuando una decisión de
diseño choca con la continuidad, gana la continuidad: el ejercicio del Q-Q se dejó con
los cuartiles del curso, y no con los de R, precisamente porque esos cuartiles ya se
habían calculado en clase con esos mismos diez datos.

El inventario de conjuntos disponibles está en `DATOS-DE-MANO.md`. Antes de inventar uno
nuevo conviene revisarlo, y si de verdad hace falta, se diseña pensando en qué unidades
posteriores podrá reaparecer y se registra ahí.

---

### Primero a mano, después en R ✔ *(regla permanente)*

Cada técnica se presenta con el **cálculo a mano** antes del comando de R, y con un
ejercicio breve en papel más sus respuestas. El grupo llegó sin poder trazar gráficas a
mano, así que la cuenta manual es la que fija el concepto; R viene después, a comprobar.

---

## Pendiente de decidir

### Vocabulario

Anotar aquí las preferencias que surjan durante la lectura:

| Uso actual en el libro | Se prefiere |
|---|---|
| "valor p" | |
| "diagrama de caja" / "boxplot" | |
| "gráfica" | |
| "conjunto de datos" | |
| "recuadro" | |
| | |

### Notación matemática

- Nivel actual: se enuncian las fórmulas clave, sin demostraciones.
- ¿$\bar{x}$ o $\hat{\mu}$?
- Notas:

### Nivel de detalle

- [ ] La extensión de los capítulos está bien
- [ ] Se prefiere más concisión
- [ ] Se prefiere más desarrollo en (indicar temas):

### Pasajes por reescribir

Marcar en el `.qmd` con `<!-- REVISAR: … -->` y anotar aquí si se quiere dejar constancia:

-

---

## Perfil de voz medido (agosto 2026)

Después de que las primeras cuatro clases de diapositivas pasaron por su revisión, se
compararon con números el texto reescrito por ella y el texto escrito por mí. Esto es
lo que salió, por cada mil palabras.

| Rasgo | Ella (lo revisado) | Yo (deck sin revisar) | Yo (libro) |
|---|---|---|---|
| Dos puntos en prosa | 10.9 | 11.4 | **20.5** |
| Raya de inciso (—) | 0.4 | 1.2 | **5.5** |
| Paréntesis | 25.1 | 37.3 | 20.6 |
| Impersonal "se" + verbo | 2.5 | 1.2 | 2.4 |
| Nosotros de autor (-amos/-emos) | 7.4 | 7.2 | 7.9 |
| "nótese / obsérvese" | 0.9 | 0.0 | 0.7 |

**Lo que las cuatro sesiones sí revelan.** Puntuación y ritmo. Ella usa **la mitad de
dos puntos** que yo en el libro, y **casi ninguna raya de inciso**. El registro
impersonal y el nosotros de autor ya coincidían, así que en eso el libro está bien.

**Lo que no revelan.** Vocabulario. Sus ediciones conservan las dos variantes de casi
todas las palabras que yo esperaba que resolviera. En el conteo aparecían "renglón" y
"fila" mezcladas, "librería" y "paquete", "dataset" y "conjunto de datos". Al
preguntárselo directamente resolvió la primera, y las otras siguen abiertas.

### Rasgos de estilo verificados en sus ediciones

1. **Títulos descriptivos y cortos, sin dos puntos ni guiños.** Cambió "El directorio de
   trabajo: de dónde cree R que está" por "El directorio de trabajo", y "Cuando algo
   falla, y va a fallar" por "Errores típicos".
2. **Poda los adornos narrativos.** Borró frases como "Leer un mensaje de error completo
   antes de pedir auxilio es una habilidad, y se practica".
3. **Primera persona del plural para las acciones.** Escribe "Instalamos el paquete",
   "Cargamos la librería", "Escribamos en un archivo", donde yo había puesto "se
   instala", "se carga".
4. **Convierte prosa larga en listas.** La destaca de "Precauciones para quienes vienen
   de otro lenguaje" la volvió tres viñetas.
5. **Prefiere lo llano sobre lo metafórico.** "nativamente" en vez de "de nacimiento",
   "por detrás" en vez de "por debajo".
6. **Línea en blanco antes de cada `\vspace`.** No es capricho, es necesario: sin ella
   LaTeX aplica el espacio en modo horizontal y el bloque queda desalineado.
7. **Capitaliza los nombres de las áreas.** "la Estadística", "Estadística Descriptiva",
   "Diseño de Experimentos", "la Probabilidad".

### Regla de puntuación adoptada ✔

**Los dos puntos se usan con moderación.** Se aplicó una pasada completa al deck y a los
once capítulos, que quitó **53** dos puntos de tipo explicativo, los que unen dos
oraciones completas y que en español se resuelven mejor con punto y seguido.

Los que **sí se conservan**, porque son correctos y no delatan a nadie:

| Uso | Cuántos quedan | Ejemplo |
|---|---|---|
| Antes de una lista o de un bloque de código | 143 | "hay dos familias:" |
| Después de una etiqueta corta | 216 | "*Moraleja:*", "Ilustración:" |
| Antes de una enumeración de sustantivos | 80 | "tres formas de obtener datos: un censo…" |
| En celda de tabla | 4 | "Experimento: control, aleatorización" |

### Vocabulario decidido ✔

**Renglón, nunca fila.** Aplicado en todo el material, con la concordancia ajustada:
"los renglones" (no "las filas"), "un renglón por juez", "338 renglones más". Se
respetaron los identificadores de código, donde `filas` sigue siendo un nombre de
variable.

Siguen abiertas, por falta de evidencia: "librería" contra "paquete", y "dataset"
contra "conjunto de datos". Ella usa las dos de cada par.

**Gráfica, nunca panel.** Cuando una figura trae dos o más dibujos, se les llama
*gráficas* y se ubican por su lugar: "la de la izquierda", "la gráfica de al lado". La
palabra *panel* es jerga de quien programa la figura, no de quien la lee, y Rosalía no
la usa. Se corrigieron los dos lugares donde se había colado (semana 2 y semana 3).

### La raya de inciso ✔

Se usa, pero con moderación, porque en exceso delata. De las 150 que había se
convirtieron **57 a paréntesis** y una a comas. Se conservaron **15 pares**, los que
encierran algo que ya trae paréntesis adentro o que va en una frase con varios
paréntesis cerca, donde meter otro par apretaría la lectura.

Quedan 37 rayas en los capítulos, contra 150 al inicio.

### Pendiente de decidir

- **El patrón de etiqueta** (*Moraleja:*, *Regla práctica:*, *Truco:*). Son 216 y
  también son un tic reconocible. A cambio, ayudan a que el estudiante escanee la
  página y encuentre la idea. Conviene decidirlo con ese costo a la vista, no solo por
  estilo.
