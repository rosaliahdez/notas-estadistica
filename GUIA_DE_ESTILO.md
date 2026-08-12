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
