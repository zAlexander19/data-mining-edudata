# Guion de presentación — Alexander Farías

**Proyecto de Minería de Datos · EduData Analytics · 2026**

Tus diapositivas: **1–2** (apertura), **4** (problemática), **7** (entendimiento de los datos), **8** (EDA 1/4), **9** (EDA 2/4), **19** (qué aprendió el árbol), **23** (Hopkins), **28** (despliegue · análisis de riesgo) y **30** (conclusiones: lección metodológica + cierre de riesgos).

Tiempo total estimado: **8 a 9 minutos** repartidos en siete intervenciones.

> **Tu arco:** abres con el problema → demuestras criterio descartando variables (EDA) → entregas el hallazgo central (el árbol) → demuestras rigor (Hopkins) → asumes el riesgo con resguardos → **y cierras con la lección**. Empiezas y terminas tú: la primera y la última idea del proyecto son tuyas.

---

## SLIDE 1–2 · Apertura e índice
**Tiempo: ~50 segundos** · *Tono: firme, sin leer la lámina.*

> Buenos días, profesor, compañeros. Somos Alexander Farías, Joaquín Ortiz, Benjamín Muñoz y Amin Carrizo, y venimos a presentar nuestro proyecto de Minería de Datos: **detección temprana de reprobación y segmentación de estudiantes**, desarrollado sobre el caso de EduData Analytics.
>
> El proyecto está estructurado de principio a fin con la metodología **CRISP-DM**, y ese va a ser el hilo conductor de toda la presentación. Vamos a recorrer cinco bloques: primero el **problema y los objetivos**; después el **entendimiento y la preparación de los datos**; luego las dos tareas de minería, una **predictiva** —clasificación— y una **descriptiva** —agrupamiento—; y cerramos con el **despliegue y las conclusiones**.
>
> Parto yo con el contexto y el problema.

**No falles en:** los cuatro nombres del equipo y la palabra CRISP-DM.

---

## SLIDE 4 · Problemática
**Tiempo: ~1 minuto** · *Esta es tu lámina de impacto. El número manda.*

> El problema de EduData Analytics se resume en un número: **el 39,8 % de sus estudiantes reprueba o abandona antes de la evaluación final**. Es decir, prácticamente **cuatro de cada diez**.
>
> Y el punto no es solo que la cifra sea alta. El punto es que la institución **hoy no sabe a quién dirigir sus programas de apoyo**. Tiene tutorías, tiene talleres, tiene orientación… pero los reparte a ciegas: sin saber quién está realmente en riesgo y sin saber qué intervención le sirve a cada estudiante. Los programas existen, pero **no tienen foco**.
>
> Entonces el proyecto se plantea para responder exactamente dos preguntas, y de ahí salen nuestras dos tareas de minería:
>
> La primera es una **tarea predictiva**: *¿quién está en riesgo de reprobar?* Necesitamos anticiparlo, no constatarlo cuando ya pasó.
>
> Y la segunda es una **tarea descriptiva**: *¿qué perfiles de estudiante existen y cómo se interviene a cada uno?* Porque no basta con saber quién va mal: hay que saber **por qué** va mal para poder ofrecerle la ayuda correcta.
>
> Estas dos preguntas son las que van a guiar todo lo que viene.

**No falles en:** 39,8 %. Es el número que se repite en toda la presentación (objetivo, conclusiones y análisis de riesgo).

**Si preguntan:** *"¿de dónde sale ese 39,8 %?"* → Es la proporción de la clase **Fail** en el dataset, definida con el umbral de aprobación de **50 puntos** sobre la nota final.

---

## SLIDE 7 · Entendimiento de los datos
**Tiempo: ~1 min 15 s** · *Aquí cambias el registro: de negocio a datos.*

> Ya con el problema claro, pasamos a la segunda fase de CRISP-DM: **entender los datos con los que contamos**.
>
> Trabajamos con un dataset del repositorio público **Kaggle** —el *300K Student Performance Prediction Dataset*, con licencia Apache 2.0—: **300.000 registros**, un estudiante por fila, con **25 atributos** cada uno, en un rango etario de **15 a 21 años**.
>
> Los atributos se ordenan en cinco grandes grupos: **hábitos de estudio** —horas, tareas, ensayos, calidad de los apuntes—; **organización y ánimo** —gestión del tiempo, motivación, salud mental—; **estilo de vida** —sueño, pantalla, redes sociales—; **contexto socioeconómico** —ingreso familiar, educación de los padres, acceso a internet—; y finalmente el **resultado**, que es la nota final.
>
> Nuestra **variable objetivo** es `pass_fail` —aprueba o reprueba—, que se deriva de la nota final con el umbral 50.
>
> Y acá hay una advertencia que queremos dejar dicha desde el principio, porque es honesta y porque explica varias cosas que van a ver después: **estos datos son sintéticos**. Fueron generados artificialmente. Eso significa que nuestras conclusiones **validan la metodología** —el pipeline completo funciona—, pero antes de llevar esto a producción haría falta **un piloto con datos reales** de la institución.
>
> Y justamente porque son sintéticos, el análisis exploratorio nos encontró un par de sorpresas. Vamos a eso.

**No falles en:** 300.000 · 25 · Kaggle · `pass_fail` · umbral 50 · datos sintéticos.

**Ojo:** la frase "los datos son sintéticos" **te da la entrada perfecta** a las dos láminas de EDA que vienen. No la sueltes como disculpa, sueltala como hallazgo.

---

## SLIDE 8 · EDA 1/4 — La edad no aporta información
**Tiempo: ~1 minuto**

> Primer hallazgo del EDA: **la edad no sirve para nada**.
>
> Miren la distribución: es **perfectamente uniforme** entre los 15 y los 21 años. Cada edad concentra alrededor de un **14,3 %** del alumnado —que es exactamente un séptimo—. En una cohorte real esto **no pasa nunca**: siempre hay cursos más numerosos, siempre hay una campana. Esta uniformidad es la **huella dactilar de un dato generado sintéticamente**.
>
> Y lo confirmamos con el número duro: la **correlación de la edad con la nota final es 0,00**. Cero. No explica ni predice absolutamente nada del rendimiento.
>
> ¿Qué hicimos con eso? Tomamos una **decisión metodológica**: la edad **no entra como predictor** en ningún modelo. La usamos solo para **acotar la población** al segmento escolar, de 15 a 18 años, que es el que le interesa a la institución. Nada más.
>
> Este es el primer ejemplo de algo que vamos a repetir todo el rato: **una variable no entra al modelo solo porque esté en la tabla. Entra si aporta.**

**No falles en:** distribución uniforme · 14,3 % · correlación 0,00 · la edad solo filtra (15–18), no predice.

**Si preguntan:** *"¿por qué cortan en 18 si el dataset llega a 21?"* → Porque el caso de negocio es **población escolar**. El filtro deja 171.334 registros, y en la verificación post-ETL (slide 15) mostramos que **no alteró las distribuciones**: la proporción de Fail se mantiene en 39,8 %.

---

## SLIDE 9 · EDA 2/4 — Picos por recorte (*clipping*)
**Tiempo: ~1 minuto** · *Es la lámina más técnica de tu bloque. Ve despacio y apóyate en el argumento del "valor exacto".*

> Segundo hallazgo, y este es más fino. Al mirar los histogramas encontramos **picos anómalos justo en los topes de la escala** —las barras rojas del gráfico—. En **asistencia**, un pico en el **100 %**, que concentra el **6,6 %** de los estudiantes. Y en **tareas completadas**, un pico en el valor **10**, el máximo, con el **16 %** de los casos: uno de cada seis.
>
> ¿Por qué decimos que estos picos son artificiales? Por un detalle clave: **estas dos variables son continuas**, tienen decimales. Una asistencia real en el dataset se ve como 79,213 o 91,004. Y en una variable continua, **un mismo valor exacto no debería repetirse jamás**.
>
> Pero se repite. **El valor exactamente 100,000 lo tiene el 6,6 % de los estudiantes… mientras que todo el tramo entre 99 y 100 —que son miles de valores distintos— apenas tiene el 1,4 %.** Un solo punto concentra casi **cinco veces más gente** que todo el intervalo que tiene al lado. Eso no ocurre de forma natural: **alguien los puso ahí a la fuerza**.
>
> Y lo que ocurrió fue esto: el generador sintético sorteó los valores desde una **campana normal**, y esa campana produce valores **que se salen de la escala** —asistencias de 105 %, de 112 %, absurdas—. En vez de descartarlos, el código los **truncó al tope**: *todo lo que pase de 100, ponlo en 100*. Eso es el **recorte**, o *clipping*. **Toda la cola que se escapaba quedó aplastada sobre un único punto.**
>
> Y la conclusión, que es lo importante: ese pico **no es un grupo real de estudiantes ejemplares**. Es una **bolsa revuelta** de alumnos cuyo valor original era 100, 104 o 109, aplastados todos contra el borde. Si uno no lo detecta, se lo lleva al modelo creyendo que descubrió un perfil de "alumnos perfectos", y en realidad **está modelando una cicatriz del código que generó los datos**.

**No falles en:** son variables **continuas** → un valor exacto no debería repetirse · exactamente 100 → **6,6 %** vs. todo el tramo 99–100 → **1,4 %** · tareas: exactamente 10 → **16 %** · *clipping* = recorte · **no es un subgrupo real**.

**Dato de reserva (si quieres rematar):** si uno calcula cuánta masa de esa campana normal *debería* haber caído por encima de 100, da alrededor del **5 %** — y el pico observado en 100 es del **6,6 %**. **La cola que falta y el pico que sobra son la misma masa.** Eso confirma el diagnóstico.

**Si preguntan:** *"¿y por qué no los eliminaron?"* → Porque **no son errores**: una asistencia de 100 % es un valor perfectamente válido. Eliminarlos significaría borrar el 6,6 % y el 16 % de la base y **sesgar la muestra a propósito**. Lo correcto era **detectarlos, documentarlos y no interpretarlos como señal** — que es exactamente lo que hicimos.

> *(Cierras tu bloque de EDA y pasas la palabra: "Continúa [compañero] con los dos hallazgos que faltan del exploratorio.")*

---

## SLIDE 19 · Tarea predictiva · Qué aprendió el árbol C4.5
**Tiempo: ~1 min 15 s** · *Esta es la lámina que más le gusta a la gente. Aprovéchala.*

> Vamos a abrir el árbol y ver **qué aprendió**, porque esa es la gran ventaja del C4.5: **se puede leer**.
>
> Lo primero, lo más importante de toda la lámina: **la raíz del árbol divide por horas de estudio, en 4,59 horas**. Es decir, el algoritmo, solo, sin que nadie le dijera nada, eligió las **horas de estudio como la primera pregunta que hay que hacerle a un estudiante**. En azul se van los que aprueban, en naranjo los que reprueban.
>
> El árbol completo tiene **1.653 hojas y profundidad 16** —acá en pantalla ven solo los primeros tres niveles, porque el completo es ilegible—.
>
> Y cuando uno mira la **importancia de las variables**, aparece el hallazgo central del proyecto. **Horas de estudio: 24,5 %.** **Gestión del tiempo: 14,7 %.** **Motivación: 13,4 %.** **Tareas completadas: 12,0 %.** Y más atrás, ensayos de práctica con 7,1 % y calidad de apuntes con 7,0 %.
>
> Sumen las cuatro primeras: **casi dos tercios del poder predictivo está en hábitos que el estudiante puede cambiar**.
>
> Y ahora el contraste que le da sentido a todo el proyecto: **los factores socioeconómicos aportan menos del 10 %**. El ingreso familiar, la educación de los padres, el acceso a internet: **menos del 10 % combinados**.
>
> Esto es una **muy buena noticia para la institución**. Porque el ingreso familiar es algo sobre lo que un colegio **no puede hacer nada**. Pero la gestión del tiempo, la motivación y los hábitos de estudio **sí son intervenibles**: son exactamente el tipo de cosa que un taller o una tutoría puede mover. El árbol nos está diciendo dónde vale la pena poner los recursos.

**No falles en:** raíz = horas de estudio ≤ 4,59 · 1.653 hojas / profundidad 16 · 24,5 % / 14,7 % / 13,4 % / 12,0 % · socioeconómico < 10 %.

**Si preguntan:** *"si el árbol es tan interpretable, ¿por qué eligieron Naïve Bayes?"* → Porque **el criterio de éxito era cuantitativo**: el árbol llega a 73,3 % de exactitud y no alcanza el 80 % exigido; Naïve Bayes llega a 80,2 % con recall Fail de 81,2 %. **El árbol lo usamos para explicar, y Naïve Bayes para predecir** — y las variables que ambos destacan son las mismas, lo que refuerza el hallazgo.

---

## SLIDE 23 · Tarea descriptiva · Test de Hopkins
**Tiempo: ~1 min 15 s** · *Aquí no vendes un resultado bonito: vendes rigor. Este es tu momento fuerte.*

> Antes de agrupar, nos hicimos una pregunta que muchos proyectos se saltan: **¿realmente existen grupos naturales en estos datos?**
>
> Y no la respondimos con una intuición. La respondimos con el **estadístico de Hopkins**, que mide precisamente la **tendencia al agrupamiento** de un conjunto de datos: qué tan lejos está de ser una nube uniforme y sin estructura.
>
> El resultado: **H = 0,67**.
>
> Para que ese número signifique algo, lo comparamos contra dos referencias que simulamos nosotros mismos. Una **nube única, sin estructura**, da **0,68**. Y un conjunto con **cuatro grupos realmente separados** da **0,86**.
>
> Nuestro 0,67 está **prácticamente pegado a la nube única** y **muy lejos** de los cuatro grupos reales. La conclusión es directa y hay que decirla sin adornos: **en estos datos no existen clusters naturales que descubrir**. Los estudiantes forman **un continuo**, no islas separadas.
>
> Y esto no nos sorprendió: **ya lo habíamos anticipado en el EDA**, cuando vimos que todos los hábitos son independientes entre sí y que las distribuciones son unimodales. Hopkins simplemente **confirmó la hipótesis con un número**.
>
> Entonces, ¿por qué agrupamos igual? Porque el objetivo de negocio ON-03 **lo pide**: la institución necesita perfiles para diseñar intervenciones. Lo que hicimos fue **cambiar la interpretación**: los cuatro grupos **no son "tipos naturales de estudiante"**, son una **partición operativa** —un corte útil sobre un continuo— y por eso la validamos **por resultado**, no por geometría, como van a ver enseguida.
>
> La idea que queremos dejar acá es una sola: **los supuestos se verifican, no se asumen.**

**No falles en:** H = 0,67 · nube única = 0,68 · cuatro grupos reales = 0,86 · **partición operativa**, no tipos naturales · "se verifica antes de modelar".

**Si preguntan:** *"¿entonces el clustering no sirve?"* → Sirve, pero **no como se suele vender**. No descubre tipos preexistentes; **corta un continuo en segmentos accionables**. Y esa partición **sí es útil**: la reprobación va de **18 % a 52 %** entre los grupos, y la **nota previa es idéntica en los cuatro** (69,8–69,9), lo que prueba que los grupos se formaron **por hábitos y no por historial académico**. Eso es exactamente lo que necesita la institución para focalizar.

**Si preguntan:** *"¿cómo calcularon las referencias 0,68 y 0,86?"* → Simulando datos con la misma cantidad de puntos y dimensiones: un caso con **una sola nube** y otro con **cuatro grupos bien separados**, y corriendo Hopkins sobre ellos. Sin esas referencias, un 0,67 no se puede interpretar.

---

## SLIDE 28 · Despliegue · Análisis de riesgo
**Tiempo: ~1 min 15 s** · *Cierre de tu participación. Es una lámina ética/de decisión: habla con calma y con criterio.*

> Terminamos con una pregunta incómoda que decidimos **no esquivar**: si los grupos están solapados —si son cortes de un continuo, como demostró Hopkins— **¿corresponde operar con ellos?**
>
> **El riesgo es real y hay que nombrarlo.** Como los perfiles no son tipos naturales, un estudiante que queda **en el límite entre dos grupos** puede terminar recibiendo la intervención del grupo vecino. Le mandamos a un taller de gestión del tiempo cuando quizás su problema era la motivación.
>
> **¿Por qué decidimos asumir ese riesgo? Por dos razones.**
>
> La primera: **el costo del error es bajo y benigno**. ¿Qué pasa si nos equivocamos? Que un estudiante asiste a un taller de organización que no era su prioridad… **y aun así refuerza una habilidad útil**. El error **no destruye valor**. Esto es muy distinto de un modelo que niega un crédito o que descarta a alguien de un trabajo.
>
> Y la segunda: **la alternativa es peor**. No actuar significa dejar los programas de apoyo **sin ningún foco**, repartidos a ciegas, frente a un **39,8 % de reprobación**. El costo de la inacción es claramente mayor que el costo de una asignación imperfecta.
>
> Entonces la decisión es **operar** — pero con **tres resguardos** que son los que evitan el mal uso:
>
> **Uno: el perfil es una priorización de apoyo, no una etiqueta que se le cuelga al estudiante.** Nadie "es" un G3. El estudiante nunca ve su grupo.
>
> **Dos: la decisión final es humana.** El sistema **sugiere**; quien decide es **el orientador**, no el algoritmo.
>
> **Y tres: monitoreo semestral**, para corregir el rumbo y **reasignar** al estudiante si sus hábitos cambian. El perfil **no es permanente**.
>
> Con estos tres resguardos, creemos que el modelo se puede llevar a operación de forma responsable.

**No falles en:** el riesgo (estudiante limítrofe → intervención vecina) · costo del error **bajo y benigno** · 39,8 % como costo de no actuar · **los tres resguardos, en orden**.

**Si preguntan:** *"¿no es discriminatorio segmentar estudiantes?"* → Es la pregunta correcta, y por eso está esta lámina. **La segmentación se usa para dar más apoyo, nunca menos**: ningún estudiante pierde acceso a nada por su perfil. Además el perfil **no se le comunica al estudiante**, **no queda en su registro** y **se revisa cada semestre**. La decisión final siempre es de una persona.

---

## SLIDE 30 · Conclusiones — Lección metodológica y cierre de riesgos
**Tiempo: ~1 min 15 s** · *Es el cierre intelectual del proyecto. Baja la velocidad, sube la convicción. No leas: mira al profesor.*

> Y déjenme cerrar con **la lección metodológica**, que para nosotros es lo más valioso que nos dejó este proyecto — más incluso que el modelo.
>
> Nosotros entramos comparando dos algoritmos para predecir. Por un lado, el **árbol C4.5**: potente, flexible, capaz de construir mil seiscientas reglas. Por el otro, **Naïve Bayes**: un modelo tan simple que su nombre significa literalmente **"bayes ingenuo"**, porque asume algo que casi nunca se cumple —que todas las variables son independientes entre sí—.
>
> Y ganó el ingenuo. **Naïve Bayes: 80,2 % de exactitud. El árbol: 73,3 %.** Siete puntos de diferencia a favor del modelo más simple.
>
> ¿Por qué? **Porque sus supuestos eran ciertos en estos datos.** Nosotros lo habíamos verificado en el EDA: los hábitos son **independientes entre sí** —correlación prácticamente cero— y se distribuyen **normalmente dentro de cada clase**. Es decir, Naïve Bayes le pedía a los datos exactamente lo que los datos tenían para darle. El árbol, en cambio, buscaba **umbrales limpios** para cortar… en un conjunto que es **un continuo sin fronteras**. Más potencia, peor encaje.
>
> Y de ahí sale la lección, que es la frase que nos gustaría que se llevaran: **el ajuste entre los supuestos del algoritmo y la naturaleza real de los datos pesa más que la sofisticación del modelo.** No gana el algoritmo más complejo. Gana **el que calza**. Y para saber cuál calza, hay que **haber mirado los datos primero**.
>
> Lo cual nos lleva al segundo aprendizaje, que es el mismo principio aplicado a la otra tarea: **los supuestos se verifican, no se asumen.** Nosotros **no dimos por hecho** que existieran grupos naturales: corrimos el **test de Hopkins antes de agrupar**, nos dio 0,67, y nos dijo que **no los había**. Un proyecto que se salta ese paso habría presentado los cuatro perfiles como "tipos naturales de estudiante" — y habría estado **contando un cuento**. Nosotros preferimos el resultado incómodo pero honesto: es una **partición operativa**, y como tal la validamos y como tal la usamos.
>
> **Y con eso cierro también el análisis de riesgo.** Nuestro modelo **no es perfecto y no lo estamos vendiendo como tal**. Sabemos que los grupos se solapan, sabemos que un estudiante limítrofe puede recibir la intervención vecina, y sabemos que **estos son datos sintéticos**, de modo que antes de operar en serio **hace falta un piloto con datos reales** de la institución.
>
> Pero decidimos **operar igual**, y de forma consciente, por una razón simple: **el costo de equivocarnos es bajo y benigno** —un taller de más nunca le hace daño a nadie—, mientras que **el costo de no hacer nada es un 39,8 % de reprobación atendido a ciegas**. Y operamos con los tres resguardos: **el perfil prioriza, no etiqueta; la decisión final es humana; y se monitorea cada semestre.**
>
> Un modelo imperfecto pero **honesto sobre sus límites**, y usado con resguardos, es mejor que la ceguera con la que se trabaja hoy. Eso es lo que dejamos.
>
> *(Traspaso)* Gracias — [compañero], cierras tú.

**No falles en:**
- **Naïve Bayes 80,2 % le gana al árbol 73,3 %** → gana el modelo *simple*.
- **Por qué:** sus supuestos (independencia + normalidad por clase) **se verificaron en el EDA y se cumplían**.
- **La frase:** *el ajuste entre supuestos y datos pesa más que la sofisticación del modelo.*
- **La segunda frase:** *los supuestos se verifican, no se asumen* (Hopkins **antes** de agrupar).
- **Cierre de riesgo:** solapamiento + datos sintéticos (piloto pendiente) · error **bajo y benigno** vs. **39,8 %** de inacción · **los tres resguardos**.

**Si preguntan:** *"entonces, ¿el árbol fue una pérdida de tiempo?"* → **Al contrario.** El árbol no ganó en métricas, pero es el que **explica**: es el que nos mostró que la raíz divide por horas de estudio y que **lo socioeconómico aporta menos del 10 %**. Y como **ambos modelos coinciden en las mismas variables clave**, el hallazgo queda **doblemente respaldado**. Usamos el árbol para **entender** y Naïve Bayes para **predecir**.

**Si preguntan:** *"¿qué habrían hecho distinto?"* → Incorporar el **test de Hopkins desde el inicio**, no en la revisión de procesos. Y **partir con datos reales**: los sintéticos nos validaron el pipeline, pero **el artefacto del *clipping* y la edad uniforme nos costaron tiempo** de interpretación que con datos reales no habríamos gastado.

---

## Chuleta de números (lo que no puedes equivocar)

| Dato | Valor | Dónde |
|---|---|---|
| Tasa de reprobación | **39,8 %** | Slides 4 y 28 |
| Registros / atributos | **300.000 / 25** | Slide 7 |
| Edad: correlación con la nota | **0,00** (uniforme, ~14,3 % por edad) | Slide 8 |
| Clipping | asistencia 100 % → **6,6 %** · tareas 10 → **16 %** | Slide 9 |
| Raíz del árbol | **horas de estudio ≤ 4,59** | Slide 19 |
| Importancias | **24,5 · 14,7 · 13,4 · 12,0 %** · socioec. **< 10 %** | Slide 19 |
| Tamaño del árbol | **1.653 hojas · profundidad 16** | Slide 19 |
| Hopkins | **H = 0,67** (nube única 0,68 · 4 grupos 0,86) | Slide 23 |

**Para la conclusión (slide 30), estos sí son tuyos:** Naïve Bayes **80,2 %** de exactitud (recall Fail **81,2 %**) vs. árbol **73,3 %** — **7 puntos a favor del modelo simple**. De apoyo: reprobación por perfil de **18 % a 52 %**; nota previa idéntica en los 4 grupos (**69,8–69,9**).

---

## Cuatro ideas que debe recordar el profesor de tu parte

1. **Las variables entran al modelo si aportan, no porque estén en la tabla.** (edad fuera, notas fuera)
2. **Lo que predice la reprobación son hábitos modificables, no el origen socioeconómico.** (< 10 %)
3. **Los supuestos se verifican, no se asumen.** (test de Hopkins **antes** de agrupar, no después)
4. **El ajuste entre supuestos y datos pesa más que la sofisticación del modelo.** (ganó el "ingenuo", porque sus supuestos eran ciertos)

> Las ideas 3 y 4 son **la misma idea aplicada dos veces** — y son tu cierre. Si el profesor se lleva una sola frase de tu presentación, que sea esa.
