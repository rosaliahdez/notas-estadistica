# Esquema de cuestionarios en Moodle · Estadística LCC 2026-2

## Cómo vamos a trabajarlo

Un cuestionario por unidad, más uno inicial de herramientas. Cada uno se arma
**después** de que la unidad se dio en clase, no antes, para que los reactivos usen
los mismos ejemplos, el mismo vocabulario y los mismos datos que se vieron. Así el
cuestionario refuerza la clase en lugar de competir con ella.

El orden de trabajo de cada unidad, entonces, es: se pulen las diapositivas, se da la
clase, y con lo que pasó en clase se cierran los reactivos.

## Estado del banco

El banco se reconstruye desde cero, categoría por categoría, conforme cada unidad se
da en clase. Del banco heredado se recuperaron 50 reactivos y se van reescribiendo
antes de volver a importarlos. Esta es la situación y el plan:

| Cuestionario | Se abre al terminar | Reactivos que hay | Meta | Qué falta hacer |
|---|---|---|---|---|
| **U0 Herramientas: R y RStudio** | Al cerrar el bloque de R | **14** ✅ | 14 | Listo, con retroalimentación completa |
| **U1 Exploración de datos** | Unidad 1 | **12** ✅ | 12 | Listo. Los 4 heredados reescritos y 8 nuevos |
| U2 Descriptiva: medidas y gráficas | Unidad 2 | 11 | 14 | Revisar redacción, agregar 3 de interpretación |
| U3 Correlación y regresión descriptiva | Unidad 3 | 3 | 10 | Redactar 7 |
| U4 Muestreo | Unidad 4 | 2 | 10 | Redactar 8 |
| U5 Diseño de experimentos | Unidad 5 | 6 | 10 | Redactar 4 |
| U6 Distribuciones muestrales y TCL | Unidad 6 | 0 | 8 | Redactar los 8 |
| U7 Intervalos y prueba de hipótesis | Unidad 7 | 11 | 14 | Revisar redacción, agregar 3 |
| U8 Inferencia para dos medias | Unidad 8 | 5 | 12 | Redactar 7 |
| U8c Complemento: varianzas | Unidad 8 | 6 | 6 | **Renombrar la categoría** (ver abajo) |
| U9 Proporciones y ji-cuadrada | Unidad 9 | 6 | 10 | Redactar 4 |
| U10 ANOVA | Unidad 10 | 2 | 10 | Redactar 8 |
| U11 Inferencia en regresión | Unidad 11 | 0 | 8 | Redactar los 8 |

Entregados y listos para importar: **26** (U0 y U1). El resto se arma unidad por unidad.

**Al reimportar, cuidar el nombre de una categoría.** En el banco heredado se llama
*"U8c Complemento MCD: pruebas para varianzas"*. Ese nombre lo alcanzan a ver los
estudiantes, y quedamos en no hacer referencias explícitas a la maestría. Al rehacerla
conviene dejarla como *"U8c Complemento: pruebas para varianzas"*.

**Una dependencia que conviene evitar.** Un reactivo heredado venía en formato
**STACK**, que necesita un plugin instalado en el servidor. Se convirtió a
emparejamiento, que es de Moodle base. Si aparecen más reactivos STACK al revisar las
otras unidades, se hará lo mismo, salvo que Ramanujan ya lo tenga instalado.

## Cómo se importa, paso a paso

Conviene aclarar algo del formato, porque el nombre confunde. Los archivos `.xml` que
entrego **no son cuestionarios**, son **paquetes de preguntas**. Lo que pasa es que el
formato de Moodle usa `<quiz>` como etiqueta que envuelve todo, aunque adentro solo
haya preguntas. Al importarlo, cada reactivo **se guarda por separado en el banco**,
dentro de la categoría que viene declarada en el archivo. No se crea ninguna actividad.

Es exactamente lo que ya sabes hacer, importar preguntas. Nada nuevo.

### 1. Meter las preguntas al banco

1. Entrar al curso.
2. **Moodle 4**: menú **Más ▸ Banco de preguntas**, y arriba el desplegable **Importar**.
   **Moodle 3**: bloque de administración, **Banco de preguntas ▸ Importar**.
3. Formato: **Formato XML de Moodle**.
4. En *General*, dejar marcado **Obtener categoría desde el archivo**. Así se crea sola
   la categoría "U0 Herramientas: R y RStudio" y las preguntas caen ahí. Si se desmarca,
   todo se va a la categoría que esté seleccionada arriba, revuelto.
5. Arrastrar el archivo y pulsar **Importar**.
6. Moodle muestra la lista de lo que va a importar. Revisar que estén los 14 nombres y
   pulsar **Continuar**.

Si se importa dos veces el mismo archivo, las preguntas quedan **duplicadas**. Moodle no
las reconoce como repetidas.

### 2. Crear el cuestionario que las usa

El cuestionario es una actividad aparte, y se arma después.

1. **Activar edición ▸ Añadir una actividad ▸ Cuestionario**. Ponerle nombre y guardar.
2. Ajustarlo según la tabla de arriba, sobre todo *Comportamiento* y *Opciones de
   revisión*, que es de donde depende que se vea la retroalimentación.
3. Entrar al cuestionario, pestaña **Preguntas ▸ Añadir**.
4. Elegir **"una pregunta aleatoria"**, no "del banco de preguntas". Seleccionar la
   categoría y cuántas se quieren por intento.

Para los cuestionarios de práctica de este curso, en el paso 4 conviene agregar
**todas** las preguntas de la categoría, no una selección. El porqué está explicado
más arriba, en la discusión sobre cuántas preguntas por intento.

## Sobre STACK

Confirmado que Ramanujan lo tiene, así que se puede usar. Vale la pena saber dónde
paga y dónde no.

**Donde paga: cálculo con datos aleatorios.** STACK genera los números al vuelo, así
que cada estudiante calcula con su propia muestra y no hay respuesta que copiar. Las
unidades donde eso rinde son:

| Unidad | Qué se puede parametrizar |
|---|---|
| U2 | Media, mediana, desviación y coeficiente de variación de una muestra chica |
| U6 | Estandarizar un valor, calcular $z$ y su probabilidad |
| U7 | Estadístico $t$, grados de libertad, intervalo de confianza |
| U8 | Diferencia de medias, con muestras generadas al azar |
| U9 | Frecuencias esperadas y contribución de cada celda al $\chi^2$ |
| U10 | Completar la tabla de ANOVA a partir de dos o tres celdas dadas |

Ahí STACK además permite evaluar **el procedimiento** y no solo el número final, y
aceptar respuestas equivalentes escritas de otra forma.

**Donde no paga: los reactivos conceptuales.** En la Unidad 1 casi todo es tipo de
variable, escala y tipo de estudio. No hay número que aleatorizar, y armar la misma
pregunta en STACK cuesta bastante más trabajo que en opción múltiple. Para que no todos
vean lo mismo, ahí sirve mejor lo del paso 4: tener más reactivos en la categoría de los
que se piden por intento.

Por eso el reactivo heredado de observacional contra experimental lo dejé en
emparejamiento. Su versión original en STACK sigue guardada en el banco heredado, así
que no se perdió nada.

**Propuesta.** Cuando llegues a la Unidad 2, armo esa categoría con tres o cuatro
reactivos STACK de cálculo con datos aleatorios, más los conceptuales en opción
múltiple. Así pruebas el plugin con algo que de verdad lo aprovecha, y de paso vemos
cómo se comporta en tu servidor antes de depender de él para un parcial.

## Por qué no aparecía la retroalimentación

Son dos cosas, y las dos hay que arreglar.

**1. Los reactivos heredados no la traen.** De los 50, solo 1 tiene retroalimentación
general, y **ninguno** tiene retroalimentación por opción. Aunque Moodle estuviera bien
configurado, no había nada que mostrar. Los reactivos nuevos ya vienen con las tres
capas: por opción, general, y mensaje al acertar.

**2. Hay que habilitarla en los ajustes del cuestionario.** No se muestra por omisión.
En *Editar ajustes* del cuestionario:

- **Comportamiento de las preguntas → Cómo se comportan las preguntas.** Con
  *Retroalimentación diferida* (el valor por omisión) el estudiante no ve nada hasta
  enviar todo. Para práctica conviene **Retroalimentación inmediata**, que muestra el
  comentario apenas contesta cada pregunta.
- **Opciones de revisión.** Es una cuadrícula de casillas. Hay que marcar
  **Retroalimentación específica** y **Retroalimentación general** en la columna
  *Inmediatamente después del intento* (y también en *Durante el intento* si se eligió
  retroalimentación inmediata). Sin esas casillas, el texto existe pero no se muestra.

## Cómo conviene configurar cada cuestionario

| Ajuste | Valor sugerido | Por qué |
|---|---|---|
| Intentos permitidos | Ilimitados | Es práctica, no examen. La nota es por participar y aprender |
| Método de calificación | Calificación más alta | Premia insistir |
| Comportamiento | Retroalimentación inmediata | El comentario llega cuando todavía importa |
| Orden de las preguntas | Al azar | Dos personas sentadas juntas no ven lo mismo en la pantalla |
| Orden de las opciones | Al azar | Ya viene activado en los reactivos |
| Cuántas preguntas por intento | **Todas**, mientras el banco sea chico | Ver la discusión de abajo |
| Puntuación de cada pregunta | La misma, 1 punto | Ver la discusión de abajo |
| Penalización por reintento | 0 | Es práctica. Ya viene en 0 en los reactivos |
| Cierre | Antes del parcial de la unidad | Que sirvan de repaso |

### ¿Todas las preguntas o una selección al azar?

Conviene distinguir dos situaciones, porque la respuesta cambia.

**En un cuestionario de práctica, con intentos ilimitados, van todas.** Sacar 8 de 14
no evita que se copien, porque con intentos ilimitados cualquiera puede reintentar hasta
ver las 14. Y en cambio sí tiene un costo: alguien podría terminar la unidad sin
haberse encontrado nunca con el reactivo de los ceros de la tabla de contingencia, que
es de los que más enseñan. Para que dos personas sentadas juntas no vean lo mismo basta
con **aleatorizar el orden** de las preguntas y de las opciones, que no cuesta nada.

**La selección al azar paga en dos casos.** Uno, cuando la categoría crece bastante más
que el cuestionario que se quiere aplicar, por ejemplo 25 reactivos en el banco y 10 en
el cuestionario, por tiempo de clase. Dos, cuando el cuestionario es **calificable con
un solo intento**, como un parcial en línea, donde sí importa que cada quien tenga su
propia versión.

Con 14 y 12 reactivos, que es donde estamos, van todos.

### ¿Todos valen lo mismo?

**Sí, un punto cada uno, que es lo que Moodle pone por omisión.** No hay que configurar
nada.

Tres razones. Ponerle más peso a unos que a otros supone que sabemos cuáles son más
difíciles, y todavía no lo sabemos; después del primer semestre las estadísticas de
Moodle lo dirán. Es más fácil de explicar al grupo. Y si algún día se usa selección al
azar, los pesos desiguales harían que dos intentos no sean comparables.

Hay un detalle que ya trabaja a favor sin que haya que tocarlo. Los reactivos de
**emparejamiento** y los de **seleccionar palabras faltantes** se califican por partes.
Quien acierta tres de cuatro casillas obtiene 0.75 del punto, no cero. Así que el
reactivo que exige cuatro juicios ya reparte su punto entre esos cuatro juicios.

La suma cruda es 14 puntos. Lo que se lleva a la libreta de calificaciones lo decide
**Calificación máxima**, en los ajustes del cuestionario. Si ahí se pone 10, Moodle
escala solo, y ese 10 entra al 20 % de cuestionarios del curso.

**Cuándo sí cambiaría los pesos.** En un examen, no en una práctica. Ahí un
emparejamiento de cinco pares y una de verdadero o falso no deberían valer igual, porque
la de verdadero o falso se acierta la mitad de las veces al azar. En ese caso les
pondría 2 puntos a los de varias partes y 1 a los demás.

## Qué se les corrigió a los reactivos heredados

El contenido estaba bien; el problema era de redacción. Dos ejemplos concretos de la
Unidad 1.

El de escalas de medición abría con tres oraciones de contexto que no hacían falta,
*"Los investigadores analizaron cuatro variables diferentes para entender mejor las
preferencias y características de los compradores"*, antes de llegar a la tarea. Ahora
arranca en una línea y las cuatro variables quedan a la vista.

El del centro comercial dedicaba cinco renglones a explicar que el objetivo era *"mejorar
la experiencia del cliente y aumentar las ventas"*, que no tiene nada que ver con lo que
se evalúa. Además traía una coma que separaba el sujeto del verbo. Se recortó a la
pregunta y las cuatro variables.

El de análisis exploratorio tenía tres distractores que hablaban los tres de modelos
predictivos, así que se acertaba por descarte sin saber el tema. Los nuevos distractores
son confusiones reales, como creer que calcular un valor p es parte de explorar.

## Cómo están redactados los reactivos nuevos

Estas son las reglas que se siguieron, y con las que se revisarán las unidades que faltan:

1. **Una idea por reactivo.** Si el enunciado necesita dos condiciones para responderse,
   se parte en dos reactivos.
2. **Enunciado corto y en voz activa.** Primero el contexto, luego la pregunta, al final
   las opciones.
3. **Las cuatro opciones parecidas en largo.** La opción más larga no puede ser siempre
   la correcta.
4. **Los distractores son errores reales**, de los que efectivamente se cometen en clase,
   no opciones absurdas de relleno.
5. **Retroalimentación en tres capas:**
   - *por opción*: por qué esa opción específica está bien o mal;
   - *general*: el concepto completo, que ve todo el grupo, haya acertado o no;
   - *al acertar*: una frase de refuerzo que agrega algo, no un "correcto" pelón.
6. **Nada de "todas las anteriores" ni "ninguna de las anteriores".** Miden lectura, no
   estadística.

## Archivos

Se les cambió el nombre de "Cuestionario" a "Banco", porque eso es lo que son.

- `Banco_U0_Herramientas_R.xml` — 14 reactivos de R y RStudio.
- `Banco_U1_Exploracion.xml` — 12 reactivos de la Unidad 1.
- `generar-banco-U0-R.py` y `generar-banco-U1.py` — los generadores. Conviene editar
  ahí y volver a correrlos, en lugar de tocar el XML a mano, porque validan la suma de
  fracciones y que ninguna opción se quede sin retroalimentación.
- `Banco_Estadistica_Reorganizado_2026-2.xml` y `Reactivos_U5_Diseno_Experimentos.xml`
  — el banco heredado, del que se van reescribiendo las unidades conforme se dan.
