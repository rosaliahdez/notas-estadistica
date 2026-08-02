# Celdas de R ejecutables en el libro (WebR / quarto-live)

Cómo activar la página `laboratorio-r.qmd`, donde el estudiante escribe y ejecuta
R **dentro del navegador**, sin instalar nada y sin servidor. Equivale a lo que hace
SageCell en las páginas de SageMath, pero para R y sin depender de un servicio externo.

> **Pruébalo antes de decidir.** Estos pasos no los pude ejecutar por ti (no tengo
> Quarto ni R en mi entorno), así que trátalos como una receta a validar. Si algo
> falla, mándame el mensaje de error y lo ajustamos.

## Pasos

**1. Instala la extensión** (una vez, desde la carpeta del repo):

```bash
quarto add r-wasm/quarto-live
```

Esto crea la carpeta `_extensions/r-wasm/live/`. **Debe subirse al repositorio**
(no la pongas en `.gitignore`), porque `quarto publish` la necesita.

**2. Cambia el formato del libro.** En `_quarto.yml`, sustituye `html:` por
`live-html:` conservando todas las opciones que ya tiene:

```yaml
format:
  live-html:          # <- antes decía html
    theme:
      - cosmo
      - theme.scss
    toc: true
    # ...el resto igual
```

**3. Agrega la página al índice.** En `_quarto.yml`, dentro de `chapters:`, añade
`laboratorio-r.qmd` donde quieras que aparezca (sugerencia: justo después de
`index.qmd`, para que esté disponible desde el primer día).

**4. Prueba localmente:**

```bash
quarto preview
```

Abre la página del laboratorio. La primera celda tardará unos segundos mientras el
navegador descarga R. Si las celdas aparecen con un botón para ejecutar, funcionó.

**5. Publica como siempre:** commit, push y `quarto publish gh-pages`.

## Qué esperar

- **La primera carga es lenta** (decenas de MB de R en WebAssembly). Después queda
  en caché del navegador y es rápida.
- **Solo pesa en las páginas que tienen celdas `{webr}`.** Por eso el libro conserva
  sus bloques `{r}` normales: esos se renderizan al compilar y no cuestan nada al lector.
- **No todos los paquetes están disponibles** en WebR. `ggplot2` y `dplyr` sí,
  pero cargarlos añade tiempo de descarga. Por eso el laboratorio usa R base
  (`mean`, `t.test`, `boxplot`), que arranca de inmediato.

## Los ejercicios con pistas y solución

La sintaxis que ya quedó escrita en `laboratorio-r.qmd`:

````markdown
```{webr}
#| exercise: nombre_del_ejercicio
datos <- c(1, 2, 3)
______
```

::: { .hint exercise="nombre_del_ejercicio"}
La pista que ve el estudiante si se atora.
:::

::: { .solution exercise="nombre_del_ejercicio"}
La solución, con su explicación.
:::
````

Los guiones bajos `______` marcan los huecos por completar. La extensión también
permite **verificación automática** de la respuesta con `gradethis`; si te interesa,
lo agregamos después.

## Si decides no usarlo

No pasa nada: borra `laboratorio-r.qmd` del `_quarto.yml` y deja `html:` como estaba.
El libro funciona igual. Los laboratorios con deslizadores (OJS) **no** dependen de
esto: esos ya funcionan sin extensiones.

## Referencias

- Documentación: <https://r-wasm.github.io/quarto-live/>
- Crear ejercicios: <https://r-wasm.github.io/quarto-live/exercises/exercises.html>
- WebR: <https://docs.r-wasm.org/webr/latest/>
