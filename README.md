# Estadística para Ciencias de la Computación

Notas del curso de **Estadística** (LCC, Universidad de Sonora) como libro Quarto,
publicable en GitHub Pages. El **Capítulo 1 está completo**; los capítulos 2–11 son
plantillas con su estructura ya fijada.

## Requisitos (una sola vez)

1. **R** + **RStudio** (o **Posit Cloud**).
2. **Quarto**: <https://quarto.org/docs/get-started/>
3. Paquetes de R:

   ```r
   install.packages(c("tidyverse", "palmerpenguins"))
   ```

## Publicar en GitHub Pages — mismo flujo que tu libro de Grafos

1. **Crea un repositorio vacío** en GitHub (por ejemplo `estadistica-lcc`), **sin** README ni .gitignore (para que no choque con estos archivos).

2. En **RStudio**: `File > New Project > Version Control > Git`, pega la URL del repo y clónalo.

3. **Copia el contenido de esta carpeta** (todos los `.qmd`, `_quarto.yml`, `datos/`, `theme.scss`, `.gitignore`, `estadistica-lcc.Rproj`, etc.) dentro de la carpeta del proyecto que RStudio acaba de clonar.

4. **Commit y push** (pestaña *Git* de RStudio, o en la terminal):

   ```bash
   git add .
   git commit -m "Libro del curso: capítulo 1 y plantillas"
   git push
   ```

5. **Publica el sitio** desde la terminal (igual que en Grafos):

   ```bash
   quarto publish gh-pages
   ```

   Esto **renderiza** el libro y sube el resultado a la rama `gh-pages`. La primera vez
   configura esa rama y te pide confirmar; después, GitHub Pages sirve el sitio en
   `https://TU-USUARIO.github.io/estadistica-lcc/`.

> **El ciclo de trabajo** es: editas los `.qmd` → `commit` + `push` (esto guarda tu
> *fuente* en la rama `main`) → `quarto publish gh-pages` (esto actualiza el *sitio*).
> La carpeta de salida `_book/` y `.quarto/` están en `.gitignore` a propósito: no se
> suben a `main`, porque `quarto publish` ya se encarga de la rama `gh-pages`.

## Vista previa local (mientras escribes)

```bash
quarto preview     # abre el libro y se actualiza solo al guardar
quarto render      # genera _book/ sin publicar
```

## Estructura

```
.
├── _quarto.yml            Configuración del libro (capítulos, formato, tema)
├── index.qmd              Presentación / prefacio
├── 01-exploracion.qmd     Capítulo 1 — COMPLETO
├── 02-…-11-….qmd          Capítulos 2 a 11 — plantillas
├── references.qmd/.bib    Bibliografía
├── theme.scss             Estilo visual (colores Unison)
├── estadistica-lcc.Rproj  Proyecto de RStudio
├── .gitignore
└── datos/                 Los CSV del curso (para que el código corra)
```

## Cómo escribir un capítulo

Sigue el patrón del Capítulo 1: **pregunta real → técnica → supuestos → cómputo en R →
interpretación**. Los datos se leen con, por ejemplo, `read.csv("datos/galletas.csv")`.

Cada capítulo lleva cuatro elementos fijos:

1. **Recuadros del mapa de decisión**: `::: {.callout-tip title="¿Qué técnica uso?"}`
2. **Recuadros de interpretación**: `::: {.callout-note title="Interpreta"}`
3. **Un laboratorio interactivo** donde ayude a entender (ver abajo).
4. **Solucionario con retroalimentación** al final de los ejercicios:
   `::: {.callout-tip title="Soluciones y retroalimentación" collapse="true"}`
   Cada respuesta incluye el razonamiento y, en *cursiva*, el error típico a evitar.
   El `collapse="true"` deja el bloque plegado: el estudiante lo abre cuando ya intentó.

## Laboratorios interactivos (Observable JS)

Los deslizadores usan **OJS**, que Quarto trae integrado y corre **en el navegador**:
funcionan en el sitio publicado en GitHub Pages sin servidor ni Shiny. El patrón es:

````markdown
```{ojs}
//| panel: input
//| echo: false
viewof n = Inputs.range([1, 100], {value: 30, step: 1, label: "tamaño n"})
```

```{ojs}
//| echo: false
Plot.plot({ marks: [ /* usa n aquí; se redibuja solo */ ] })
```
````

`Plot` (Observable Plot), `d3` e `Inputs` están disponibles sin importarlos. Para pasar
datos de R a OJS, en un chunk de R usa `ojs_define(mis_datos = df)` y en OJS
`transpose(mis_datos)` (ver el Capítulo 1).

Laboratorios ya escritos: ancho de clase (cap. 1), media vs. mediana (cap. 2),
correlación (cap. 3), tamaño de muestra y sesgo (cap. 4), estandarización y TCL
(Parte III).
