# Control de calidad en el aula: los pingüinos Marinela

Actividad opcional, **fuera de la semana 1**. Las diapositivas están en
`presentaciones/actividad-control-calidad.tex`, como fragmento independiente que se
inserta con `\input{actividad-control-calidad}` donde convenga.

## Cuándo conviene usarla

La actividad tiene dos mitades que rinden en momentos distintos del curso:

- **La discusión del diseño** (las dos primeras diapositivas) cae bien en la
  **unidad 5**, producción de datos, que es donde se estudian control,
  aleatorización y ciego.
- **El análisis** cae bien en la **unidad 7**, que es donde se aprende la prueba
  contra un valor de referencia. Esa es la pregunta principal de la actividad.

Lo natural es **capturar en la unidad 5 y analizar en la 7**, con los mismos datos.
Así la captura tiene una promesa concreta y el análisis llega con datos propios.

## Por qué un producto industrial funciona mejor que un pan artesanal

Un pan hecho a mano varía porque está hecho a mano, y no hay contra qué comparar. Un
producto industrial trae dos cosas que un pan artesanal no:

1. **Un valor de referencia impreso en el empaque**: el contenido neto declarado. Ese
   número es el $\mu_0$ de la prueba de hipótesis, y no lo puso el profesor.
2. **La promesa de ser idéntico**. Toda la teoría del control de calidad vive de que
   la promesa no se cumple exactamente, y de cuantificar por cuánto.

Además existe la **NOM-002-SCFI**, norma mexicana que fija las tolerancias del
contenido neto y los **planes de muestreo** para verificarlo. Es muestreo (unidad 4) y
prueba de hipótesis (unidad 7) con fuerza de ley, aplicados a un producto de la tienda
de la esquina. Vale la pena mostrarla aunque sea de pasada.

## El valor de referencia

Se lee del empaque que se compre. Según las presentaciones que se anuncian
comercialmente, los **mini** rondan los 25 g por pieza y los **grandes** los 40 g,
pero el número operativo es **el que diga la envoltura**, y conviene que sean los
estudiantes quienes lo lean.

Para 20 personas, los mini en caja salen más a cuenta y además dan lotes distintos
para comparar.

## El diseño

Cada pieza se mide **dos veces**, por dos observadores distintos, con el orden
contrabalanceado en dos bloques de diez:

| Bloque | Piezas | Primera medición | Segunda medición |
|---|---|---|---|
| 1 | las de índice par | Observador A | Observador B |
| 2 | las de índice impar | Observador B | Observador A |

Se mide la **masa** con báscula de 0.1 g y el **diámetro** con regla. La distinción
importa, y es la parte más elegante de la actividad:

- La **masa** la lee una báscula digital, así que **no depende de quién la lea**. Pero
  sí baja con la manipulación, porque se desprende chocolate.
- El **diámetro** lo lee una persona con una regla, así que **sí depende del
  observador**, y en cambio la manipulación no lo cambia.

Un mismo diseño, dos fuentes de error distintas, cada una en la variable que le
corresponde.

## Preguntas y unidades

| Pregunta | Técnica | Unidad |
|---|---|---|
| ¿La masa promedio coincide con el contenido declarado? | Una muestra contra valor de referencia, `t.test(x, mu = declarado)` | 7 |
| ¿Cuánta variación hay de pieza a pieza? | Desviación estándar, coeficiente de variación | 2 |
| ¿Qué proporción queda por debajo de lo declarado? | Estimación de una proporción | 9 |
| ¿Coinciden los dos observadores? | Prueba $t$ pareada | 8 |
| ¿Pierde masa al ser manipulada? | Prueba $t$ pareada | 8 |
| ¿Difieren dos lotes? | Dos muestras independientes | 8 |
| ¿Cuántas piezas harían falta para detectar medio gramo? | Tamaño de muestra y potencia | 7 |

Y una que **este diseño no puede contestar**: *¿cuál báscula es más precisa?*
Precisión es variabilidad al repetir, y aquí cada pieza se pesa una sola vez con cada
instrumento. Haría falta pesar la misma pieza varias veces. Es un cambio de diseño, no
una técnica más fina.

## La interpretación que vale la clase

Hay una **asimetría económica** en el llenado: llenar de menos incumple lo declarado y
arriesga sanción; llenar de más cumple pero cuesta, multiplicado por millones de
piezas. Por eso un proceso bien ajustado apunta **un poco por arriba** del valor
declarado.

Eso hace la hipótesis **unilateral** ($H_0: \mu = \mu_0$ contra $H_a: \mu > \mu_0$) y
cambia la lectura del resultado: si sale significativo, la conclusión no es que la
empresa engañe, sino que el proceso está ajustado por arriba, como corresponde.

## Los archivos de respaldo

Simulados, para que el análisis se pueda preparar antes de tener los datos reales.
**Conviene reemplazarlos** en cuanto exista la captura del grupo.

- `pinguinos-marinela-ejemplo.csv` — 20 renglones, uno por pieza (solo la primera
  medición). Columnas: `id`, `lote`, `masa_g`, `diametro_mm`.
- `pinguinos-marinela-diseno-ejemplo.csv` — 40 renglones, uno por **medición**, con
  `observador` y `orden`.

Se generan con `generar-control-calidad.py`, que al correr imprime la verificación de
cada efecto. Lo que se les sembró:

| Efecto sembrado | Magnitud | Qué debe salir |
|---|---|---|
| Llenado por arriba de lo declarado | $+1.1$ g | Se detecta: media 26.2 g contra 25 declarados, $t = 6.05$ |
| Pérdida de masa al manipular | $-0.12$ g | Se detecta: $-0.105$ g, $t = -3.90$ |
| Efecto del observador **sobre la masa** | $0$ | **No** se detecta, $t = 0.88$. La báscula no sabe quién la lee |
| Sesgo del observador B **en el diámetro** | $+0.5$ mm | Se detecta: $+0.79$ mm, $t = 3.52$ |
| Diferencia entre lotes | $+0.35$ g | **No** se detecta, $t = 1.61$, aunque es real: harían falta unas 92 piezas por lote |

Dos de los cinco efectos no se detectan, y por razones distintas: uno porque
verdaderamente no existe, y otro porque existe pero la muestra es demasiado chica.
Distinguir esos dos casos es justamente lo que se aprende en la unidad 7.
