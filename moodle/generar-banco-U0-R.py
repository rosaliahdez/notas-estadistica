# -*- coding: utf-8 -*-
"""Genera el banco de herramientas: R y RStudio.
   Todos los reactivos llevan:
     - retroalimentacion por opcion (por que esa opcion esta bien o mal)
     - retroalimentacion general (el concepto, para quien acerto y para quien no)
     - mensaje de refuerzo al acertar
   Salida: Banco_U0_Herramientas_R.xml, listo para importar a Moodle.
"""
import xml.etree.ElementTree as ET, html, os

CAT = "$course$/top/Estadística LCC 2026-2/U0 Herramientas: R y RStudio"
partes = []

def cdata(x): return x  # se escribe con ET, que ya escapa

def q_abierta(tipo):
    return f'<question type="{tipo}">'

def bloque_multi(nombre, enunciado, general, opciones, single=True):
    """opciones: lista de (fraccion, texto, retro)"""
    op = "".join(
        f'  <answer fraction="{f}" format="html"><text><![CDATA[{t}]]></text>'
        f'<feedback format="html"><text><![CDATA[{r}]]></text></feedback></answer>\n'
        for f, t, r in opciones)
    return f'''<question type="multichoice">
  <name><text>{html.escape(nombre)}</text></name>
  <questiontext format="html"><text><![CDATA[{enunciado}]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[{general}]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.0000000</penalty>
  <hidden>0</hidden>
  <single>{'true' if single else 'false'}</single>
  <shuffleanswers>true</shuffleanswers>
  <answernumbering>abc</answernumbering>
  <correctfeedback format="html"><text><![CDATA[<p>Correcto.</p>]]></text></correctfeedback>
  <partiallycorrectfeedback format="html"><text><![CDATA[<p>Parcialmente correcto: hay más de una opción válida y falta alguna.</p>]]></text></partiallycorrectfeedback>
  <incorrectfeedback format="html"><text><![CDATA[<p>No es correcto. Vale la pena leer la explicación de abajo y volver a intentar.</p>]]></text></incorrectfeedback>
{op}</question>'''

def bloque_vf(nombre, enunciado, general, correcta, retro_v, retro_f):
    fv, ff = (100, 0) if correcta else (0, 100)
    return f'''<question type="truefalse">
  <name><text>{html.escape(nombre)}</text></name>
  <questiontext format="html"><text><![CDATA[{enunciado}]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[{general}]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.0000000</penalty>
  <hidden>0</hidden>
  <answer fraction="{fv}" format="moodle_auto_format"><text>true</text><feedback format="html"><text><![CDATA[{retro_v}]]></text></feedback></answer>
  <answer fraction="{ff}" format="moodle_auto_format"><text>false</text><feedback format="html"><text><![CDATA[{retro_f}]]></text></feedback></answer>
</question>'''

def bloque_emparejar(nombre, enunciado, general, pares):
    sub = "".join(
        f'  <subquestion format="html"><text><![CDATA[{a}]]></text>'
        f'<answer><text>{html.escape(b)}</text></answer></subquestion>\n' for a, b in pares)
    return f'''<question type="matching">
  <name><text>{html.escape(nombre)}</text></name>
  <questiontext format="html"><text><![CDATA[{enunciado}]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[{general}]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.0000000</penalty>
  <hidden>0</hidden>
  <shuffleanswers>true</shuffleanswers>
  <correctfeedback format="html"><text><![CDATA[<p>Correcto.</p>]]></text></correctfeedback>
  <partiallycorrectfeedback format="html"><text><![CDATA[<p>Hay algunas bien y algunas mal. Conviene revisar cuáles.</p>]]></text></partiallycorrectfeedback>
  <incorrectfeedback format="html"><text><![CDATA[<p>No es correcto. La explicación de abajo ordena las cinco.</p>]]></text></incorrectfeedback>
{sub}</question>'''

partes.append(f'''<question type="category">
  <category><text>{CAT}</text></category>
  <info format="html"><text><![CDATA[<p>Reactivos sobre el uso de R y RStudio: la interfaz, cargar paquetes y datos, tipos de datos, subconjuntos de una tabla y resúmenes por grupo. Corresponden al bloque de herramientas, antes de entrar a la Unidad 1. Pensados para intentos ilimitados y peso bajo: sirven para practicar, no para filtrar.</p>]]></text></info>
</question>''')

# ---------------------------------------------------------------- 1
partes.append(bloque_multi(
  "U0-01 Dónde se escribe el análisis",
  "<p>En este curso, ¿dónde conviene escribir el análisis?</p>",
  "<p>La consola sirve para probar; el <em>script</em> es donde se trabaja. Un análisis que solo "
  "existe en la consola no se guarda: no se puede repetir ni revisar después. Eso es lo que "
  "significa que un análisis sea <strong>reproducible</strong>.</p>",
  [(100, "En un <em>script</em> (archivo <code>.R</code>), ejecutando cada línea con Ctrl + Enter",
        "<p>Correcto. Y al guardarlo queda el registro completo de lo que se hizo, en orden.</p>"),
   (0, "Directamente en la consola, que para eso está",
       "<p>La consola es útil para probar algo rápido, pero lo que se teclea ahí no queda guardado.</p>"),
   (0, "En la pestaña Terminal",
       "<p>Esa pestaña no es R: es la línea de comandos del sistema operativo.</p>"),
   (0, "En la ventana Environment",
       "<p>Esa ventana solo <em>muestra</em> los objetos que existen; no se escribe código ahí.</p>")]))

# ---------------------------------------------------------------- 2
partes.append(bloque_multi(
  "U0-02 install.packages contra library",
  "<p>La semana pasada se instaló <code>palmerpenguins</code> en la computadora. Hoy se abre RStudio "
  "de nuevo y se quiere usar la tabla <code>penguins</code>. ¿Qué hay que hacer?</p>",
  "<p>Son dos acciones distintas: <code>install.packages()</code> <strong>baja e instala</strong> el "
  "paquete, y se hace <strong>una sola vez</strong>. <code>library()</code> lo <strong>carga en la "
  "sesión actual</strong>, y se hace <strong>cada vez</strong> que se abre R. Esta distinción explica "
  "buena parte de los errores de las primeras semanas.</p>",
  [(100, "Solo <code>library(palmerpenguins)</code>",
        "<p>Correcto. Ya está instalado; falta cargarlo en esta sesión.</p>"),
   (0, "Volver a correr <code>install.packages(\"palmerpenguins\")</code>",
       "<p>No hace falta, y tarda. Instalar es una vez; cargar es cada sesión.</p>"),
   (0, "Nada: si ya se instaló, queda disponible siempre",
       "<p>Instalado sí queda, pero cada sesión nueva arranca sin paquetes cargados.</p>"),
   (0, "Primero <code>install.packages()</code> y luego <code>library()</code>, siempre en ese orden",
       "<p>Ese es el orden la <em>primera</em> vez. Después basta con <code>library()</code>.</p>")]))

# ---------------------------------------------------------------- 3
partes.append(bloque_multi(
  "U0-03 NA se contagia",
  "<p>¿Qué devuelve <code>mean(c(3750, NA, 3250))</code>?</p>",
  "<p><code>NA</code> significa <em>no se sabe</em>. Si uno de los valores es desconocido, el promedio "
  "también lo es: por eso R contesta <code>NA</code> en lugar de ignorar el faltante en silencio. "
  "Para pedirle explícitamente que lo omita se escribe <code>mean(x, na.rm = TRUE)</code>. "
  "Obliga a que la decisión sea consciente.</p>",
  [(100, "<code>NA</code>",
        "<p>Correcto. R no decide por nosotros qué hacer con lo que falta.</p>"),
   (0, "3500, porque promedia los dos valores que sí existen",
       "<p>Eso ocurre solo si se agrega <code>na.rm = TRUE</code>. Sin eso, el resultado es <code>NA</code>.</p>"),
   (0, "2333.33, tomando el <code>NA</code> como cero",
       "<p>R nunca convierte un faltante en cero: son cosas distintas. Un dato desconocido no es un dato igual a cero.</p>"),
   (0, "Un mensaje de error",
       "<p>No hay error: la operación es válida y su resultado, legítimamente, es desconocido.</p>")]))

# ---------------------------------------------------------------- 4
partes.append(bloque_multi(
  "U0-04 Sintaxis del corchete",
  "<p>¿Qué extrae <code>penguins[1:5, c(\"species\", \"body_mass_g\")]</code>?</p>",
  "<p>La regla es <strong>corchete, renglones, coma, columnas, corchete</strong>. Antes de la coma van los "
  "renglones; después, las columnas. Dejar un lado vacío significa <em>todos</em>: "
  "<code>penguins[ , 1]</code> es la columna 1 completa y <code>penguins[1, ]</code> es el renglón 1 completo.</p>",
  [(100, "Los primeros 5 renglones, y de ellos solo esas dos columnas",
        "<p>Correcto. Cinco renglones por dos columnas.</p>"),
   (0, "Las columnas 1 a 5 de las variables mencionadas",
       "<p>El <code>1:5</code> está antes de la coma, así que se refiere a renglones, no a columnas.</p>"),
   (0, "Los renglones donde <code>species</code> vale entre 1 y 5",
       "<p>El corchete no filtra por valor así. Para filtrar se usa una condición, como <code>penguins[penguins$species == \"Gentoo\", ]</code>.</p>"),
   (0, "Un error, porque no se pueden mezclar números y nombres",
       "<p>Sí se puede: los renglones por número y las columnas por nombre.</p>")]))

# ---------------------------------------------------------------- 5
partes.append(bloque_vf(
  "U0-05 La pestaña Terminal",
  "<p>La pestaña <strong>Terminal</strong> de RStudio es otra consola de R, igual a la primera.</p>",
  "<p>La <strong>consola</strong> es el intérprete de R. La <strong>Terminal</strong> es la línea de "
  "comandos del <strong>sistema operativo</strong>: ahí se usa <code>git</code>, se navega entre "
  "carpetas o se arranca R sin RStudio escribiendo <code>R</code>. Están una junto a la otra, pero no "
  "son lo mismo.</p>",
  correcta=False,
  retro_v="<p>No: si se escribe <code>mean(1:10)</code> en la Terminal, no va a funcionar, porque ahí no está R esperando.</p>",
  retro_f="<p>Correcto. Son dos intérpretes distintos que comparten vecindario en la ventana.</p>"))

# ---------------------------------------------------------------- 6
partes.append(bloque_multi(
  "U0-06 tapply y dplyr contestan lo mismo",
  "<p>¿Cuál de estos pares de instrucciones contesta <strong>la misma</strong> pregunta?</p>",
  "<p>Las dos calculan la masa promedio <strong>por especie</strong>. <code>tapply()</code> es el "
  "camino de R base; <code>group_by()</code> con <code>summarise()</code> es el de <code>dplyr</code>. "
  "El resultado es el mismo: cambia la forma de escribirlo, no la estadística. En el curso usaremos "
  "<code>dplyr</code> porque se lee mejor cuando hay varios pasos encadenados.</p>",
  [(100, "<code>tapply(penguins$body_mass_g, penguins$species, mean)</code> &nbsp;y&nbsp; "
         "<code>penguins |&gt; group_by(species) |&gt; summarise(mean(body_mass_g))</code>",
        "<p>Correcto. Mismo número, dos escrituras.</p>"),
   (0, "<code>mean(penguins$body_mass_g)</code> &nbsp;y&nbsp; "
       "<code>penguins |&gt; group_by(species) |&gt; summarise(mean(body_mass_g))</code>",
       "<p>La primera da <strong>un</strong> promedio general; la segunda da <strong>uno por especie</strong>. No es la misma pregunta.</p>"),
   (0, "<code>dim(penguins)</code> &nbsp;y&nbsp; <code>summary(penguins)</code>",
       "<p><code>dim()</code> da el tamaño de la tabla; <code>summary()</code> resume cada columna. Son distintas.</p>"),
   (0, "<code>table(penguins$species)</code> &nbsp;y&nbsp; <code>tapply(penguins$body_mass_g, penguins$species, mean)</code>",
       "<p>La primera <em>cuenta</em> cuántos hay de cada especie; la segunda <em>promedia</em> la masa. Distinto.</p>")]))

# ---------------------------------------------------------------- 7
partes.append(bloque_multi(
  "U0-07 No such file or directory",
  "<p>Al leer un archivo, R contesta:</p>"
  "<pre>Error in file(file, \"rt\") : cannot open file 'datos/mis-datos.csv': No such file or directory</pre>"
  "<p>El archivo existe y el nombre está bien escrito. ¿Cuál es la causa más probable?</p>",
  "<p>R busca los archivos a partir de <strong>una</strong> carpeta: el directorio de trabajo. "
  "Se consulta con <code>getwd()</code> y se ve su contenido con <code>list.files()</code>. "
  "La forma recomendable de evitar este error es trabajar dentro de un <strong>Proyecto</strong> de "
  "RStudio y usar rutas relativas.</p>",
  [(100, "R está mirando otra carpeta: hay que revisar <code>getwd()</code>",
        "<p>Correcto. El mensaje dice que <em>desde donde R está parado</em> ese archivo no existe.</p>"),
   (0, "El archivo está dañado",
       "<p>Si estuviera dañado, R lo abriría y fallaría al interpretarlo. Aquí no logra ni abrirlo.</p>"),
   (0, "Falta instalar un paquete para leer CSV",
       "<p><code>read.csv()</code> viene en R base, no hace falta instalar nada.</p>"),
   (0, "El CSV tiene acentos y R no los soporta",
       "<p>Los acentos pueden verse mal, pero eso es otro problema y otro mensaje.</p>")]))

# ---------------------------------------------------------------- 8
partes.append(bloque_multi(
  "U0-08 Qué es un factor",
  "<p>En R, ¿qué es un <strong>factor</strong>?</p>",
  "<p>Un factor es el tipo con el que R representa una variable <strong>categórica</strong>: guarda los "
  "valores y además la lista de <strong>niveles</strong> posibles, incluso los que no aparecen en los "
  "datos. Por eso <code>table()</code> puede mostrar una categoría con cero casos, lo que resulta útil "
  "para no perder de vista lo que se esperaba observar.</p>",
  [(100, "Una variable categórica que además guarda la lista de categorías posibles",
        "<p>Correcto. Los valores y los niveles, juntos.</p>"),
   (0, "Cualquier vector de texto",
       "<p>Un vector de texto es de tipo <code>character</code>. El factor es distinto: tiene niveles declarados.</p>"),
   (0, "Un número con decimales",
       "<p>Eso es <code>numeric</code>.</p>"),
   (0, "Una tabla de dos dimensiones",
       "<p>Eso sería un <code>data.frame</code> o una matriz.</p>")]))

# ---------------------------------------------------------------- 9
partes.append(bloque_emparejar(
  "U0-09 Qué hace cada instrucción",
  "<p>Relacionar cada instrucción con lo que hace.</p>",
  "<p>Estas cinco son el primer contacto con cualquier tabla, y conviene correrlas <strong>antes</strong> "
  "de calcular nada: cuántos renglones hay, cómo se llaman las columnas, de qué tipo es cada una, "
  "cuántos faltantes tiene y en qué carpeta está trabajando R.</p>",
  [("<code>dim(penguins)</code>", "Cuántos renglones y cuántas columnas tiene la tabla"),
   ("<code>str(penguins)</code>", "El tipo de cada columna y sus primeros valores"),
   ("<code>summary(penguins)</code>", "Un resumen numérico de cada columna, con los faltantes contados"),
   ("<code>table(penguins$species)</code>", "Cuántos casos hay de cada categoría"),
   ("<code>getwd()</code>", "En qué carpeta está trabajando R")]))

# ---------------------------------------------------------------- 10
partes.append(bloque_multi(
  "U0-10 Aritmética de punto flotante",
  "<p>En la consola, <code>0.1 + 0.2 == 0.3</code> devuelve <code>FALSE</code>. ¿Por qué?</p>",
  "<p>No es un defecto de R: es <strong>aritmética de punto flotante</strong>, y ocurre igual en C, "
  "Python o Java. El número 0.1 no tiene representación exacta en binario, así que la suma queda "
  "0.30000000000000004. La consecuencia práctica para todo el curso: <strong>no comparar con "
  "<code>==</code> el resultado de un cálculo</strong>. Se usa <code>all.equal()</code> o se compara "
  "la diferencia contra una tolerancia.</p>",
  [(100, "Porque los decimales se guardan en binario y 0.1 no tiene representación exacta",
        "<p>Correcto. Y por eso conviene usar <code>all.equal(0.1 + 0.2, 0.3)</code>, que sí devuelve <code>TRUE</code>.</p>"),
   (0, "Porque R tiene un error de programación en la suma",
       "<p>No: cualquier lenguaje que use punto flotante da lo mismo. Es una limitación de la representación, no un error.</p>"),
   (0, "Porque debe usarse <code>=</code> en lugar de <code>==</code>",
       "<p><code>=</code> asigna y <code>==</code> compara. El operador está bien elegido.</p>"),
   (0, "Porque falta redondear con <code>round()</code>",
       "<p>Redondear disimula el síntoma. La comparación exacta de decimales sigue siendo mala práctica.</p>")]))

# ---------------------------------------------------------------- 11
partes.append(bloque_vf(
  "U0-11 Los índices empiezan en 1",
  "<p>En R, el primer elemento de un vector <code>x</code> se obtiene con <code>x[0]</code>.</p>",
  "<p>En R los índices <strong>empiezan en 1</strong>: el primer elemento es <code>x[1]</code>. "
  "Es una diferencia con C, Java o Python, donde empiezan en 0. <code>x[0]</code> no da error: "
  "devuelve un vector vacío, que es más difícil de detectar que un error.</p>",
  correcta=False,
  retro_v="<p>No. <code>x[0]</code> devuelve un vector vacío. El primer elemento es <code>x[1]</code>.</p>",
  retro_f="<p>Correcto. En R se cuenta desde 1, y <code>x[0]</code> devuelve un vector vacío en silencio.</p>"))

# ---------------------------------------------------------------- 12
partes.append(bloque_multi(
  "U0-12 Leer una instrucción anidada de R base",
  "<p>En R base, esta instrucción se lee <strong>de adentro hacia afuera</strong>:</p>"
  "<pre>nrow(penguins[penguins$body_mass_g &gt; mean(penguins$body_mass_g, na.rm = TRUE), ])</pre>"
  "<p>¿Qué hace?</p>",
  "<p>Se lee empezando por el paréntesis más interno. Primero <code>mean(...)</code> calcula "
  "el promedio general de la masa. Después el <strong>corchete</strong> se queda con los renglones "
  "cuya masa supera ese promedio. Y al final <code>nrow(...)</code> cuenta cuántos quedaron.</p>"
  "<p>Tres pasos que ocurren en un orden, pero escritos en el orden contrario. Esa distancia "
  "entre cómo se escribe y cómo se piensa es justamente lo que resuelve la tubería.</p>",
  [(100, "Cuenta cuántos pingüinos pesan más que el promedio general",
        "<p>Correcto. Y nótese que hubo que leerla de adentro hacia afuera para descubrirlo.</p>"),
   (0, "Calcula el promedio de la masa de los pingüinos más pesados",
       "<p>El promedio se calcula, pero solo como paso intermedio para poder comparar. El resultado final es un conteo, porque la función de más afuera es <code>nrow()</code>.</p>"),
   (0, "Devuelve la masa del pingüino más pesado",
       "<p>Eso sería <code>max(penguins$body_mass_g, na.rm = TRUE)</code>. Aquí no aparece ningún máximo.</p>"),
   (0, "Cuenta cuántos pingüinos tienen la masa faltante",
       "<p>Eso sería <code>sum(is.na(penguins$body_mass_g))</code>. El <code>na.rm = TRUE</code> de aquí solo sirve para que el promedio se pueda calcular.</p>")]))

# ---------------------------------------------------------------- 13
partes.append(bloque_multi(
  "U0-13 La misma instrucción, con dplyr",
  "<p>Esta instrucción de R base cuenta cuántos pingüinos pesan más que el promedio general:</p>"
  "<pre>nrow(penguins[penguins$body_mass_g &gt; mean(penguins$body_mass_g, na.rm = TRUE), ])</pre>"
  "<p>¿Cuál de estas tuberías hace lo mismo?</p>",
  "<p>La tubería se lee <strong>en el orden en que ocurren los pasos</strong>. Toma "
  "<code>penguins</code>, <em>y luego</em> quédate con los que superan el promedio, "
  "<em>y luego</em> cuéntalos. La versión de R base dice exactamente lo mismo, pero hay que "
  "descifrarla de adentro hacia afuera.</p>"
  "<p>No es que una sea más rápida ni más potente. Es que una se lee como una secuencia de "
  "pasos y la otra como una composición de funciones.</p>",
  [(100, "<pre>penguins |&gt;\n  filter(body_mass_g &gt; mean(body_mass_g, na.rm = TRUE)) |&gt;\n  nrow()</pre>",
        "<p>Correcto. Dentro de <code>filter()</code> ya no hace falta escribir <code>penguins$</code>, porque la tubería ya entregó la tabla.</p>"),
   (0, "<pre>penguins |&gt;\n  filter(body_mass_g &gt; mean(body_mass_g)) |&gt;\n  nrow()</pre>",
       "<p>Casi. Sin <code>na.rm = TRUE</code>, el promedio vale <code>NA</code>, toda comparación contra <code>NA</code> vale <code>NA</code>, y <code>filter()</code> descarta esos renglones. El resultado sería <strong>0</strong>. Es el error más común de la semana.</p>"),
   (0, "<pre>penguins |&gt;\n  summarise(mean(body_mass_g, na.rm = TRUE)) |&gt;\n  nrow()</pre>",
       "<p>Esto devuelve <strong>1</strong>, porque <code>summarise()</code> deja una tabla de un solo renglón con el promedio. Se cuenta el resumen, no los pingüinos.</p>"),
   (0, "<pre>penguins |&gt;\n  arrange(desc(body_mass_g)) |&gt;\n  nrow()</pre>",
       "<p>Ordenar no descarta a nadie, así que esto devuelve los 344 pingüinos.</p>")]))

# ---------------------------------------------------------------- 14
partes.append(bloque_multi(
  "U0-14 Composición contra secuencia",
  "<p>La expresión anidada <code>f(g(h(x)))</code> y la tubería "
  "<code>x |&gt; h() |&gt; g() |&gt; f()</code> dan el mismo resultado. "
  "¿Cuál es entonces la diferencia entre las dos?</p>",
  "<p>La diferencia es de <strong>lectura</strong>, no de resultado ni de velocidad. La "
  "expresión anidada es una <em>composición de funciones</em>, y se descifra de adentro hacia "
  "afuera, al revés de como se piensa. La tubería es una <em>secuencia de pasos</em> en el "
  "orden en que ocurren.</p>"
  "<p>Por eso el curso usa <code>dplyr</code>. No porque sea más corto, sino porque cuando hay "
  "cuatro o cinco pasos encadenados, uno se entiende al leerlo y el otro hay que reconstruirlo.</p>",
  [(100, "La tubería se lee en el mismo orden en que ocurren los pasos, de izquierda a derecha",
        "<p>Correcto. Y esa ventaja crece con el número de pasos: con uno solo da igual, con cinco no.</p>"),
   (0, "La tubería se ejecuta más rápido",
       "<p>El costo es prácticamente el mismo. La ventaja es de legibilidad, no de rendimiento.</p>"),
   (0, "La expresión anidada no admite argumentos adicionales",
       "<p>Sí los admite. En el ejemplo de esta serie, <code>na.rm = TRUE</code> va dentro de una función anidada sin problema.</p>"),
   (0, "La tubería <code>|&gt;</code> solo funciona con paquetes del <em>tidyverse</em>",
       "<p>No. El operador <code>|&gt;</code> es parte de <strong>R base</strong> desde la versión 4.1, y funciona con cualquier función. Lo que sí viene del <em>tidyverse</em> es el operador <code>%&gt;%</code>, que es anterior y muy parecido.</p>")]))

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n' + "\n".join(partes) + "\n</quiz>\n"
aqui=os.path.dirname(os.path.abspath(__file__))
ruta=os.path.join(aqui,"Banco_U0_Herramientas_R.xml")
open(ruta,"w",encoding="utf-8").write(xml)

# ------- validación -------
r=ET.parse(ruta).getroot()
tipos={}; sin_retro=[]; n=0
for q in r.findall('question'):
    tp=q.get('type')
    if tp=='category': continue
    n+=1; tipos[tp]=tipos.get(tp,0)+1
    nom=q.find('name/text').text
    gf=q.find('generalfeedback/text')
    if gf is None or not (gf.text or '').strip(): sin_retro.append(nom+" (general)")
    for a in q.findall('answer'):
        fb=a.find('feedback/text')
        if fb is None or not (fb.text or '').strip(): sin_retro.append(nom+" (opción)")
    if tp=='multichoice':
        tot=sum(float(a.get('fraction')) for a in q.findall('answer') if float(a.get('fraction'))>0)
        assert abs(tot-100)<0.01, f"{nom}: las fracciones correctas suman {tot}"
print(f"XML válido. Reactivos: {n} -> {tipos}")
print("sin retroalimentación:", sin_retro or "ninguno")
