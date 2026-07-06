ENTREGA - ETAPAS VI (MODELAMIENTO), VII (EVALUACION) Y VIII (DESPLIEGUE)
Proyecto Data Mining - EduData Analytics (dataset sintetico Kaggle, 300.000 estudiantes)
=========================================================================

DECISIONES METODOLOGICAS (incorporadas tras la revision con el profesor)
------------------------------------------------------------------------
1. previous_grade NO es variable de entrada de ningun modelo. La nota del anio
   anterior domina la correlacion con el objetivo y sesga el analisis; como el
   objetivo es medir el impacto de los HABITOS, la nota solo se usa para
   etiquetar (pass_fail proviene de final_grade) y para validar, nunca como
   predictor.
2. El clustering se hace SOLO con habitos (12 variables conductuales, sin age
   ni previous_grade). La nota se "agrega" DESPUES de formar los grupos, para
   validar la coherencia de los perfiles (% de reprobacion y terciles de
   rendimiento Bajo/Medio/Alto por grupo).
3. Split estratificado 70/15/15 (train/validacion/prueba); cada fila es una
   persona unica (el ETL verifica que no haya student_id duplicados).
4. Balanceo de clases (la base viene 60,2% Pass / 39,8% Fail): se comparan
   sobremuestreo con reemplazo y submuestreo de la mayoritaria (sin datos
   sinteticos), aplicados SOLO al entrenamiento; validacion y prueba conservan
   la distribucion real. El MODELO FINAL es el balanceado (50/50) aunque su
   accuracy sea algo menor que la del modelo sesgado; la version sin balancear
   se reporta unicamente como referencia. La validacion cruzada re-muestrea
   dentro de cada fold (sin fuga de informacion por filas duplicadas).

ENTREGABLES DEL DESPLIEGUE (segun apuntes del curso)
----------------------------------------------------
- Tarea DESCRIPTIVA -> INFORME: "Informe Segmentacion Conductual (entregable
  tarea descriptiva).docx" (analisis de los 4 perfiles desde el negocio).
- Tarea PREDICTIVA -> SISTEMA: scripts/05_sistema_prediccion.py (ver abajo).

ESTRUCTURA DE LA CARPETA
------------------------
scripts/
  01_etl_vistas_minables.py   ETL completo (Etapa V): filtro edad 15-18, limpieza,
                              transformaciones y exportacion de las vistas minables.
                              La vista de clasificacion EXCLUYE previous_grade.
  02_clasificacion.py         Tarea predictiva: Arbol de Decision (C4.5, entropia)
                              vs. Naive Bayes mixto. Split estratificado 70/15/15,
                              malla de hiperparametros x 4 estrategias de balanceo
                              (original / ponderacion / sobremuestreo / submuestreo),
                              seleccion final entre las estrategias de re-muestreo.
  03_clustering.py            Tarea descriptiva: K-Means vs. K-Medoids (CLARA).
                              Codo + silueta, 3 vistas comparadas, k=4 sobre la
                              vista conductual (solo habitos) + validacion de
                              coherencia con la nota a posteriori.
  04_despliegue.py            Etapa VIII: aplica el NB aprobado sobre casos de
                              ejemplo del conjunto de prueba (P(reprobar) por
                              estudiante), analisis de umbral segun capacidad
                              operativa y catalogo de segmentos/intervenciones.
  05_sistema_prediccion.py    SISTEMA (entregable de la tarea predictiva segun
                              los apuntes): predice P(reprobar), alerta y perfil
                              conductual para estudiantes nuevos.
                                - interactivo:  python scripts/05_sistema_prediccion.py
                                - lote (CSV):   ... --csv entrada.csv salida.csv
                                - demostracion: ... --demo
                                - umbral configurable: --umbral 0.6
                              Plantilla de entrada: datos/sistema_plantilla.csv
                              (se puede llenar en Excel y guardar como CSV).
  06_generar_demo_web.py      Genera la DEMO WEB (demo_web/index.html): exporta
                              los parametros de los modelos aprobados y los
                              inyecta en la plantilla HTML.

demo_web/
  index.html                  DEMO WEB interactiva del modelo: un solo archivo
                              autocontenido (sin servidor ni internet, se abre
                              con doble clic). Sliders de habitos en vivo,
                              P(reprobar), umbral ajustable, perfil K-Means y
                              casos de ejemplo. Replica el modelo en JavaScript
                              y ejecuta un autotest al cargar que compara 4
                              casos contra el modelo original de Python.
  plantilla_core.html         Plantilla usada por 06_generar_demo_web.py.

datos/
  vista_minable_clasificacion.csv    171.334 x 21 (20 predictores + pass_fail,
                                     SIN previous_grade)
  vista_minable_clasificacion.arff   La misma vista en formato Weka
  vista_minable_clustering.csv       171.334 x 31 (vista A, documentada en 5.4)
  vista_minable_clustering_conductual.csv  171.334 x 12 (vista C: solo habitos,
                                     sin age ni previous_grade; seleccionada en VI)
  base_limpia_para_perfilamiento.csv Variables originales para el EDA por grupo
  sistema_plantilla.csv              Plantilla de entrada del sistema de prediccion
                                     (3 estudiantes de ejemplo; editable en Excel)

modelos/
  arbol_decision_c45.joblib     Arbol final (entropia, submuestreo 50/50,
                                prof. 16, hojas 1.653)
  naive_bayes_mixto.joblib      Naive Bayes mixto (submuestreo 50/50,
                                MODELO APROBADO, accuracy 80,2%)
  kmeans.joblib                 K-Means k=4 sobre vista conductual (MODELO APROBADO)
  kmedoids_clara.joblib         Medoides finales (comparacion)

resultados/
  metricas_clasificacion.json   Todas las metricas: split, balanceo, modelo final
                                balanceado y referencia sin balancear, CV5
  metricas_clustering.json      Barrido de k, silueta, Davies-Bouldin, ARI,
                                coherencia de rendimiento por grupo
  grid_search_arbol.csv         112 configuraciones (28 x 4 estrategias de balanceo)
  grid_search_naive_bayes.csv   27 configuraciones (9 x 3 estrategias de balanceo)
  arbol_reglas.txt              Reglas del arbol (hasta profundidad 4)
  arbol_importancia_variables.csv
  naive_bayes_medias_por_clase.csv
  clustering_perfiles_kmeans.csv / _kmedoids.csv   EDA por grupo (perfilamiento)
  clustering_coherencia_rendimiento_kmeans.csv / _kmedoids.csv
                                Validacion a posteriori: % de cada tercil de
                                rendimiento (Bajo/Medio/Alto) dentro de cada grupo
  clustering_asignaciones.csv   Grupo asignado a cada estudiante (ambos algoritmos)
  clustering_barrido_k.csv      Inercia y silueta para k=2..10 en las 3 vistas
  rangos_normalizacion.json     Rangos Min-Max (para aplicar a datos nuevos)
  despliegue_casos_ejemplo.csv  8 casos de ejemplo con P(reprobar), alerta,
                                perfil conductual, accion y resultado real
  despliegue_umbral_alertas.csv Alertas/recall/precision para umbral 0,3..0,7
  despliegue_segmentos.csv      Catalogo operativo: grupo, tamano, % reprobacion,
                                programa de intervencion

figuras/                        Todas las figuras insertadas en el informe (PNG)

COMO REPRODUCIR
---------------
Requisitos: Python 3.10+ con pandas, scikit-learn, scipy, matplotlib, joblib.
El CSV crudo (student_performance_prediction_dataset-2.csv) debe estar en la
carpeta padre de esta carpeta. Ejecutar en orden:

  python scripts/01_etl_vistas_minables.py
  python scripts/02_clasificacion.py
  python scripts/03_clustering.py
  python scripts/04_despliegue.py

Todos los procesos usan semilla fija (42): los resultados son reproducibles.

NOTA IMPORTANTE (carga de datos)
--------------------------------
En device_type y extracurriculars el valor "None" es una CATEGORIA valida
(sin dispositivo / sin actividad), no un dato faltante. pandas convierte por
defecto la cadena "None" en nulo: los scripts leen el CSV con
keep_default_na=False, na_values=[""] para evitarlo.

RESULTADOS PRINCIPALES
----------------------
Clasificacion (conjunto de prueba, n=25.701, distribucion real 60/40; modelos
finales entrenados con submuestreo 50/50 en train+validacion):
  - Naive Bayes balanceado:  accuracy 80,2% | recall Fail 81,2% | kappa 0,59 | AUC 0,89
    -> CUMPLE el Criterio de Exito 1 (accuracy>=80%, recall Fail>=75%). APROBADO.
    CV5 (re-muestreo por fold): 80,1% - 80,4% (estable).
  - Naive Bayes sin balancear (referencia): accuracy 80,5% | recall Fail 68,2%
    -> misma accuracy que el balanceado, pero deja escapar 1 de cada 3 reprobados:
    ilustra el sesgo de clase que el balanceo corrige.
  - Arbol balanceado (C4.5): accuracy 73,3% | recall Fail 74,4% | kappa 0,46 | AUC 0,81
    -> no alcanza el 80% de accuracy.
  - Arbol sin balancear (referencia): accuracy 74,8% | recall Fail 65,8%.
  - Baseline clase mayoritaria: 60,2%.

Agrupamiento (vista conductual de 12 habitos, sin nota ni edad; k=4):
  - K-Means (APROBADO): silueta 0,063 | Davies-Bouldin 2,77
    4 perfiles: Alto desempeno autonomo (18,0% reprobacion), Riesgo por
    desmotivacion (51,7%), Riesgo por gestion del tiempo (46,7%), Riesgo por
    apuntes deficientes (44,7%).
  - Validacion a posteriori (coherencia): previous_grade es practicamente
    identica entre los 4 grupos (69,8-69,9), es decir, los grupos NO se
    formaron por la nota; aun asi su % de reprobacion va de 18% a 52% y el
    grupo de mejores habitos concentra el 56,2% del tercil de rendimiento
    Alto (vs. 22,0% del grupo de menor rendimiento): los habitos por si
    solos separan perfiles de exito y de riesgo.
  - K-Medoids (CLARA): silueta 0,045 | Davies-Bouldin 3,38 (descartado).
