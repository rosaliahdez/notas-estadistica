# Cómo actualizar el material del curso

Bitácora de los procedimientos que se repiten cada semana. Está escrita para no
tener que acordarse de nada.

---

## 1. Publicar el libro en GitHub

El libro vive en dos lugares. El **código fuente** (los `.qmd`) está en la rama
`main` del repositorio, y el **sitio que ven los estudiantes** está en la rama
`gh-pages`, que Quarto genera y actualiza sola. Nunca hay que tocar `gh-pages` a
mano.

Son dos pasos, y el orden importa.

### Paso 1. Guardar los cambios en el repositorio

En RStudio, con el proyecto abierto:

1. Pestaña **Git**, arriba a la derecha.
2. Palomear los archivos modificados en la columna **Staged**.
3. **Commit**, escribir un mensaje corto que diga qué se cambió, y **Commit**.
4. Botón **Push** (la flecha verde hacia arriba).

Si no se hace *push*, los cambios quedan solo en la computadora.

### Paso 2. Publicar el sitio

En la pestaña **Terminal** de RStudio, no en la consola de R:

```
quarto publish gh-pages
```

La primera vez pregunta si se quiere usar el repositorio detectado. Se contesta
que sí. Después renderiza los once capítulos, sube el resultado y termina
imprimiendo la dirección del sitio.

**El sitio tarda uno o dos minutos** en reflejar el cambio. Si al abrirlo se ve
igual, conviene esperar y recargar con Ctrl + F5, que ignora la copia guardada
en el navegador.

### Errores que salen seguido

| Lo que dice | Qué pasó |
|---|---|
| `Unable to publish, uncommitted changes` | Falta el paso 1. Quarto exige el repositorio limpio |
| `quarto: command not found` | Se escribió en la consola de R y no en la Terminal |
| El sitio se ve viejo | Todavía no termina de propagarse, o es la copia del navegador |
| Falla al renderizar un capítulo | Un bloque de R con error. El mensaje dice cuál. Se corrige y se repite |

### Comprobación rápida antes de publicar

Conviene renderizar en local primero, para no publicar algo roto:

```
quarto render
```

Si eso pasa sin errores, `quarto publish gh-pages` también va a pasar.

---

## 2. Quitar las respuestas de una presentación

Las presentaciones traen las diapositivas de respuestas de la práctica. Mientras
la entrega sigue abierta conviene compartir la versión sin ellas.

En el preámbulo del `.tex`, cerca del inicio, están estas dos líneas:

```latex
\newif\ifrespuestas
\respuestastrue
```

- `\respuestastrue` produce el PDF **completo**, que es el de dar clase.
- `\respuestasfalse` produce el PDF **sin las diapositivas de respuestas**.

Se cambia esa palabra, se vuelve a compilar y listo. En la semana 1 son 55
páginas contra 53.

El **cierre de la semana** quedó fuera de ese interruptor a propósito, así que
aparece en las dos versiones. Es la diapositiva que más necesita quien faltó.

---

## 3. Subir una presentación a Overleaf

Cada archivo de semana es **autocontenido**, trae su propio preámbulo y no llama
a ningún otro archivo. Se abre, se copia entero y se pega en un archivo nuevo
dentro de la carpeta **Estadistica** del proyecto **CURSOS**.

Las figuras van aparte, en la carpeta `figuras` de esa misma carpeta. Los `.tex`
compilan aunque falten, porque cada imagen está envuelta en `\IfFileExists` y
tiene un respaldo dibujado.

Para regenerar las figuras, desde el proyecto de RStudio:

```r
source("presentaciones/figuras-para-diapositivas.R")
```

---

## 4. Importar preguntas a Moodle

El procedimiento completo está en `moodle/ESQUEMA-Moodle.md`, con los ajustes
que hay que marcar para que la retroalimentación se vea.

Lo esencial: los `.xml` son **paquetes de preguntas**, no cuestionarios. Se
importan en *Banco de preguntas ▸ Importar*, con **Formato XML de Moodle** y con
la casilla **Obtener categoría desde el archivo** marcada. El cuestionario es una
actividad aparte que se arma después.

Importar dos veces el mismo archivo **duplica** las preguntas.
