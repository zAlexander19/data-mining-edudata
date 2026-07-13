# Guía para replicar las vistas minables en KNIME

Proyecto **EduData Analytics** — Etapa V (Preparación de Datos / ETL)
Equivalente KNIME del script `scripts/01_etl_vistas_minables.py`

---

## 0. Qué vamos a construir

El ETL parte de **un solo CSV crudo** (300.000 filas × 25 columnas) y produce **cuatro salidas**. Este es el contrato que el workflow de KNIME debe cumplir exactamente:

| Salida | Archivo | Filas | Columnas | Para qué sirve |
|---|---|---|---|---|
| Base limpia | `base_limpia_para_perfilamiento.csv` | 171.334 | 25 | Perfilar los clusters en la escala original del negocio (horas, notas, %) |
| Vista de clasificación | `vista_minable_clasificacion.csv` (+ `.arff`) | 171.334 | 21 | Entrenar árbol C4.5 y Naïve Bayes (objetivo `pass_fail`) |
| Vista de clustering (completa) | `vista_minable_clustering.csv` | 171.334 | 31 | Vista A/B del barrido de k (todo codificado y normalizado) |
| Vista de clustering conductual | `vista_minable_clustering_conductual.csv` | 171.334 | 12 | **La vista que realmente se modeló**: solo hábitos |

Dos decisiones metodológicas que el workflow **debe** respetar (son feedback del profesor, no detalles técnicos):

1. **`previous_grade` no es predictor.** La nota del año anterior domina cualquier modelo y tapa el efecto de los hábitos. Se usa solo para construir la etiqueta (`pass_fail` viene de `final_grade`) y para validar a posteriori. Por eso se elimina de la vista de clasificación.
2. **El clustering es solo de hábitos.** La vista conductual excluye `age` y `previous_grade`, y también todas las categóricas socioeconómicas. Son 12 variables de comportamiento y nada más.

---

## 1. Requisitos previos

- **KNIME Analytics Platform 5.x** (las instrucciones también funcionan en 4.7+; donde cambia el nodo lo aclaro).
- El CSV crudo `student_performance_prediction_dataset-2.csv` accesible desde el equipo.
- Nodos usados — todos vienen en la instalación base, no hace falta instalar extensiones:
  `CSV Reader`, `Row Filter` (o `Rule-based Row Filter`), `Column Filter`, `Normalizer`, `Rule Engine`, `String Manipulation`, `Domain Calculator`, `One to Many`, `Column Resorter`, `CSV Writer`, `ARFF Writer`, `PMML Writer`, `Extract Table Dimension`, `GroupBy`, `Statistics`.

> **Consejo de organización:** creá un workflow llamado `01_ETL_vistas_minables` y agrupá los bloques con *Annotations* (clic derecho en el lienzo → *New Workflow Annotation*) con los títulos "A. Extracción", "B. Selección y limpieza", etc. Además de ordenar, te deja tomar un pantallazo del workflow directamente presentable para el informe.

---

## 2. Mapa del workflow

```
                                 ┌─ [Column Filter: quita id, final_grade,
                                 │   grade_category, previous_grade]
                                 │        └─> CSV Writer  → vista_minable_clasificacion.csv
                                 │        └─> ARFF Writer → vista_minable_clasificacion.arff
                                 │
[CSV Reader]                     │
     │  300.000 × 25             │
     ▼                           │
[Row Filter: age 15–18]          │
     │  171.336                  │
     ▼                           │
[Row Filter: final_grade > 0] ───┼─> CSV Writer → base_limpia_para_perfilamiento.csv
     │  171.334 × 25             │
     │                           │
     └───────────────────────────┴─ [Normalizer Min-Max 0–1 (14 numéricas)]
                                          │        └─> PMML Writer → rangos_normalizacion.pmml
                                          ▼
                                    [Rule Engine ×2: ordinales]
                                          ▼
                                    [Rule Engine ×2: binarias]
                                          ▼
                                    [String Manipulation ×3: prefijo de valores]
                                          ▼
                                    [Domain Calculator] → [One to Many]  (One-Hot)
                                          ▼
                                    [Column Filter + Column Resorter]
                                          │  171.334 × 31
                                          ├─> CSV Writer → vista_minable_clustering.csv
                                          ▼
                                    [Column Filter: solo las 12 conductuales]
                                          │  171.334 × 12
                                          └─> CSV Writer → vista_minable_clustering_conductual.csv
```

---

## 3. Bloque A — Extracción (`CSV Reader`)

Arrastrá un **CSV Reader** y apuntalo al archivo crudo.

**Configuración obligatoria:**

| Opción | Valor | Por qué |
|---|---|---|
| Column delimiter | `,` | |
| Has column header | ✅ | La primera fila trae los nombres |
| Decimal separator | `.` | El CSV está en formato anglosajón; si KNIME usa `,` te leerá los decimales como texto |
| Thousands separator | *(vacío)* | |
| Encoding (Advanced) | UTF-8 | |

### ⚠️ La trampa más importante de todo el ETL: el valor `"None"`

En las columnas `device_type` y `extracurriculars`, el texto **`None` es una categoría real** ("no tiene dispositivo" / "no hace actividades extracurriculares"), **no un dato faltante**. Si KNIME lo interpreta como *missing*, perdés ~1/4 y ~1/6 de esas columnas y todos los conteos posteriores dejan de cuadrar.

En el script Python esto se resuelve con `keep_default_na=False, na_values=[""]`. En KNIME:

1. Abrí el CSV Reader → pestaña **Advanced Settings**.
2. Buscá el campo de **patrón de valores faltantes** (*"Missing value pattern"* / *"Replace this string with missing value"*). **Debe estar vacío o no contener `None`.** No escribas `None`, `NA`, `null` ni nada parecido.
3. Dejá activada la opción de **convertir strings vacíos en missing** (*"Replace empty strings with missing values"*). Los únicos faltantes reales del dataset son 4 celdas vacías de `grade_category`, y esas sí deben quedar como missing.

**Verificación inmediata:** ejecutá el nodo y abrí la vista de la tabla. En la columna `device_type` tenés que ver la palabra `None` escrita como texto (celda normal), **no** la celda gris con un `?` que KNIME usa para faltantes.

**Punto de control A:** conectá un **Extract Table Dimension** → debe decir **300.000 filas × 25 columnas**.

---

## 4. Bloque B — Selección de registros y limpieza

Se aplican dos filtros. **Hacelos en dos nodos separados**, aunque podrían ir en uno: así podés ver el conteo intermedio y usarlo como evidencia en el informe (la sección V documenta la caída de registros paso a paso).

### B.1 — Filtro de edad: población escolar (`Row Filter`)

El dataset trae edades de 15 a 25 años. El proyecto estudia a la **población escolar**, así que se conservan solo los de **15 a 18 años inclusive**.

- Nodo: **Row Filter**
- Columna: `age`
- Condición: rango numérico, **lower bound = 15**, **upper bound = 18**, ambos inclusive.

> En KNIME 4.x el `Row Filter` clásico permite un solo criterio: elegí *"Use range checking"* y completá ambos límites. Si preferís una sola expresión, usá **Rule-based Row Filter** con:
> `$age$ >= 15 AND $age$ <= 18 => TRUE` (modo *Include TRUE matches*).

**Punto de control B.1:** **171.336 filas**. Si te da otro número, el problema casi siempre es que `age` se leyó como texto (`String`) en vez de número: revisá el tipo en el CSV Reader.

### B.2 — Limpieza de registros erróneos (`Row Filter`)

Quedan **2 registros corruptos**: tienen `final_grade = 0` y la columna `grade_category` vacía. Son los únicos faltantes reales del dataset y se eliminan por completo (no se imputan: son un error de generación del dato, no una ausencia informativa).

- Nodo: **Row Filter**
- Columna: `final_grade`
- Condición: **> 0** (excluir los que valgan 0).

**Punto de control B.2 (el más importante del workflow):**

| Métrica | Valor esperado |
|---|---|
| Filas | **171.334** |
| Columnas | 25 |
| Valores faltantes | **0** (verificalo con un nodo `Missing Value Column Filter` o mirando la vista `Statistics`) |
| `student_id` duplicados | 0 |
| Distribución de `pass_fail` | **Pass 103.108 (60,18 %)** / **Fail 68.226 (39,82 %)** |

Para la distribución, colgá un **GroupBy** (agrupar por `pass_fail`, agregación `Count` sobre `student_id`) o un **Value Counter**. Ese 60/40 es el desbalance que después se corrige **solo en el train** (ver Anexo 1).

### B.3 — Salida: base limpia

Desde la salida de B.2, un **CSV Writer** → `datos/base_limpia_para_perfilamiento.csv`.
Sin transformar nada: es el dataset limpio en **escala original** y sirve para perfilar los clusters en unidades que el negocio entiende (horas de sueño, % de asistencia, puntaje 1–10).

Configuración del CSV Writer (usá la misma en todos los del workflow):

- **Write column header:** ✅
- **Write row ID:** ❌ (si lo dejás activado, KNIME agrega una columna `Row0, Row1...` que Python no tiene)
- **Encoding:** UTF-8
- **Missing value pattern:** vacío

---

## 5. Bloque C — Vista minable de clasificación (21 columnas)

Esta vista mantiene las **escalas originales** y las categóricas como **texto nominal**: ni normalización ni One-Hot. Los algoritmos que la consumen (árbol de decisión y Naïve Bayes) no lo necesitan, y así el árbol produce reglas legibles (`if time_management_score <= 5.2 ...` en vez de valores entre 0 y 1).

### C.1 — `Column Filter`

Desde B.2, un **Column Filter** en modo **Exclude** con estas 4 columnas:

| Columna eliminada | Motivo |
|---|---|
| `student_id` | Identificador: no aporta información, y si el árbol lo usa memoriza en vez de aprender |
| `final_grade` | **Fuga de información**: es la nota de la que se deriva la etiqueta (`Pass ⟺ final_grade > 50`). Dejarla sería predecir la etiqueta con la etiqueta |
| `grade_category` | Misma fuga: es la nota categorizada en letras |
| `previous_grade` | **Decisión del profesor**: domina la predicción y sesga el análisis de hábitos (ver §0) |

Quedan **21 columnas**: 13 numéricas + 7 categóricas + la etiqueta `pass_fail`.

**Punto de control C:** **171.334 × 21**.

### C.2 — Salidas

- **CSV Writer** → `datos/vista_minable_clasificacion.csv`
- **ARFF Writer** → `datos/vista_minable_clasificacion.arff` (formato Weka)

> **Antes del ARFF Writer, insertá un `Domain Calculator`** (con todas las columnas nominales seleccionadas y "Restrict number of possible values" desactivado o en un tope alto). El ARFF declara los valores posibles de cada atributo nominal en el encabezado (`@attribute gender {Female,Male,Other}`), y los toma del **dominio** que KNIME tiene registrado. Si el dominio venía recortado de un nodo anterior, el ARFF sale incompleto y Weka rechaza el archivo al leerlo.

---

## 6. Bloque D — Vista minable de clustering (31 columnas)

Acá sí hay transformación pesada. El clustering usa **distancias euclidianas**, así que toda variable debe estar en una escala comparable: si dejáramos `attendance` (40–100) junto a `motivation_level` (1–10), la asistencia pesaría ~7 veces más solo por su unidad de medida.

El orden de los nodos importa: **normalizar primero** (mientras las numéricas siguen siendo numéricas y están todas presentes), después codificar las categóricas.

### D.1 — `Normalizer`: Min-Max a [0, 1] sobre 14 numéricas

- Nodo: **Normalizer**
- Método: **Min-Max Normalization**, **Min = 0.0**, **Max = 1.0**
- Columnas incluidas (**las 14**, incluyendo `age` y `previous_grade` — se excluyen recién en la vista conductual):

```
age, study_hours, attendance, sleep_hours, previous_grade,
assignments_completed, practice_tests_taken, group_study_hours,
notes_quality_score, time_management_score, motivation_level,
mental_health_score, screen_time, social_media_hours
```

KNIME calcula el mínimo y el máximo **a partir de la tabla que entra**. Como venimos de la tabla ya filtrada (171.334 filas), los rangos deben coincidir exactamente con los que produjo Python. Verificalos con un nodo **Statistics** contra esta tabla:

| Variable | min | max |  | Variable | min | max |
|---|---|---|---|---|---|---|
| `age` | 15 | 18 | | `practice_tests_taken` | 0 | 10 |
| `study_hours` | 0 | 12 | | `group_study_hours` | 0 | 5,8406 |
| `attendance` | 40 | 100 | | `notes_quality_score` | 1 | 10 |
| `sleep_hours` | 3 | 10 | | `time_management_score` | 1 | 10 |
| `previous_grade` | 20 | 100 | | `motivation_level` | 1 | 10 |
| `assignments_completed` | 0 | 10 | | `mental_health_score` | 1 | 10 |
| | | | | `screen_time` | 0 | 12 |
| | | | | `social_media_hours` | 0 | 8 |

> **Si un rango no coincide, el filtro del bloque B está mal.** Es el síntoma clásico de haber olvidado el filtro de edad (con todas las edades, `age` iría de 15 a 25 y `age` normalizada sería otra cosa).

**El puerto azul cuadrado del Normalizer es oro para el despliegue.** Contiene el modelo de normalización (los min/max aprendidos), que es exactamente lo que en Python se guardó como `resultados/rangos_normalizacion.json`. Conectale un **PMML Writer** → `resultados/rangos_normalizacion.pmml`. Cuando llegue un estudiante nuevo, se normaliza con **Normalizer (Apply)** usando ese mismo modelo; si recalcularas los min/max sobre los datos nuevos, el modelo entrenado dejaría de ser válido.

### D.2 — Ordinales: `Rule Engine` (×2)

Estas dos variables **tienen orden natural**, así que se codifican con enteros que lo preservan (no con One-Hot, que destruiría el orden).

> ⚠️ **No uses el nodo `Category To Number`** para esto: asigna los códigos según el orden en que aparecen los valores en los datos (o alfabético), no según el orden semántico. Terminarías con `High = 0` y `Low = 2`, es decir, el orden invertido, y el clustering leería "ingreso alto" como el extremo bajo del eje.

**Rule Engine #1** — Replace column: `family_income`

```
$family_income$ = "Low"    => 0
$family_income$ = "Medium" => 1
$family_income$ = "High"   => 2
```

**Rule Engine #2** — Replace column: `parent_education`

```
$parent_education$ = "High School" => 0
$parent_education$ = "Bachelor"    => 1
$parent_education$ = "Master"      => 2
$parent_education$ = "PhD"         => 3
```

En ambos nodos elegí **"Replace Column"** y seleccioná la columna original (no "Append Column", o te quedarás con la de texto además de la codificada).

### D.3 — Binarias: `Rule Engine` (×2)

Dos categorías → un solo 0/1. One-Hot acá sería redundante (dos columnas perfectamente colineales).

**Rule Engine #3** — Replace column: `internet_access`

```
$internet_access$ = "No"  => 0
$internet_access$ = "Yes" => 1
```

**Rule Engine #4** — Replace column: `school_type`

```
$school_type$ = "Public"  => 0
$school_type$ = "Private" => 1
```

### D.4 — Nominales: One-Hot en dos pasos

`gender`, `device_type` y `extracurriculars` **no tienen orden** (¿es `Tablet` mayor que `Laptop`?), así que van a One-Hot: una columna binaria por cada valor posible.

#### ⚠️ Segunda trampa: la colisión de nombres `None`

El nodo **One to Many** de KNIME nombra las columnas nuevas **con el valor de la categoría**, sin prefijo. Y acá hay un problema: **`device_type` tiene el valor `None` y `extracurriculars` también**. Las dos generarían una columna llamada `None` → colisión (KNIME aborta o renombra con un sufijo raro tipo `None (#1)`).

Python no sufre esto porque `pd.get_dummies(prefix=...)` antepone el nombre de la columna. La forma limpia de reproducirlo en KNIME es **meter el prefijo dentro del valor antes de hacer el One-Hot**. Así, de paso, los nombres de columna te quedan idénticos a los del CSV de Python.

**Paso 1 — `String Manipulation` (×3, o un `String Manipulation (Multi Column)`):**

| Nodo | Expresión | Modo |
|---|---|---|
| #1 | `join("gender_", $gender$)` | Replace column `gender` |
| #2 | `join("device_type_", $device_type$)` | Replace column `device_type` |
| #3 | `join("extracurriculars_", $extracurriculars$)` | Replace column `extracurriculars` |

Ahora los valores son `gender_Male`, `device_type_None`, `extracurriculars_None`… — ya no colisionan.

**Paso 2 — `Domain Calculator`:** seleccioná las 3 columnas modificadas. Necesario porque `One to Many` crea una columna por cada valor **del dominio registrado**, y acabás de cambiar todos los valores.

**Paso 3 — `One to Many`:** incluí las 3 columnas y activá **"Remove included columns from output"** (si no, te quedan las de texto además de las dummies).

Se generan **13 columnas** (0/1):

```
gender_Female, gender_Male, gender_Other                                    (3)
device_type_Laptop, device_type_Mobile, device_type_None, device_type_Tablet   (4)
extracurriculars_Arts, extracurriculars_Coding Club, extracurriculars_Debate,
extracurriculars_Music, extracurriculars_None, extracurriculars_Sports        (6)
```

> Si las dummies salen como `Double` (`1.0` / `0.0`) y querés que el CSV sea idéntico al de Python (`1` / `0`), agregá un **Double To Int** sobre esas 13 columnas. Es cosmético: no cambia ningún resultado de clustering.

### D.5 — Selección y orden final: `Column Filter` + `Column Resorter`

**Column Filter** — quedate solo con estas **31 columnas** (quedan fuera `student_id`, `final_grade`, `grade_category` y `pass_fail`: **la vista de clustering no lleva variable objetivo**, es aprendizaje no supervisado).

**Column Resorter** — poné este orden exacto si querés que el CSV sea comparable columna a columna con el de Python:

1. Las **14 numéricas normalizadas**, en el orden de la lista de D.1.
2. Las **2 ordinales**: `family_income`, `parent_education`.
3. Las **2 binarias**: `internet_access`, `school_type`.
4. Las **13 dummies**, en el orden de D.4.

**Punto de control D:** **171.334 × 31**. Pasale un **Statistics**: las 14 normalizadas deben ir de **0 a 1** exactas, y las 31 columnas no deben tener ningún faltante (un faltante ahí significa que un valor de categoría se te escapó de alguna regla del Rule Engine).

### D.6 — Salida

**CSV Writer** → `datos/vista_minable_clustering.csv`

---

## 7. Bloque E — Vista minable conductual (12 columnas) ← **la que se modela**

Esta es la vista con la que efectivamente se corrió K-Means y K-Medoids. Nace de la decisión metodológica del profesor: **el clustering debe segmentar por hábitos de estudio, no por perfil demográfico ni por rendimiento previo**. Si dejáramos `previous_grade`, los grupos se ordenarían por nota y no descubriríamos nada sobre conducta; si dejáramos las socioeconómicas, estaríamos segmentando por contexto familiar en vez de por comportamiento.

- Nodo: **Column Filter** sobre la salida de D.5 (la vista de 31 columnas, **ya normalizada**).
- Modo **Include**, exactamente estas **12**:

```
study_hours, attendance, sleep_hours, assignments_completed,
practice_tests_taken, group_study_hours, notes_quality_score,
time_management_score, motivation_level, mental_health_score,
screen_time, social_media_hours
```

Es decir: se quitan `age`, `previous_grade`, las 2 ordinales, las 2 binarias y las 13 dummies.

**Punto de control E:** **171.334 × 12**, todas las columnas entre 0 y 1.

**CSV Writer** → `datos/vista_minable_clustering_conductual.csv`

> Detalle importante para el informe: se filtra **después** de normalizar, no antes. Da lo mismo numéricamente (Min-Max es columna por columna, no depende de las otras columnas), pero así una sola rama del workflow alimenta las dos vistas de clustering y no hay riesgo de que se desincronicen.

---

## 8. Checklist de verificación final

Antes de dar el ETL por bueno, corré esta lista. Cada línea corresponde a un `assert` del script Python:

- [ ] CSV crudo leído: **300.000 × 25**
- [ ] En `device_type` y `extracurriculars`, `None` aparece como **texto**, no como celda faltante
- [ ] Tras filtro de edad: **171.336** filas
- [ ] Tras limpieza de `final_grade = 0`: **171.334** filas
- [ ] **Cero** valores faltantes en la tabla limpia
- [ ] **Cero** `student_id` duplicados
- [ ] `pass_fail`: **Pass 103.108 (60,18 %)** / **Fail 68.226 (39,82 %)**
- [ ] Vista clasificación: **171.334 × 21**, sin `previous_grade`, sin `final_grade`, sin `grade_category`, sin `student_id`
- [ ] Rangos Min-Max coinciden con la tabla de §D.1 (sobre todo `age` = 15–18)
- [ ] Vista clustering: **171.334 × 31**, todas las numéricas en [0, 1], sin `pass_fail`
- [ ] Vista conductual: **171.334 × 12**
- [ ] ARFF abre en Weka sin error de atributo nominal

### Comparación automática contra los CSV de Python (opcional pero contundente)

Si querés demostrar que la réplica es exacta:

1. Agregá un segundo **CSV Reader** apuntando al `vista_minable_clasificacion.csv` que generó Python.
2. Conectá ambas tablas a un nodo **Table Difference Finder** (KNIME 5.x; en 4.x usá `Joiner` por índice + `Math Formula` con la diferencia absoluta + `Rule-based Row Filter` con tolerancia `> 1e-9`).
3. Resultado esperado: **cero diferencias**.

Sobre los decimales: Python y KNIME escriben `double` con la misma precisión IEEE-754, pero pueden diferir en la **representación textual** (`0.3718437962059558` vs `0.37184379620595580`, o notación científica en valores muy chicos). Si comparás los archivos con un diff de texto vas a ver ruido; compará **valores numéricos con tolerancia**, no strings.

---

## Anexo 1 — Partición y balanceo (el paso siguiente, ya en modelamiento)

No forma parte de las vistas minables, pero es donde más gente se equivoca al pasar el pipeline a KNIME, así que lo dejo documentado.

### Partición 70 / 15 / 15 estratificada

Se hace con **dos nodos Partitioning** encadenados sobre la **vista de clasificación**:

| Nodo | Configuración | Salida |
|---|---|---|
| Partitioning #1 | Relative 70 %, **Stratified sampling** sobre `pass_fail`, *Use random seed* = 42 | arriba: **train (70 %)** · abajo: resto (30 %) |
| Partitioning #2 (sobre el 30 %) | Relative 50 %, **Stratified sampling** sobre `pass_fail`, semilla fija | arriba: **validación (15 %)** · abajo: **prueba (15 %)** |

Estratificar no es opcional: garantiza que el 60/40 de `pass_fail` se mantenga en los tres subconjuntos, y por lo tanto que las métricas de prueba sean comparables.

### Balanceo: **solo sobre el train**, nunca sobre validación ni prueba

Esta es la regla que más se viola. Si balanceás **antes** de partir, las copias de la clase minoritaria (sobremuestreo) terminan repartidas entre train y test: el modelo evalúa sobre filas que ya vio y el accuracy sale inflado y mentiroso. **Primero se parte, después se balancea la rama de train.**

| Estrategia | Nodo KNIME | Cómo |
|---|---|---|
| **Submuestreo** (la del modelo final) | **Equal Size Sampling** | Columna nominal: `pass_fail`. Método: *exact* / *approximate*. Descarta al azar casos de la clase mayoritaria (`Pass`) hasta igualar 50/50 |
| **Sobremuestreo** | `Row Splitter` por clase → **Bootstrap Sampling** sobre la minoritaria (tamaño = nº de casos de la mayoritaria) → `Concatenate` | Repite filas reales existentes con reemplazo |
| **Ponderación** (solo árbol) | Opción de *class weights* del Decision Tree / o un `Math Formula` que asigne peso | Sin re-muestrear |

> 🚫 **No uses el nodo SMOTE.** Genera registros sintéticos interpolando vecinos, y el criterio del proyecto es explícito: el balanceo se hace **repitiendo o descartando casos reales**, sin inventar datos. Usar SMOTE cambiaría la metodología documentada en el informe.

### Sobre la reproducibilidad exacta

La semilla 42 en KNIME **no genera las mismas filas** que `random_state=42` en scikit-learn: son generadores de números aleatorios distintos. Las particiones serán equivalentes en tamaño y proporción, pero no idénticas fila a fila, y por eso las métricas te van a dar parecidas pero no exactamente iguales (diferencias de décimas). Eso es esperable y correcto; lo que **sí** debe reproducirse exactamente son las **vistas minables** (§8), porque el ETL es determinista y no tiene ningún componente aleatorio.

---

## Anexo 2 — Trampas conocidas, ordenadas por frecuencia con que muerden

| # | Síntoma | Causa | Solución |
|---|---|---|---|
| 1 | Aparecen faltantes en `device_type` / `extracurriculars`; los conteos no cuadran | KNIME leyó la **categoría** `None` como valor faltante | CSV Reader → Advanced: quitar `None` del patrón de missing (§3) |
| 2 | `One to Many` falla o crea `None (#1)` | Colisión: `device_type` y `extracurriculars` comparten el valor `None` | Prefijar los valores con `String Manipulation` antes del One-Hot (§D.4) |
| 3 | El clustering da grupos con sentido invertido en ingreso/educación | `Category To Number` codificó los ordinales en orden alfabético o de aparición | Usar `Rule Engine` con el mapeo explícito (§D.2) |
| 4 | Los rangos Min-Max no coinciden (p. ej. `age` 15–25) | Se normalizó **antes** de filtrar por edad | El `Normalizer` va después del bloque B |
| 5 | El accuracy sale sospechosamente alto (>95 %) | Quedó `final_grade`, `grade_category` o `previous_grade` en la vista de clasificación | Revisar el `Column Filter` de §C.1 |
| 6 | El CSV tiene una columna extra `Row0, Row1...` | El `CSV Writer` tiene *Write row ID* activado | Desactivarlo |
| 7 | Los decimales se leen como texto | `Decimal separator` configurado como `,` | Ponerlo en `.` |
| 8 | Weka rechaza el `.arff` | El dominio nominal estaba incompleto | `Domain Calculator` antes del `ARFF Writer` (§C.2) |

---

## Anexo 3 — Tabla de equivalencias Python ↔ KNIME

| Paso del ETL | Python (`01_etl_vistas_minables.py`) | KNIME |
|---|---|---|
| Leer CSV sin convertir `None` en NaN | `pd.read_csv(..., keep_default_na=False, na_values=[""])` | `CSV Reader` + patrón de missing vacío |
| Filtrar edad | `df[df.age.between(15, 18)]` | `Row Filter` (rango 15–18) |
| Limpiar registros erróneos | `df[df.final_grade > 0]` | `Row Filter` (> 0) |
| Quitar columnas | `df.drop(columns=[...])` | `Column Filter` (Exclude) |
| Normalizar Min-Max | `(x - min) / (max - min)` | `Normalizer` (Min-Max 0–1) |
| Guardar rangos para despliegue | `rangos_normalizacion.json` | Puerto de modelo del `Normalizer` + `PMML Writer` |
| Aplicar rangos a datos nuevos | leer el JSON y aplicar la fórmula | `Normalizer (Apply)` |
| Codificar ordinales | `df[col].map({"Low": 0, ...})` | `Rule Engine` (Replace column) |
| Codificar binarias | `df[col].map({"No": 0, "Yes": 1})` | `Rule Engine` (Replace column) |
| One-Hot | `pd.get_dummies(df[col], prefix=col)` | `String Manipulation` (prefijo) + `Domain Calculator` + `One to Many` |
| Exportar CSV | `df.to_csv(ruta, index=False)` | `CSV Writer` (sin Row ID) |
| Exportar ARFF | función `exportar_arff()` | `ARFF Writer` |
| Partición estratificada | `train_test_split(..., stratify=y)` | `Partitioning` (Stratified) ×2 |
| Submuestreo a 50/50 | `rng.choice(idx_may, size=len(idx_min), replace=False)` | `Equal Size Sampling` |
| Sobremuestreo a 50/50 | `rng.choice(idx_min, ..., replace=True)` | `Bootstrap Sampling` + `Concatenate` |
