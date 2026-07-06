# Proyecto Data Mining — EduData Analytics

Proyecto completo de minería de datos sobre rendimiento estudiantil, siguiendo la metodología **CRISP-DM**. Sobre un dataset sintético de **300.000 estudiantes** (Kaggle) se desarrollan dos tareas:

- **Tarea predictiva** — predecir la reprobación de un estudiante a partir de sus **hábitos** (Árbol de Decisión C4.5 vs. Naive Bayes).
- **Tarea descriptiva** — segmentar a los estudiantes en **perfiles conductuales** (K-Means vs. K-Medoids/CLARA).

Incluye una **demo web interactiva** (un solo `.html` autocontenido, sin servidor) para probar el modelo en vivo.

---

## 🚀 Demo web (lo más rápido para ver el proyecto)

Abrí con doble clic:

```
entrega_modelamiento/demo_web/index.html
```

No necesita servidor ni internet. Trae sliders de hábitos en vivo, la probabilidad de reprobar `P(reprobar)`, umbral ajustable, el perfil de K-Means y casos de ejemplo. Al cargar corre un autotest que compara 4 casos contra el modelo original de Python.

> También está `Demo Sistema Alerta Temprana.html` en la raíz.

---

## 📊 Resultados principales

### Clasificación (conjunto de prueba, n = 25.701, distribución real 60/40)

| Modelo | Accuracy | Recall Fail | Kappa | AUC | Estado |
|---|---|---|---|---|---|
| **Naive Bayes (balanceado)** | **80,2 %** | **81,2 %** | 0,59 | 0,89 | ✅ **APROBADO** |
| Naive Bayes (sin balancear, ref.) | 80,5 % | 68,2 % | — | — | referencia |
| Árbol C4.5 (balanceado) | 73,3 % | 74,4 % | 0,46 | 0,81 | no alcanza 80 % |
| Baseline (clase mayoritaria) | 60,2 % | — | — | — | — |

El modelo aprobado cumple el criterio de éxito (accuracy ≥ 80 % y recall Fail ≥ 75 %). CV5 estable: 80,1 %–80,4 %.

### Clustering (vista conductual de 12 hábitos, k = 4)

**K-Means (aprobado)** — silueta 0,063 · Davies-Bouldin 2,77. Cuatro perfiles:

| Perfil | % Reprobación |
|---|---|
| Alto desempeño autónomo | 18,0 % |
| Riesgo por gestión del tiempo | 46,7 % |
| Riesgo por apuntes deficientes | 44,7 % |
| Riesgo por desmotivación | 51,7 % |

Validación *a posteriori*: `previous_grade` es casi idéntica entre grupos (69,8–69,9), es decir **los grupos NO se formaron por la nota**; aun así el % de reprobación va de 18 % a 52 %. Los hábitos por sí solos separan perfiles de éxito y de riesgo.

---

## 🧭 Decisiones metodológicas clave

1. **`previous_grade` NO es predictor de ningún modelo.** La nota del año anterior domina la correlación y sesga el análisis; como el objetivo es medir el impacto de los *hábitos*, la nota solo se usa para etiquetar y validar.
2. **El clustering usa SOLO hábitos** (12 variables conductuales, sin edad ni nota). La nota se agrega *después* de formar los grupos, para validar la coherencia de los perfiles.
3. **Split estratificado 70/15/15** con `student_id` único (sin filas duplicadas entre conjuntos).
4. **Balanceo de clases** (la base viene 60,2 % Pass / 39,8 % Fail): el modelo final es el balanceado 50/50, aplicado solo al entrenamiento; validación y prueba conservan la distribución real.

---

## 📁 Estructura

```
entrega_modelamiento/
├── scripts/          Pipeline reproducible (ETL → clasificación → clustering → despliegue)
│   ├── 01_etl_vistas_minables.py
│   ├── 02_clasificacion.py
│   ├── 03_clustering.py
│   ├── 04_despliegue.py
│   ├── 05_sistema_prediccion.py   Sistema de predicción para estudiantes nuevos
│   └── 06_generar_demo_web.py
├── demo_web/         Demo web interactiva (index.html autocontenido)
├── datos/            Vistas minables (CSV / ARFF para Weka)
├── modelos/          Modelos entrenados (.joblib)
├── resultados/       Métricas, grids de hiperparámetros, perfiles (JSON/CSV/TXT)
├── figuras/          Figuras del informe (PNG)
└── README.txt        Detalle técnico completo de la entrega

Informe Data Mining (4) ... .docx      Informe final completo
Mineria-de-datos-apuntes.md            Apuntes del curso
crisp-dm.pdf                           Referencia metodológica
```

---

## ▶️ Reproducir

Requisitos: **Python 3.10+** con `pandas`, `scikit-learn`, `scipy`, `matplotlib`, `joblib`.

El CSV crudo (`student_performance_prediction_dataset-2.csv`) debe estar en la raíz. Ejecutar en orden:

```bash
python entrega_modelamiento/scripts/01_etl_vistas_minables.py
python entrega_modelamiento/scripts/02_clasificacion.py
python entrega_modelamiento/scripts/03_clustering.py
python entrega_modelamiento/scripts/04_despliegue.py
```

Todos los procesos usan **semilla fija (42)**: los resultados son reproducibles.

> **Nota de carga:** en `device_type` y `extracurriculars` el valor `"None"` es una **categoría válida** (sin dispositivo / sin actividad), no un dato faltante. Los scripts leen el CSV con `keep_default_na=False, na_values=[""]`.

---

*Proyecto académico — Minería de Datos · EduData Analytics.*
