# Flujo de trabajo del libro

Chuleta para retomar después de un rato sin tocarlo.

## Abrir el proyecto

Doble clic en **`notas-estadistica.Rproj`**. Eso abre RStudio ya parado en esta
carpeta (importante: si abres RStudio "a secas", las rutas como `datos/galletas.csv`
no funcionarán).

## Ver el libro mientras escribes

En la pestaña **Terminal** de RStudio (no en la consola de R):

```bash
quarto preview
```

Se abre el libro en el navegador y **se actualiza solo** cada vez que guardas un
`.qmd`. Déjalo corriendo mientras trabajas.

Para detenerlo: clic en la Terminal y **Ctrl + C**.

> Si prefieres botones: con un `.qmd` abierto, RStudio muestra arriba el botón
> **Render**. Hace lo mismo para ese archivo.

## Probar código de R sin renderizar todo

Dentro de un `.qmd`, cada bloque de código tiene un **triángulo verde ▶** en su
esquina derecha: lo ejecuta y muestra el resultado ahí mismo, sin recompilar el libro.

- Ejecutar el bloque donde está el cursor: **Ctrl + Shift + Enter**
- Ejecutar solo la línea seleccionada: **Ctrl + Enter**
- Ejecutar todos los bloques anteriores: el ícono ▼ gris a la izquierda del ▶

Esto es lo más rápido para verificar que un análisis corre bien antes de renderizar.

## Publicar los cambios

Dos pasos distintos, y conviene no confundirlos:

**1. Guardar tu fuente en GitHub** (pestaña *Git* de RStudio):

- Marca las casillas de los archivos cambiados
- **Commit** → escribe un mensaje → **Push**

**2. Actualizar el sitio web** (Terminal):

```bash
quarto publish gh-pages
```

Renderiza el libro y sube el resultado a la rama `gh-pages`. El sitio queda en
<https://rosaliahdez.github.io/notas-estadistica/>

> Puedes trabajar varios días haciendo solo commits, y publicar una sola vez al final.
> No hace falta publicar en cada cambio.

## Estructura

```
notas-estadistica/
├── index.qmd                  Presentación
├── 01…11-*.qmd                Los once capítulos
├── laboratorio-estandarizacion.qmd
├── laboratorio-r.qmd          (requiere extensión; ver INSTALAR_CELDAS_EJECUTABLES.md)
├── datos/                     Los CSV que usan los capítulos
├── _quarto.yml                Índice y formato del libro
├── theme.scss                 Colores
└── references.bib             Bibliografía
```

## Si algo truena

- **"cannot open file 'datos/…'"** → no abriste el proyecto desde el `.Rproj`.
- **"there is no package called…"** → falta instalar: `install.packages(c("tidyverse", "palmerpenguins"))`
- **Los deslizadores no aparecen** → son celdas `{ojs}`; requieren que el libro se
  vea en el navegador (`quarto preview`), no en el panel de RStudio.
- **El preview se quedó pegado** → Ctrl + C en la Terminal y vuelve a lanzarlo.

## Nota sobre los laboratorios interactivos

Los deslizadores usan **Observable JS** (celdas `{ojs}`) y no necesitan instalar nada:
funcionan en el sitio publicado. Las celdas donde el estudiante *escribe y ejecuta R*
(`laboratorio-r.qmd`) sí requieren la extensión `quarto-live`; están desactivadas en
`_quarto.yml` hasta que la instales.
