# Correcciones aplicadas — "Informe Data Mining (7) - corregido.docx"

Fecha: 2026-07-18. Origen: revisión de 79 hallazgos (ver "REVISION - Informe DM (6) - hallazgos (detalle).md").
El original (6) quedó intacto. Verificación automática posterior: 92 checks, 0 fallas
(números de figuras/tablas correlativos, referencias XI en orden alfabético, textos viejos ausentes,
imágenes correctas bajo cada caption, bytes de media = figuras regeneradas).

## Texto y tablas (aplicado)
- **F16** Tabla 55: referencia del Hopkins corregida a Figura 5.3 (Crítico).
- **F89** 7.1.1 y 9.3: "el 56,2% del grupo de mejores hábitos pertenece al tercil Alto…" (denominador corregido).
- **F80** Figuras 4.13–4.16: imágenes intercambiadas a su caption correcto (histogramas regenerados + swap de ECDF/violín).
- **F68** "13 atributos numéricos" · **F48** "seis lecciones" · **F76** "ocho secciones" · **F72** 24,1% (×3, ahora suman 100,0%) · **F60** "2 registros erróneos…" · **F62** umbral unificado "Pass (> 50)" · **F64** regla del anexo acotada a re-muestreo · **R1/R2** superlativos de simetría/normalidad rebajados.
- **F25** Caso de negocio realineado con la Gantt: 600 h × $5.000 = $3.000.000; inversión $3.170.000; **VAN $11.751.112; TIR ≈181%** (recalculados; siguen positivos).
- **F24** Párrafo en 3.1 que ancla ON-02 al EDA (D.1/D.2) e importancias (6.3.2.2). *Opcional manual: agregar un CE3 formal en 3.2 y su fila en Tabla 65.*
- **F27** CE2 operacionalizado en 3.2 (brecha ≥ 15 pts) y Tabla 65 evaluada contra esa meta (33,7 pts).
- **F26/F30** Tabla 55: verificación del supuesto NB declarada como marginal, con independencia de categóricos asumida; quitada la mención de final_grade en 5.5.
- **F28** Justificación sustantiva del re-muestreo vs. pesos por clase · **F29** cifra del sobremuestreo NB (80,1%/81,6%) añadida.
- **F33** Casos del despliegue reformulados como "mensaje de los patrones", sin afirmar cumplimiento literal de P3/P1–P4.
- **F34** "secciones IV a VIII" · **F35** supuesto de beneficios condicionado al piloto R-02 declarado en 2.8 · **F36** vínculo reprobación→deserción explicitado.
- **F70/F71/F75** Tabla A.2 acotada: qué genera el pipeline y qué son análisis auxiliares (Hopkins, Figs. 6.5 y 7.1).
- **F77** Tabla A.2 con filas nuevas (GUIA_KNIME, plantilla_core.html); `scripts/__pycache__/` eliminado.
- **Citas** (F38, F41–F46, F58, F13): Hopkins y Skellam 1954, Tukey 1977, Sapag y Sapag 2008, Arthur y Vassilvitskii 2007, Hubert y Arabie 1985 (6.2 y 7.1.1), Cohen 1988, Chapman et al. 2000 (2.7 y 9.2), Quinlan/Witten/Rousseeuw en 2.7, Wang y Strong 1996, Pedregosa et al. 2011, Ghai 2026. **XI pasa de 9 a 15 referencias**, en orden alfabético.
- **Estilo** (F4, F5, F6, F10–F14, F19–F23, F47, F50–F57, F79, F92, F93, F94): criterio a priori en 5.3; regresión de 7.3 marcada como exploratoria; "(ver Tabla 63)" en primer uso de vistas A/B/C; introducciones de fase I–IV y IX; cierre de la Etapa VIII; frases introductorias para Tablas 1–5, 12–14 y 43; portada sin doble espacio; capitalización de títulos (con espejo en el índice); citas múltiples en orden APA; impersonal en 7.2 y 9.4; sin "entregable de la tarea"/"carpeta de la entrega"; cita textual de la demo corregida; captions de 4.1, 6.2 y 6.4 precisados; "dos hábitos accionables más débiles" en 8.2.2.

## Nueva Tabla 70 (Lote 3 — conexión de modelos pedida por el profesor)
Cruce agregado calculado con el modelo NB real (`naive_bayes_mixto.joblib`, matriz reconstruida idéntica
a la publicada) × grupos de `clustering_asignaciones.csv`, sobre el conjunto de prueba (umbral 0,5):

| Grupo | n prueba | % alertado | % reprobación real |
|---|---|---|---|
| G0 – Riesgo por gestión del tiempo | 6.652 | 53,1% | 46,1% |
| G1 – Alto desempeño autónomo | 6.783 | 17,4% | 18,0% |
| G2 – Riesgo por calidad de apuntes | 6.190 | 50,2% | 45,0% |
| G3 – Riesgo por desmotivación | 6.076 | 60,2% | 52,0% |
| Total | 25.701 | 44,7% | 39,8% |

Insertada en 8.2.1 con su párrafo interpretativo; la antigua Tabla 70 (umbrales) pasó a ser **Tabla 71**
con sus referencias actualizadas.

## Figuras regeneradas (28 reemplazos dentro del docx)
- 12 histogramas del EDA (4.3, 4.5, 4.9, 4.11, 4.13, 4.15, 4.17, 4.19, 4.21, 4.23, 4.25, 4.27): la barra
  destacada ahora mide exactamente el n del valor apilado (F81/F86), ticks del eje Y enteros (F82),
  leyenda unificada "línea negra = mediana" (F85) y anotaciones corregidas (R1).
- 9 categóricas (4.31–4.39) re-estiladas con n y % sobre cada barra (F88).
- Q-Q 4.24 con pie corregido "aplanamiento en el tope 10" (F87).
- Matriz 4.42 sin colisión de etiquetas (F95).
- 6.1: árbol re-entrenado idéntico (1.653 hojas, raíz 4,591) re-exportado sin texto recortado (F103).
- 6.3 y 8.6 con decimales en coma (F100). 6.4 con texto blanco sobre celdas oscuras (F102).
- 6.6 con millares con punto y decimales con coma (F91).
- `entrega_modelamiento/figuras/` actualizada con las 5 figuras de scripts, y los scripts 02/03
  parchados para regenerarlas así (formato español, contraste condicional, árbol más ancho).

## Pendientes manuales (no automatizables con seguridad)
1. **Actualizar el índice en Word** (clic derecho → Actualizar campos): las inserciones desplazan la paginación.
   Aprovechar de insertar **Índice de Figuras e Índice de Tablas** (F9) y ampliar el TOC a nivel 4 (F7).
2. **F8**: reordenar niveles de título dentro de 4.3.3 (A)–D) vs. D.1–D.3) — cambio de estilos en Word.
3. **Figura 7.1**: mantiene punto decimal; no hay datos fuente para regenerarla (los valores del experimento
   no están en la entrega — véase F70). Si se desea, regenerar a mano desde el análisis auxiliar.
4. **F70**: no se agregó script de Hopkins: una reimplementación da H≈0,676 (≈0,68), no exactamente el
   0,67/rango 0,671–0,676 publicado (depende de detalles de implementación). El texto de A.2 ya lo acota
   como análisis auxiliar; si el equipo conserva el script original, conviene añadirlo a `scripts/`.
5. Portada: agregar nombre del docente y fecha exacta si se desea (F12 parcial: se corrigió el doble espacio).
