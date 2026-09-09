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

### Qué escribir en el mensaje del commit

Es la parte que más cuesta, y hay una razón. Un mensaje como *"Versión 2"* obliga
a llevar la cuenta de memoria, igual que pasaba con el número de sesión en las
diapositivas. Git ya guarda el orden y la fecha de cada commit, así que ese dato
sobra. Lo que Git **no** puede saber es qué se cambió.

**La fórmula: qué cambió, en una línea, sin punto final.**

Sirve pensarlo como si alguien preguntara *"¿qué hiciste?"* y hubiera que
contestar en cinco o seis palabras.

| En vez de | Conviene |
|---|---|
| Versión 3 | Portada dice Profesora y crédito al inicio |
| Cambios | Aviso de revisión en los capítulos 2 a 11 |
| Actualización | Corrijo tuteo en el capítulo 1 |
| Avances | Agrego banco de preguntas de la unidad 1 |
| . | Nota sobre nombres de columna al leer CSV |

Tres cosas que ayudan:

- **Que quepa en una línea.** Si hace falta más, casi siempre es que son dos
  commits distintos.
- **Que se entienda dentro de seis meses**, sin tener el archivo enfrente.
- **Que no invente numeración.** Ni versiones, ni fechas, ni "parte 2". Eso ya
  lo pone Git solo.

No hay que agonizar. Un mensaje imperfecto pero descriptivo vale mucho más que
uno perfecto que nunca se escribió, y nadie más que tú va a leer la mayoría.

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

### Si el push falla por autenticación

El mensaje es este:

```
remote: Invalid username or token. Password authentication is not supported
fatal: Authentication failed for 'https://github.com/...'
```

**No es que la contraseña esté mal.** GitHub dejó de aceptar contraseñas para Git
en 2021. En su lugar se usa un **token**, que es una clave larga que se genera en
GitHub y que caduca en la fecha que uno elija. Cuando caduca, el push falla así.

La forma más cómoda desde RStudio, porque hace los dos pasos de un jalón, es esta.
En la **consola de R**:

```r
install.packages(c("usethis", "gitcreds"))   # solo la primera vez

usethis::create_github_token()
```

Eso abre el navegador en la página de GitHub con los permisos correctos ya
marcados. Solo hay que ponerle un nombre, elegir la caducidad y pulsar
**Generate token**. Aparece una clave larga que empieza con `ghp_`.

**Hay que copiarla en ese momento.** GitHub no la vuelve a mostrar.

Enseguida, de vuelta en la consola de R:

```r
gitcreds::gitcreds_set()
```

Pregunta por el token y se pega ahí. Si ya había uno guardado, ofrece
reemplazarlo, que es justo lo que se necesita cuando el viejo caducó.

Después de eso, el **Push** de RStudio funciona normal.

**Sobre la caducidad.** Al generar el token conviene elegir una fecha lejana, por
ejemplo un año, y anotarla. Si se elige "sin caducidad" ya no vuelve a fallar,
aunque es menos seguro. Para un repositorio de notas de curso, cualquiera de las
dos está bien.

**La ruta manual**, por si la de R no funciona, es entrar a GitHub, foto de perfil
arriba a la derecha, **Settings**, en la barra de la izquierda hasta abajo
**Developer settings**, luego **Personal access tokens ▸ Tokens (classic)** y
**Generate new token (classic)**. El permiso que hace falta es el que dice
**repo**.

### Errores que salen seguido

| Lo que dice | Qué pasó |
|---|---|
| `Unable to publish, uncommitted changes` | Falta el paso 1. Quarto exige el repositorio limpio |
| `Authentication failed` al hacer push | El token caducó. Ver la sección de arriba |
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

## 3. Compartir la presentación clase por clase

Cada clase se comparte en **su propio PDF**, con solo lo que se vio ese día. En el
preámbulo, junto al interruptor de las respuestas:

```latex
\setcounter{claseActual}{0}
```

| Valor | Qué sale |
|---|---|
| **1 a 5** | únicamente esa clase |
| **0** | la semana completa, para dar clase y para armar el parcial |

Páginas de cada archivo, ya compiladas y verificadas:

| | Clase 1 | 2 | 3 | 4 | 5 | Completa (0) |
|---|---|---|---|---|---|---|
| Semana 1 | 15 | 16 | 10 | 7 | 15 | 55 |
| Semana 2 | 14 | 17 | 10 | 7 | 8 | 52 |

La portada y la diapositiva de despedida salen en **todos** los archivos, para que cada
uno se identifique solo y cierre bien. Por eso las clases sueltas suman más que la
semana completa.

### Cómo nombrarlos en Teams

Con la fecha por delante, para que la carpeta quede ordenada sola:

```
2026-0818 Presentacion.pdf
2026-0820 Presentacion.pdf
```

Como cada archivo trae una sola clase, no hay que reemplazar nada. Se van acumulando en
orden, y al llegar el parcial basta con recompilar con `0` para tener el material de esas
semanas en un solo documento.

### El ritual de cada día, de dos minutos

1. Poner en `claseActual` el número de la clase que se acaba de dar.
2. Recompilar en Overleaf y descargar el PDF.
3. Renombrarlo con la fecha y subirlo a Teams.

**Los dos interruptores se combinan.** Si la clase del día trae la práctica entregable,
se comparte con `\respuestasfalse` mientras la entrega siga abierta, y se vuelve a subir
con `\respuestastrue` al cerrarla.

**Si algo truena al compilar**, casi siempre es un `\fi` borrado. Cada bloque abre con
`\bloqueClase{N}\ifmostrar` y cierra con su `\fi`, rotulado con el número de clase al
que pertenece.

## 4. Subir una presentación a Overleaf

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

## 5. Importar preguntas a Moodle

El procedimiento completo está en `moodle/ESQUEMA-Moodle.md`, con los ajustes
que hay que marcar para que la retroalimentación se vea.

Lo esencial: los `.xml` son **paquetes de preguntas**, no cuestionarios. Se
importan en *Banco de preguntas ▸ Importar*, con **Formato XML de Moodle** y con
la casilla **Obtener categoría desde el archivo** marcada. El cuestionario es una
actividad aparte que se arma después.

Importar dos veces el mismo archivo **duplica** las preguntas.
