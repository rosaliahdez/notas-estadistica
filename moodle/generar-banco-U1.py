# -*- coding: utf-8 -*-
"""Cuestionario de la Unidad 1. Los cuatro reactivos heredados se conservan en
   contenido, con el enunciado acortado, la gramática revisada y retroalimentación
   agregada. El que venía en formato STACK se convirtio a emparejamiento, para que
   no dependa de que el plugin este instalado en Moodle."""
import xml.etree.ElementTree as ET, html, os, re

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


def bloque_gapselect(nombre, enunciado, general, opciones):
    """opciones: lista de (texto, grupo). El enunciado lleva [[1]], [[2]]..."""
    op="".join(f'  <selectoption><text>{t}</text><group>{g}</group></selectoption>\n' for t,g in opciones)
    return f"""<question type="gapselect">
  <name><text>{html.escape(nombre)}</text></name>
  <questiontext format="html"><text><![CDATA[{enunciado}]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[{general}]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.0000000</penalty>
  <hidden>0</hidden>
  <shuffleanswers>1</shuffleanswers>
  <correctfeedback format="html"><text><![CDATA[<p>Correcto en todas.</p>]]></text></correctfeedback>
  <partiallycorrectfeedback format="html"><text><![CDATA[<p>Hay algunas bien y algunas mal. Conviene revisar cuáles antes de reintentar.</p>]]></text></partiallycorrectfeedback>
  <incorrectfeedback format="html"><text><![CDATA[<p>No es correcto. La explicación de abajo ordena los cuatro casos.</p>]]></text></incorrectfeedback>
{op}</question>"""

CAT = "$course$/top/Estadística LCC 2026-2/U1 Exploración de datos"
partes = []
partes.append(f"""<question type="category">
  <category><text>{CAT}</text></category>
  <info format="html"><text><![CDATA[<p>Individuos y variables, tipos y escalas de medición, estudio observacional contra experimento, y lectura de gráficas. Corresponde a la Unidad 1 del curso. Los cuatro reactivos heredados se conservaron en contenido, con el enunciado acortado y con retroalimentación agregada.</p>]]></text></info>
</question>""")

# ============ 1. HEREDADO, reescrito: escalas de medición ============
partes.append(bloque_gapselect(
  "U1-01 Escalas de medición en un estudio de mercado",
  "<p>En una encuesta a clientes se registraron cuatro variables. Indicar la escala de medición de cada una.</p>"
  "<ul>"
  "<li><strong>Edad</strong> del comprador, en años cumplidos: [[1]]</li>"
  "<li><strong>Satisfacción</strong> con el producto, de <em>muy baja</em> a <em>muy alta</em>: [[2]]</li>"
  "<li><strong>Método de pago</strong> (efectivo, tarjeta, transferencia): [[3]]</li>"
  "<li><strong>Temperatura</strong> del local en grados Celsius: [[4]]</li>"
  "</ul>",
  "<p>La escala decide qué operaciones tienen sentido.</p><ul>"
  "<li><strong>Nominal</strong>, solo distingue categorías. No hay orden.</li>"
  "<li><strong>Ordinal</strong>, hay orden pero las distancias no están definidas. Entre <em>baja</em> y <em>media</em> no hay la misma distancia garantizada que entre <em>media</em> y <em>alta</em>.</li>"
  "<li><strong>Intervalo</strong>, hay orden y distancias, pero el cero es convencional. 0 °C no es ausencia de temperatura, y por eso 20 °C no es el doble de calor que 10 °C.</li>"
  "<li><strong>Razón</strong>, hay orden, distancias y cero absoluto. Alguien de 40 años sí tiene el doble de edad que alguien de 20.</li></ul>"
  "<p>La edad es de razón y no de intervalo justamente por el cero.</p>",
  [("Razón",1),("Ordinal",1),("Nominal",1),("Intervalo",1)]))

# ============ 2. HEREDADO, reescrito: tipos de variable ============
partes.append(bloque_gapselect(
  "U1-02 Tipos de variable en una encuesta",
  "<p>Una encuesta en un centro comercial incluye estas cuatro preguntas. Indicar de qué tipo es cada respuesta.</p>"
  "<ul>"
  "<li>¿Cuántos minutos duró su visita? [[1]]</li>"
  "<li>¿En qué piso entró al centro comercial? [[2]]</li>"
  "<li>¿Cuánto gastó hoy, en pesos? [[3]]</li>"
  "<li>¿Usó alguna promoción? (sí o no) [[4]]</li>"
  "</ul>",
  "<p>El criterio no es si la respuesta se escribe con números, sino si esos números "
  "<strong>miden una cantidad</strong>.</p>"
  "<p>El piso se anota con un número, pero funciona como <strong>etiqueta</strong>. Promediar "
  "pisos no significa nada, igual que promediar el año de observación en los pingüinos.</p>"
  "<p>Los minutos y el gasto sí son cantidades, así que son <strong>cuantitativas</strong>. "
  "El uso de promoción tiene dos categorías, así que es <strong>categórica binaria</strong>.</p>",
  [("Cuantitativa",1),("Categórica",1),("Cuantitativa",1),("Categórica",1)]))

# ============ 3. HEREDADO, reescrito: qué es explorar datos ============
partes.append(bloque_multi(
  "U1-03 Qué se hace en un análisis exploratorio",
  "<p>¿Cuál de estas actividades forma parte de un <strong>análisis exploratorio de datos</strong>?</p>",
  "<p>Explorar es <strong>mirar</strong> antes de concluir. Se resume, se grafica, se buscan "
  "valores raros y datos faltantes, y se detectan grupos escondidos. Todavía no se afirma nada "
  "sobre la población.</p>"
  "<p>Afirmar algo sobre la población a partir de una muestra es <strong>inferencia</strong>, y "
  "llega hasta la unidad 6. Explorar primero no es un trámite: es lo que permite saber si la "
  "técnica que se piensa usar después tiene sentido.</p>",
  [(100, "Graficar la distribución de cada variable para detectar patrones, valores raros y datos faltantes",
        "<p>Correcto. Y muchas veces ahí aparece lo importante, como los dos montículos del histograma de masa.</p>"),
   (0, "Calcular un valor p para decidir si dos grupos difieren",
       "<p>Eso es inferencia, no exploración. Llega hasta la unidad 7, y se apoya en lo que la exploración haya revelado.</p>"),
   (0, "Estimar el error de un modelo con datos de prueba",
       "<p>Eso pertenece a la evaluación de modelos predictivos, que queda fuera de este curso.</p>"),
   (0, "Elegir el tamaño de muestra necesario para el estudio",
       "<p>Eso se decide <strong>antes</strong> de tener los datos, y es tema de las unidades 4 y 7.</p>")]))

# ============ 4. HEREDADO (era STACK), convertido a emparejamiento ============
partes.append(bloque_emparejar(
  "U1-04 Observacional o experimental",
  "<p>Clasificar cada estudio.</p>",
  "<p>La pregunta que decide es una sola. <strong>¿Quién asignó el tratamiento?</strong> Si lo "
  "asignó el investigador, y además al azar, es un <strong>experimento</strong> y se puede "
  "hablar de causa. Si el grupo ya venía dado, es <strong>observacional</strong> y solo se puede "
  "hablar de asociación.</p>"
  "<p>Cuidado con confundir <em>planear bien la recolección</em> con <em>hacer un experimento</em>. "
  "El estudio de los pingüinos de Palmer se planeó con enorme cuidado y aun así es observacional, "
  "porque nadie asignó la especie ni el sexo de cada pingüino.</p>",
  [("Se asigna al azar a los pacientes al medicamento nuevo o a un placebo, y después se mide la presión arterial",
    "Experimental"),
   ("Se compara la temperatura corporal de lagartijas de ciudad y de campo, tal como se encuentran",
    "Observacional"),
   ("Se registran las horas de estudio y la calificación de un grupo de estudiantes, sin intervenir",
    "Observacional"),
   ("Se sortea qué bolsas de sustrato reciben cada mezcla y se mide el rendimiento del cultivo",
    "Experimental")]))

# ============ 5. NUEVO: individuo y variable ============
partes.append(bloque_multi(
  "U1-05 Qué es un individuo en la tabla de la cata",
  "<p>En la cata de galletas, cada juez califica cuatro marcas. ¿Qué es un <strong>individuo</strong> "
  "en esa tabla de datos?</p>",
  "<p>El individuo es la unidad de la que se toma <strong>una</strong> medición, y aquí cada "
  "medición es una calificación. Por eso la tabla lleva un renglón por juez y por marca, no un "
  "renglón por marca.</p>"
  "<p>Si se armara con un renglón por marca, se perdería quién calificó qué, y con eso se pierde "
  "la posibilidad de analizar nada. Confundir el individuo con el grupo es el error número uno "
  "de todo el curso.</p>",
  [(100, "Cada calificación, es decir, un renglón por juez y por marca",
        "<p>Correcto. Con 20 jueces y 4 marcas, la tabla tendría 80 renglones.</p>"),
   (0, "Cada marca de galleta",
       "<p>La marca es el <strong>tratamiento</strong>, no el individuo. Es una columna de la tabla, no un renglón.</p>"),
   (0, "Cada juez",
       "<p>El juez tampoco, porque cada juez aporta cuatro calificaciones, no una.</p>"),
   (0, "La calificación promedio de cada marca",
       "<p>Ese es un <strong>resumen</strong> que se calcula después. Los datos originales tienen que guardar cada calificación por separado.</p>")]))

# ============ 6. NUEVO: número que no es cantidad ============
partes.append(bloque_multi(
  "U1-06 Un número que no es una cantidad",
  "<p>En la tabla <code>penguins</code>, la columna <code>year</code> guarda 2007, 2008 o 2009. "
  "¿De qué tipo es esa variable?</p>",
  "<p>Se escribe con números, pero funciona como <strong>etiqueta</strong>. Promediar años de "
  "observación no significa nada, y esa es la prueba práctica para distinguirlas.</p>"
  "<p>Es ordinal y no nominal porque los años sí tienen un orden natural: 2007 va antes que 2008. "
  "El mismo criterio aplica a un código de muestra como <code>G134</code>, que es nominal.</p>",
  [(100, "Categórica ordinal, porque es una etiqueta que además tiene orden",
        "<p>Correcto. Y por eso en R conviene tratarla como <code>factor</code> y no como número.</p>"),
   (0, "Cuantitativa discreta, porque toma valores enteros",
       "<p>Ser entero no basta. La prueba es si promediar tiene sentido, y el promedio de los años de observación no significa nada.</p>"),
   (0, "Cuantitativa continua",
       "<p>No hay valores intermedios posibles ni la variable mide una cantidad.</p>"),
   (0, "Categórica nominal, porque es una etiqueta sin orden",
       "<p>Es etiqueta, sí, pero los años están ordenados. Nominal sería el código de la muestra o la isla.</p>")]))

# ============ 7. NUEVO: la escala hedónica ============
partes.append(bloque_multi(
  "U1-07 La escala de agrado de la cata",
  "<p>En la cata, el agrado se califica de 1 a 9, donde 1 es <em>me disgusta muchísimo</em> y 9 es "
  "<em>me gusta muchísimo</em>. ¿Cómo conviene describir esa variable?</p>",
  "<p>Estrictamente es <strong>ordinal</strong>, porque no hay garantía de que la distancia entre "
  "3 y 4 sea la misma que entre 8 y 9. Aun así, en análisis sensorial se trata como cuantitativa "
  "por convención, y por eso más adelante se le podrá calcular un promedio y aplicarle un ANOVA.</p>"
  "<p>Lo que no se vale es esconder la decisión. Conviene decir en el reporte que se tomó, porque "
  "un lector podría no estar de acuerdo y tiene derecho a saberlo.</p>",
  [(100, "Es ordinal, aunque por convención se trate como cuantitativa, y conviene decirlo",
        "<p>Correcto. Hacer explícita una decisión discutible es parte del oficio.</p>"),
   (0, "Es cuantitativa, porque son números del 1 al 9",
       "<p>Los números son etiquetas ordenadas. Nada garantiza que las distancias entre niveles consecutivos sean iguales.</p>"),
   (0, "Es nominal, porque son categorías de opinión",
       "<p>Son categorías, pero están claramente ordenadas de menor a mayor agrado.</p>"),
   (0, "Es cuantitativa continua, porque se puede promediar",
       "<p>Que se pueda calcular un promedio no vuelve continua a una variable. Entre 4 y 5 no hay valores posibles.</p>")]))

# ============ 8. NUEVO: la trampa de la tabla de contingencia ============
partes.append(bloque_multi(
  "U1-08 Ceros que no son un hallazgo",
  "<p>Al contar pingüinos por especie e isla aparecen varios ceros. Los Juanito solo están en "
  "Biscoe y los Barbijo solo en Dream. ¿Qué se puede concluir?</p>",
  "<p>Los ceros no son un descubrimiento sobre la naturaleza sino una consecuencia del "
  "<strong>diseño del muestreo</strong>. A los Juanito se los buscó únicamente en Biscoe y a los "
  "Barbijo únicamente en Dream, porque ahí están sus colonias.</p>"
  "<p>Una prueba estadística aplicada a esa tabla daría una asociación fuertísima, y aun así la "
  "conclusión sería falsa. Ninguna técnica avisa de esto. Solo avisa conocer el contexto y saber "
  "cómo se recolectaron los datos.</p>",
  [(100, "Nada sobre la naturaleza. Los ceros vienen de dónde se buscó a cada especie",
        "<p>Correcto. Es el mejor argumento del curso para leer siempre cómo se produjeron los datos.</p>"),
   (0, "Que la especie depende de la isla, y la prueba lo confirmaría",
       "<p>La prueba sí saldría significativa, y precisamente por eso el ejemplo es peligroso. Un resultado estadístico correcto puede sostener una conclusión falsa si se ignora el diseño.</p>"),
   (0, "Que la muestra es demasiado pequeña para concluir",
       "<p>El problema no es el tamaño. Con diez veces más datos recolectados igual, los ceros seguirían ahí.</p>"),
   (0, "Que hay un error de captura en la tabla",
       "<p>Los datos están bien capturados. Reflejan fielmente dónde se buscó.</p>")]))

# ============ 9. NUEVO: qué preguntas se pueden responder ============
partes.append(bloque_multi(
  "U1-09 Lo que limita las preguntas",
  "<p>El estudio de Palmer quería saber si el hielo marino de cada invierno se relaciona con la "
  "alimentación de los pingüinos. Con las ocho columnas de <code>penguins</code>, ¿se puede "
  "responder?</p>",
  "<p>No, y la razón no es la técnica sino los <strong>datos</strong>. La alimentación se midió "
  "con isótopos estables en muestras de sangre, y el hielo marino con datos satelitales. Ninguna "
  "de esas variables está en nuestra tabla de 344 por 8.</p>"
  "<p>La regla vale para todo el curso. Qué preguntas se pueden responder depende de qué "
  "variables se midieron, no de qué técnicas se conocen. Si la variable no está en la tabla, "
  "ninguna técnica la inventa.</p>",
  [(100, "No, porque ni la alimentación ni el hielo marino están entre las variables medidas",
        "<p>Correcto. Y conviene notar que sí están en la versión completa del conjunto, <code>penguins_raw</code>.</p>"),
   (0, "Sí, con una prueba de correlación entre año y masa corporal",
       "<p>El año no mide el hielo, y la masa no mide la alimentación. Sería sustituir las variables de la pregunta por otras que no significan lo mismo.</p>"),
   (0, "Sí, comparando las tres temporadas con un ANOVA",
       "<p>Eso compararía las temporadas entre sí, que no es la pregunta. Además no habría ninguna medida de alimentación que comparar.</p>"),
   (0, "No, porque la muestra de 344 pingüinos es insuficiente",
       "<p>El tamaño no es el obstáculo. Con 3 000 pingüinos y las mismas ocho columnas, la pregunta seguiría sin poder responderse.</p>")]))

# ============ 10. NUEVO: histograma bimodal ============
partes.append(bloque_multi(
  "U1-10 Un histograma con dos montículos",
  "<p>El histograma de la masa corporal de los 344 pingüinos muestra <strong>dos montículos</strong> "
  "en lugar de uno. ¿Qué conviene hacer?</p>",
  "<p>Dos montículos casi siempre significan que hay <strong>grupos distintos mezclados</strong>. "
  "Al separar por especie, el misterio se resuelve: los Juanito son bastante más pesados que las "
  "otras dos especies.</p>"
  "<p>La moraleja sirve para todo el curso. Cuando una distribución se ve rara, casi siempre hay "
  "una variable escondida que la explica, y buscarla es parte del análisis, no un paso opcional.</p>",
  [(100, "Sospechar que hay grupos mezclados y volver a graficar separando por alguna variable categórica",
        "<p>Correcto. Aquí la variable escondida era la especie.</p>"),
   (0, "Descartar los datos del segundo montículo por atípicos",
       "<p>No son errores ni casos raros: son 124 pingüinos Juanito. Descartarlos sería tirar un tercio de los datos por no entenderlos.</p>"),
   (0, "Calcular la media, que resume la distribución de todos modos",
       "<p>La media caería en el valle entre los dos montículos, donde casi no hay pingüinos. Sería un resumen que no describe a nadie.</p>"),
   (0, "Aumentar el ancho de clase hasta que se vea un solo montículo",
       "<p>Eso esconde la estructura en lugar de explicarla. El histograma se vería más limpio y diría menos.</p>")]))

# ============ 11. NUEVO: ancho de clase ============
partes.append(bloque_vf(
  "U1-11 El ancho de clase",
  "<p>Dos personas grafican el histograma de los <strong>mismos</strong> datos y obtienen figuras "
  "de forma distinta. Necesariamente una de las dos se equivocó.</p>",
  "<p>No necesariamente. El <strong>ancho de clase</strong> lo elige quien grafica, y cambia la "
  "historia que cuenta el histograma. Con intervalos muy angostos solo se ve ruido; con "
  "intervalos muy anchos desaparece la estructura, incluidos los dos montículos.</p>"
  "<p>Un histograma no es un dato objetivo sino una <strong>decisión</strong>. Por eso conviene "
  "probar varios anchos antes de quedarse con uno.</p>",
  correcta=False,
  retro_v="<p>No. Las dos pueden estar bien hechas y verse distintas, porque el ancho de clase es una decisión de quien grafica.</p>",
  retro_f="<p>Correcto. Y por eso vale la pena mirar el mismo histograma con dos o tres anchos antes de concluir.</p>"))

# ============ 12. NUEVO: censo, muestra, experimento ============
partes.append(bloque_emparejar(
  "U1-12 Tres formas de obtener datos",
  "<p>Relacionar cada situación con la forma de obtener datos que le corresponde.</p>",
  "<p>El <strong>censo</strong> mide a toda la población, y suele ser caro o imposible. La "
  "<strong>muestra</strong> mide una parte bien elegida, y es el tema de la unidad 4. El "
  "<strong>experimento</strong> produce datos nuevos aplicando tratamientos, y es el de la unidad 5.</p>"
  "<p>Conviene recordar que hay encuestas con millones de respuestas que han fallado en predecir "
  "una elección. El problema no fue el tamaño sino cómo se eligió a quién preguntar.</p>",
  [("Se pregunta a todos los estudiantes inscritos en la licenciatura", "Censo"),
   ("Se eligen al azar 60 estudiantes de la licenciatura y se les pregunta", "Muestra"),
   ("Se sortea qué estudiantes usan cada versión del sitio y se miden sus tiempos", "Experimento"),
   ("Se revisan los expedientes completos de las cuatro generaciones egresadas", "Censo")]))

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n' + "\n".join(partes) + "\n</quiz>\n"
aqui=os.path.dirname(os.path.abspath(__file__))
ruta=os.path.join(aqui,"Banco_U1_Exploracion.xml")
open(ruta,"w",encoding="utf-8").write(xml)
r=ET.parse(ruta).getroot()
tipos={}; sin=[]; n=0
for q in r.findall('question'):
    tp=q.get('type')
    if tp=='category': continue
    n+=1; tipos[tp]=tipos.get(tp,0)+1
    nom=q.find('name/text').text
    gf=q.find('generalfeedback/text')
    if gf is None or not (gf.text or '').strip(): sin.append(nom)
    if tp=='multichoice':
        tot=sum(float(a.get('fraction')) for a in q.findall('answer') if float(a.get('fraction'))>0)
        assert abs(tot-100)<0.01, f"{nom}: suma {tot}"
        for a in q.findall('answer'):
            fb=a.find('feedback/text')
            assert fb is not None and (fb.text or '').strip(), f"{nom}: opción sin retro"
    if tp=='gapselect':
        huecos=len(re.findall(r'\[\[\d+\]\]', q.find('questiontext/text').text))
        ops=len(q.findall('selectoption'))
        assert huecos<=ops, f"{nom}: {huecos} huecos y {ops} opciones"
print(f"XML válido. Reactivos: {n} -> {tipos}")
print("sin retroalimentación general:", sin or "ninguno")
