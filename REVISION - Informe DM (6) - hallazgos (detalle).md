# Revisión académica — Informe Data Mining (6) - redaccion academica.docx
Fecha de revisión: 2026-07-18. Método: extracción completa del docx (texto, 72 tablas, 64 imágenes),
10 revisores paralelos (estructura, numeración, cadena lógica, redacción/citas, consistencia numérica,
contraste con entrega_modelamiento/, inspección visual de las 64 figuras, contraste con feedback),
deduplicación y verificación: citas comprobadas literalmente contra el texto extraído, aritmética
recomputada en Python, 16 figuras re-inspeccionadas visualmente, negativos (citas/menciones ausentes)
re-verificados por grep. Detalle de cada hallazgo a continuación; el resumen ejecutivo, el mapa de
feedback y el plan de corrección están en la respuesta del chat.

## Hallazgos recuperados en la verificación final (la deduplicación automática los había absorbido por error)

## R1 [C/Mayor] 4.3.3 (time_management_score vs mental_health_score; Figs. 4.19 y 4.23)
HALLAZGO: Superlativo contradictorio: la línea 767 declara time_management_score "el puntaje de habilidades más simétrico (asimetría −0,17)", pero la línea 791 declara mental_health_score "la variable más simétrica y compacta de las habilidades", y según la propia Tabla 46 mental_health es más simétrica (−0,12 vs −0,17). La afirmación errónea está además impresa dentro de la Figura 4.19 ("El puntaje más simétrico y de media más baja de las habilidades (6,46)", verificado en la imagen).
CORRECCION: En 4.3.3/Figura 4.19 reformular a "uno de los puntajes más simétricos y el de media más baja", reservando el superlativo para mental_health_score.

## R2 [C/Mayor] 4.3.3 (sleep_hours vs final_grade; Figs. 4.8 y 4.30)
HALLAZGO: Doble superlativo de normalidad: línea 697 dice de sleep_hours "Es la variable más cercana a una distribución normal de todo el conjunto" y línea 827 dice de final_grade "Es la distribución más simétrica y cercana a la normal de todo el conjunto". Con los estadísticos de la Tabla 46 (final_grade −0,04 vs sleep −0,09 de asimetría), la afirmación de sleep_hours es la que sobra.
CORRECCION: Reformular la línea 697 (p. ej. "una de las más cercanas a la normal") y dejar el superlativo en final_grade.

---
# Detalle de los 77 hallazgos del workflow (verificados)
## F16 [A/Crítico] 6.1.2 (Tabla 55) (origen numeracion)
HALLAZGO: Referencia cruzada rota a un resultado clave: la fila común de K-Means/K-Medoids de la Tabla 55 remite el estadístico de Hopkins a la 'Figura 5.1', pero la Figura 5.1 es la estructura de la vista minable de clasificación; el Hopkins está en la Figura 5.3. La referencia apunta a una figura existente pero de contenido distinto (referencia rota por renumeración/tema).

EVIDENCIA: "| K-Means y K-Medoids (común) | Tendencia de agrupamiento: que exista estructura de grupos que descubrir | NO se cumple: Hopkins 0,67 ≈ nube única (sección 5.5, Figura 5.1). Se declara partición operativa (ON-03) y la validez se juzga por resultado (7.1.1) |" — full_text.md línea 1135 y [TABLA-DOCX 55] (tables.md línea 475). Contraste: "Figura 5.1 – Estructura de la vista minable de clasificación: 10 primeras instancias..." (línea 1076) vs. "Figura 5.3 – Tendencia de agrupamiento (estadístico de Hopkins) de la vista conductual, calibrada contra escenarios simulados..." (línea 1104).

CORRECCION: En la Tabla 55, cambiar "(sección 5.5, Figura 5.1)" por "(sección 5.5, Figura 5.3)", que es la figura que muestra el Hopkins 0,67 calibrado contra escenarios simulados.

---
## F24 [B/Mayor] 3.1/3.2 → 7.1.2 (Tabla 65) (origen cadena-logica)
HALLAZGO: El objetivo de negocio ON-02 no tiene objetivo de minería de datos ni criterio de éxito asociado: la sección 3.1 define solo dos objetivos (clasificación y agrupamiento, mapeados a ON-01 y ON-03) y la 3.2 solo dos criterios; sin embargo, en 7.1.2 se declara 'ON-02 cumplido' sin ninguna meta previa contra la cual verificarlo. Es un eslabón roto de la cadena negocio→minería→criterio→verificación.

EVIDENCIA: Línea 174: 'ON-02: Comprender qué factores (hábitos de estudio, asistencia, gestión del tiempo, salud mental, motivación, contexto socioeconómico) se asocian con un mejor o peor rendimiento...'. Líneas 505-506 definen únicamente 'Objetivo específico 1 (Tarea Predictiva – Clasificación)' y 'Objetivo específico 2 (Tarea Descriptiva – Agrupamiento)'. Línea 1305: 'ON-02 cumplido (los factores asociados al rendimiento quedaron identificados y cuantificados: horas de estudio, gestión del tiempo, motivación...)'.

CORRECCION: Añadir en 3.1/3.2 un objetivo de DM y un criterio medible asociado a ON-02 (p. ej. 'identificar y cuantificar los factores con mayor asociación al rendimiento mediante correlaciones e importancia de variables, reportando al menos los 5 principales'), o declarar explícitamente en 3.1 que ON-02 se satisface transversalmente con el EDA (D.1/D.2) y las importancias del árbol, para que la declaración de cumplimiento en 7.1.2 tenga un referente.

---
## F25 [B/Mayor] 2.8 (Tabla 39) vs 3.3 (Tabla 42) (origen cadena-logica)
HALLAZGO: El costo de desarrollo se calcula para '1 mes' (160 horas = 4 analistas × ~10 hrs/semana × 4 semanas), pero la Carta Gantt del propio plan abarca del 04-08-2026 al 16-11-2026, es decir ~15 semanas (104 días). Con la dedicación declarada, el esfuerzo sería ~600 horas (~$3.000.000), no 160 h ($800.000): el caso de negocio (costos, y por ende VAN y TIR) es inconsistente con el plan del proyecto.

EVIDENCIA: Líneas 477-482: 'Tabla 39 – Costo de Desarrollo del Proyecto (1 mes) ... | Tiempo invertido | 160 horas de esfuerzo total del equipo (4 analistas × ~10 hrs/semana × 4 semanas) | — | ... | Costo de desarrollo | 160 hrs × $5.000 | $800.000 |'. Líneas 518-523 (Tabla 42): '| 1. Comprensión del Negocio | ... | 04-08-2026 | 17-08-2026 |' ... '| 6. Despliegue | ... | 03-11-2026 | 16-11-2026 |' (104 días ≈ 15 semanas, verificado aritméticamente).

CORRECCION: Alinear ambas secciones: o recalcular el costo de desarrollo con la duración del Gantt (≈600 h × $5.000 = $3.000.000; total proyecto ≈ $3.170.000, recalculando VAN/TIR, que siguen siendo positivos), o corregir el rótulo '1 mes / 4 semanas' y las horas por semana para que el esfuerzo total de 160 h sea coherente con las 15 semanas planificadas.

---
## F26 [B/Mayor] 6.1.2 (Tabla 55) y 5.5 (origen cadena-logica)
HALLAZGO: El supuesto de Naïve Bayes 'numéricas aproximadamente normales dentro de cada clase' se da por verificado citando el EDA (4.3.3) y el EDA 2 (5.5), pero ambas verificaciones son sobre las distribuciones marginales de toda la población, no condicionadas por clase (Pass/Fail), que es lo que el supuesto exige. Peor aún, 5.5 cita la casi-normalidad de final_grade como 'relevante para los supuestos de Naïve Bayes' cuando final_grade está excluida de la vista de clasificación por fuga de información: la evidencia citada no verifica lo afirmado.

EVIDENCIA: Línea 1132 (Tabla 55): '| Naïve Bayes | Independencia condicional entre atributos; numéricas aproximadamente normales dentro de cada clase | El EDA mostró correlaciones bajas entre predictores y distribuciones simétricas cercanas a la normal (verificado en 4.3.3 y en el EDA 2 de 5.5): supuesto plausible |'. Línea 1101 (5.5): '(3) las formas de distribución descritas en el EDA (sección 4.3.3) se conservan, en particular la casi-normalidad de sleep_hours y final_grade, relevante para los supuestos de Naïve Bayes'. Línea 1031 (Tabla 51): '| final_grade | Numérica (resultado) | Eliminado por fuga de información (ver 5.2). |'.

CORRECCION: Verificar el supuesto condicionalmente: reportar asimetría/curtosis (o QQ-plots) de los 13 predictores numéricos separados por clase Pass/Fail (los datos están disponibles; la Tabla 59 ya muestra medias por clase), o al menos declarar en Tabla 55 que la verificación realizada es marginal y que la normalidad intra-clase se asume como aproximación. Eliminar la mención de final_grade como evidencia para los supuestos de NB.

---
## F27 [B/Mayor] 3.2 (Criterio de Éxito 2) y 7.1.2 (Tabla 65) (origen cadena-logica)
HALLAZGO: El Criterio de Éxito 2 no es medible pese a que 3.2 afirma que los criterios 'se definen con metas medibles': 'claramente diferenciables entre sí' y 'perfil claro e interpretable' carecen de métrica y umbral. La operacionalización real (diferenciación del % de reprobación entre grupos) se fija recién en 5.5/7.1.1 sin umbral numérico ('diferir sustancialmente'), y el veredicto de Tabla 65 ('CUMPLIDO con reserva') se emite contra una métrica (silueta 0,063) y una brecha de reprobación que nunca se comprometieron en 3.2.

EVIDENCIA: Línea 509: 'Los criterios de éxito están directamente relacionados con los objetivos específicos y se definen con metas medibles'. Línea 511: '...si el algoritmo de agrupamiento (K-Means / K-Medoids) logra identificar al menos 3 grupos (segmentos) de estudiantes claramente diferenciables entre sí, y si cada grupo resultante puede describirse con un perfil de estudiante claro e interpretable...'. Línea 1302 (Tabla 65): '| CE2 – ≥ 3 grupos diferenciables e interpretables | ≥ 3 grupos | K-Means: 4 grupos | (K-Medoids: descartado) | CUMPLIDO con reserva: perfiles nítidos y reprobación 18,0%–51,7%, pero separación geométrica débil (silueta 0,063) |'.

CORRECCION: Dotar a CE2 de un umbral verificable en 3.2 (p. ej. 'diferencia de % de reprobación entre el grupo de mayor y menor riesgo ≥ 15 puntos' y/o 'silueta mínima aceptable'), o reformularlo explícitamente como criterio mixto cuantitativo-cualitativo; así el 'CUMPLIDO con reserva' de Tabla 65 quedaría anclado a la meta prometida y no a métricas elegidas ex post.

---
## F38 [B/Mayor] 5.5 (y 6.1.2, 6.3.2.3, 7.1.1, 9.4) (origen redaccion-citas)
HALLAZGO: El estadístico de Hopkins —pieza metodológica central del informe, con umbrales teóricos de interpretación (0,50 uniforme; ~0,86 con grupos)— se usa transversalmente sin ninguna cita bibliográfica, y no existe entrada para Hopkins en la sección XI REFERENCIAS.

EVIDENCIA: Línea 1102: "el estadístico de Hopkins la confirma: H = 0,67 sobre la vista conductual (muestra de 20.000, media de 5 repeticiones con semilla fija, rango 0,671–0,676), prácticamente idéntico al de una nube gaussiana única simulada en las mismas 12 dimensiones (0,68) y lejos tanto del escenario con cuatro grupos separados (0,86) como del uniforme sin estructura (0,50)". Ninguna de las 10 apariciones de "Hopkins" (líneas 1102, 1104, 1135, 1192, 1244, 1260, 1290, 1304, 1319, 1413) lleva cita; XI (líneas 1547–1555) no contiene la referencia.

CORRECCION: Agregar en XI la referencia original (Hopkins, B. y Skellam, J. G. (1954). A new method for determining the type of distribution of plant individuals. Annals of Botany, 18(2), 213–227) y/o una secundaria (p. ej. Banerjee, A. y Davé, R. N. (2004)), y citarla en el primer uso (sección 5.5, línea 1102).

---
## F68 [C/Mayor] 6.1.1 (origen numeros-fuente)
HALLAZGO: El informe afirma que el Naïve Bayes modela 14 atributos numéricos, pero la entrega tiene 13: la vista minable de clasificación (sin previous_grade) contiene 13 columnas numéricas, la constante NUMERICAS de scripts/02_clasificacion.py (líneas 66-71) lista 13 variables y resultados/naive_bayes_medias_por_clase.csv tiene 13 columnas de atributos. Decir '14 numéricos' implica que previous_grade estaría en el modelo, contradiciendo la decisión metodológica central de excluirla (además, 6.1.1 y 8.2.3 declaran '20 atributos' en total, que solo cuadra con 13+7).

EVIDENCIA: "distribución normal por clase para los 14 atributos numéricos y tablas de frecuencia con corrección de Laplace para los 7 categóricos" (full_text.md línea 1122). Fuente: datos/vista_minable_clasificacion.csv → 13 numéricas (age, study_hours, attendance, sleep_hours, assignments_completed, practice_tests_taken, group_study_hours, notes_quality_score, time_management_score, motivation_level, mental_health_score, screen_time, social_media_hours); naive_bayes_medias_por_clase.csv (2 filas x 13 atributos).

CORRECCION: Cambiar '14 atributos numéricos' por '13 atributos numéricos' en 6.1.1 (la cuenta 13 numéricos + 7 categóricos = 20 atributos es la consistente con la vista entregada y con la sección 8.2.3).

---
## F70 [C/Mayor] 5.5 / 7.1.1 (origen numeros-fuente)
HALLAZGO: Dos verificaciones formales del informe no tienen respaldo en la carpeta de entrega: (a) el estadístico de Hopkins (H=0,67, rango 0,671-0,676, calibraciones 0,68/0,86/0,50, Figura 5.3) y (b) el experimento de silueta por subconjuntos de variables (0,22-0,24 con 3 variables, 0,32 con 2, 0,233; Figura 7.1). Ningún script 01-06 los calcula (grep 'hopkins' sobre scripts/ y resultados/: 0 coincidencias) y no existe CSV/JSON ni PNG en la entrega que los contenga. Esto contradice la afirmación de la Tabla A.2 ('Pipeline reproducible completo con semilla fija 42') y el propio texto de 5.5 ('con semilla fija') para estos resultados.

EVIDENCIA: "el estadístico de Hopkins la confirma: H = 0,67 sobre la vista conductual (muestra de 20.000, media de 5 repeticiones con semilla fija, rango 0,671–0,676)" (full_text.md línea 1102); "la silueta crece sistemáticamente al bajar la dimensión — de 0,063 con las 12 variables a 0,22–0,24 con 3, y 0,32 con 2 —, y los tres hábitos que definen la partición rinden exactamente igual que tres variables al azar (0,233) — Figura 7.1" (línea 1290). Fuente: ls entrega_modelamiento/scripts y resultados/ — sin script ni archivo de Hopkins ni de silueta por subconjuntos; [TABLA-DOCX 72]: "Pipeline reproducible completo con semilla fija 42".

CORRECCION: Añadir a scripts/ el código que calcula Hopkins y el barrido de silueta por subconjuntos (y sus salidas a resultados/ y figuras/), o bien acotar en Tabla A.2 y en 5.5 qué resultados provienen de análisis auxiliares no incluidos en el pipeline entregado.

---
## F71 [C/Mayor] 10.3 (Tabla A.2) (origen numeros-fuente)
HALLAZGO: La Tabla A.2 declara que figuras/ contiene 'Todas las figuras del informe en PNG', pero la carpeta real tiene solo 10 PNG (calidad_datos, clasificacion_arbol_decision, clasificacion_importancia_variables, clasificacion_matrices_confusion, clustering_codo_silueta, clustering_coherencia_rendimiento, clustering_pca_scatter, clustering_perfiles_heatmap, clustering_tamanos_reprobacion, despliegue_umbral). Faltan la Figura 5.3 (Hopkins), la Figura 6.5, la Figura 7.1, las Figuras 8.1-8.5 y todas las del EDA (4.1-4.42); además contiene clustering_pca_scatter.png, una figura que NO aparece en el informe (fue reemplazada por la Figura 6.5 según 6.3.2.1).

EVIDENCIA: "| figuras/ | Todas las figuras del informe en PNG |" ([TABLA-DOCX 72], reproducida en full_text.md línea 1541). Fuente: ls entrega_modelamiento/figuras → 10 archivos PNG; comparación MD5: solo las Figuras 6.1-6.4, 6.6-6.8, 8.6 y una de calidad de datos coinciden con PNG de la carpeta.

CORRECCION: Cambiar la descripción a 'Figuras generadas por los scripts 02-04 (clasificación, clustering y despliegue) en PNG', o completar figuras/ con las figuras restantes del informe y retirar clustering_pca_scatter.png si se mantiene la decisión de no usarla.

---
## F80 [C/Mayor] 4.3.3 (Figs. 4.13–4.16) (origen figuras-1)
HALLAZGO: Las dos parejas de figuras de practice_tests_taken y group_study_hours están intercambiadas: bajo los captions de las Figuras 4.13/4.14 (practice_tests_taken) aparecen los gráficos de group_study_hours, y bajo los captions de las Figuras 4.15/4.16 (group_study_hours) aparecen los de practice_tests_taken. Además, por el intercambio, el tipo de gráfico tampoco coincide: el caption 4.14 anuncia una ECDF pero la imagen es un violín, y el caption 4.16 anuncia un violín pero la imagen es una ECDF. El análisis textual queda desalineado: la línea 731 dice de practice_tests 'La ECDF es una S suave y casi recta en el centro', pero la figura mostrada bajo ese caption (IMG#017) es un violín de group_study_hours.

EVIDENCIA: Línea 727: "Figura 4.13 – practice_tests_taken — Ensayos de práctica: histograma de distribución (n = 300.000)" y línea 729: "Figura 4.14 – practice_tests_taken — Ensayos de práctica: distribución acumulada (ECDF)"; sin embargo IMG#016 (image16.png) lleva el título interno "group_study_hours — Estudio en grupo: distribución" (eje x "Horas de estudio en grupo", nota "Barra ámbar = 6,6 % que no dedica tiempo a estudio grupal") e IMG#017 (image17.png) se titula "group_study_hours — Estudio en grupo: violín". A la inversa, línea 739: "Figura 4.15 – group_study_hours — Estudio en grupo: histograma de distribución (n = 300.000)" y línea 741: "Figura 4.16 – group_study_hours — Estudio en grupo: violín (densidad y caja)", pero IMG#018 (image18.png) se titula "practice_tests_taken — Ensayos de práctica: distribución" (eje x "Ensayos de práctica") e IMG#019 (image19.png) "practice_tests_taken — Ensayos de práctica: ECDF". Texto línea 731: "La ECDF es una S suave y casi recta en el centro, coherente con la simetría."

CORRECCION: Intercambiar las dos parejas de imágenes en el docx: colocar image18/image19 (histograma y ECDF de practice_tests_taken) bajo los captions de las Figuras 4.13 y 4.14, y colocar image16/image17 (histograma y violín de group_study_hours) bajo los captions de las Figuras 4.15 y 4.16. El contenido de los cuatro gráficos es correcto (cifras coinciden con Tabla 46 y con el análisis); solo hay que reubicarlos.

---
## F89 [A/Mayor] 7.1.1 y 9.3 (Figura 6.8) (origen figuras-3)
HALLAZGO: El texto invierte el denominador al describir la Figura 6.8: afirma que el grupo de mejores hábitos 'concentra el 56,2% del tercil Alto', pero la figura (eje Y: '% de estudiantes del grupo') y el CSV de respaldo muestran que el 56,2% DE G1 pertenece al tercil Alto. G1 concentra en realidad ~44,5% del tercil Alto (0,562 × 45.206 = 25.406 de ~57.111 estudiantes del tercil). La afirmación, tal como está redactada, es numéricamente falsa y se repite en las Conclusiones.

EVIDENCIA: Línea 1289: 'los terciles de rendimiento final (Bajo/Medio/Alto) se distribuyen de forma coherente con los perfiles: el grupo de mejores hábitos concentra el 56,2% del tercil Alto, contra 22,0% del grupo más frágil (Figura 6.8)'. Línea 1410: 'el grupo de mejores hábitos concentra el 56,2% del tercil alto de rendimiento'. IMG#057 (Figura 6.8): barra G1 con segmento Alto = 56,2% del grupo; eje Y rotulado '% de estudiantes del grupo'.

CORRECCION: Reformular en ambas ubicaciones: 'el 56,2% del grupo de mejores hábitos pertenece al tercil Alto, contra el 22,0% del grupo más frágil', o bien recalcular si se quiere hablar del tercil como denominador (~44,5%).

---
## F101 [D/Mayor] 8.2.1 / 6.3.2.3 (origen feedback)
HALLAZGO: La observación del profesor sobre la 'conexión de modelos' (cruzar los resultados del modelo predictivo con los clusters: ¿a qué grupo del modelo descriptivo pertenecen mayoritariamente los alumnos que el predictivo marca como aprobados/reprobados?) solo está resuelta a nivel de estudiante individual (la tabla de casos y los sistemas de despliegue muestran juntos P(reprobar) y perfil K-Means por persona). No existe en todo el informe ningún cruce AGREGADO entre las predicciones/alertas del Naïve Bayes y los grupos G0–G3 (p. ej. % de alertados por grupo, o distribución de grupos dentro de los predichos Pass/Fail).

EVIDENCIA: Único punto de encuentro de ambos modelos, caso a caso: '| Estudiante (ID) | Hábitos observados | P(reprobar) | Alerta (0,5) | Perfil conductual y acción | Resultado real |' (línea 1359, [TABLA-DOCX 69]). El cruce por grupo que sí existe usa la reprobación REAL, no la predicción: 'Figura 6.7 – Tamaño de los grupos y % de reprobación por grupo (K-Means)' (línea 1246).

CORRECCION: Añadir en 8.1 u 8.2.1 una tabla o figura de cruce agregado sobre el conjunto de prueba: % de estudiantes alertados por el Naïve Bayes (umbral 0,5) dentro de cada grupo G0–G3, o la distribución de grupos entre los predichos Fail y Pass (los insumos ya existen: resultados/clustering_asignaciones.csv + predicciones de 04_despliegue.py), comentando la coherencia esperada (G1 con tasa mínima de alerta; G3 con la máxima). El profesor señaló explícitamente que 'esa conexión es lo que realmente valorará'.

---
## F102 [D/Mayor] 6.3.2.1, Figura 6.4 (origen feedback)
HALLAZGO: La observación del profesor sobre contraste/legibilidad de etiquetas en las figuras queda sin resolver en la Figura 6.4: precisamente las tres cifras que definen los perfiles de la segmentación (−1,1 de gestión del tiempo en G0; −1,2 de calidad de apuntes en G2; −1,2 de motivación en G3) están rotuladas en texto NEGRO sobre celdas azul marino oscuro del mapa de calor — contraste casi nulo en los valores centrales de la figura (el resto de las figuras del informe sí tiene contraste correcto).

EVIDENCIA: IMG#053 (image51.png), 'Figura 6.4 – Perfiles de los 4 grupos (K-Means) en z-score respecto de la población' (línea 1191); verificado por inspección de píxeles (recortes de las tres celdas): los rótulos '-1.1' y '-1.2' son negros sobre fondo azul marino, mientras el texto asociado afirma 'cada grupo se separa de la media en una dimensión de hábito distinta' (línea 1189), es decir, esas tres celdas son el mensaje principal de la figura.

CORRECCION: Re-exportar la Figura 6.4 con color de texto condicional al fondo (blanco cuando la celda es oscura, p. ej. cuando |z| > 0,8), tal como ya se hace correctamente en la Figura 6.6 (matrices de confusión, números blancos sobre celdas oscuras).

---
## F4 [A/Menor] 5.3 (Balanceo de clases) (origen estructura)
HALLAZGO: En plena fase de Preparación de Datos se declara cuál será el modelo final y se anticipa el resultado de la comparación de exactitudes (que su exactitud será "algo menor" que la del modelo sin balancear), decisión y resultado que metodológicamente pertenecen a las fases de Modelamiento (6.3.2.4) y Evaluación (7.1.2).

EVIDENCIA: Línea 1067: "El modelo final es el entrenado con la base balanceada, aunque su exactitud sea algo menor que la del modelo sesgado: un modelo que aprende de forma pareja de ambas clases es metodológicamente más sólido y más útil en la práctica."

CORRECCION: Reformular en 5.3 como criterio a priori (p. ej. "se preferirá el modelo entrenado con la base balanceada, aun si su exactitud resultara algo menor") y dejar la constatación del resultado real para 6.3.2.4/7.1.2.

---
## F5 [A/Menor] 7.3 (Tabla 67, acción 6) (origen estructura)
HALLAZGO: En la fase de Evaluación aparecen resultados numéricos de un modelo de regresión (R² ≈ 0,68, error medio ≈ 7 puntos) que nunca fue presentado ni documentado en la fase de Modelamiento (VI); la palabra "regresión" y esas cifras solo existen en esta línea del informe.

EVIDENCIA: Línea 1331: "| 6. Complementar la clasificación con una regresión del puntaje final | Estimación preliminar con los mismos hábitos: R² ≈ 0,68 y error medio ≈ 7 puntos; permitiría priorizar por severidad dentro del grupo alertado. |" (única aparición de "regresi"/"R²" en full_text.md, verificado por grep).

CORRECCION: Etiquetar explícitamente la cifra como experimento exploratorio no incluido en el modelamiento (con su script/salida en anexo) o eliminar las cifras y dejar la acción como propuesta cualitativa.

---
## F6 [A/Menor] 5.1.1 (Tabla 51) y 6.3.2.1 (Figura 6.3) (origen estructura)
HALLAZGO: Los rótulos de las vistas minables "A", "B" y "C" se usan antes de ser definidos: aparecen en la Tabla 51 ("vistas A/B") y en el caption de la Figura 6.3, pero solo se definen en la Tabla 63 (sección 6.3.2.4), varias páginas después.

EVIDENCIA: Línea 1014: "Normalización Min-Max [0,1] (clustering, vistas A/B); EXCLUIDA de la vista de clasificación..."; línea 1188: "Figura 6.3 – Método del codo y coeficiente de silueta según k (vistas A, B y C)"; la definición recién aparece en la línea 1256: "| A – completa (5.4) | ..." (Tabla 63).

CORRECCION: Definir los rótulos A/B/C en su primera aparición (p. ej. en la nota de 5.4 sobre las vistas adicionales) o añadir "(ver Tabla 63)" en la Tabla 51 y en el caption de la Figura 6.3.

---
## F7 [A/Menor] Índice de Contenidos vs. 6.3.2.1–6.3.2.6 (origen estructura)
HALLAZGO: El índice llega solo hasta el nivel 3, por lo que las seis subsecciones formalmente numeradas de nivel 4 (6.3.2.1 a 6.3.2.6) no aparecen en él, pese a ser secciones citadas desde otras partes del informe (p. ej. 6.3.2.5 se cita en 8.2.1).

EVIDENCIA: La entrada más profunda del índice para esa rama es "<<TOC 3>> 6.3.2. Modelos	90" (línea 114), mientras el cuerpo contiene "<<HEADING 4>> 6.3.2.1. Visualización de los Modelos" (línea 1179) hasta "<<HEADING 4>> 6.3.2.6. Interpretación de cada Patrón en Lenguaje del Negocio" (línea 1275).

CORRECCION: Ampliar el índice a 4 niveles (al menos para las subsecciones numeradas 6.3.2.x) o reestructurar 6.3.2.1–6.3.2.6 como nivel 3 renumerado.

---
## F8 [A/Menor] 4.3.3, bloques A)–D) y D.1–D.3 (origen estructura)
HALLAZGO: La jerarquía de títulos no refleja el anidamiento lógico dentro de 4.3.3: los bloques A)–D) y sus contenidos comparten todos el mismo nivel de encabezado (nivel 4). Así, "D.1", "D.2" y "D.3" quedan al mismo nivel que su título padre "D)", y las variables (p. ej. "age — Edad") al mismo nivel que su bloque "A)".

EVIDENCIA: Línea 935: "<<HEADING 4>> D) Relaciones Observadas en los Datos (análisis de apoyo)" y línea 938: "<<HEADING 4>> D.1. Relación de cada variable con la nota final" (mismo nivel 4); igualmente línea 632: "<<HEADING 4>> A) Variables Numéricas — Resumen estadístico" y línea 653: "<<HEADING 4>> age — Edad".

CORRECCION: Bajar D.1–D.3 y los títulos de variable a un nivel inferior al de sus bloques A)–D) (o promover A)–D) a nivel 3 con numeración 4.3.3.1–4.3.3.4).

---
## F9 [A/Menor] Elementos formales (índices) (origen estructura)
HALLAZGO: El documento contiene 61 figuras y 72 tablas numeradas pero no incluye Índice de Figuras ni Índice de Tablas; el único índice existente es el de contenidos.

EVIDENCIA: Línea 14: "Índice de Contenidos" es la única línea de índice del documento; la única otra aparición de "Índice de" es el término del glosario "Índice de Silueta (Silhouette)..." (línea 451). Verificado por búsqueda sobre todo full_text.md.

CORRECCION: Agregar un Índice de Figuras (4.1–4.43, 5.1–5.3, 6.1–6.8, 7.1, 8.1–8.6) y un Índice de Tablas (1–70, A.1, A.2) a continuación del índice de contenidos.

---
## F19 [A/Menor] 2.1.1 (origen numeracion)
HALLAZGO: Las Tablas 1 a 5 (integrantes y asesor) no están citadas ni comentadas por ningún párrafo: la sección 2.1.1 comienza directamente con la Tabla 1, sin frase introductoria, y ningún texto del informe las menciona.

EVIDENCIA: "<<HEADING 3>> 2.1.1. Recursos Humanos" seguido inmediatamente de "Tabla 1 – Integrante Equipo de Trabajo" — full_text.md líneas 181–182 (y captions en líneas 188, 194, 200, 206 igualmente sin texto entre medio). El barrido de referencias cruzadas no encontró ninguna mención "Tabla 1"–"Tabla 5" en texto corrido.

CORRECCION: Añadir una frase introductoria al inicio de 2.1.1, p. ej.: "El equipo de trabajo está conformado por cuatro analistas y un asesor, según se detalla en las Tablas 1 a 5:".

---
## F20 [A/Menor] 2.2 (origen numeracion)
HALLAZGO: Las Tablas 12 a 14 (requerimientos RQ-01 a RQ-03) no están citadas ni comentadas: la sección 2.2 comienza directamente con la Tabla 12 sin ninguna frase introductoria, y ningún párrafo del informe las menciona.

EVIDENCIA: "<<HEADING 2>> 2.2. Requerimientos" seguido inmediatamente de "Tabla 12 – Requerimiento 01" — full_text.md líneas 261–262 (captions de Tablas 13 y 14 en líneas 268 y 274, también sin texto). Sin menciones "Tabla 12"–"Tabla 14" en texto corrido según el barrido de referencias.

CORRECCION: Añadir una frase introductoria en 2.2, p. ej.: "Los requerimientos del proyecto se especifican en las Tablas 12 a 14:".

---
## F21 [A/Menor] 4.2 (origen numeracion)
HALLAZGO: La Tabla 43 (herramientas de la etapa de Entendimiento de los Datos) no está citada ni comentada: la sección 4.2 consiste únicamente en la tabla, sin frase introductoria ni comentario posterior, y ningún párrafo la menciona.

EVIDENCIA: "<<HEADING 2>> 4.2. Descripción de Herramientas Utilizadas" seguido inmediatamente de "Tabla 43 – Herramientas utilizadas en la etapa de Entendimiento de los Datos" — full_text.md líneas 556–557. Sin menciones "Tabla 43" en texto corrido según el barrido de referencias.

CORRECCION: Añadir una frase introductoria en 4.2, p. ej.: "La Tabla 43 resume el rol de cada herramienta en esta etapa:".

---
## F28 [B/Menor] 6.3.1 (Tabla 57) (origen cadena-logica)
HALLAZGO: La preferencia del re-muestreo sobre los pesos por clase tiene justificación circular: la configuración con pesos por clase rinde levemente mejor en validación en ambas métricas (73,7%/75,4% vs. 73,6%/75,2%) y cumpliría la regla declarada ('entre las que cumplen, maximizar la exactitud'), pero se descarta con el argumento 'se prefiere el re-muestreo como técnica explícita de balanceo (5.3)', es decir, porque es lo ya decidido; ni 5.3, ni 7.2, ni 9.1 dan una razón sustantiva de por qué re-muestreo es preferible a pesos por clase.

EVIDENCIA: Línea 1151: 'la regla de selección fue: cumplir recall(Fail) ≥ 75% (Criterio de Éxito 1) y, entre las que cumplen, maximizar la exactitud'. Línea 1155: '| 16 | 50 | submuestreo (50/50) | 73,6% | 75,2% | SELECCIONADA...'. Línea 1157: '| 16 | 50 | pesos por clase | 73,7% | 75,4% | resultado comparable; se prefiere el re-muestreo como técnica explícita de balanceo (5.3) |'. Línea 1319 (7.2): 'el reemplazo de los pesos por clase por re-muestreo aplicado solo al entrenamiento' (sin razón).

CORRECCION: Agregar la justificación sustantiva (p. ej.: el re-muestreo es agnóstico al algoritmo y se aplica idéntico a árbol y NB —GaussianNB no admite pesos de instancia de forma nativa—, hace el balanceo explícito y auditable en los datos, y la diferencia de métricas es estadísticamente irrelevante), o reconocer que ambas estrategias son equivalentes y la elección es por consistencia metodológica del pipeline.

---
## F29 [B/Menor] 6.3.1 (Naïve Bayes) vs 5.3 (origen cadena-logica)
HALLAZGO: La comparación sobremuestreo vs. submuestreo prometida en 5.3 se reporta para el árbol (Tabla 57) pero no para Naïve Bayes: en 6.3.1 solo se contrastan 'base original' y 'submuestreo', y se selecciona submuestreo sin mostrar el resultado del sobremuestreo, dejando esa rama de la decisión sin evidencia.

EVIDENCIA: Línea 1067 (5.3): 'se comparan el sobremuestreo con reemplazo de la clase minoritaria (repite casos reales; no se generan datos sintéticos) y el submuestreo aleatorio de la clase mayoritaria, ambos hasta 50/50'. Línea 1161 (6.3.1): 'estrategia de balanceo ∈ {original, sobremuestreo, submuestreo}... con la base original el recall de Fail queda en 68,7%, mientras que con submuestreo sube a 81,6%... Se seleccionó submuestreo, var_smoothing = 1e-9 y alpha = 0,1' (no se reporta ninguna cifra del sobremuestreo para NB).

CORRECCION: Reportar en 6.3.1 las métricas de validación del NB con sobremuestreo (una línea basta) y la razón de preferir submuestreo (p. ej. resultados equivalentes con menor costo computacional).

---
## F30 [B/Menor] 6.1.2 (Tabla 55) y 4.3.3-D.3 (origen cadena-logica)
HALLAZGO: La verificación del supuesto de independencia de Naïve Bayes cubre solo los predictores numéricos: la matriz de correlación citada abarca 'las 12 variables conductuales', pero el modelo usa además 7 atributos categóricos (family_income, parent_education, internet_access, device_type, school_type, extracurriculars, gender) cuya independencia (entre sí y con las numéricas) nunca se examina.

EVIDENCIA: Línea 949 (D.3): 'la matriz de correlación de las 12 variables conductuales (Figura 4.42) muestra que todos los pares de hábitos tienen correlación prácticamente nula (|r| máximo observado: 0,005)'. Línea 1132 (Tabla 55): 'El EDA mostró correlaciones bajas entre predictores' como verificación de 'Independencia condicional entre atributos'. Línea 1122 (6.1.1): 'tablas de frecuencia con corrección de Laplace para los 7 categóricos'.

CORRECCION: Añadir una verificación de asociación para los categóricos (chi-cuadrado o V de Cramér entre pares de categóricas y con las numéricas discretizadas), o acotar la afirmación de la Tabla 55 a los predictores numéricos, señalando que la independencia de los categóricos se asume.

---
## F33 [B/Menor] 8.2.1 y 8.2.3 (origen cadena-logica)
HALLAZGO: Citas de patrones incorrectas al interpretar el despliegue: el caso 283553 (estudio 8,3 h/d, gestión 7,0, motivación 1,8) se declara 'coherente con el patrón P3', pero P3 exige horas de estudio ≤ 4,6 y motivación ≤ 6,8 con gestión > 6,8, condiciones que el caso no cumple (estudia 8,3 h). Análogamente, 8.2.3 afirma que el caso desmotivado con buenos hábitos de estudio 'reproduce los patrones P1–P4', pero P1–P3 exigen estudio ≤ 4,6 y P4 exige gestión ≤ 6,0. La cadena patrones (6.3.2.5) → interpretación en despliegue queda rota en esos casos.

EVIDENCIA: Línea 1368: 'el caso 283553 estudia 8,3 horas diarias y aun así el sistema lo alerta (69,4%) por su motivación crítica (1,8), coherente con el patrón P3 de la sección 6.3.2.5'. Línea 1269 (Tabla 64): '| P3 | horas de estudio ≤ 4,6 Y gestión del tiempo > 6,8 Y motivación ≤ 6,8 | 52,3% | 14.675 |'. Línea 1380: 'Ambos casos reproducen los patrones P1–P4 de la sección 6.3.2.5' aplicado a 'un estudiante con buenos hábitos de estudio pero motivación crítica (2,0/10)'.

CORRECCION: Reformular como analogía con el mensaje de P3/P4 ('un solo hábito débil mantiene el riesgo: ningún hábito compensa por sí solo') sin afirmar que los casos cumplen las condiciones literales de esos patrones, o referir al complemento de P5 (motivación ≤ 6,7) que sí describe a ambos casos.

---
## F34 [B/Menor] 3.3 (Plan del Proyecto) (origen cadena-logica)
HALLAZGO: El cierre del plan mapea las fases restantes de CRISP-DM solo a 'las secciones IV a VII', omitiendo el Despliegue (sección VIII) que el propio plan incluye como fase 6 y que el informe efectivamente desarrolla; el mapa plan→informe queda incompleto.

EVIDENCIA: Línea 531: 'Fin de la fase de Comprensión del Negocio (secciones I a III). Las fases siguientes de la metodología se desarrollan en las secciones IV a VII de este informe.' Línea 523 (Tabla 42): '| 6. Despliegue | Aplicación de los modelos predictivos... | 03-11-2026 | 16-11-2026 |'. Línea 1335: '<<HEADING 1>> VIII. DESPLIEGUE'.

CORRECCION: Cambiar a 'se desarrollan en las secciones IV a VIII de este informe'.

---
## F35 [B/Menor] 2.8 (Tabla 41) vs R-02 y 8.2.4 (origen cadena-logica)
HALLAZGO: El flujo de caja asume beneficios plenos ($6.000.000) desde el Año 1, pero la restricción R-02 y el propio plan de despliegue establecen que los resultados no son aplicables al mundo real sin revalidación y que el primer despliegue debe ser un piloto con datos reales de la institución: el caso de negocio no incorpora ese período de validación previo a la captura de beneficios.

EVIDENCIA: Línea 495 (Tabla 41): '| Beneficios | $0 | $6.000.000 | $6.000.000 | $6.000.000 |'. Línea 311 (R-02): 'las conclusiones no pueden extrapolarse directamente como hallazgos del mundo real sin una validación posterior con datos reales'. Línea 1399 (8.2.4): 'por la restricción R-02 (datos sintéticos), el primer despliegue real debe ser un piloto con datos de la institución (acción 3 de 7.3)'.

CORRECCION: Declarar en 2.8 el supuesto de que los beneficios comienzan tras un piloto exitoso (p. ej. beneficios parciales o nulos en el Año 1, plenos desde el Año 2) y recalcular el VAN bajo ese escenario, o al menos anotar que la evaluación económica es condicional a la revalidación exigida por R-02.

---
## F36 [B/Menor] 2.8 (Tabla 40) vs 1.2 (origen cadena-logica)
HALLAZGO: El beneficio principal cuantificado ($4.200.000) es la 'reducción de la deserción' (retención de matrículas), pero el objetivo de negocio declarado y las tareas de minería apuntan a la reprobación (pass_fail); el vínculo causal reprobación→deserción, aunque sugerido en 1.1, no se argumenta en 2.8, dejando el mayor beneficio del caso de negocio apoyado en un resultado que ningún modelo del proyecto mide.

EVIDENCIA: Línea 489 (Tabla 40): '| Reducción de la deserción: retención de estudiantes que de otro modo abandonarían (matrículas conservadas). | $4.200.000 |'. Línea 171 (1.2): 'El objetivo principal del negocio es reducir la tasa de reprobación estudiantil de EduData Analytics mediante la identificación temprana de los estudiantes en riesgo académico...'.

CORRECCION: Explicitar en 2.8 el supuesto que conecta ambas cosas (p. ej. 'la reprobación es el principal antecedente del abandono en la institución, por lo que reducir reprobación retiene matrículas') o reexpresar el beneficio en términos de reprobación evitada.

---
## F41 [B/Menor] 4.3.3 (origen redaccion-citas)
HALLAZGO: El criterio de Tukey se menciona por nombre pero sin año ni formato de cita, siendo esta la única mención textual que ancla la referencia Tukey (1977) de XI.

EVIDENCIA: Línea 629: "porcentaje de valores atípicos (outliers) detectados por el criterio de Tukey (1,5 × IQR)" — sin "(Tukey, 1977)"; la entrada existe en XI (línea 1554: "Tukey, J. W. (1977). Exploratory data analysis. Addison-Wesley.").

CORRECCION: Completar la cita en línea 629: "...detectados por el criterio de Tukey (1,5 × IQR) (Tukey, 1977)".

---
## F42 [B/Menor] 2.8 (origen redaccion-citas)
HALLAZGO: Los criterios de decisión financiera VAN y TIR (VAN positivo ⇒ proyecto viable; TIR > tasa de descuento ⇒ rentable) se enuncian como reglas teóricas sin cita de literatura.

EVIDENCIA: Línea 498: "Valor Actual Neto (VAN): calculado a una tasa de descuento del 10%... el proyecto presenta un VAN positivo de $13.951.112, lo que indica que el proyecto es viable y aceptable." Línea 499: "la TIR del flujo de caja es de aproximadamente 617%, muy superior a la tasa de descuento del 10%, lo que confirma la alta rentabilidad".

CORRECCION: Añadir una cita de evaluación de proyectos (p. ej., Sapag Chain, N. y Sapag Chain, R. (2008). Preparación y evaluación de proyectos) en 2.8 e incorporarla a XI.

---
## F43 [B/Menor] 6.1 / 6.3.1 (origen redaccion-citas)
HALLAZGO: La inicialización k-means++ se declara tres veces como decisión de configuración sin citar su fuente (Arthur y Vassilvitskii, 2007).

EVIDENCIA: Línea 1118: "K-Means (inicialización k-means++)"; línea 1162: "configuración final: k = 4, inicialización k-means++, 10 reinicios (n_init)"; línea 1163: "con inicialización tipo k-means++". Sin cita en ninguna y sin entrada en XI.

CORRECCION: Citar "(Arthur y Vassilvitskii, 2007)" en la primera aparición (Tabla 54 o 6.3.1) y agregar la referencia a XI.

---
## F44 [B/Menor] 6.3.2.3 (origen redaccion-citas)
HALLAZGO: Dos métricas tomadas de literatura se usan sin cita: el índice de Rand ajustado (también en 6.2, 6.3.2.4 y 7.1.1) y el estadístico η² (eta cuadrado) para el análisis de varianza entre grupos.

EVIDENCIA: Línea 1146: "la concordancia entre ambas particiones (índice de Rand ajustado)"; línea 1244: "(η² ≈ 0,49–0,50 cada uno, siendo η² la proporción de la varianza de la variable explicada por la pertenencia a los grupos)". Ninguna lleva cita; XI no contiene Hubert y Arabie ni fuente para η².

CORRECCION: Citar "(Hubert y Arabie, 1985)" en el primer uso del índice de Rand ajustado (línea 1146) y una fuente para η² (p. ej. Cohen, 1988) en línea 1244; incorporar ambas a XI.

---
## F45 [B/Menor] 2.7 (origen redaccion-citas)
HALLAZGO: Toda la sección de Terminología define conceptos tomados de literatura (CRISP-DM y sus 6 fases, J48/C4.5, Naïve Bayes, K-Means, K-Medoids/PAM, silueta) sin una sola cita; las citas aparecen recién en 3.3 y 6.1.1.

EVIDENCIA: Línea 434: "CRISP-DM: Cross Industry Standard Process for Data Mining. Metodología estándar de referencia que estructura un proyecto de minería de datos en 6 fases..."; línea 443: "J48 (C4.5): Algoritmo de clasificación que construye un árbol de decisión; altamente interpretable, genera reglas legibles." — sin (Autor, año) en toda la sección 2.7 (líneas 430–466).

CORRECCION: Añadir las citas ya disponibles en XI a las definiciones de 2.7: (Chapman et al., 2000) para CRISP-DM, (Quinlan, 1993) para J48, (Witten et al., 2016) para Naïve Bayes/clasificación, (Kaufman y Rousseeuw, 1990) para K-Medoids y (Rousseeuw, 1987) para silueta.

---
## F46 [B/Menor] 4.3.4 (origen redaccion-citas)
HALLAZGO: Se invoca un marco de literatura ("dimensiones clásicas de calidad" de los datos) sin cita que lo respalde.

EVIDENCIA: Línea 954: "organizada según las dimensiones clásicas de calidad —completitud, unicidad, validez, consistencia, exactitud y presencia de valores atípicos—".

CORRECCION: Citar una fuente de calidad de datos (p. ej., Wang, R. Y. y Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers) o reformular sin apelar a "clásicas" de la literatura.

---
## F48 [B/Menor] 9.4 (origen redaccion-citas)
HALLAZGO: Inconsistencia de conteo: el párrafo anuncia "cinco lecciones" pero enumera seis ítems, (1) a (6).

EVIDENCIA: Línea 1413: "El aprendizaje más profundo del trabajo es metodológico y se resume en cinco lecciones. (1) Una variable dominante... (6) Los supuestos habilitantes se verifican antes de modelar".

CORRECCION: Cambiar "cinco lecciones" por "seis lecciones" (o fusionar dos ítems si se desea conservar cinco).

---
## F50 [B/Menor] 9.4 (origen redaccion-citas)
HALLAZGO: Ruptura de la redacción impersonal en la frase final de las conclusiones: primera persona plural ("aprendimos") y alusión directa a la retroalimentación recibida en el curso, que delata la dinámica académica dentro del marco de negocio del informe.

EVIDENCIA: Línea 1413: "Como equipo, además, aprendimos a recibir retroalimentación técnica y transformarla en cambios concretos, re-ejecutados y verificados — probablemente la competencia más transferible que deja el proyecto."

CORRECCION: Reformular en impersonal: "El equipo aprendió, además, a incorporar revisiones metodológicas externas y transformarlas en cambios concretos, re-ejecutados y verificados".

---
## F54 [B/Menor] 4.1.1 (y 5.2, 7.2) (origen redaccion-citas)
HALLAZGO: Los mínimos "exigidos" de 30.000 registros y 15 atributos delatan la pauta del curso: no corresponden a ningún requerimiento declarado en 2.2 ni a una exigencia del negocio, y la fuente de la exigencia nunca se identifica.

EVIDENCIA: Línea 542: "Volumen suficiente: posee 300.000 registros, muy por encima del mínimo de 30.000 exigido."; línea 543: "Cantidad de atributos: posee 25 atributos, superando el mínimo de 15 exigido."; también línea 548, línea 1048 ("el mínimo exigido de 30.000") y línea 1319.

CORRECCION: Anclar los umbrales a un requerimiento del proyecto (p. ej., añadir en 2.2 un RQ de volumen mínimo de datos con su justificación estadística) o reformular: "por encima del mínimo de 30.000 registros definido como criterio de selección del proyecto".

---
## F58 [B/Menor] 9.2 (origen redaccion-citas)
HALLAZGO: Afirmación atribuida genéricamente a "la literatura de CRISP-DM" (que la preparación de datos consume la mayor parte del esfuerzo) sin cita concreta, pese a que la fuente pertinente ya está en XI.

EVIDENCIA: Línea 1407: "la preparación de datos y las decisiones metodológicas consumieron más tiempo que el modelado mismo — proporción esperable según la literatura de CRISP-DM, pero que solo se dimensiona al vivirla".

CORRECCION: Citar la fuente: "...proporción esperable según la guía de la metodología (Chapman et al., 2000)...".

---
## F60 [C/Menor] 7.2 (Tabla 66) (origen numeros-internos)
HALLAZGO: La Tabla 66 afirma que se eliminaron 4 registros erróneos, pero según 5.3 en el subconjunto escolar solo quedaban 2 (los otros 2 salieron por el filtro etario), y la propia aritmética del informe lo confirma: 171.336 − 2 = 171.334 (con −4 daría 171.332, contradiciendo el conteo verificado en la misma tabla).

EVIDENCIA: "| Calidad de datos | 4 registros erróneos eliminados; etiqueta 'None' tratada como categoría válida al cargar los datos (4.3.4) | Correcto |" ([TABLA-DOCX 66], full_text.md línea 1317) vs. "En el subconjunto escolar correspondían a 2 registros." (línea 1063) y "Tras la limpieza, la vista minable final contiene 171.334 registros" (línea 1066); misma Tabla 66: "conteos verificados (300.000 → 171.336 → 171.334)".

CORRECCION: En Tabla 66 escribir "2 registros erróneos eliminados en la limpieza de la vista escolar (los otros 2 de los 4 detectados en el EDA quedaron fuera por el filtro etario)".

---
## F61 [C/Menor] 6.3.2.4 (Tabla 63) vs 6.3.2.3 (Tabla 62) (origen numeros-internos)
HALLAZGO: La silueta de K-Means con k = 4 sobre la vista C aparece con dos valores distintos sin conciliación: 0,062 en el barrido de k (Tabla 63 y texto '0,062–0,074') y 0,063 como resultado final (Tabla 62, Tabla 65, 7.1.1, 7.1.2 y 9.3). Provienen de corridas distintas (barrido 0,0617 vs. modelo final 0,0629 según los JSON), pero el informe no lo explica.

EVIDENCIA: "C – conductual | 12 numéricas (sin age ni previous_grade) | 0,074 (k = 2); 0,062 (k = 4)" ([TABLA-DOCX 63], full_text.md línea 1259) vs. "| Coeficiente de silueta (muestra 10.000) | 0,063 | 0,045 |" ([TABLA-DOCX 62], línea 1240).

CORRECCION: Unificar el valor o añadir una nota: "0,062 en el barrido exploratorio de k; 0,063 en el modelo final (corridas con muestras distintas)".

---
## F62 [C/Menor] 4.3.2 (Tabla 45) vs 4.3.4 (origen numeros-internos)
HALLAZGO: El umbral de aprobación se define de dos formas contradictorias en el límite exacto de 50 puntos: la Tabla 45 asigna la nota 50 a Pass (≥ 50) mientras que 4.3.4 la asigna a Fail (Pass solo si > 50). La sección 5.2 ('umbral en 50') no resuelve la ambigüedad.

EVIDENCIA: "pass_fail | Condición final: Aprueba (≥ 50) o Reprueba (< 50). Variable objetivo de la tarea predictiva." (Tabla 45, full_text.md línea 626) vs. "aprueba quien supera los 50 puntos: final_grade > 50, y las notas iguales o inferiores a 50 corresponden a Fail" (línea 959).

CORRECCION: Unificar la regla en ambas secciones según lo verificado en los datos (según 4.3.4 la regla observada es Pass si final_grade > 50; corregir la Tabla 45 a "Aprueba (> 50) o Reprueba (≤ 50)").

---
## F64 [C/Menor] 10.2 (Anexo, Tabla A.1) (origen numeros-internos)
HALLAZGO: El anexo enuncia la regla de selección sin la restricción de re-muestreo: según la propia Tabla A.1, la configuración de pesos por clase 16/50 (accuracy 73,7%, recall 75,4%) supera en exactitud a la seleccionada (submuestreo 16/50, 73,6%) cumpliendo también recall ≥ 75%, por lo que la frase es falsa tal como está escrita. En 6.3.1 y Tabla 57 la regla sí está correctamente acotada a 'las estrategias de re-muestreo'.

EVIDENCIA: "la configuración seleccionada (submuestreo, profundidad 16, mínimo 50 por hoja) es la de mejor exactitud entre las que cumplen recall(Fail) ≥ 75%" (full_text.md línea 1516) vs. "| ponderación (pesos por clase) | 16 | 50 | 73,7% | 75,4% | 1709 |" y "| submuestreo (50/50) | 16 | 50 | 73,6% | 75,2% | 1357 |" ([TABLA-DOCX 71]).

CORRECCION: Reescribir en 10.2: "...es la de mejor exactitud entre las estrategias de re-muestreo que cumplen recall(Fail) ≥ 75%", igual que en Tabla 57 y 6.3.1.

---
## F72 [C/Menor] Tabla 60 (origen numeros-fuente)
HALLAZGO: El % del alumnado del grupo G2 difiere de la fuente: el informe dice 24,2% pero 41.377/171.334 = 24,15% → 24,1%, valor que registra despliegue_segmentos.csv (pct_alumnado = 24.1). Con 24,2% los cuatro porcentajes de la tabla suman 100,1%. El error se repite en la Tabla 68 y en el texto de 6.3.2.6 ('G2 "Riesgo por calidad de apuntes deficiente" (24,2% del alumnado...)', línea 1280).

EVIDENCIA: "| G2 | 41.377 (24,2%) | calidad de apuntes: 4,62 vs. 6,94 | 44,7% | Riesgo por calidad de apuntes deficiente |" ([TABLA-DOCX 60]); "| G2 – Riesgo por calidad de apuntes deficiente | 41.377 (24,2%) | 44,7% |..." ([TABLA-DOCX 68]). Fuente: despliegue_segmentos.csv fila G2: n=41377, pct_alumnado=24.1; verificación aritmética 41.377/171.334 = 24,1499%.

CORRECCION: Cambiar 24,2% por 24,1% en Tabla 60, Tabla 68 y la sección 6.3.2.6 (así los porcentajes suman 100,0%).

---
## F75 [C/Menor] 6.3.2.1 (Figura 6.5) (origen numeros-fuente)
HALLAZGO: La Figura 6.5 (grupos K-Means sobre los hábitos que definen la partición) no es generada por ningún script de la entrega: 03_clustering.py produce en su lugar clustering_pca_scatter.png (líneas 280-292), es decir, exactamente la visualización por componentes principales que el informe declara reemplazada. La figura del informe no existe en figuras/ ni puede reproducirse con el pipeline entregado.

EVIDENCIA: "Tras la revisión metodológica, el gráfico de grupos se construye sobre los hábitos que definen la partición, en lugar de componentes principales" (full_text.md línea 1192, IMG#054/image52.png). Fuente: scripts/03_clustering.py genera solo clustering_pca_scatter.png ('# dispersión PCA con ambos algoritmos', fig.savefig(FIGURAS / "clustering_pca_scatter.png")); la imagen image52.png no coincide (MD5) con ningún PNG de figuras/.

CORRECCION: Actualizar 03_clustering.py para generar la figura de hábitos de la Figura 6.5 (y guardarla en figuras/), o dejar constancia en el informe de que esa figura proviene de un análisis auxiliar no incluido en el pipeline.

---
## F76 [C/Menor] 8.1 (origen numeros-fuente)
HALLAZGO: El informe dice que el 'Informe Segmentación Conductual' se estructura en siete secciones, pero acto seguido enumera ocho, y el documento entregado tiene efectivamente 8 secciones Heading 1 (1. Propósito … 8. Alcance y limitaciones).

EVIDENCIA: "El documento se estructura en siete secciones: (1) propósito del informe; (2) qué se hizo... (7) el análisis de riesgo de operar con grupos solapados...; y (8) alcance y limitaciones." (full_text.md línea 1349). Fuente: 'Informe Segmentacion Conductual (entregable tarea descriptiva).docx' contiene 8 títulos Heading 1: 1. Propósito de este informe; 2. Qué se hizo; 3. Los cuatro perfiles encontrados; 4. ¿Son creíbles estos grupos?...; 5. Recomendaciones por segmento; 6. Cómo usar la segmentación...; 7. ¿Debe el negocio actuar sobre grupos solapados?...; 8. Alcance y limitaciones.

CORRECCION: Cambiar 'siete secciones' por 'ocho secciones'.

---
## F77 [C/Menor] 10.3 (Tabla A.2) (origen numeros-fuente)
HALLAZGO: El inventario de la carpeta de entrega omite archivos realmente presentes: GUIA_KNIME_vistas_minables.md (raíz de entrega_modelamiento) y demo_web/plantilla_core.html (la Tabla A.2 solo menciona demo_web/index.html); además existe scripts/__pycache__/ con artefactos compilados.

EVIDENCIA: [TABLA-DOCX 72] lista solo: scripts/ (01…06), datos/, modelos/, resultados/, figuras/, "demo_web/index.html", Informe Segmentación Conductual (.docx) y README.txt. Fuente: ls entrega_modelamiento → GUIA_KNIME_vistas_minables.md y demo_web/plantilla_core.html existen y no aparecen en la tabla.

CORRECCION: Agregar a la Tabla A.2 la guía KNIME y la plantilla de la demo (o moverlas/eliminarlas de la carpeta), y borrar scripts/__pycache__/ del paquete de entrega.

---
## F81 [C/Menor] 4.3.3 (Figs. 4.3, 4.5, 4.9, 4.11, 4.17 y los histogramas de practice/group) (origen figuras-1)
HALLAZGO: En todos los histogramas del EDA con barra resaltada, la nota al pie de la figura y el texto identifican la barra coloreada con el porcentaje apilado EXACTAMENTE en el límite de la escala, pero la barra dibujada corresponde al bin completo (valor exacto + resto del intervalo), por lo que su altura supera sistemáticamente la cifra declarada. Caso más claro y medible: en la Figura 4.5 el texto afirma n ≈ 19.773 exactamente en 100 %, pero la barra roja alcanza ≈24.000, claramente por encima de la línea de cuadrícula de 20K. El mismo patrón se observa en Fig. 4.3 (1,2 % ≈ 3.732 vs. barra ≈5.500), Fig. 4.9 (2,2 % ≈ 6.600 vs. ≈9.200), Fig. 4.11 (16 % = 48.000 vs. ≈51.500), Fig. 4.17 (6,7 % ≈ 20.100 vs. ≈24.000), y en los histogramas de group_study (6,6 % ≈ 19.800 vs. ≈31.500, IMG#016) y practice_tests (2,3 % ≈ 6.900 vs. ≈9.600, IMG#018).

EVIDENCIA: Línea 685: "El 6,6% se ubica exactamente en 100% (n ≈ 19.773)"; en IMG#008 (Figura 4.5) la nota interna dice "La barra roja es el 6,6 % apilado exactamente en 100 %" pero la barra roja llega a ≈24K, por sobre la gridline de 20K (19.773 debería quedar bajo 20K). Análogo en línea 673: "Un 1,2% se ubica exactamente en 0 horas de estudio (n ≈ 3.732)" vs. barra ámbar ≈5,5K en IMG#006; y línea 757: "un pico en el valor máximo (10), alcanzado por un 6,7% de los estudiantes (resaltado en naranja)" vs. barra ámbar ≈24K en IMG#020.

CORRECCION: Dibujar la barra resaltada solo con las observaciones del valor exacto del límite (una barra aparte para el valor apilado), o bien reformular la nota de cada figura a algo como 'la barra coloreada corresponde al último intervalo, dominado por el X % apilado exactamente en el límite', para que la altura mostrada coincida con la cifra afirmada.

---
## F82 [A/Menor] 4.3.3 (Fig. 4.3 y figura bajo el caption 4.15) (origen figuras-1)
HALLAZGO: En dos histogramas el eje Y tiene etiquetas de ticks redondeadas e incorrectas: las líneas de cuadrícula están equiespaciadas (paso real de 2.500) pero se rotulan "0K, 2K, 5K, 8K, 10K, 12K, 15K, 18K", de modo que "2K" es en realidad 2.500, "8K" es 7.500, "12K" es 12.500 y "18K" es 17.500. El lector que lea las alturas contra esas etiquetas comete errores de hasta 25 %. Afecta a IMG#006 (Figura 4.3, study_hours) y a IMG#018 (histograma de practice_tests_taken, mostrado bajo el caption de la Figura 4.15).

EVIDENCIA: IMG#006 (caption línea 667: "Figura 4.3 – study_hours — Horas de estudio: histograma de distribución (n = 300.000)"): el eje Y muestra la secuencia "18K, 15K, 12K, 10K, 8K, 5K, 2K, 0K" con separación visual uniforme; los saltos nominales (2,3,3,2,2,3,3) son incompatibles con gridlines equidistantes, lo que delata redondeo de ticks de 2.500. Idéntica secuencia en IMG#018.

CORRECCION: Regenerar ambas figuras con ticks en múltiplos exactos del formato mostrado (p. ej. 0, 2.500, 5.000, … rotulados "2,5K") o forzar ticks enteros (0K, 5K, 10K, 15K) para que la etiqueta coincida con el valor real de la línea.

---
## F83 [A/Menor] 4.3.3 (Fig. 4.1) (origen figuras-1)
HALLAZGO: El caption de la Figura 4.1 la llama "histograma de distribución", pero el gráfico insertado es un diagrama de barras de frecuencia relativa: su título interno es "age — Edad: barras de frecuencia por edad" y el eje Y está en "% de estudiantes" (no en frecuencias n), sin curva KDE. El caption no describe el tipo de gráfico realmente mostrado.

EVIDENCIA: Línea 655: "Figura 4.1 – age — Edad: histograma de distribución (n = 300.000)"; IMG#004 (image4.png) titulado "age — Edad: barras de frecuencia por edad", eje Y "% de estudiantes" y nota "Línea roja discontinua = reparto perfectamente uniforme (1/7 = 14,3 %)".

CORRECCION: Cambiar el caption a "Figura 4.1 – age — Edad: barras de frecuencia por edad (% de estudiantes, n = 300.000)" o regenerar el gráfico como histograma de frecuencias absolutas con KDE para que coincida con el caption.

---
## F84 [C/Menor] 4.3.3 (párrafo metodológico; Figs. 4.1 y 4.7) (origen figuras-1)
HALLAZGO: El párrafo metodológico del EDA afirma que para cada variable numérica se presenta "un histograma con su curva de densidad (KDE)", pero dos figuras no cumplen esa promesa: la Figura 4.1 (age) es un gráfico de barras en % sin KDE, y la Figura 4.7 (sleep_hours) superpone la curva normal teórica (roja discontinua) en lugar de la KDE.

EVIDENCIA: Línea 630: "Para cada variable numérica se presentan dos gráficos: un histograma con su curva de densidad (KDE) y un segundo gráfico complementario…". IMG#004 no contiene ninguna curva de densidad; IMG#010 (caption línea 691) tiene una única curva roja discontinua cuya nota interna la identifica como "la curva normal teórica (roja)", no como KDE.

CORRECCION: Matizar el párrafo metodológico (p. ej., "…un histograma con su curva de densidad (KDE) — o, en variables discretas o de contraste con la normal, barras de frecuencia o la curva normal teórica—…") o añadir la KDE a las Figuras 4.1 y 4.7.

---
## F86 [C/Menor] 4.3.3 (Figuras 4.19, 4.21, 4.23, 4.25 y 4.27) (origen figuras-2)
HALLAZGO: En los cinco histogramas con barra ámbar del rango revisado, la altura de la barra destacada no corresponde al porcentaje que el pie de figura y el texto le atribuyen: la barra es el último (o primer) intervalo del histograma e incluye además valores continuos vecinos, por lo que queda sistemáticamente 20–35% más alta que el conteo citado. En Fig 4.19 la barra mide ≈14.600 (supera la línea de 14K) pero 4,0% de 300.000 = 12.000; en Fig 4.21 ≈24.200 vs 6,8% = 20.400; en Fig 4.23 ≈9.100 vs 2,3% = 6.900; en Fig 4.25 ≈8.900 vs 2,2% = 6.600; en Fig 4.27 ≈18.300 vs 4,75% = 14.250 (alturas verificadas por calibración de píxeles contra las líneas de cuadrícula). Un lector que lea la barra contra el eje obtiene un porcentaje distinto del declarado.

EVIDENCIA: full_text.md línea 770: "Presenta un pico menor en el tope (4% en 10, resaltado en naranja)." y pie interno de IMG#022: "La barra ámbar marca el 4,0 % en el tope (10); curva verde = densidad (KDE).", mientras la barra ámbar de IMG#022 supera la gridline de 14K (≈14,6K ≠ 12.000 = 4% de 300.000). Mismo patrón en IMG#024 ("La barra ámbar marca el 6,8 % en el máximo (10)", barra ≈24,2K), IMG#026 ("marca el 2,3 % en 10", barra ≈9,1K), IMG#028 ("marca el 2,2 % que declara 0 horas", barra ≈8,9K) e IMG#030 ("marca el 4,75 % que declara no usar redes", barra ≈18,3K).

CORRECCION: Aclarar en los pies que la barra ámbar es el intervalo extremo del histograma (contiene el pico exacto en 10 o en 0 más los valores del tramo adyacente), o bien graficar la espiga del valor exacto como barra separada / anotar el n exacto (p. ej. 12.000) sobre la barra, para que la altura leída coincida con el porcentaje citado.

---
## F87 [C/Menor] 4.3.3 (Figura 4.24) (origen figuras-2)
HALLAZGO: El pie interno del gráfico Q-Q de mental_health_score afirma aplanamiento en ambos topes de la escala (1 y 10), pero la figura solo muestra el efecto en el tope 10 (los puntos se saturan en 10 mientras la recta roja continúa hasta ≈11,6); los cuantiles observados graficados comienzan en ≈2,3, de modo que el valor 1 ni siquiera aparece en el gráfico y el aplanamiento en el tope 1 no es verificable en la figura.

EVIDENCIA: Texto incrustado en IMG#027 (Figura 4.24): "Los puntos siguen la recta roja en casi todo el recorrido: forma prácticamente normal, con leve aplanamiento en los topes 1 y 10." — en la misma imagen el punto observado mínimo está en ≈2,3 (esquina inferior izquierda) y la saturación solo es visible en 10. El rango declarado es "rango 1–10" (full_text.md línea 790).

CORRECCION: Reformular el pie interno a "leve aplanamiento en el tope 10" o graficar los cuantiles extremos completos (incluyendo el mínimo 1) para que el aplanamiento inferior sea visible en la figura.

---
## F91 [C/Menor] 6.3.2.3 Figura 6.6 (origen figuras-3)
HALLAZGO: Formato numérico anglosajón dentro de la figura, incoherente con la convención española del documento y ambiguo: las celdas de las matrices usan coma como separador de millares ('7,616', '12,299'), que en convención española se lee como decimal (7,616 ≈ 7,6), mientras el título de la misma figura usa 'n=25.701' con punto de millares y el texto escribe '7.616'/'8.309'. Los subtítulos usan además punto decimal ('accuracy=0.733') frente al '73,3%' del texto.

EVIDENCIA: IMG#055 (Figura 6.6): celdas '7,616 / 2,618 / 4,257 / 11,210' y '8,309 / 1,925 / 3,168 / 12,299'; subtítulos 'accuracy=0.733 · recall Fail=0.744' y 'accuracy=0.802 · recall Fail=0.812'; título 'Matrices de confusión — conjunto de prueba (n=25.701)'. Texto línea 1235: 'Naïve Bayes detecta 8.309 (81,2%) con 3.168 falsas alarmas, y el árbol detecta 7.616 (74,4%) con 4.257 falsas alarmas'.

CORRECCION: Regenerar la figura con separador de millares con punto (7.616, 12.299) y decimales con coma (accuracy=0,733), homogéneo con el texto.

---
## F92 [C/Menor] 6.3.2.1 Figura 6.2 (origen figuras-3)
HALLAZGO: La Figura 6.2 muestra solo 12 de los 20 predictores del árbol (únicamente las variables numéricas) y omite sin indicarlo los atributos categóricos one-hot y la edad (gender_Male 0,0008, family_income 0,0006, age 0,0004, etc., según arbol_importancia_variables.csv). El aporte de 'los atributos socioeconómicos y demográficos' que el texto discute expresamente no puede leerse de la figura, y ni el título ni el caption aclaran que es un subconjunto.

EVIDENCIA: Línea 1197: 'los atributos socioeconómicos y demográficos (ingreso familiar, educación de los padres, género, edad, actividad extracurricular) aportan en conjunto menos del 10%'. IMG#051 (Figura 6.2): solo aparecen 12 barras (study_hours … group_study_hours); ninguna de las variables citadas está en la figura. Caption línea 1185: 'Figura 6.2 – Importancia de variables del árbol de decisión'.

CORRECCION: Añadir al caption o al título de la figura la aclaración '(12 variables numéricas; los atributos categóricos y la edad suman <1% y se omiten)' o regenerarla incluyendo todas las variables.

---
## F93 [C/Menor] 6.3.2.1 Figura 6.4 (origen figuras-3)
HALLAZGO: El heatmap de perfiles incluye las columnas age y previous_grade (14 columnas) pese a que la vista conductual con la que se ejecutó K-Means las excluye (12 variables). Ni el caption ni el texto que la introduce aclaran que esas dos columnas se muestran solo como comprobación pasiva, por lo que un lector puede concluir erróneamente que participaron del agrupamiento, contradiciendo la Tabla 63.

EVIDENCIA: IMG#053 (Figura 6.4): columnas visibles 'age' y 'previous_grade' junto a las 12 conductuales. Tabla 63 (línea 1259): 'C – conductual | 12 numéricas (sin age ni previous_grade)'. Caption línea 1191: 'Figura 6.4 – Perfiles de los 4 grupos (K-Means) en z-score respecto de la población' (sin aclaración).

CORRECCION: Aclarar en el caption: 'age y previous_grade no participaron del agrupamiento; se incluyen solo para verificar que no difieren entre grupos', o eliminar esas dos columnas de la figura.

---
## F94 [C/Menor] 8.2.2 Figura 8.2 (origen figuras-3)
HALLAZGO: Incoherencia entre lo que el texto promete y lo que la figura muestra: el texto afirma que el sistema entrega '(d) los hábitos del estudiante que quedan por debajo de la media poblacional', pero el sistema (y la salida capturada en la Figura 8.2) lista solo las 2 palancas más débiles (nsmallest(2) en el script 05, con déficit en unidades crudas). En el caso C la figura muestra solo 'Asistencia' y 'Horas de estudio' y omite gestión del tiempo (3,0 vs media 6,46), justamente el hábito que el propio texto de la Figura 8.5 destaca como causa del riesgo del mismo caso.

EVIDENCIA: Línea 1371: '(d) los hábitos del estudiante que quedan por debajo de la media poblacional, insumo concreto para la conversación de orientación'. IMG#060 (Figura 8.2), Estudiante C: 'Hábitos más débiles : Asistencia (%): 78.0 (media 84.7); Horas de estudio diarias: 1.0 (media 4.5)' — sin gestión del tiempo, que en el script (05_sistema_prediccion.py, líneas 93-99) es time_management_score=3. Línea 1380: 'gestión del tiempo 3,0/10'.

CORRECCION: Corregir el texto a 'los 2 hábitos accionables más débiles del estudiante (cuando quedan bajo la media poblacional)', o modificar el sistema para listar todos los hábitos bajo la media (y comparar déficits en escala normalizada, no cruda, para que asistencia no domine).

---
## F95 [C/Menor] 4.3.3-D.3 Figura 4.42 (origen figuras-3)
HALLAZGO: Defecto de legibilidad: las etiquetas rotadas del eje X de la matriz de correlación descienden sobre la nota al pie de la figura y se cruzan con su texto ('assignments_completed' atraviesa '|r| < 0,01' y 'time_management_score' atraviesa '0,005)'), dificultando la lectura de la cifra clave de la nota.

EVIDENCIA: IMG#045 (Figura 4.42): nota al pie 'Todos los pares de hábitos tienen |r| < 0,01 (máximo observado: 0,005): variables independientes entre sí…' superpuesta con las etiquetas rotadas del eje X (verificado en recorte ampliado). Caption línea 951.

CORRECCION: Regenerar la figura aumentando el margen inferior (p. ej. plt.subplots_adjust(bottom=…) o colocando la nota con y más negativo) para que la nota no colisione con las etiquetas rotadas.

---
## F103 [D/Menor] 6.3.2.1, Figura 6.1 (origen feedback)
HALLAZGO: En la figura de acercamiento del árbol (respuesta a la petición del profesor de ver el árbol de cerca), los ocho nodos del cuarto nivel tienen el texto recortado por el borde de la caja: en varios no se ve el umbral ('assignments_completed <=' sin el número) y el vector de proporciones queda cortado ('value = [0.799, 0.201' sin cierre), restando legibilidad al zoom solicitado.

EVIDENCIA: IMG#050 (image48.png), 'Figura 6.1 – Árbol de decisión (criterio de entropía), primeros 3 niveles' (línea 1182): en la imagen, la fila de nodos de assignments_completed muestra texto truncado en el borde derecho de cada caja (p. ej. 'assignments_completed <=' sin umbral visible; 'value = [0.612, 0.38' cortado).

CORRECCION: Re-exportar la figura con mayor ancho o menor tamaño de fuente (ajustar proporciones de plot_tree), o dibujar solo los 3 niveles efectivos de división para que ningún rótulo quede cortado; las reglas completas ya están respaldadas en la Tabla 64 y el Anexo 10.1.

---
## F10 [A/Estilo] I, II, III, IV y IX (aperturas de capítulo) (origen estructura)
HALLAZGO: Falta de homogeneidad en las aperturas de fase: los capítulos V, VI, VII, VIII y X tienen párrafo introductorio entre el título de la fase y la primera subsección, mientras que I, II, III, IV y IX pasan directamente del título de capítulo al primer subtítulo.

EVIDENCIA: Línea 1401: "<<HEADING 1>> IX. CONCLUSIONES FINALES" seguida inmediatamente (línea 1403) de "<<HEADING 2>> 9.1. Sobre la Tecnología Data Mining"; en contraste, tras "<<HEADING 1>> V. PREPARACIÓN DE DATOS" (línea 988) sigue el párrafo "A partir de los hallazgos de la Etapa IV (Entendimiento de los Datos), en esta etapa se aplica un proceso ETL..." (línea 989). Igual patrón sin introducción en I (162→164), II (177→179), III (501→503) y IV (533→535).

CORRECCION: Añadir 2–3 líneas introductorias bajo los títulos de los capítulos I, II, III, IV y IX, describiendo el propósito de la fase, para uniformar con V–VIII y X.

---
## F11 [A/Estilo] 2.5.5, 8.2.1–8.2.4, 10.1–10.2 (títulos) (origen estructura)
HALLAZGO: Capitalización de títulos inconsistente: la mayoría de los títulos usa mayúscula inicial en cada palabra significativa, pero varios usan minúsculas tipo oración.

EVIDENCIA: Línea 383: "<<HEADING 3>> 2.5.5. Riesgos relacionados a los datos y la fuente de datos" frente a línea 363: "<<HEADING 3>> 2.5.4. Riesgos Técnicos"; línea 1355: "<<HEADING 3>> 8.2.1. Aplicación del modelo sobre datos de ejemplo" frente a línea 1338: "<<HEADING 2>> 8.1. Modelos Descriptivos"; línea 1418: "<<HEADING 2>> 10.1. Reglas del árbol de decisión (extracto hasta profundidad 4)".

CORRECCION: Homogeneizar el criterio de capitalización de títulos (p. ej. "2.5.5. Riesgos Relacionados a los Datos y la Fuente de Datos", "8.2.1. Aplicación del Modelo sobre Datos de Ejemplo", etc.), y actualizar el índice en consecuencia.

---
## F12 [A/Estilo] Portada (origen estructura)
HALLAZGO: Errata de doble espacio en el título del trabajo en la portada; además la portada no identifica al docente/asesor de la asignatura (que sí figura en la Tabla 5) ni una fecha más precisa que el año.

EVIDENCIA: Línea 6: "INFORME TRABAJO  DE DATA MINING" (doble espacio entre "TRABAJO" y "DE"). La portada (líneas 1–13) contiene facultad, carrera, título, asignatura, integrantes, "IQUIQUE-CHILE" y "2026", sin nombre del docente; el asesor aparece solo en la Tabla 5 (línea 209: "| Nombre | Francisco García B. |").

CORRECCION: Corregir a "INFORME TRABAJO DE DATA MINING" y añadir en la portada el nombre del docente/asesor y la fecha de entrega.

---
## F13 [A/Estilo] XI. Referencias (origen estructura)
HALLAZGO: Dos entradas de la lista de referencias no tienen cita formal autor-año en el cuerpo: Pedregosa et al. (2011) (scikit-learn se menciona repetidamente sin citarla) y Ghai (2026) (el dataset se menciona con el alias del autor pero sin cita formal).

EVIDENCIA: Línea 1551: "Pedregosa, F., Varoquaux, G., ... (2011). Scikit-learn: Machine learning in Python..." mientras que la mención principal de la herramienta (línea 1110) dice "los modelos definitivos se construyeron en Python 3 (Anaconda) con la librería scikit-learn" sin cita; línea 536: "(autor: PinkPixelAI / rhythmghai)" sin cita formal (Ghai, 2026). Verificado por grep: "Pedregosa" y "Ghai" no aparecen en el cuerpo (líneas 1–1545).

CORRECCION: Citar "(Pedregosa et al., 2011)" en la nota de herramientas de la sección VI (o en 2.1.3) y "(Ghai, 2026)" en 4.1 al presentar el dataset.

---
## F14 [A/Estilo] VIII → IX (cierre de fase) (origen estructura)
HALLAZGO: Los cierres de fase son inconsistentes: existen párrafos "Fin de la fase/Etapa..." al terminar III, V y VI–VII, pero la fase VIII (Despliegue) termina sin párrafo de cierre ni transición hacia las Conclusiones.

EVIDENCIA: Línea 1333: "Fin de las Etapas VI y VII. La etapa siguiente (Despliegue) aplicará el modelo predictivo aprobado...", mientras que la sección VIII termina en la línea 1399 ("...y el desempeño del modelo se re-audita cada semestre antes de renovar su uso.") seguida directamente de "<<HEADING 1>> IX. CONCLUSIONES FINALES" (línea 1401).

CORRECCION: Añadir al final de 8.2.4 un párrafo de cierre del tipo "Fin de la Etapa VIII. Con los modelos desplegados, la sección IX presenta las conclusiones finales del proyecto."

---
## F22 [A/Estilo] 5.5 (origen numeracion)
HALLAZGO: Referencia informal a una tabla sin usar su número: "(Tabla de rangos de 5.1)" alude a la Tabla 52, que además está en la subsección 5.1.1 (no en 5.1); rompe la homogeneidad del resto del informe, que cita las tablas por número.

EVIDENCIA: "(4) las variables numéricas de la vista de clustering quedaron efectivamente escaladas al rango [0, 1] tras la normalización Min-Max (Tabla de rangos de 5.1)" — full_text.md línea 1101. Contraste: "Tabla 52 – Rangos [mín, máx] de la normalización" (línea 1035, bajo el encabezado 5.1.1, línea 1005).

CORRECCION: Reemplazar "(Tabla de rangos de 5.1)" por "(Tabla 52)".

---
## F23 [A/Estilo] 2.7 (origen numeracion)
HALLAZGO: Referencia a capítulo con numeración arábiga ("sección 4") cuando el resto del informe cita los capítulos en romanos ("secciones I a III", "secciones IV a VII", "sección VI", "secciones VI y VII"); inconsistencia de estilo de referencia.

EVIDENCIA: "El glosario completo de los 25 atributos se detallará en la sección 4 (Entendimiento de los Datos)." — full_text.md línea 466. Contraste con el estilo dominante: "Fin de la fase de Comprensión del Negocio (secciones I a III). Las fases siguientes de la metodología se desarrollan en las secciones IV a VII de este informe." (línea 531) y "la justificación metodológica se detalla en la nota inicial de la sección VI" (línea 259).

CORRECCION: Cambiar a "la sección IV (Entendimiento de los Datos)" o, más preciso, "la sección 4.3.2" (donde está la Tabla 45 con el glosario completo).

---
## F47 [B/Estilo] 6.1.1 / 6.2 / 7.1.1 (origen redaccion-citas)
HALLAZGO: En las tres citas múltiples entre paréntesis, el orden de las obras no es alfabético (Rousseeuw antes que Davies y Bouldin), contrario a la norma APA de ordenar las citas múltiples como en la lista de referencias.

EVIDENCIA: Línea 1123: "(el máximo de silueta y el mínimo de Davies-Bouldin señalan la cantidad ideal de grupos; Rousseeuw, 1987; Davies y Bouldin, 1979)"; se repite en línea 1146 y línea 1289.

CORRECCION: Reordenar las tres apariciones a "(Davies y Bouldin, 1979; Rousseeuw, 1987)".

---
## F51 [B/Estilo] 7.2 (origen redaccion-citas)
HALLAZGO: Uso de primera persona plural en la traducción de la pregunta guía de CRISP-DM ("¿construimos...?"), única otra ruptura del registro impersonal del documento.

EVIDENCIA: Línea 1308: "Revisión de aseguramiento de calidad del proceso completo (salida \"Review of process\" de CRISP-DM: ¿construimos el modelo correctamente?)".

CORRECCION: Impersonalizar: "¿se construyó el modelo correctamente?".

---
## F52 [B/Estilo] IX (9.2 y 9.4) (origen redaccion-citas)
HALLAZGO: Expresiones coloquiales o metafóricas impropias del registro académico formal concentradas en las conclusiones.

EVIDENCIA: Línea 1407: "proporción esperable según la literatura de CRISP-DM, pero que solo se dimensiona al vivirla" y "evitó el sesgo de \"declarar victoria\" con la métrica que resultara conveniente"; línea 1413: "Desconfiar de las métricas demasiado cómodas" y "convirtieron una corrección mayor en un trámite de horas".

CORRECCION: Sustituir por formulaciones formales: "...que solo se dimensiona en la ejecución del proyecto"; "evitó sesgar la evaluación hacia la métrica más favorable"; "Desconfiar de las métricas aparentemente favorables"; "redujeron una corrección mayor a horas de trabajo".

---
## F53 [B/Estilo] 6.3.2.4 (origen redaccion-citas)
HALLAZGO: Superlativo coloquial "muchísimas" en la explicación técnica de la comparación de modelos.

EVIDENCIA: Línea 1251: "el árbol, en cambio, construye una partición cuadricular del espacio (Quinlan, 1993) y necesita muchísimas divisiones para aproximar una frontera aditiva suave."

CORRECCION: Reemplazar por "un gran número de divisiones" o "numerosas divisiones".

---
## F55 [B/Estilo] 8.2.2 / 8.1 / 10.3 (origen redaccion-citas)
HALLAZGO: La fórmula "entregable de la tarea (predictiva/descriptiva)" evoca el encargo del curso (entregable de una tarea encomendada) más que el producto de la tarea de minería, ambigüedad que se repite en título, TOC, cuerpo y anexo.

EVIDENCIA: Línea 1370: "<<HEADING 3>> 8.2.2. Sistema de predicción por consola (entregable de la tarea predictiva)" (también TOC línea 136); línea 1349: "Entregable de la tarea descriptiva: el despliegue de la segmentación se materializa en un informe de resultados independiente"; línea 1543: "Entregable de la tarea descriptiva (sección 8.1)".

CORRECCION: Reformular como "producto de despliegue de la tarea predictiva/descriptiva" o "sistema entregado para la tarea predictiva", eliminando la ambigüedad con la jerga de encargos del curso.

---
## F56 [B/Estilo] V / X / 10.3 (origen redaccion-citas)
HALLAZGO: El documento se refiere repetidamente a "la entrega" (carpeta de la entrega, adjunto a la entrega), vocabulario de entrega académica que rompe el marco de proyecto profesional para EduData Analytics.

EVIDENCIA: Línea 989: "script 01_etl_vistas_minables.py, adjunto a la entrega"; línea 1416: "Todos los archivos citados se adjuntan en la carpeta de la entrega (entrega_modelamiento/)"; línea 1533: "<<HEADING 2>> 10.3. Contenido de la carpeta de entrega" (también TOC línea 158, y líneas 1110, 1336, 1349).

CORRECCION: Uniformar a "carpeta de entregables digitales del proyecto (entrega_modelamiento/)" o "material adjunto al informe", reservando "entrega" solo como parte del nombre técnico de la carpeta.

---
## F57 [B/Estilo] 9.3 (origen redaccion-citas)
HALLAZGO: La frase de cierre de 9.3 es un principio operativo de despliegue (repite el punto 6 del plan de mantención de 8.2.4), es decir, una recomendación de uso y no una conclusión sobre los resultados — el mismo patrón que el profesor observó ("el punto sobre riesgo se consideró más una recomendación que una conclusión").

EVIDENCIA: Línea 1410: "En el despliegue, ambas salidas se entregan bajo un principio de uso responsable: priorizan apoyo, no etiquetan estudiantes, y la decisión final permanece siempre en el equipo humano de orientación."

CORRECCION: Trasladar la frase a 8.2.4 (donde ya existe el punto de uso responsable) o reformularla como conclusión: p. ej., "los resultados muestran que la utilidad del modelo depende de usarse como priorización de apoyo y no como etiqueta, condición verificada en el diseño del despliegue (8.2.4)".

---
## F79 [C/Estilo] 8.2.3 (origen numeros-fuente)
HALLAZGO: La cita literal del pie de página del autotest no coincide con el texto real de la demo: el informe cita 'autotest del modelo: OK — 4/4 casos verificados vs. Python' (con guion largo) y la página genera 'autotest del modelo: OK (4/4 casos verificados vs. Python)' (con paréntesis).

EVIDENCIA: "el resultado se muestra en el pie de la página (\"autotest del modelo: OK — 4/4 casos verificados vs. Python\", visible en la Figura 8.3)" (full_text.md línea 1376). Fuente: demo_web/plantilla_core.html: el.textContent = `autotest del modelo: OK (${ok}/${MODELO.presets.length} casos verificados vs. Python)`.

CORRECCION: Ajustar la cita del informe al texto exacto de la página: 'autotest del modelo: OK (4/4 casos verificados vs. Python)'.

---
## F85 [A/Estilo] 4.3.3 (Fig. 4.17) (origen figuras-1)
HALLAZGO: La leyenda de la línea vertical discontinua es inconsistente entre los histogramas del EDA: en las Figuras 4.3 y 4.5 la nota la define como mediana ("línea negra = media = mediana", "línea negra = mediana"), pero en la Figura 4.17 se define como "línea negra = media 6,9", y además 6,95 (media de Tabla 46) aparece truncado a 6,9 en vez de redondeado a 7,0.

EVIDENCIA: IMG#020 (caption línea 751: "Figura 4.17 – notes_quality_score — Calidad de los apuntes: histograma de distribución (n = 300.000)"), nota interna: "(mediana 7,0; línea negra = media 6,9)"; frente a IMG#008 (Fig. 4.5): "centrada en 85 % (línea negra = mediana)". Tabla 46 (línea 644): "| notes_quality_score | 6,95 | 7,01 | …".

CORRECCION: Unificar la convención (línea discontinua = mediana en todos los histogramas EDA) y, si se mantiene la media, escribir 7,0 (redondeo de 6,95) o el valor con dos decimales (6,95).

---
## F88 [A/Estilo] 4.3.3 B) Variables Categóricas (Figuras 4.31–4.39) (origen figuras-2)
HALLAZGO: Las nueve figuras de variables categóricas rompen la homogeneidad visual del resto del EDA: título interno solo con el nombre técnico ("Frecuencia: gender") sin el rótulo bilingüe ni la anotación n = 300.000 que sí llevan las Figuras 4.1–4.30, sin subtítulo interpretativo incrustado, sin etiquetas de valor o porcentaje sobre las barras (los porcentajes que el texto cita, p. ej. 48,0/48,0/4,0, no pueden leerse directamente del gráfico) y con eje y en números completos sin separador de miles ("160000") en lugar del formato "14K" usado en las figuras numéricas.

EVIDENCIA: Caption en full_text.md línea 874: "Figura 4.31 – gender — Género: distribución de frecuencias (n = 300.000)" frente al título interno de IMG#034: "Frecuencia: gender", con eje y rotulado "N° estudiantes" y marcas "160000…20000" sin etiquetas de datos sobre las barras; mismo formato en IMG#035–IMG#042. Contraste con IMG#022 (Figura 4.19), cuyo título interno es "time_management_score — Gestión del tiempo: distribución" con subtítulo interpretativo y eje en formato "14K".

CORRECCION: Regenerar las Figuras 4.31–4.39 con el mismo estilo de las numéricas: título bilingüe (variable — nombre en español), eje y con formato compacto de miles, y etiquetas de n y % sobre cada barra (p. ej. "144.083 (48,0%)"), de modo que los porcentajes citados en el análisis sean legibles en la propia figura.

---
## F100 [C/Estilo] Figuras 6.3, 6.6, 7.1 y 8.6 (origen figuras-3)
HALLAZGO: Los ejes y anotaciones de varias figuras generadas con matplotlib usan punto decimal (convención inglesa) mientras todo el texto del informe usa coma decimal, restando homogeneidad al documento.

EVIDENCIA: IMG#064 (Figura 8.6): eje X '0.30 0.35 0.40 … 0.70' frente al texto de la Tabla 70 ('0,30', '0,50 (nominal)', línea 1393). IMG#052 (Figura 6.3): eje Y '0.18 … 0.06'. IMG#058 (Figura 7.1): eje Y '0.30, 0.25 …'. IMG#055 (Figura 6.6): 'accuracy=0.733'.

CORRECCION: Regenerar las figuras con locale es (p. ej. locale + rcParams['axes.formatter.use_locale']=True) o formateadores con coma decimal, para homogeneidad con el texto.

---


---
# Mapa punto a punto de la retroalimentación del profesor (Dimensión D)

- [Resuelto] (message (11) §1) De tareas a objetivos: los objetivos deben redactarse como objetivo de minería de datos, no como tarea
  DONDE: 3.1, línea 505
  COMENTARIO: El objetivo está redactado como objetivo de DM con finalidad de negocio: 'Construir un modelo de clasificación que prediga si un estudiante aprobará o reprobará (pass_fail)… con el fin de seleccionar el modelo de mayor exactitud y exhaustividad para la detección temprana del riesgo de reprobación'; ídem Objetivo 2 para segmentación (línea 506).
- [Resuelto] (message (11) §1) Redacción técnica con umbral (ej.: 'precisión/exactitud superior al 80%')
  DONDE: 3.2, línea 510
  COMENTARIO: El umbral existe y es medible: 'exactitud (accuracy) igual o superior al 80% en el conjunto de prueba, con una exhaustividad (recall) de la clase "Reprueba" igual o superior al 75%', criterio 'asociado al Objetivo 1'. El umbral está en los Criterios de Éxito (práctica CRISP-DM) y no incrustado en la frase del objetivo 3.1, pero el vínculo es explícito.
- [No aplica al informe] (message (11) §1) Optimización: adaptar la diapositiva actual en vez de agregar una nueva
  DONDE: —
  COMENTARIO: Consejo de edición del deck de presentación; no tiene contraparte en el documento.
- [Resuelto] (message (11) §2) Incluir capturas de pantalla de la estructura de las vistas minables
  DONDE: 5.4, Figuras 5.1 y 5.2 (líneas 1074–1078; IMG#047/IMG#048)
  COMENTARIO: 'La estructura completa de ambas vistas minables se presenta en las Figuras 5.1 y 5.2, que muestran las diez primeras instancias con la totalidad de sus columnas' — capturas presentes y verificadas en las imágenes.
- [Parcial] (message (11) §2) Legibilidad: números y etiquetas (como 'Medium', 'High') deben destacar sobre el fondo
  DONDE: Figs 5.1/5.2 y 4.31–4.39 correctas; Figura 6.4 (IMG#053) con defecto
  COMENTARIO: En las capturas de vistas y en las barras del EDA el contraste es correcto (verificado en image63/64 y image35). Pero en la Figura 6.4 los tres valores que definen los perfiles (−1,1 y −1,2) están en negro sobre celdas azul marino: contraste casi nulo (ver finding). 
- [Resuelto] (message (11) §2) Alcance: mostrar la vista minable completa (todas las columnas), no extractos
  DONDE: Figuras 5.1 y 5.2 (línea 1074)
  COMENTARIO: Verificado en las imágenes: 21 columnas (clasificación) y 31 columnas (clustering) completas, coincidentes con '171.334 instancias × 21 atributos' y '× 31 atributos' (líneas 1072–1073).
- [Resuelto] (message (11) §2) Bitácora: mencionar que probaron varias vistas minables y por qué se quedaron con la de mejores resultados
  DONDE: Tabla 63 (líneas 1254–1259); también 5.4 línea 1080, 7.2 línea 1319, 9.1 línea 1404
  COMENTARIO: 'Como parte de la bitácora metodológica del proyecto se registran todas las vistas minables evaluadas' — vistas A y B DESCARTADAS con motivo explícito (grupos dominados por one-hot / por la edad, reprobación plana) y C SELECCIONADA (perfiles interpretables, reprobación 18,0%–51,7%).
- [Parcial] (message (11) §3) Árbol de decisión: las reglas no se aprecian por el tamaño; verlo de cerca o destacar las reglas principales
  DONDE: Figura 6.1 (IMG#050), Tabla 64, Anexo 10.1
  COMENTARIO: Resuelto en lo sustantivo: zoom a 3 niveles (Figura 6.1), reglas destacadas con % y n (Tabla 64, P1–P5) y reglas hasta profundidad 4 en el Anexo 10.1. Queda un defecto puntual: los nodos del 4.º nivel de la Figura 6.1 tienen el texto recortado (umbral y value cortados) — ver finding Menor.
- [Resuelto] (message (11) §3) Matriz de confusión: demasiado pequeña e ilegible; agrandarla y números claros
  DONDE: Figura 6.6 (IMG#055, image53.png) y línea 1235
  COMENTARIO: Figura dedicada, grande, con ambas matrices y números con separador de miles legibles (blanco sobre celdas oscuras); acompañada de lectura textual: 'de los 10.234 estudiantes que efectivamente reprobaron…, Naïve Bayes detecta 8.309 (81,2%)…'.
- [Resuelto] (message (11) §3) Test de Hopkins: se validó su uso para reforzar el 'porqué' de los resultados del clustering
  DONDE: 5.5 (línea 1102), Figura 5.3, 6.3.2.3 (línea 1244), 7.2 (línea 1319)
  COMENTARIO: El informe mantiene y amplía Hopkins con calibración contra escenarios simulados y lo usa exactamente para explicar el porqué de la silueta baja: 'Este resultado no es un defecto de los modelos sino la confirmación de lo verificado antes de modelar… Hopkins (0,67 ≈ nube única)'.
- [Resuelto] (message (11) §4) Mostrar los experimentos previos (resultados con K=2, K=3, etc.), no saltar directo a K=4
  DONDE: 6.2 (línea 1146), Figura 6.3 (IMG#052), Tabla 63, 6.3.2.4 línea 1260
  COMENTARIO: 'explorar k = 2 a 10 con el método del codo (inercia) y el coeficiente de silueta'; la Figura 6.3 grafica k=2..10 para tres vistas y la línea 1260 describe qué pasa con k=3 y k=5 ('los perfiles de riesgo se mezclan' / 'se fragmentan').
- [Resuelto] (message (11) §4) Incluir el Diagrama de Codo para justificar el número de clusters
  DONDE: Figura 6.3 (línea 1188) + línea 1260
  COMENTARIO: 'Figura 6.3 – Método del codo y coeficiente de silueta según k (vistas A, B y C)', con lectura explícita y decisión razonada de k=4 por interpretabilidad al no ser concluyente el codo.
- [Resuelto] (message (11) §5) Conclusiones: interpretación y razonamiento sobre el fenómeno, no resumen de resultados
  DONDE: IX (líneas 1404–1413)
  COMENTARIO: Las conclusiones razonan causas y lecciones, p. ej. 'el ajuste entre los supuestos del algoritmo y la naturaleza de los datos pesa más que la sofisticación del modelo' (9.1) y 'la métrica global escondía exactamente la diferencia que le importa al negocio' (9.3).
- [Resuelto] (message (11) §5) El 'porqué': explicar por qué ciertos grupos tienen alto/bajo rendimiento o por qué se dan los patrones
  DONDE: 6.3.2.4 (línea 1251), 6.3.2.6 (líneas 1276–1280), 7.1.1 (línea 1289), 9.3 (línea 1410)
  COMENTARIO: Se explica el porqué del desempeño de NB (atributos independientes de efecto acumulativo), el rol modulador de la motivación ('reduce la reprobación de 72,3% a 51,1%'), y que el grupo de alto rendimiento se explica por hábitos y no por historial ('la nota previa resulta prácticamente idéntica entre los cuatro grupos (69,8–69,9)').
- [Resuelto] (message (11) §5) Recomendaciones: el punto sobre 'riesgo' era más recomendación que conclusión técnica (separar)
  DONDE: 7.3 (Tabla 67), 8.1 (línea 1348) y 8.2.4 vs. IX
  COMENTARIO: Las recomendaciones operativas (umbral, piloto con datos reales, riesgo de operar con grupos solapados, 'se recomienda por tanto asumir el riesgo y operar') viven en Evaluación/Despliegue; la sección IX no mezcla recomendaciones.
- [No aplica al informe] (message (11) §6) Asistencia: recordatorio del porcentaje de asistencia para la presentación final
  DONDE: —
  COMENTARIO: Observación administrativa al equipo, sin contraparte posible en el documento.
- [Resuelto] (message (11) §6) Gráficos de grupos (K=4) elogiados, pero mostrarlos en el contexto de la comparativa con otros modelos
  DONDE: Tabla 62 (líneas 1237–1243), 6.3.2.4 (línea 1252), Figura 6.3
  COMENTARIO: La visualización de grupos convive con la comparación K-Means vs K-Medoids (silueta, Davies-Bouldin, tamaños, Rand ajustado 0,087) y con la comparación entre las tres vistas minables (Tabla 63 y Figura 6.3).
- [Resuelto] (message (12) §1) Tarea vs. objetivo: redactar el objetivo en términos de rendimiento y utilidad (ej. 'F1 > 0.85, permitiendo intervenciones oportunas')
  DONDE: 3.1 (líneas 505–506) + 3.2 (líneas 510–511)
  COMENTARIO: El objetivo incorpora la utilidad ('detección temprana del riesgo de reprobación') y las metas numéricas están en los criterios de éxito vinculados (accuracy ≥ 80%, recall Fail ≥ 75%); la evaluación se cierra contra esas metas en Tabla 65.
- [Resuelto] (message (12) §2) Método del codo: no ponerlo solo como imagen; explicar la lectura ('probamos de K=2 a K=10; en K=4…')
  DONDE: 6.3.2.4, línea 1260
  COMENTARIO: Lectura explícita y honesta: 'el codo de la Figura 6.3 no es concluyente y la silueta de la vista C es casi plana entre k = 2 y k = 5 (0,062–0,074), por lo que… el número de grupos se decidió por interpretabilidad y utilidad de negocio', con el comportamiento de k=3 y k=5 descrito.
- [Resuelto] (message (12) §2) Vistas minables descartadas: mencionar qué columnas quitaron y por qué
  DONDE: 5.2 (líneas 1049–1052) y Tabla 63 (líneas 1256–1259)
  COMENTARIO: Columnas descartadas con motivo (student_id; final_grade/grade_category por fuga; previous_grade por dominancia) y vistas A/B descartadas con explicación del comportamiento observado (edad domina la partición, reprobación plana).
- [Resuelto] (message (12) §3) Conclusiones explicativas ('pasó esto debido a esto'), no descriptivas
  DONDE: IX (líneas 1404–1413) y 6.3.2.4 (línea 1251)
  COMENTARIO: Mismo sustento que los puntos §5 de message (11): causas explícitas del desempeño de cada modelo y de los perfiles.
- [Resuelto] (message (12) §3) Si el Cluster 1 es el de mayor rendimiento: ¿qué variables comparten? ¿ingresos, asistencia o formación previa?
  DONDE: Tabla 60 (G1), 7.1.1 (línea 1289), 7.1.2 (línea 1305)
  COMENTARIO: La pregunta se responde: G1 comparte 'los mejores hábitos generales (gestión del tiempo: 7,99 vs. 6,46)'; se descarta la formación previa (nota previa idéntica 69,8–69,9 entre grupos) y se acota el peso socioeconómico ('los factores socioeconómicos pesan poco en este conjunto').
- [Parcial] (message (12) §3) Conexión de modelos: cruzar los resultados del predictivo con los clusters (¿los predichos 'aprobados' pertenecen mayoritariamente a qué cluster?)
  DONDE: Tabla 69 (línea 1359), 8.2.2 (línea 1371), 8.2.3 (línea 1377)
  COMENTARIO: Ambos modelos se combinan por estudiante (P(reprobar) + perfil K-Means en la tabla de casos, el sistema por consola y la demo web), pero NO hay un cruce agregado predicción×grupo en ninguna tabla o figura del informe; la Figura 6.7 cruza los grupos con la reprobación real, no con la salida del modelo predictivo. Ver finding Mayor.
- [Parcial] (message (12) §4) Contraste y color: nombres de columnas (p. ej. 'CAT', 'INCOME') con negro más fuerte que los números, dificultando la lectura
  DONDE: Figs 5.1/5.2 correctas (IMG#047/048); Figura 6.4 (IMG#053) con defecto
  COMENTARIO: En las capturas de vistas minables el problema de las diapositivas está corregido (encabezados blancos sobre fondo oscuro, números oscuros sobre fondo claro). Persiste un caso real del mismo tipo: en la Figura 6.4 los valores −1,1/−1,2 (los que definen cada perfil) van en negro sobre azul marino. Ver finding Mayor.
- [Resuelto] (message (12) §4) Escalabilidad del árbol: usar zoom o resaltar las '3 reglas de oro' en lugar del árbol microscópico completo
  DONDE: Figura 6.1, Tabla 64 (líneas 1266–1271), 6.3.2.6, Anexo 10.1
  COMENTARIO: Se aplican ambas alternativas sugeridas: zoom (primeros 3 niveles) y reglas de oro destacadas con métricas (P1 '72,3%' de reprobación, P5 perfil protector '11,4%'), interpretadas en lenguaje de negocio. (El recorte de texto del 4.º nivel de la figura se reporta como finding Menor en el punto §3 de message (11).)
- [Resuelto] (message (12) §5) Hopkins: explicar que es la prueba de que los datos no son aleatorios y que el clustering tiene sentido matemático; si es cercano a 1, justificarlo con fuerza
  DONDE: 5.5 (líneas 1102–1105), Figura 5.3 (IMG#049), Tabla 55 (línea 1135)
  COMENTARIO: El informe explica Hopkins como test calibrado (uniforme 0,50 / nube única 0,68 / 4 grupos 0,86) y, como el valor real es 0,67 (no cercano a 1), justifica con fuerza la lectura opuesta: los datos no contienen grupos densos y el resultado se declara 'partición operativa de un continuo conductual', decisión documentada y usada coherentemente en 6.3.2.3, 7.1.2 y IX. La anotación de la propia figura enseña la escala: 'H ≈ 0,5 indica ausencia de estructura y H → 1 fuerte tendencia a grupos'.


---
# Comprobaciones realizadas sin hallazgos (cobertura, 239 ítems)

- [estructura] Orden y completitud de las 11 secciones CRISP-DM: I. DOMINIO DEL PROBLEMA (l.162) → II. EVALUACIÓN DE LA SITUACIÓN (l.177) → III. OBJETIVOS DE DATA MINING (l.501) → IV. ENTENDIMIENTO DE LOS DATOS (l.533) → V. PREPARACIÓN DE DATOS (l.988) → VI. MODELAMIENTO (l.1108) → VII. EVALUACIÓN (l.1282) → VIII. DESPLIEGUE (l.1335) → IX. CONCLUSIONES FINALES (l.1401) → X. ANEXOS (l.1415) → XI. REFERENCIAS (l.1546): orden exacto al esperado, sin secciones faltantes ni repetidas ✓
- [estructura] Índice vs. cuerpo (script Python, comparación literal uno a uno): las 73 entradas <<TOC>> coinciden en texto, nivel y orden con los 73 encabezados de niveles 1–3 del cuerpo; cero divergencias de redacción y cero títulos faltantes en ambos sentidos ✓
- [estructura] Todas las subsecciones esperadas presentes y en orden: 1.1–1.2, 2.1–2.8 (con 2.1.1–2.1.3 y 2.5.1–2.5.5), 3.1–3.3, 4.1–4.3 (con 4.1.1–4.1.2 y 4.3.1–4.3.4), 5.1–5.5 (con 5.1.1 y 5.2.1), 6.1–6.3 (con 6.1.1–6.1.2 y 6.3.1–6.3.2), 7.1–7.3 (con 7.1.1–7.1.2), 8.1–8.2 (con 8.2.1–8.2.4), 9.1–9.4, 10.1–10.3 ✓
- [estructura] Jerarquía de encabezados (script sobre los 110 encabezados): ningún salto de nivel mayor a +1 (ningún Heading 3 sin Heading 2 previo, ningún Heading 4 colgando de un Heading 2) ✓
- [estructura] Numeración de figuras completa y correcta: las 61 figuras esperadas (4.1–4.43, 5.1–5.3, 6.1–6.8, 7.1, 8.1–8.6) están todas presentes, sin duplicados, en orden estrictamente ascendente, y cada una con caption "Figura N – descripción" completo ✓
- [estructura] Numeración de tablas completa y correcta: captions Tabla 1–70 + Tabla A.1 + Tabla A.2 (72 en total, igual a las 72 TABLA-DOCX extraídas), sin duplicados ni saltos, en orden ascendente; A.1/A.2 correctamente ubicadas en los Anexos (l.1517 y l.1534) ✓
- [estructura] Las 64 imágenes del documento: 61 tienen caption de figura adyacente; las 3 sin caption (IMAGEN #001–#003, image1–3.png) son los logos/escudos de la portada, donde el caption no corresponde ✓
- [estructura] Anexos (X) y Referencias (XI) correctamente al final del documento y en ese orden; los anexos contienen los productos extensos (reglas del árbol, grid search, estructura de la entrega) referenciados desde el cuerpo (10.1 desde 6.3.2.5, A.1 desde 6.3.1/10.2, A.2 desde 6.3.2/10.3) ✓
- [estructura] Referencias: lista en orden alfabético (Chapman → Witten); las citas del cuerpo Chapman et al. 2000 (l.514, 1253, 1283), Witten et al. 2016 (9 apariciones), Quinlan 1993 (l.1121, 1251), Rousseeuw 1987 (l.1123, 1146, 1289), Davies y Bouldin 1979 (l.1123, 1146, 1289), Kaufman y Rousseeuw 1990 (l.1124) y Tukey (criterio 1,5×IQR, l.629) tienen todas su entrada en XI ✓
- [estructura] Números de página del índice monotónicamente crecientes (5 → 128), sin retrocesos ✓
- [estructura] Ubicación metodológica correcta de la evaluación técnica: las métricas de test y el ranking del analista están en VI como salida "Model assessment"/"Models" de CRISP-DM (l.1109 declara las cuatro tareas y salidas oficiales de la fase), mientras la evaluación contra criterios de éxito del negocio, la aprobación de modelos y la revisión del proceso están en VII (Tabla 65, l.1296; "Modelo aprobado", l.1303–1304) — separación técnico/negocio conforme a CRISP-DM ✓
- [estructura] Ubicación correcta de otras salidas de fase: acciones de limpieza solo planificadas (no ejecutadas) en 4.3.4 (Tabla 49, columna "Acción en la preparación de datos"); plan de monitoreo y mantención dentro de Despliegue (8.2.4, l.1399); conclusiones únicamente en IX; la vista conductual derivada en Modelamiento queda declarada en 5.4 como iteración explícita del ciclo CRISP-DM con referencia cruzada a 6.3 (l.1080) ✓
- [estructura] Transiciones entre fases presentes donde el flujo lo exige: cierre de I–III (l.531), cierre en prosa de IV (l.986: "...se puede avanzar a la etapa de Preparación de Datos..."), "Fin de la Etapa V" (l.1106) y "Fin de las Etapas VI y VII" (l.1333); párrafos introductorios de fase en V, VI, VII, VIII y X ✓
- [estructura] Portada presente con facultad, carrera, título del trabajo, asignatura, integrantes (4), ciudad y año (l.1–13) ✓
- [estructura] Observaciones estructurales del profesor (message (11).txt / (12).txt) atendidas en el informe: estructura de las vistas minables completas mostrada (Figuras 5.1 y 5.2, l.1075–1078), bitácora de vistas minables probadas y descartadas (Tabla 63, l.1254–1259), método del codo y silueta con el barrido k=2..10 (Figura 6.3, l.1188; "Elección de k", l.1260), y conclusiones explicativas con el porqué de los resultados (IX, l.1404–1413) ✓
- [numeracion] Secuencia de captions de Figuras completa y correlativa: 4.1–4.43, 5.1–5.3, 6.1–6.8, 7.1, 8.1–8.6 (61 captions, líneas 655–1397 de full_text.md), sin saltos, sin duplicados y en orden correcto — coincide exactamente con la numeración esperada del briefing.
- [numeracion] Secuencia de captions de Tablas completa y correlativa: Tabla 1–70 más A.1 y A.2 (72 captions, líneas 182–1534), sin saltos, sin duplicados y en orden correcto.
- [numeracion] Apareamiento 72 tablas físicas vs. captions verificado 1:1: cada caption 'Tabla n' precede inmediatamente a su [TABLA-DOCX n] (Tabla 1→DOCX 1 … Tabla 70→DOCX 70, Tabla A.1→DOCX 71, Tabla A.2→DOCX 72); sin tablas huérfanas ni captions sin tabla.
- [numeracion] Las 21 referencias 'Figura X' del texto corrido (4.42, 5.1, 5.2, 5.3, 6.3, 6.4, 6.5, 6.7, 6.8, 7.1, 8.1–8.6) apuntan a figuras existentes; coherencia temática verificada en todas salvo la de la Tabla 55 (hallazgo Crítico reportado).
- [numeracion] Las 6 referencias 'Tabla Y' del texto corrido (Tabla 45 en línea 1377, Tabla 59 en 1272, Tabla 60 en 1273, Tabla 68 en 1371, Tabla 70 en 1377, Tabla A.1 en 1516) existen y su contenido corresponde a lo descrito.
- [numeracion] Todas las referencias 'sección Z' con palabra explícita (5.2, VI, I–III, IV–VII, 5.5, 4.3.3, 1.1, 4.1.1, 6.3.1, 6.3, 7.1.1, 3.1, 6.3.2.5, 4.3.4, 6.3.2.4, III, 6.2, 3.2, 7.1.2, VI y VII, 7.3, 8.2.3, 8.1) apuntan a secciones existentes y temáticamente correctas (p. ej. el filtro etario 15–18 sí está en 5.2; el Hopkins sí está en 5.5; la exploración de k sí se discute en 6.3.2.4).
- [numeracion] Las referencias parentéticas informales sin la palabra 'sección' — (5.1), (5.2), (5.3), (5.4), (4.3.4), (2.1.3), (6.3.2.3), (6.3.2.4), (7.1.1), (7.3), 'ver 5.2' en Tablas 50/51 — resuelven todas a secciones existentes y coherentes.
- [numeracion] 'Anexo 10.3' (línea 1416) existe (encabezado 10.3, línea 1533) y su contenido (estructura de la carpeta de entrega) coincide con lo referenciado; anexos 10.1–10.3 correlativos.
- [numeracion] Encabezados de capítulo I–XI presentes en romano, en orden, coincidentes con la numeración esperada del briefing; subsecciones correlativas sin saltos ni duplicados: 1.1–1.2, 2.1–2.8 (2.1.1–2.1.3, 2.5.1–2.5.5), 3.1–3.3, 4.1–4.3 (4.1.1–4.1.2, 4.3.1–4.3.4), 5.1–5.5 (5.1.1, 5.2.1), 6.1–6.3 (6.1.1–6.1.2, 6.3.1–6.3.2, 6.3.2.1–6.3.2.6), 7.1–7.3 (7.1.1–7.1.2), 8.1–8.2 (8.2.1–8.2.4), 9.1–9.4, 10.1–10.3.
- [numeracion] El índice (TOC) coincide 1:1 con los encabezados reales del cuerpo (mismos números y mismos títulos) y sus números de página son monótonamente crecientes (5 → 128); los niveles 4 (6.3.2.x, apartados A–D del EDA) quedan fuera del TOC de forma consistente (profundidad 3).
- [numeracion] Las 61 figuras tienen su imagen inmediatamente adyacente al caption (imagen antes del caption en todos los casos, incluida la Figura 4.42 cuya imagen va tras el párrafo de análisis); las únicas 3 imágenes sin caption son los logos de portada (image1–image3), lo que cuadra: 61 + 3 = 64 imágenes.
- [numeracion] Chequeo 'figura/tabla insertada pero no comentada': todas las figuras están comentadas por texto cercano aunque no siempre citadas por número — las Figuras 4.1–4.39 por los bloques Estadísticos/Análisis/Hallazgos de cada variable (con alusiones directas al gráfico: 'En el histograma se ve la campana' línea 671, 'el gráfico Q-Q lo confirma' 695, 'en la ECDF aparece como un salto vertical' 719, 'resaltado en naranja' 757/770/805/817), la 4.40/4.41 por los análisis D.1/D.2, la 4.43 por 'la figura distingue los valores faltantes reales…' (962), la 6.1 por el párrafo de la raíz del árbol (1180), la 6.2 por su frase introductoria (1183), la 6.6 por 'Lectura de las matrices de confusión…' (1235).
- [numeracion] La Figura 5.2 sí está citada por número: 'se presenta en las Figuras 5.1 y 5.2' (línea 1074) — la mención plural se verificó manualmente (el regex simple solo capturaba el primer número).
- [numeracion] Tablas 6–11, 15–42, 44–58, 61–67, 69 y A.2: aunque no citadas por número, todas tienen frase introductoria o comentario adyacente ('se muestran a continuación', 'La siguiente tabla…', 'Las configuraciones más relevantes:', 'cuya estructura se detalla en el Anexo 10.3', etc.); las únicas sin mención NI comentario son las reportadas en hallazgos (Tablas 1–5, 12–14, 43).
- [numeracion] Referencias a acciones de la Tabla 67 verificadas: 'acción 4 de la sección 7.3' (línea 1387) = fila 4 'Ajustar el umbral de probabilidad del Naïve Bayes' y 'acción 3 de 7.3' (línea 1399) = fila 3 'Recolectar datos reales'; también 'la 3 — complementada con… la acción 5' (línea 1332) coincide con las filas 3 y 5.
- [numeracion] Referencias a códigos definidos en la sección II: ON-01/ON-02/ON-03 (definidos en 1.2), R-02 (Tabla 19), PC-04 (Tabla 35), y los 'Afecta a' de las Tablas 32–36 (RF-01, RF-02, RT-01, RT-02, RD-01, RT-03, RD-02, RN-02, RO-01, RO-02) apuntan todos a códigos existentes en las Tablas 18–31.
- [numeracion] Patrones P1–P5 de la Tabla 64 correlativos, sin saltos, y todos interpretados en 6.3.2.6 (P1, P1 vs P2, P3 y P4, P5); la referencia 'patrones P1–P4' (línea 1380) existe como rango válido.
- [numeracion] Referencias internas del EDA: 'apartado A' (línea 949) existe como encabezado 'A) Variables Numéricas' y 'sección D.1' (línea 662) existe como 'D.1. Relación de cada variable con la nota final'.
- [numeracion] 'sección 7 del informe de segmentación adjunto' (línea 1348) es coherente con el ítem (7) de la enumeración del entregable en la línea 1349 (análisis de riesgo de grupos solapados); referencia externa consistente.
- [numeracion] Coherencia temática de menciones numéricas asociadas a referencias verificada por muestreo: 'más de 33 puntos entre grupos (Figura 6.7)' cuadra con 51,7%−18,0%=33,7; '10.234 estudiantes que efectivamente reprobaron' cuadra con la fila Fail de la matriz (8.309+1.925); los captions de Figuras 5.1/5.2 (21 y 31 atributos) cuadran con el texto de 5.4 (líneas 1072–1073).
- [cadena-logica] Cadena ON-01 → Objetivo específico 1 (3.1) → Criterio de Éxito 1 (3.2: accuracy ≥ 80% y recall Fail ≥ 75% en prueba) → diseño (6.2/6.3.1: la regla de selección de hiperparámetros usa explícitamente 'recall(Fail) ≥ 75% (Criterio de Éxito 1)') → Tabla 65 (CE1a/CE1b con las MISMAS métricas y umbrales: 80,2% y 81,2% de NB) → 9.3 ('cumpliendo ambas metas del Criterio de Éxito 1'): completa, sin cambio de métricas ni umbrales.
- [cadena-logica] Cadena ON-03 → Objetivo específico 2 → CE2 (≥ 3 grupos) → k=4 → Tabla 65 CE2 → 9.3: verificación explícita presente en Tabla 65, con la reserva de la silueta declarada honestamente y retomada en las conclusiones.
- [cadena-logica] CE1c ('identificar cuál de los dos algoritmos ofrece el mejor desempeño y por qué') verificado en Tabla 65 con remisión a la explicación técnica de 6.3.2.4 (ajuste de supuestos de NB a datos con atributos independientes de efecto aditivo): verificación no circular.
- [cadena-logica] VAN Tabla 41: -970.000 + 6.000.000/1,1 + /1,21 + /1,331 = $13.951.112 — coincide exactamente con la cifra del texto (línea 498). Verificado con cálculo.
- [cadena-logica] TIR del flujo [-970.000; 6M; 6M; 6M] = 616,9% ≈ 'aproximadamente 617%' (línea 499). Verificado con cálculo.
- [cadena-logica] Split 70/15/15 de 171.334 = 119.933/25.700/25.701 con 39,82% Fail en los tres subconjuntos (Tabla 56) — coincide con ground truth y con la aritmética (0,70×171.334=119.933,8).
- [cadena-logica] Matriz NB test [[8309,1925],[3168,12299]]: recall Fail 8.309/10.234 = 81,2%, precisión Fail 8.309/11.477 = 72,4%, accuracy 80,2% — consistentes entre Tabla 61, línea 1235 ('detecta 8.309... con 3.168 falsas alarmas'), Tabla 70 (fila 0,50: 11.477 alertas = 44,7% del alumnado) y 7.1.2 ('de cada 100 alertas emitidas, ~72 son correctas'; falsos negativos ~19/100 = 1−0,812).
- [cadena-logica] Matriz árbol test [[7616,2618],[4257,11210]]: accuracy 73,3%, recall Fail 74,4%, precisión Fail 64,2%, recall Pass 72,5%, precisión Pass 81,1% — todas las celdas de Tabla 61 verificadas aritméticamente contra la matriz y el ground truth.
- [cadena-logica] Conteos del filtro etario coherentes en toda la cadena: 300.000 − 171.336 = 128.664 descartados (42,9%, línea 1048); 171.336 − 2 registros erróneos = 171.334 (5.3); 7.2 'conteos verificados (300.000 → 171.336 → 171.334)' — todo consistente.
- [cadena-logica] Tamaños de grupos K-Means 43.655+45.206+41.377+41.096 = 171.334 y K-Medoids 47.618+37.545+52.542+33.629 = 171.334 — consistentes en Tablas 60, 62 y 68 y con ground truth; % de reprobación por grupo (46,7/18,0/44,7/51,7) idénticos entre Tabla 60, 6.3.2.6 y Tabla 68.
- [cadena-logica] Decisión de balanceo SOLO en entrenamiento: declarada y justificada en 5.3 (validación y prueba con distribución real 'para que las métricas reflejen el desempeño verdadero'), aplicada en 6.3.1, auditada en Tabla 66 ('Re-muestreo... aplicado SOLO al entrenamiento') y coherente con ground truth (train 72.175/47.758; submuestreo 47.758+47.758).
- [cadena-logica] Filtro etario 15–18 justificado no circularmente: alcance de negocio declarado desde 1.1 ('ver sección 5.2') y 4.1.1, con costo explícito (42,9% descartado) y descargo predictivo (edad r=0,00, distribución uniforme) en 5.2, re-auditado en 7.2 hallazgo (1).
- [cadena-logica] Exclusión de final_grade y grade_category justificada por fuga de información (5.2, línea 1051) y verificada en la revisión de procesos (Tabla 66 'Sin fuga'); exclusión de previous_grade justificada (dominancia y sesgo de la medición del impacto de los hábitos, línea 1052) y coherente en 6.3.2.1, 7.2(3), 9.1 y 9.4(1); pass_fail retirada de la vista de clustering y usada solo ex post (5.2, 6.2, Tabla 66).
- [cadena-logica] Conservación de outliers justificada dos veces (4.3.4 punto 6: 'valores extremos plausibles... no errores'; 5.3: 'se conservan, ya que están dentro de rangos válidos', con opción de capping documentada) y coherente con 6.1.1, donde la ventaja anti-atípicos de K-Medoids se declara 'secundaria (atípicos: solo 0,3–0,7%)'.
- [cadena-logica] Elección de k=4 justificada sin circularidad: Tabla 63 y línea 1260 reconocen que el codo no es concluyente y la silueta es casi plana (0,062–0,074, coincide con el barrido del ground truth: k=2 0,0744 ... k=4 0,0617), y fundamentan k=4 en interpretabilidad/accionabilidad con contraste explícito de k=3 (perfiles se mezclan) y k=5 (se fragmentan) — resuelve además la observación del profesor de mostrar experimentos con otros k (Figura 6.3 y Tabla 63).
- [cadena-logica] Elección de NB como modelo final justificada por dominancia en TODAS las métricas de Tabla 61 (verificadas contra ground truth) más explicación causal (6.3.2.4); elección de K-Means justificada por silueta (0,063 vs 0,045), Davies-Bouldin (2,77 vs 3,38) y tamaños equilibrados, cifras que coinciden con metricas_clustering.json (0,0629/0,0445; 2,7669/3,3767; ARI 0,0871 ≈ 0,087 en Tabla 62 y 0,09 en 6.3.2.4).
- [cadena-logica] Vista conductual de 12 hábitos justificada con bitácora completa de vistas A/B/C (Tabla 63: A descartada por dominancia one-hot y reprobación plana 39,6–39,9%; B por dominancia de la edad con reprobación idéntica; C con reprobación diferenciada 18,0–51,7%) — responde a la observación del profesor sobre vistas minables descartadas y 'narrativa de la experimentación' (messages 11 y 12).
- [cadena-logica] Supuesto de tendencia de agrupamiento declarado, verificado empíricamente ANTES de modelar (Hopkins H=0,67, calibrado contra nube gaussiana 0,68, cuatro grupos 0,86 y uniforme 0,50; 5.5, coincide con briefing) y con su violación discutida e integrada en cadena: hipótesis en D.3 → verificación 5.5 → encuadre 'partición operativa' → lectura de la silueta baja en 6.3.2.3 → reserva en Tabla 65 → limitación en 9.3 y lección en 9.4(6). Observación del profesor sobre Hopkins atendida con interpretación correcta del valor.
- [cadena-logica] Supuesto de independencia de NB verificado para los predictores numéricos (D.3: matriz de las 12 conductuales, |r| máx 0,005; 6.1.1 'atributos poco correlacionados... vuelve plausible su supuesto') — cadena EDA → justificación de técnica coherente (la cobertura de los categóricos se reporta como hallazgo aparte).
- [cadena-logica] Nota de 2.3 ('No se asume que los datos siguen una distribución normal; dicha condición... será verificada empíricamente') cumplida a nivel marginal: 4.3.3 reporta asimetría, curtosis y gráficos Q-Q por variable (la condicionalidad por clase se reporta como hallazgo aparte).
- [cadena-logica] División 70/15/15 con justificación presente (6.2: gran volumen disponible, uso habitual, 25.701 casos de prueba 'más que suficientes para estimar las métricas con precisión') y estratificación justificada con cita (Witten et al., 2016).
- [cadena-logica] Regla de decisión de Tabla 57 aplicada consistentemente dentro de las estrategias de re-muestreo: submuestreo (73,6%/75,2%) supera a sobremuestreo (71,8%/75,3%) en exactitud cumpliendo ambos el recall ≥ 75% — la fila 'SELECCIONADA' es coherente con la regla enunciada.
- [cadena-logica] Referencia sin balancear coherente en toda la cadena: árbol 75,0%/66,1% (validación, Tabla 57), NB 80,5%/68,2% en test (6.3.2.4, coincide con ground truth 0,8050/0,6821) y 68,7% en validación (6.3.1) — cifras distintas por conjunto distinto, sin contradicción; baseline clase mayoritaria 60,2% consistente en 6.2, Tabla 61 y 7.1.1.
- [cadena-logica] Coherencia resultados→conclusiones: 9.3 repite exactamente las cifras aprobadas (80,2%, 81,2%, 25.701 casos, silueta 0,063, brecha 18,0%–51,7%, tercil alto 56,2% del grupo de mejores hábitos — coincide con terciles del ground truth g1 Alto 56,2) y mantiene las limitaciones (R-02, uso operativo no taxonómico).
- [cadena-logica] Despliegue coherente con los criterios: 8.2.4 usa el mismo umbral comprometido como gatillo de reentrenamiento ('si el recall de Fail cae bajo el 75% comprometido') y la fila del umbral nominal 0,5 de Tabla 70 reproduce la operación comprometida en CE1 (81,2% de recall).
- [cadena-logica] Aritmética de comparaciones de negocio verificada: brecha de reprobación 51,7−18,0 = 33,7 ('más de 33 puntos', línea 1244) y 51,7/18,0 = 2,87 ('casi triplica', líneas 1304 y 1347).
- [cadena-logica] Observación del profesor sobre conclusiones explicativas ('el porqué') razonablemente atendida en IX: 9.1 explica por qué ganó NB (ajuste supuestos-datos), 9.3 explica por qué la métrica global escondía el problema de recall y 9.4 destila lecciones causales, no solo resumen de resultados.
- [cadena-logica] Observación del profesor 'de tareas a objetivos' atendida: los objetivos 3.1 se redactan como construcción de modelos con finalidad de negocio ('detección temprana del riesgo de reprobación') y las metas cuantitativas quedan en 3.2 (accuracy ≥ 80%, recall ≥ 75%), estructura estándar CRISP-DM equivalente al ejemplo dado por el profesor.
- [cadena-logica] Coherencia interna 5.3–5.4: la nota de 5.3 aclara correctamente que el muestreo estratificado opcional de 5.4 'conserva la proporción de clases, pero no constituye una técnica de balanceo' — sin confusión entre ambos mecanismos.
- [cadena-logica] Coherencia de la vista de clasificación entre secciones: 21 atributos = 20 predictores + pass_fail (5.4, Figura 5.1) = 13 numéricos + 7 categóricos tras excluir previous_grade; los '20 atributos de la vista minable' de la demo web (8.2.3) coinciden con los 20 predictores (la única cifra discordante, '14 atributos numéricos' en 6.1.1, se reporta como hallazgo).
- [redaccion-citas] Barrido grep -i de palabras prohibidas (diapositiva, diapo, slide, ppt, profesor, pauta, rúbrica, cátedra, instrucciones de curso) sobre full_text.md y tables.md: cero apariciones que delaten material del curso.
- [redaccion-citas] "docente" aparece solo en "ahorro de horas docentes" (línea 490 y TABLA-DOCX 40): uso legítimo del dominio de negocio (beneficio económico), no alusión al profesor del curso.
- [redaccion-citas] "apuntes" (todas sus apariciones, p. ej. líneas 612, 749-759, 1192, 1214, 1345) refiere siempre a la variable notes_quality_score del dataset: uso legítimo.
- [redaccion-citas] "clase/clases" aparece solo como clase Fail/Pass (machine learning), "pesos por clase" o "asistencia a clases" (variable attendance): ningún uso en el sentido de sesión del curso universitario.
- [redaccion-citas] "presentación" no aparece como palabra: los matches del grep corresponden a "representación/sobre-representación" (líneas 876, 924).
- [redaccion-citas] "instrucciones" solo en "instrucciones de reproducción" del README (líneas 1544 y TABLA-DOCX 72): uso legítimo de documentación técnica.
- [redaccion-citas] Redacción impersonal verificada con barrido de ~35 formas verbales de 1.ª persona (hicimos, nuestro, nosotros, creemos, hemos, podemos, observamos, etc.): solo 2 apariciones en 1.554 líneas (líneas 1308 "¿construimos...?" y 1413 "aprendimos"), ambas reportadas; el resto del informe mantiene el registro impersonal.
- [redaccion-citas] Cruce citas→referencias completo: las 6 obras citadas en el texto (Chapman et al., 2000; Quinlan, 1993; Witten et al., 2016; Rousseeuw, 1987; Davies y Bouldin, 1979; Kaufman y Rousseeuw, 1990) existen todas en la sección XI.
- [redaccion-citas] Sección XI en orden alfabético correcto (Chapman → Davies → Ghai → Kaufman → Pedregosa → Quinlan → Rousseeuw → Tukey → Witten) y conector "y" antes del último autor homogéneo en las 9 entradas.
- [redaccion-citas] Silueta y Davies-Bouldin correctamente citados en su primer uso metodológico (línea 1123: Rousseeuw, 1987; Davies y Bouldin, 1979) y reiterados en 6.2 y 7.1.1; corrección de Laplace citada vía Witten et al., 2016 (línea 1161).
- [redaccion-citas] CRISP-DM citado en su primer uso estructural (línea 514, "las 6 fases de la metodología CRISP-DM (Chapman et al., 2000)"), en la bitácora de iteraciones (línea 1253) y en VII (línea 1283).
- [redaccion-citas] Conclusión 9.1 razona el porqué de los fenómenos (por qué NB superó al árbol: ajuste de supuestos a datos con atributos independientes; por qué Python fue la herramienta definitiva): interpretación, no resumen.
- [redaccion-citas] Conclusión 9.3 declara explícitamente las limitaciones exigidas: datos sintéticos (restricción R-02, conclusiones metodológicas hasta revalidar con datos reales) y silueta 0,063 (uso operativo y no taxonómico de la segmentación): validez externa acotada.
- [redaccion-citas] Observación del profesor "el punto sobre riesgo es más recomendación que conclusión" resuelta: el análisis de riesgo de operar con grupos solapados está ubicado en el Despliegue (8.1, línea 1348) y no en las Conclusiones IX (queda solo la frase menor de uso responsable reportada como Estilo).
- [redaccion-citas] Observación del profesor "conclusiones descriptivas, no explicativas" atendida en lo sustantivo: 9.1–9.4 contienen razonamiento causal (p. ej. línea 1410: "la métrica global escondía exactamente la diferencia que le importa al negocio"; línea 1413: lecciones con su porqué).
- [redaccion-citas] Observación del profesor sobre redacción de objetivos (tarea→objetivo con meta medible) atendida: 3.1 redacta los objetivos con fin de negocio (líneas 505-506) y 3.2 fija metas cuantitativas (accuracy ≥ 80%, recall Fail ≥ 75%, ≥ 3 grupos interpretables).
- [redaccion-citas] Conteos textuales verificados correctos: "tres lecciones" en 9.2 = 3 ítems (a-c); "tres modos" en 8.2.2 = 3; "cuatro bloques" y "cuatro casos precargados" en 8.2.3 = 4; "ocho casos representativos" = 8 filas en Tabla 69; "dos áreas" de la interfaz en 8.2.3 = 2; "6 fases" CRISP-DM = 6 filas en Tabla 42 (solo fallan los dos conteos reportados: 9.4 y 8.1).
- [redaccion-citas] Naturaleza sintética de los datos declarada de forma consistente y honesta en 1.1 (línea 168), 4.1 (línea 538), R-02 (línea 311), PC-04 (línea 421), 7.2 (línea 1319) y 9.3 (línea 1410): la limitación de validez externa está bien cubierta.
- [redaccion-citas] Terminología 2.7 y glosarios (Tablas 37 y 45): lenguaje de negocio formal y consistente, sin coloquialismos; fuera de IX y de la línea 1251 no se detectaron expresiones informales en el barrido.
- [numeros-internos] Conteo de registros: 300.000 − 128.664 = 171.336 y 128.664/300.000 = 42,89% ≈ 42,9% (líneas 1048 y 1319); 171.336 − 2 = 171.334 (líneas 1063/1066) y cadena '300.000 → 171.336 → 171.334' de Tabla 66 aritméticamente correcta
- [numeros-internos] Split 70/15/15: 119.933 + 25.700 + 25.701 = 171.334 (Tabla 56); 0,70×171.334 = 119.933,8 y 0,15×171.334 = 25.700,1 → redondeos correctos; % Fail 39,82% idéntico en los tres subconjuntos y coherente con pct_fail 0,3982 del JSON
- [numeros-internos] Matriz NB [[8309,1925],[3168,12299]]: accuracy 0,8018→80,2%; recall Fail 8309/10234 = 0,8119→81,2%; precisión Fail 8309/11477 = 0,7240→72,4%; F1 Fail 0,7654→76,5%; precisión Pass 0,8647→86,5%; recall Pass 0,7952→79,5%; F1 Pass 0,8285→82,9%; kappa 0,5949→0,595 — todos coinciden con Tabla 61, texto 6.3.2.3/6.3.2.4, Tabla 65, 7.1.2 y conclusiones 9.3
- [numeros-internos] Matriz árbol [[7616,2618],[4257,11210]]: accuracy 0,7325→73,3%; recall Fail 0,7442→74,4%; precisión Fail 0,6415→64,2%; F1 Fail 0,6890→68,9%; precisión Pass 0,8107→81,1%; recall Pass 0,7248→72,5%; F1 Pass 0,7653→76,5%; kappa 0,4566→0,457 — coinciden con Tabla 61 y todo el texto
- [numeros-internos] Figura 6.6 (IMG#055) muestra exactamente los mismos conteos de ambas matrices (7.616/2.618/4.257/11.210 y 8.309/1.925/3.168/12.299) y accuracy 0.733/0.802, recall 0.744/0.812 — consistente con Tabla 61
- [numeros-internos] '10.234 estudiantes que efectivamente reprobaron' = 8.309 + 1.925 y equivale a 0,3982×25.701; las 11.477 alertas del umbral 0,50 (Tabla 70) = 8.309 + 3.168 de la matriz NB — consistencia texto-tabla-matriz
- [numeros-internos] Tamaños K-Means 43.655 + 45.206 + 41.377 + 41.096 = 171.334 y porcentajes 25,5/26,4/24,2/24,0 correctos e idénticos en Tabla 60, 6.3.2.6, Tabla 68 y Figura 6.7 (IMG#056); tamaños K-Medoids 47.618 + 37.545 + 52.542 + 33.629 = 171.334
- [numeros-internos] % de reprobación por grupo (46,7/18,0/44,7/51,7) idéntico en Tabla 60, 6.3.2.6, Tabla 68, 8.2.3 (51,7% del G3), Figura 6.7 y conclusiones; ponderado por tamaños da 39,84% ≈ 39,8% global; brecha 51,7 − 18,0 = 33,7 → 'más de 33 puntos' y 'casi triplica' correctos
- [numeros-internos] Tabla 70 internamente consistente: % del alumnado = alertas/25.701 en los 5 umbrales (67,44/55,55/44,66/34,22/24,32) y recall×10.234 ≈ precisión×alertas en los 5 umbrales (difs ≤ 7 casos por redondeo); Figura 8.6 (IMG#064) coincide punto a punto
- [numeros-internos] VAN: −970.000 + 6.000.000×(1/1,1 + 1/1,1² + 1/1,1³) = 13.951.111,95 → $13.951.112 exacto; TIR del mismo flujo = 616,9% → 'aproximadamente 617%' correcto (Tabla 41 y texto 2.8)
- [numeros-internos] Costos/beneficios 2.8: 160 hrs = 4 analistas × 10 hrs/sem × 4 semanas; 160×5.000 = 800.000; 800.000 + 80.000 + 90.000 = 970.000 (Tablas 38-39); 4.200.000 + 1.800.000 = 6.000.000 (Tabla 40)
- [numeros-internos] Criterios de éxito de 3.2 reproducidos EXACTAMENTE en Tabla 65: accuracy ≥ 80% (CE1a), recall Fail ≥ 75% (CE1b), identificar el mejor algoritmo (CE1c), ≥ 3 grupos diferenciables e interpretables (CE2), con los mismos valores de Tabla 61; 'el árbol queda a 0,6 puntos de la meta' = 75,0 − 74,4 correcto
- [numeros-internos] Tabla 47: las 9 variables categóricas suman 300.000 cada una; Pass 60,24%/Fail 39,76% correctos; F (119.267) + vacío (4) = Fail (119.271) coherente; redondeos del texto (48/48/4, 45/35/20, 65,1/34,9, 71% F+D, ~16,7% extracurriculars) todos correctos
- [numeros-internos] Tabla 48/4.3.4: 300.000×25 = 7.500.000 celdas; 7.499.996 válidas = 99,99995%; 4/300.000 = 0,0013% — correctos
- [numeros-internos] Grid search: 112 = 7 profundidades × 4 mínimos × 4 estrategias (6.3.1 y anexo 10.2 coinciden); NB 27 = 3×3×3; Tabla 57 es subconjunto consistente de Tabla A.1 (submuestreo 16/50: 73,6/75,2; ponderación 16/50: 73,7/75,4; original 16/50: 75,0/66,1 idénticos en ambas)
- [numeros-internos] Árbol final 1.653 hojas / profundidad 16 idéntico en 6.3.1, 6.3.2.2, 6.3.2.5 y anexo 10.1; la diferencia con las 1.357 hojas de A.1 queda explicada en 6.3.1 (re-entrenamiento con entrenamiento+validación); raíz study_hours ≤ 4,59 del anexo coherente con Figura 6.1 y con los umbrales redondeados de la Tabla 64
- [numeros-internos] Hopkins 0,67 idéntico en 5.5, Tabla 55, 6.3.2.3, 7.1.2; rango declarado 0,671–0,676 compatible con la media 0,67; Figura 5.3 (IMG#049) muestra 0,50/0,67/0,68/0,86 = los cuatro escenarios del texto
- [numeros-internos] Silueta final 0,063/0,045 (= 0,0629/0,0445), Davies-Bouldin 2,77/3,38 (= 2,7669/3,3767) y ARI 0,087→'0,09' consistentes entre Tabla 62, 6.3.2.4, 7.1.2 y 9.3
- [numeros-internos] Tabla 63 coincide con la Figura 6.3 (IMG#052): vista A 0,125 (k=3), vista B 0,176 (k=2), vista C 0,074 (k=2) — leídos en el gráfico
- [numeros-internos] Figura 7.1 (IMG#058) coincide con el texto 7.1.1: silueta ≈0,32 con 2 variables, 0,22–0,24 con 3, 0,233 los 3 hábitos discriminantes, ≈0,063 con las 12
- [numeros-internos] Tabla 59: las 6 diferencias Pass−Fail son aritméticamente exactas (3,05/1,37/0,99/0,93/0,80/0,67) y las medias por clase ponderadas por 0,3982/0,6018 reproducen las medias poblacionales de la Tabla 53 (84,71/4,50/6,46/6,95/7,84/4,02) — fuerte coherencia interna; el texto 6.3.2.5 ('~1,4 horas más, ~3 puntos más de asistencia') coherente
- [numeros-internos] Tabla 46: IQR = Q3 − Q1 exacto en las 15 variables (±0,01 atribuible a redondeo de cuartiles); CV citados en 4.3.3 (43,9/11,1/20,9/21,0/22,1/48,7/61,6/27/30/21/49/57/23%) coherentes con SD/media; medianas y modas coinciden entre Tabla 46 y los bloques por variable
- [numeros-internos] Límites de Tukey citados en 4.3.3 verificados: study_hours >9,9 (5,84+1,5×2,70 = 9,89) y límite inferior negativo; attendance <58 (78,24−1,5×13,49 = 58,0); previous_grade <29,5 (= 29,52); group_study >4,2 (= 4,20)
- [numeros-internos] Tabla 53 (EDA 2): age vista media 16,50 y SD 1,12 = valores exactos de una uniforme {15,16,17,18}; crudo 18,00/2,00 = uniforme {15..21}; Fail 39,76% crudo vs 39,82% vista coherente con los JSON
- [numeros-internos] Porcentajes univariados coherentes entre secciones: n≈3.732 = 1,2% de 300.000 (study 0); n≈19.773 = 6,6% (attendance 100); picos en tope 16% (tareas), 6,8% (motivación), 6,7% (apuntes), 4,0% (gestión), 2,3% (salud mental) idénticos en los bloques por variable, el ranking comparativo de motivation_level y los Hallazgos Generales (C)
- [numeros-internos] Tabla 64: P1 (23.112; 72,3%) y P5 (23.692; 11,4%) idénticos en 6.3.2.6; P1 vs P2: 72,3 − 51,1 = 21,2 puntos exacto
- [numeros-internos] Tabla 69: la alerta coincide con el resultado real en exactamente 6 de 8 casos como afirma el texto, y los dos desaciertos citados (54152: P=15,7% pero reprobó; 272100: P=54,6% pero aprobó) son los correctos; todas las alertas SÍ corresponden a P>50%
- [numeros-internos] Conteo de atributos de las vistas: clasificación 21 = 13 numéricos + 7 categóricos + pass_fail (20 predictores); clustering 31 = 14 numéricas + 2 ordinales + 2 binarias + 13 one-hot (3+4+6); conductual 12 = 14 − age − previous_grade — consistente entre 5.1, 5.4, Tabla 63 y 7.2
- [numeros-internos] Figura 6.2 (IMG#051) coincide con las importancias del texto 6.3.2.2: study 24,5%, time_management ~14,7%, motivation ~13,4%, assignments ~12,0%, practice ~7,1%, notes ~7,0%
- [numeros-internos] NB sin balancear 80,5% / recall Fail 68,2% (= 0,8050/0,6821 del JSON) idéntico en 6.3.2.4 y 9.3; '1 de cada 3 no detectado' ≈ 31,8% y '4 de cada 5' ≈ 81,2% correctos; baseline clase mayoritaria 60,2% (= 0,6018) idéntico en 6.2, Tabla 61 y 7.1.1
- [numeros-internos] Validación cruzada 5 pliegues: rangos 80,1–80,4% (NB) y 73,5–74,2% (árbol), ambos con amplitud < 1 punto como afirma el texto (0,3 y 0,7)
- [numeros-internos] Figura 6.8 (IMG#057) coherente con los terciles del JSON: G0 Bajo ~39,6, G1 Bajo ~13,3 / Alto ~56, G2 Bajo ~37,6, G3 Bajo ~44,4; nota previa por grupo 69,8–69,9 idéntica en 7.1.1 y 9.3
- [numeros-internos] Carta Gantt (Tabla 42): 6 fases consecutivas sin huecos ni traslapes del 04-08-2026 al 16-11-2026
- [numeros-internos] Recuentos de contexto consistentes: 300.000 registros y 25 atributos idénticos en 1.1, 4.1, 4.1.1, Tabla 44 (25 filas), Tabla 48; mínimos exigidos 30.000/15 coherentes en 4.1.1 y 5.2; '~19 de cada 100' falsos negativos = 100 − 81,2 y '~72 de cada 100 alertas correctas' = precisión 72,4% (7.1.2)
- [numeros-fuente] Tabla 61 completa vs metricas_clasificacion.json: árbol test acc 0,7325→73,3%, kappa 0,4566→0,457, prec Fail 0,6415→64,2%, recall Fail 0,7442→74,4%, F1 Fail 0,689→68,9%, prec Pass 0,8107→81,1%, recall Pass 0,7248→72,5%, F1 Pass 0,7653→76,5%, AUC 0,8109→0,811; NB acc 0,8018→80,2%, kappa 0,5949→0,595, prec Fail 0,724→72,4%, recall Fail 0,8119→81,2%, F1 Fail 0,7654→76,5%, prec Pass 0,8647→86,5%, recall Pass 0,7952→79,5%, F1 Pass 0,8285→82,9%, AUC 0,8891→0,889; baseline 0,6018→60,2% ✓
- [numeros-fuente] Lectura de matrices de confusión (línea 1235): 10.234 reprobados reales en prueba (8.309+1.925); NB detecta 8.309 (8.309/10.234=81,2%) con 3.168 falsas alarmas; árbol 7.616 (74,4%) con 4.257 — coincide con las matrices del JSON ✓
- [numeros-fuente] Validación cruzada 5 pliegues: NB [0,8012;0,8044]→'entre 80,1% y 80,4%' ✓; árbol [0,7345;0,7418]→'entre 73,5% y 74,2%' ✓ (metricas_clasificacion.json cv5_accuracy_remuestreo_por_fold)
- [numeros-fuente] Tabla 56 (split) vs JSON: 119.933/25.700/25.701 (suma 171.334) y 39,82% de Fail en los tres subconjuntos ✓; balanceo JSON solo train: submuestreo 47.758+47.758 (prior 50/50 de 6.3.2.2 ✓) y distribución real Pass 60,2/Fail 39,8 ✓
- [numeros-fuente] Tabla 57 (las 5 filas) vs grid_search_arbol.csv: submuestreo 16/50 0,7356/0,7523; sobremuestreo 8/200 0,7184/0,7527; ponderación 16/50 0,7370/0,7544; original 16/50 0,7503/0,6613; original 4/500 0,7062/0,4861 ✓; regla de selección verificada: 16/50 submuestreo es la mayor accuracy entre configuraciones de re-muestreo con recall Fail ≥ 75% ✓
- [numeros-fuente] Tabla A.1 (12 filas) = top-3 por accuracy de cada estrategia en grid_search_arbol.csv, incluidas las hojas (1680/1680/1415; 1489/821/1709; 2037/2033/1578; 1357/1358/1211) ✓
- [numeros-fuente] Tamaños de malla: grid_search_arbol.csv tiene 112 filas (7 profundidades × 4 mínimos × 4 estrategias, anexo 10.2 ✓) y grid_search_naive_bayes.csv 27 filas (3×3×3, sección 6.3.1 ✓)
- [numeros-fuente] Selección NB: submuestreo, var_smoothing=1e-9, alpha=0,1, validación 0,8014/0,8162 → '80,1% / 81,6%' ✓; referencia original recall Fail 0,6874→'68,7%' ✓; 'configuraciones prácticamente idénticas dentro de cada estrategia' ✓ (CSV); 'cede menos de 1 punto de exactitud' (80,75→80,14) ✓
- [numeros-fuente] Árbol final 1.653 hojas y profundidad 16 (6.3.1, 6.3.2.2 y anexo 10.1) ✓ JSON; referencias sin balancear: NB test 0,805/0,6821→'80,5%/68,2%' (6.3.2.4 y 9.3) ✓; árbol sin balancear valid 75,0/66,1 ✓
- [numeros-fuente] Tabla 59 completa vs naive_bayes_medias_por_clase.csv: asistencia 82,868/85,919 (dif 3,05); estudio 3,677/5,048 (1,37); gestión 5,87/6,86 (0,99); motivación 6,386/7,317 (0,93); tareas 7,360/8,163 (0,80); ensayos 3,620/4,288 (0,67) ✓
- [numeros-fuente] Tabla 60/68 vs clustering_perfiles_kmeans.csv y despliegue_segmentos.csv: n 43.655/45.206/41.377/41.096 (suma 171.334 ✓), % reprobación 46,7/18,0/44,7/51,7 ✓, rasgos distintivos 4,32 (G0 gestión), 7,99 (G1 gestión), 4,62 (G2 apuntes), 4,63 (G3 motivación) y medias poblacionales 6,46/6,94/6,95 ✓; % alumnado G0 25,5, G1 26,4, G3 24,0 ✓ (solo G2 difiere: hallazgo)
- [numeros-fuente] Tabla 62 vs metricas_clustering.json: siluetas 0,0629→0,063 y 0,0445→0,045; Davies-Bouldin 2,7669→2,77 y 3,3767→3,38; tamaños K-Medoids 47.618/37.545/52.542/33.629 ✓; ARI 0,0871→0,087 (y 0,09 en 6.3.2.4) ✓
- [numeros-fuente] Medoides student_id 133587, 130930, 51493, 34014 (6.3.2.2) ✓ metricas_clustering.json
- [numeros-fuente] Tabla 63 vs clustering_barrido_k.csv y 'vistas_descartadas' del JSON: A 0,1247→0,125 (k=3), B 0,1759→0,176 (k=2), C 0,0744→0,074 (k=2) y 0,0617→0,062 (k=4); % fail A 39,6-39,9 plano ✓, B 39,6/40,0 con edades medias 15,5/17,5 ✓; texto de elección de k 'casi plana entre k=2 y k=5 (0,062-0,074)' = rango 0,0617-0,0744 del barrido ✓
- [numeros-fuente] Figuras 6.1, 6.2, 6.3, 6.4, 6.6, 6.7, 6.8 y 8.6 del informe son byte-idénticas (MD5) a clasificacion_arbol_decision.png, clasificacion_importancia_variables.png, clustering_codo_silueta.png, clustering_perfiles_heatmap.png, clasificacion_matrices_confusion.png, clustering_tamanos_reprobacion.png, clustering_coherencia_rendimiento.png y despliegue_umbral.png generadas por los scripts a partir de los CSV ✓ (Figura 6.3 = barrido CSV; Figura 6.8 = coherencia CSV; Figura 8.6 = umbral CSV)
- [numeros-fuente] Tabla 70 completa (25 valores) = despliegue_umbral_alertas.csv ✓; % del alumnado verificado aritméticamente sobre 25.701 (17.332→67,4%; 14.278→55,6%; 11.477→44,7%; 8.795→34,2%; 6.251→24,3%) ✓; texto de 8.2.4 (44,7%/81,2%; 0,7→24,3%/86,6%; 0,3→95,9%) ✓; métricas de umbral incrustadas en la demo (script 06 UMBRAL_STATS) idénticas al CSV ✓
- [numeros-fuente] Tabla 69: los 8 casos coinciden con despliegue_casos_ejemplo.csv en ID, hábitos, P(reprobar), alerta, perfil, acción y resultado real ✓; 'coincide en 6 de los 8 casos' verificado ✓
- [numeros-fuente] Importancias del árbol (6.3.2.2): 24,5/14,7/13,4/12,0/7,1/7,0% = arbol_importancia_variables.csv (0,2447/0,1465/0,1336/0,1204/0,0713/0,0704) ✓; socio-demográficos en conjunto 0,34% < 10% ✓
- [numeros-fuente] Anexo 10.1 idéntico línea a línea (94/94 líneas, 0 diferencias) a resultados/arbol_reglas.txt ✓; umbrales de Tabla 64 (4,6/6,8/7,2/6,8/6,0/6,4/6,7) coinciden con los cortes 4.59/6.84/7.16/6.76/6.04/6.45/6.67 de los 3 primeros niveles del árbol ✓
- [numeros-fuente] Tabla 64 recomputada sobre train+valid (mismo split, semilla 42): % reprueba 72,3/51,1/52,3/49,9/11,4 coinciden EXACTAMENTE; n (23.093/20.056/14.694/11.200/23.664) coinciden dentro de ±30 casos con los publicados (23.112/20.055/14.675/11.179/23.692), desviación atribuible a los umbrales exactos del árbol simplificado de profundidad 3 ✓
- [numeros-fuente] η² recomputado sobre la vista conductual con las asignaciones K-Means: notes 0,502, gestión 0,491, motivación 0,494 → 'η² ≈ 0,49-0,50 cada uno' ✓ y los otros nueve hábitos η² ≤ 0,004 → '≈ 0' ✓ (6.3.2.3)
- [numeros-fuente] PCA 2 componentes sobre la vista conductual: 22,0% de varianza explicada = 'los dos primeros componentes resumían solo el 22% de la información' (6.3.2.1) ✓
- [numeros-fuente] Script 01 confirma 5.1-5.3: filtro age.between(15,18), conteos asertados 300.000→171.336→171.334 (Tabla 66 ✓; '2 registros' erróneos en el subconjunto escolar ✓; 42,9%=128.664/300.000 ✓), Min-Max, codificación ordinal family_income 0/1/2 y parent_education 0/1/2/3, binarias internet_access No=0/Yes=1 y school_type Public=0/Private=1, One-Hot gender/device_type/extracurriculars (3/4/6 columnas) — todo idéntico a Tabla 51 ✓; exclusión de student_id, final_grade, grade_category y previous_grade de la vista de clasificación ✓; 'None' como categoría (keep_default_na=False) ✓; exporta ARFF ✓
- [numeros-fuente] Tabla 52 = rangos_normalizacion.json (14 pares mín/máx, incl. group_study_hours máx 5,84) ✓
- [numeros-fuente] Tabla 53 columna 'vista': medias y SD de las 14 numéricas coinciden con base_limpia_para_perfilamiento.csv (age 16,50/1,12; attendance 84,71/9,41; previous_grade 69,87/14,70; notes 6,94; motivation 6,95/1,88; etc.); n=171.334 y Fail 39,82% ✓
- [numeros-fuente] Script 02 confirma 6.2/6.3.1/7.1.1: SEED=42, split estratificado 70/15/15 (test_size 0,30 y luego 0,50), criterio 'entropy', mallas max_depth {4,6,8,10,12,16,None} × min_samples_leaf {1,50,200,500} × 4 estrategias, NB var_smoothing {1e-9,1e-7,1e-5} × alpha {0,1;1;10} × 3 estrategias, balanceo aplicado SOLO al train, CV 5 pliegues re-muestreada dentro de cada fold, reentrenamiento final con train+valid, sin datos sintéticos (solo re-muestreo de filas reales), export_text max_depth=4 para arbol_reglas.txt ✓
- [numeros-fuente] Script 03 confirma 6.3.1/6.2: K-Means init k-means++ con n_init=10 (max_iter 300 por defecto de sklearn), CLARA con 5 muestras de 4.000, PAM alternado máx 25 iteraciones con inicialización tipo k-means++, evaluación del costo sobre 30.000, asignación final de los 171.334, k=4, semilla 42; silueta sobre muestra de 10.000; barrido k=2..10 en las tres vistas; terciles de rendimiento con qcut(3); pass_fail/final_grade/previous_grade nunca entran al clustering (solo ex post) ✓
- [numeros-fuente] Vista de clasificación: 171.334 × 21 columnas (20 predictores + pass_fail, sin previous_grade) = texto de 5.4 ✓; vista de clustering 171.334 × 31 columnas ✓; vista conductual 12 columnas sin age ni previous_grade ✓; clustering_asignaciones.csv tiene 171.334 filas ('cada uno de los 171.334 estudiantes quedó etiquetado', 8.1) ✓
- [numeros-fuente] Nota previa por grupo 69,88/69,91/69,88/69,82 → 'prácticamente idéntica (69,8-69,9)' (7.1.1 y 9.3) ✓ clustering_perfiles_kmeans.csv
- [numeros-fuente] Script 04 confirma 8.2.1/8.2.4: aplica el NB aprobado sobre el conjunto de prueba reconstruyendo el split con semilla 42, 8 casos por percentiles de riesgo, umbral nominal 0,5, umbrales {0,30-0,70}, tabla de segmentos y figura despliegue_umbral.png; los tres archivos citados en VIII (despliegue_segmentos/casos_ejemplo/umbral_alertas.csv) existen ✓
- [numeros-fuente] Script 05 confirma 8.2.2: modos interactivo / lote (--csv, plantilla datos/sistema_plantilla.csv) / --demo (3 estudiantes), parámetro --umbral (defecto 0,5), usa rangos_normalizacion.json + naive_bayes_mixto.joblib + kmeans.joblib ✓
- [numeros-fuente] Demo web (script 06 + demo_web/): 4 casos precargados ('Promedio', 'A · hábitos sólidos', 'B · desmotivado', 'C · desorganizado'), autotest contra el modelo Python sobre los 4 presets con mensaje 'OK (4/4 casos verificados vs. Python)', slider de umbral min=0.3 max=0.7 ✓ (8.2.3)
- [numeros-fuente] Estructura de carpeta: todos los archivos nombrados en Tabla 58 y Tabla A.2 existen con esos nombres (4 .joblib, CSV/ARFF de datos, 6 scripts, JSONs y CSVs de resultados, README.txt, demo_web/index.html, Informe Segmentación Conductual .docx) ✓; la sección 7 del docx de segmentación es efectivamente el análisis de riesgo de grupos solapados citado en 8.1 ✓
- [numeros-fuente] Tabla 65: CE1a 73,3/80,2 y CE1b 74,4/81,2 = JSON ✓; 'el árbol queda a 0,6 puntos de la meta' (75,0-74,42=0,58) ✓; CE2 silueta 0,063 ✓
- [numeros-fuente] 8.1: 'cerca de tres de cada cuatro estudiantes pertenecen a un grupo de riesgo' = 25,5+24,1+24,0 = 73,6% ✓; 'el grupo desmotivado casi triplica la reprobación del de alto desempeño (51,7% vs. 18,0%)' ✓ fuente
- [figuras-1] IMG#001–IMG#003 (portada): logos UNAP, ICCI y sello de acreditación nítidos y legibles; no requieren caption de figura ✓
- [figuras-1] Fig 4.1 (IMG#004): coherencia texto-figura del contenido — rango 15–21 años, reparto uniforme ~14,3 % con línea de referencia 1/7, coincide con línea 659 ('cada edad concentra entre 14,2% y 14,4%, sin que ninguna predomine') ✓
- [figuras-1] Fig 4.2 (IMG#005): caja Q1–Q3 en 16–20, mediana 18, bigotes 15–21, sin atípicos = Tabla 46 (Q1 16, Q3 20, mín 15, máx 21, % outliers 0,00 %) ✓; legible
- [figuras-1] Fig 4.3 (IMG#006): forma de campana centrada en 4,5 h, barra destacada en 0 y cola fina hasta 12 h = línea 671 ✓ (aparte de los hallazgos de ticks y barra ámbar reportados)
- [figuras-1] Fig 4.4 (IMG#007): violín con caja interna Q1–Q3 3,1–5,8 h, mediana 4,5 h, cola derecha hasta 12 h y '0,35 % atípicos altos' = Tabla 46 y línea 674 ('todos por sobre 9,9 hrs') ✓
- [figuras-1] Fig 4.5 (IMG#008): sesgo a la izquierda, mediana 85 %, pico aislado en el extremo derecho = línea 683 ✓; ejes con título y unidades ('Asistencia (%)') ✓
- [figuras-1] Fig 4.6 (IMG#009): salto vertical final de ~93,4 % a 100 % (= 6,6 %) y nota 'Bajo 60 % hay apenas un 0,6 %' coherente con línea 686 ('solo un 0,62% baja del 60%') ✓
- [figuras-1] Fig 4.7 (IMG#010): centrada en 7 h, mitad central 6–8 h, acumulación leve en el tope 10 = líneas 695 y 698 ✓
- [figuras-1] Fig 4.8 (IMG#011): puntos alineados sobre la recta normal con aplanamiento horizontal en el tope 10 (y punto desviado en 3) = línea 698 ('visible en el Q-Q como puntos horizontales en los topes') ✓; ejes titulados ✓
- [figuras-1] Fig 4.9 (IMG#012): distribución amplia casi simétrica centrada en 70, nota 'SD 14,7' = línea 707 y Tabla 46 ✓
- [figuras-1] Fig 4.10 (IMG#013): caja 59,9–80,1 (IQR 20,2), mediana 70, puntos rojos de atípicos bajos < 29,5 (0,34 %) = Tabla 46 y línea 710 ('caen todos por debajo de 29,5 puntos; no hay outliers altos') ✓
- [figuras-1] Fig 4.11 (IMG#014): sesgo a la izquierda, cuerpo entre 6,7 y 9,4, barra dominante en 10 ≈ una sexta parte = líneas 719 y 721 ✓; línea discontinua en mediana 8 ✓
- [figuras-1] Fig 4.12 (IMG#015): ECDF con salto vertical de ~84 % a 100 % en x=10 = 16 % apilado, coherente con línea 721 ('El 16% se ubica exactamente en 10/10') ✓
- [figuras-1] Contenido de los gráficos de practice_tests_taken (IMG#018/IMG#019): barra ámbar '2,3 % que no realiza ningún ensayo', escalón inicial 2,3 % en la ECDF y 'mitad central entre 2,7 y 5,4' = líneas 730–733 y Tabla 46 (Q1 2,66 / Q3 5,35) ✓ — el contenido es correcto; el problema reportado es solo su ubicación bajo captions ajenos
- [figuras-1] Contenido de los gráficos de group_study_hours (IMG#016/IMG#017): sesgo a la derecha, mediana 1,5 h, barra 6,6 % en 0 h, caja 0,8–2,2 h y 'Sobre 4,2 h: 0,36 % atípicos altos' = líneas 742–746 y Tabla 46 (Q1 0,83 / Q3 2,17) ✓ — ídem, contenido correcto
- [figuras-1] Fig 4.17 (IMG#020): asimetría negativa con masa en la zona alta y pico resaltado en naranja en 10 (6,7 %) = líneas 755 y 757 ✓
- [figuras-1] Fig 4.18 (IMG#021): violín con caja Q1–Q3 5,7–8,4, mediana 7,0, cola hacia valores bajos y 'atípicos (0,37 %) son todos bajos' = Tabla 46 (5,65/8,36; 0,37 %) y línea 758 ('muy pocos estudiantes por debajo de 3 puntos') ✓
- [figuras-1] Legibilidad general IMG#004–IMG#021: tipografías grandes, alto contraste (barras azules/fondo blanco, texto negro), títulos internos y ejes con nombre y unidades en todas las figuras; sin el problema de contraste tipo 'Medium/High' criticado por el profesor en estas 21 imágenes ✓
- [figuras-1] Chequeos aritméticos: 6,6 % × 300.000 = 19.800 ≈ n 19.773 (línea 685) ✓; 1,2 % × 300.000 = 3.600 ≈ n 3.732 (línea 673, 1,24 %) ✓; salto ECDF Fig 4.12 de 84 % a 100 % = 16 % declarado ✓; 1/7 = 14,3 % línea de referencia Fig 4.1 ✓
- [figuras-1] Numeración y correspondencia caption-encabezado de las Figuras 4.1–4.12 y 4.17–4.18: cada pareja de figuras está bajo el encabezado de su variable y numerada consecutivamente según el esquema esperado (4.1–4.43) ✓
- [figuras-2] IMG#022 (Fig 4.19, time_management_score): tipo de gráfico coincide con caption (histograma); línea discontinua de la media en ≈6,46 = media declarada (full_text.md línea 766); escala 1–10 correcta; ejes con título; subtítulo interno ('media más baja 6,46, área más débil') coincide con el análisis (línea 767-769)
- [figuras-2] IMG#023 (Fig 4.20, violín gestión del tiempo): caja interna Q1–Q3 (5,1–7,8) → IQR 2,7 coincide con IQR 2,71 del texto; mediana 6,5 ≈ 6,49 declarada; mención de curtosis −0,41 idéntica en figura y texto (línea 766)
- [figuras-2] IMG#024 (Fig 4.21, motivation_level): histograma coherente con el texto (mediana 7,0; cola hacia valores bajos; pico destacado en 10); línea de media en ≈6,95 = media declarada (línea 778)
- [figuras-2] IMG#025 (Fig 4.22, violín motivación): Q1–Q3 (5,7–8,4) → IQR 2,7 = IQR 2,70 del texto; mediana 7,0 ≈ 7,01; 'atípicos 0,36 %, todos bajos' consistente con el texto (0,36%) y con la cerca superior 8,4+1,5·2,7=12,45>10 (solo puede haber atípicos bajos)
- [figuras-2] IMG#026 (Fig 4.23, mental_health_score): histograma acampanado centrado en 7 con la menor dispersión, coherente con SD 1,47 y CV 21% (línea 790-791); media marcada en ≈6,98; pico en 10 el más pequeño (2,3%) coincide con hallazgo 1 del texto (línea 793)
- [figuras-2] IMG#028 (Fig 4.25, screen_time): histograma centrado en 4 h, cola hasta 12 h y barra ámbar en 0 — coincide con análisis y hallazgos (líneas 803-807); media marcada ≈4,02; eje x con unidades (horas)
- [figuras-2] IMG#029 (Fig 4.26, violín screen_time): Q1–Q3 (2,7–5,4) → IQR 2,7 = IQR 2,70; mediana 4,0; r = −0,16 del pie interno coincide con la correlación declarada en el texto (línea 802)
- [figuras-2] IMG#030 (Fig 4.27, social_media_hours): histograma con asimetría positiva, mediana ≈2,5, cola hasta 8 h y barra ámbar en 0 — coincide con análisis y hallazgos (líneas 815-819)
- [figuras-2] IMG#031 (Fig 4.28, violín redes sociales): Q1–Q3 (1,5–3,5) → IQR 2,0 ≈ IQR 2,02 del texto; mediana 2,5; cola hasta 8 h coincide con rango 0–8
- [figuras-2] IMG#032 (Fig 4.29, final_grade): las dos líneas anunciadas por el texto ('ambas líneas marcadas en el gráfico', línea 829) están presentes: negra discontinua en ≈53 (media) y roja punteada en 50 (umbral); campana simétrica coincide con asimetría −0,04; eje 0–100 = rango declarado
- [figuras-2] IMG#033 (Fig 4.30, Q-Q final_grade): puntos alineados con la recta en todo el recorrido central con desviaciones leves solo en colas — coherente con 'la distribución más simétrica y cercana a la normal' (línea 827)
- [figuras-2] Tabla 47 recalculada: las 9 variables categóricas suman exactamente 300.000 cada una y todos los porcentajes recomputados coinciden con los publicados (gender 48,03/47,96/4,02; income 44,95/35,02/20,02; parent 45,03/35,08/14,98/4,91; internet 84,98/15,02; device 54,96/30,04/9,96/5,04; school 65,06/34,94; extracurriculars 16,57–16,75; grade F 39,76…A+ 0,10; pass_fail 60,24/39,76)
- [figuras-2] IMG#034 (Fig 4.31, gender): alturas ≈144K/144K/12K coinciden con Tabla 47 (144.083/143.871/12.046) y con el análisis 'paritaria 48,0/48,0/4,0' (línea 875)
- [figuras-2] IMG#035 (Fig 4.32, family_income): Medium≈135K > Low≈105K > High≈60K coincide con Tabla 47 y con '45,0/35,0/20,0'; la afirmación '8 de cada 10 de ingreso medio-bajo' = 79,97% ✓ (línea 881-882)
- [figuras-2] IMG#036 (Fig 4.33, parent_education): pirámide decreciente HS≈135K > Bachelor≈105K > Master≈45K > PhD≈15K = Tabla 47; 'sólo un 20% alcanza posgrado' = 14,98+4,91 = 19,89% ✓ (líneas 887-888)
- [figuras-2] IMG#037 (Fig 4.34, internet_access): Yes≈255K / No≈45K coincide con Tabla 47 (85,0/15,0) y con el análisis (línea 893)
- [figuras-2] IMG#038 (Fig 4.35, device_type): Laptop≈165K, Mobile≈90K, Tablet≈30K, None≈15K = Tabla 47; 'cerca de un tercio depende del celular y un 5% sin dispositivo' ✓ (líneas 899-900)
- [figuras-2] IMG#039 (Fig 4.36, school_type): Public≈195K / Private≈105K = 65,1/34,9, proporción 2:1 como afirma el texto (líneas 905-906)
- [figuras-2] IMG#040 (Fig 4.37, extracurriculars): seis barras ≈50K (~16,7% c/u) en el orden Arts > Coding Club > Music > None > Sports > Debate, idéntico a Tabla 47 y al análisis (línea 911)
- [figuras-2] IMG#041 (Fig 4.38, grade_category): F≈119K, D≈94K, C≈61K, B≈21K, A≈3,6K, A+≈0,3K y categoría '(vacío)' presente — coincide con Tabla 47; 'F 39,8% y D 31,5% (juntas el 71%)' = 71,24% ✓; los 4 registros vacíos mencionados en el texto (línea 918) figuran como categoría propia
- [figuras-2] IMG#042 (Fig 4.39, pass_fail): Pass≈181K (verde) / Fail≈119K (rojo) = 60,24/39,76 de Tabla 47 y del análisis (línea 923); codificación semántica de color correcta (verde aprueba / rojo reprueba)
- [figuras-2] Correspondencia caption-contenido de las Figuras 4.19–4.39: numeración secuencial sin saltos y tipo de gráfico de cada imagen coincide con lo anunciado en su caption (histograma/violín/Q-Q/distribución de frecuencias)
- [figuras-2] Legibilidad general IMG#022–IMG#033: resolución 1736×896 (histogramas/Q-Q) y 1820×644 (violines), tipografías grandes, alto contraste, ejes con título y unidades — sin problemas de lectura
- [figuras-2] Comprobado con recortes ampliados (4x) que los subtítulos internos de IMG#024 e IMG#028, que llegan al borde derecho de la imagen, terminan en palabras completas ('máximo', 'que'): no hay texto truncado
- [figuras-2] Coherencia cruzada de los picos en el tope citados en el texto (línea 781: motivación 6,8% > apuntes 6,7% > gestión del tiempo 4,0% > salud mental 2,3%) con los porcentajes de los pies internos de IMG#024, IMG#022 e IMG#026 — todos coinciden
- [figuras-3] IMG#043 (Fig 4.40): r de study_hours ≈0,43 y previous_grade ≈0,39 coinciden con el texto (línea 941); screen_time y social_media_hours negativas (~−0,16); age ≈0 y group_study_hours pequeña, coherente con 'prácticamente no se relacionan'; figura legible.
- [figuras-3] IMG#044 (Fig 4.41): diferencias Pass−Fail visibles ≈ +9,3 (previous_grade), +3,1 (attendance), +1,4 (study_hours) = texto línea 946; pantallas/redes negativas; legible.
- [figuras-3] IMG#045 (Fig 4.42): contiene exactamente las 12 variables conductuales; nota al pie '|r| < 0,01 (máximo observado: 0,005)' coincide con el texto (línea 949); diagonal 1,00 y resto ±0,00 correctos.
- [figuras-3] IMG#046 (Fig 4.43): 49.981 (extracurriculars 'None'), 15.105 (device_type 'None'), 4 (final_grade=0) y 4 (grade_category vacía) = Tabla 48; título '(las 21 columnas restantes…)' consistente con 25 atributos totales.
- [figuras-3] IMG#047 (Fig 5.1): 21 columnas contadas (20 predictores + pass_fail), sin previous_grade (coherente con 5.2), 10 filas, escalas originales, edades 15–18; legible.
- [figuras-3] IMG#048 (Fig 5.2): 31 columnas contadas (14 numéricas + family_income/parent_education ordinales + internet_access/school_type binarias + 3 gender + 4 device_type + 6 extracurriculars one-hot); numéricas en [0,1]; codificación coincide con 5.1.
- [figuras-3] Coherencia Fig 5.1 ↔ Fig 5.2: la primera fila de 5.2 es la normalización exacta de la primera fila de 5.1 (age 18→1,00; study 4,5→0,37=4,5/12; attendance 72,5→0,54=(72,5−40)/60; notes 10→1,00; Male→gender_Male=1; Laptop→device_type_Laptop=1; None→extracurriculars_None=1; Medium→1; Master→2; Public→0).
- [figuras-3] IMG#049 (Fig 5.3): barras 0,50 (uniforme), 0,67 (vista conductual), 0,68 (nube gaussiana), 0,86 (4 grupos) = texto línea 1102 y briefing (Hopkins 0,67); nota al pie coherente ('muestra de 20.000, media de 5 repeticiones'); legible.
- [figuras-3] IMG#050 (Fig 6.1): raíz study_hours ≤ 4,591 = '≤ 4,59' del texto (línea 1180); niveles siguientes gestión del tiempo, motivación y tareas = texto; umbrales coinciden redondeados con Tabla 64 (6,84→'6,8'; 7,163→'7,2'; 6,757→'6,8'; 6,038→'6,0'; 6,449→'6,4'; 6,666→'6,7'); nodo raíz value=[0.5,0.5] coherente con submuestreo 50/50.
- [figuras-3] IMG#051 (Fig 6.2): importancias del gráfico = texto (línea 1197) y CSV arbol_importancia_variables.csv: study_hours 0,2447→'24,5%', time_management 0,1465→'14,7%', motivation 0,1336→'13,4%', assignments 0,1204→'12,0%', practice_tests 0,0713→'7,1%', notes_quality 0,0704→'7,0%'.
- [figuras-3] IMG#052 (Fig 6.3): silueta vista A 0,125 en k=3, vista B 0,176 en k=2, vista C 0,074 en k=2 y ~0,062 en k=4 = Tabla 63 y barrido del briefing (k=3 0,0643; k=5 0,0620); línea discontinua en k=4 (k elegido); panel del codo sin codo claro = 'no es concluyente' (línea 1260); título 'muestra de 10.000' = diseño 6.2.
- [figuras-3] IMG#053 (Fig 6.4): n por grupo 43.655/45.206/41.377/41.096 = Tabla 60 y briefing; rasgos distintivos −1,1 (G0 gestión), +0,6/+0,8/+0,6 (G1), −1,2 (G2 apuntes), −1,2 (G3 motivación) coherentes con Tabla 60; previous_grade ≈ 0,0 en los 4 grupos, coherente con 'nota previa prácticamente idéntica' (7.1.1).
- [figuras-3] IMG#054 (Fig 6.5): centroides G0 (~4,3 gestión), G1 (~8,0), G2 (~4,6 apuntes), G3 (~4,6 motivación) = Tabla 60 (4,32/7,99/4,62/4,63); paneles = caption (gestión y apuntes frente a motivación); 'muestra de 20.000' en título = caption; nota al pie repite Hopkins 0,67 correctamente.
- [figuras-3] IMG#055 (Fig 6.6): matriz árbol [[7616,2618],[4257,11210]] y NB [[8309,1925],[3168,12299]] = ground truth del briefing; ambas suman 25.701; accuracy 0,733/0,802 y recall Fail 0,744/0,812 = Tabla 61; 7.616+2.618 = 8.309+1.925 = 10.234 reales Fail = texto línea 1235; falsas alarmas 4.257/3.168 = texto; precisión Fail derivada 7616/11873=64,2% y 8309/11477=72,4% = Tabla 61; 8.309+3.168=11.477 = 'Alertas emitidas' de la Tabla 70 en umbral 0,50 (validación cruzada de figuras).
- [figuras-3] IMG#056 (Fig 6.7): tamaños ≈43,7/45,2/41,4/41,1 mil y % reprobación ≈46,7/18,0/44,7/51,7 = Tabla 60/briefing; línea 'promedio global' ≈39,8; brecha 51,7−18,0=33,7 pts = 'difiere en más de 33 puntos' (línea 1244).
- [figuras-3] IMG#057 (Fig 6.8): composición por terciles de los 4 grupos = clustering_coherencia_rendimiento_kmeans.csv exacto (G0 39,6/34,7/25,7; G1 13,3/30,5/56,2; G2 37,6/34,8/27,6; G3 44,4/33,6/22,0) y = briefing; título aclara 'la nota NO participó en la formación de los grupos' = caption.
- [figuras-3] IMG#058 (Fig 7.1): silueta 0,063 con 12 variables (cuadrado negro), ~0,22–0,24 con 3, ~0,32 con 2, y diamante de los 3 hábitos discriminantes en 0,233 sobre la curva aleatoria = texto línea 1290 palabra por palabra; eje X 2/3/4/6/9/12; leyenda clara.
- [figuras-3] IMG#059 (Fig 8.1): la tabla de la primera página del entregable coincide con la Tabla 60: 45.206 (26,4%, 18,0%), 43.655 (25,5%, 46,7%), 41.377 (24,2%, 44,7%), 41.096 (24,0%, 51,7%); rasgos 8,0/4,3/4,6/4,6 vs medias 6,5/6,5/6,9/7,0 = Tabla 60 redondeada; '171.334 estudiantes de 15 a 18 años', '12 variables' y 'K-Means, k = 4' correctos; fecha 'Julio 2026' plausible.
- [figuras-3] IMG#060 (Fig 8.2): comando '05_sistema_prediccion.py --demo' = caption; tres casos 0,7% (sin alerta, Alto desempeño), 81,7% (SÍ, Riesgo por desmotivación, programa motivacional) y 99,3% (SÍ, Riesgo por gestión del tiempo, taller de planificación) = texto línea 1371 y briefing (81,7/99,3); medias impresas (4,5; 84,7; 7,0) = Tabla 53; entradas coinciden con el DEMO del script 05.
- [figuras-3] IMG#061 (Fig 8.3): 38,2% / RIESGO MODERADO / SIN ALERTA = caption exacto; métricas del umbral 0,50 (81,2% reprobados detectados, 72,4% alertas correctas, 44,7% alumnado alertado) = Tabla 70; pie 'Prueba (n=25.701): accuracy 80,2% · recall Fail 81,2% · AUC 0,89' = Tabla 61; encuesta con 20 atributos en 4 bloques (5+3+4+8) = texto línea 1377; 4 casos precargados (Promedio, hábitos sólidos, desmotivado, desorganizado) = texto; valores del caso Promedio ≈ medias de la Tabla 53; perfil 'Alto desempeño autónomo · Grupo 1 · 26,4% · 18,0%' = Tabla 60.
- [figuras-3] IMG#062 (Fig 8.4): P=81,7%, motivación 2,0/10 con barra roja bajo la media, alerta activada con 'programa motivacional y consejería', perfil 'Riesgo por desmotivación · Grupo 3 · 24,0% · reprobación histórica 51,7%' = caption y texto línea 1380; los 20 valores de entrada coinciden con el Estudiante B del script 05 (5,0/85/7/8/4/1,5/7/7/2/5/5/3/17/Masculino/Medio/Magíster/Sí/Celular/Privado/Ninguna).
- [figuras-3] IMG#063 (Fig 8.5): P=99,3%, riesgo crítico, estudio 1,0 h/día, asistencia 78%, gestión del tiempo 3,0/10, derivación al 'taller de planificación y organización', perfil 'Riesgo por gestión del tiempo deficiente · Grupo 0 · 25,5% · 46,7%' = caption y texto línea 1380; entradas coinciden con el Estudiante C del script 05.
- [figuras-3] IMG#064 (Fig 8.6): los 5 puntos de ambos paneles coinciden con la Tabla 70: % alumnado 67,4/55,6/44,7/34,2/24,3; recall Fail 95,9/90,2/81,2/68,5/52,9; precisión Fail 56,6/64,7/72,4/79,7/86,6; línea discontinua en el umbral nominal 0,50; texto de lectura (línea 1398) coherente con la figura.
- [figuras-3] Aritmética verificada: 43.655+45.206+41.377+41.096 = 171.334 (Figs 6.4/6.7/8.1 y Tablas 60/62/68); ambas matrices de confusión suman 25.701; recall Fail 7.616/10.234=74,42% y 8.309/10.234=81,19%; caption de la Figura 6.5 'muestra de 20.000' = título interno; caption Figura 6.3 '(vistas A, B y C)' = leyendas internas.
- [figuras-3] Captions de las 22 figuras revisadas (4.40–4.43, 5.1–5.3, 6.1–6.8, 7.1, 8.1–8.6) presentes, numerados en orden y ubicados junto a su imagen según image_map.txt; la numeración coincide con la esperada en el briefing.
- [feedback] Figura 5.1 (IMG#047, image63.png): captura de la ESTRUCTURA de la vista minable de clasificación con sus 21 columnas completas (contadas en la imagen: age…pass_fail) y encabezados blancos sobre fondo azul oscuro, números oscuros sobre filas claras — contraste correcto; resuelve 'capturas de la estructura' y 'vista completa, no extractos'.
- [feedback] Figura 5.2 (IMG#048, image64.png): 31 columnas completas verificadas (14 numéricas + family_income, parent_education, internet_access, school_type + 3 one-hot de gender + 4 de device_type + 6 de extracurriculars = 31); el encabezado más largo 'extracurriculars_Coding Club' está completo y legible (verificado con recorte ampliado).
- [feedback] Figura 6.6 (IMG#055, image53.png): matrices de confusión en figura dedicada y grande, ambas con números con separador de miles; valores 7.616/2.618/4.257/11.210 (árbol) y 8.309/1.925/3.168/12.299 (NB) coinciden con metricas_clasificacion.json; la lectura textual '10.234 estudiantes que efectivamente reprobaron' (línea 1235) = 8.309+1.925 correcto.
- [feedback] Figura 6.3 (IMG#052, image50.png): método del codo (inercia normalizada) y silueta para k=2..10 en las TRES vistas (A 31 attrs, B 14, C 12), con línea de referencia en k=4 — los experimentos con distintos k están graficados, no solo el resultado final.
- [feedback] Lectura explícita del codo y de la elección de k (línea 1260): 'el codo de la Figura 6.3 no es concluyente y la silueta de la vista C es casi plana entre k = 2 y k = 5 (0,062–0,074)… k = 4 entrega un grupo de alto desempeño integral y tres grupos de riesgo diferenciados…; con k = 3 los perfiles de riesgo se mezclan y con k = 5 se fragmentan' — el diagrama no está 'solo como imagen'; los valores 0,074 (k=2) y 0,062 (k=4) coinciden con el barrido del JSON (0,0744/0,0617).
- [feedback] Hopkins explicado como prueba calibrada de estructura vs. aleatoriedad: línea 1102 ('H = 0,67… prácticamente idéntico al de una nube gaussiana única… y lejos tanto del escenario con cuatro grupos separados (0,86) como del uniforme sin estructura (0,50)') y Figura 5.3 (IMG#049, image47.png) con la anotación 'H ≈ 0,5 indica ausencia de estructura y H → 1 fuerte tendencia a grupos'; H=0,67 coincide con el ground truth; además se usa para explicar el porqué de la silueta baja (líneas 1244 y 1304).
- [feedback] Bitácora de vistas minables probadas y descartadas con motivo: Tabla 63 (líneas 1256–1259) — vista A 'DESCARTADA: … sin valor de negocio', vista B 'DESCARTADA: la edad… domina la partición… sin valor de negocio', vista C 'SELECCIONADA' —, coherente con la nota de 5.4 (línea 1080), el hallazgo (2) de 7.2 (línea 1319) y 9.1 (línea 1404: 'La vista de agrupamiento se iteró tres veces').
- [feedback] Reglas del árbol destacadas: Tabla 64 (líneas 1266–1271, P1–P5 con % de reprobación y n) + interpretación en negocio 6.3.2.6 + Anexo 10.1 (reglas hasta profundidad 4) — cubren la petición de 'ver el árbol de cerca o destacar las reglas principales' y las '3 reglas de oro'.
- [feedback] Objetivos redactados como objetivos de DM con meta medible: 3.1 (línea 505: 'Construir un modelo de clasificación que prediga… con el fin de seleccionar el modelo de mayor exactitud y exhaustividad para la detección temprana del riesgo de reprobación') + 3.2 (línea 510: 'exactitud (accuracy) igual o superior al 80%… recall… igual o superior al 75%'), con el criterio explícitamente 'asociado al Objetivo 1'.
- [feedback] Columnas eliminadas con su porqué (vistas descartadas / narrativa de experimentación): 5.2 líneas 1050–1052 (student_id sin valor; final_grade y grade_category por fuga de información; previous_grade por dominar el modelo y sesgar la medición del impacto de los hábitos).
- [feedback] Conclusiones explicativas y no descriptivas: 6.3.2.4 línea 1251 ('La explicación técnica es directa: los datos se generaron con atributos mayormente independientes cuyo efecto sobre la nota es acumulativo, que es exactamente el supuesto de Naïve Bayes'); porqué del grupo de alto rendimiento: mejores hábitos (Tabla 60, G1) con nota previa idéntica entre grupos (línea 1289: '69,8–69,9') y factores socioeconómicos de bajo peso (línea 1305); lecciones interpretativas en 9.1–9.4 (p. ej. línea 1410: 'la métrica global escondía exactamente la diferencia que le importa al negocio').
- [feedback] Separación conclusiones vs. recomendaciones: las recomendaciones operativas están en 7.3 (Tabla 67, línea 1332 'se recomienda como proyecto siguiente') y 8.2.4 (plan de mantención y umbral); la sección IX (9.1–9.4) contiene interpretación y lecciones, sin recomendaciones operativas mezcladas.
- [feedback] El gráfico de grupos elogiado se presenta en contexto comparativo: Tabla 62 (silueta 0,063 vs 0,045; Davies-Bouldin 2,77 vs 3,38; Rand ajustado 0,087 — coinciden con metricas_clustering.json: 0,0629/0,0445, 2,7669/3,3767, 0,0871) y ranking K-Means vs K-Medoids en 6.3.2.4 (línea 1252).
- [feedback] Figura 6.8 (IMG#057, image55.png) legible; terciles por grupo coinciden con el ground truth (G1 Bajo ≈13%, Alto ≈56% vs. JSON 13,3/56,2; G0 Bajo ≈40 vs 39,6; G3 Bajo ≈44 vs 44,4).
- [feedback] Etiquetas categóricas 'Medium', 'Low', 'High' legibles en las barras del EDA (Figura 4.32, IMG#035/image35.png: texto gris oscuro sobre fondo blanco) — la crítica de legibilidad de esas etiquetas no se reproduce en las figuras del informe.
- [feedback] Figura 6.5 (IMG#054, image52.png): grupos en escala original de negocio con leyenda nombrada (G0–G3), centroides etiquetados y nota interpretativa al pie — legible y con buen contraste; además el texto (línea 1192) explica el abandono de la vista por componentes principales (solo 22% de la información).
