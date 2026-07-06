# Minería de Datos — Apuntes

> Apuntes organizados y complementados. Lo que está marcado con 💡 es información adicional para reforzar el concepto.

---

## Índice

1. [Conceptos fundamentales](#1-conceptos-fundamentales)
2. [El proceso de minería de datos](#2-el-proceso-de-minería-de-datos)
3. [Tareas de la minería de datos](#3-tareas-de-la-minería-de-datos)
4. [Tareas descriptivas (detalle)](#4-tareas-descriptivas-detalle)
5. [Evaluación del modelo e hiperparámetros](#5-evaluación-del-modelo-e-hiperparámetros)
6. [Flujo completo de un proyecto (ETL, EDA, vista minable)](#6-flujo-completo-de-un-proyecto)
7. [Resumen y glosario](#7-resumen-y-glosario)

---

## 1. Conceptos fundamentales

### Datamart vs. Minería de datos

| | **Datamart** | **Minería de datos** |
|---|---|---|
| **Objetivo** | Monitorear indicadores hasta como máximo el presente | Identificar patrones para generar conocimiento sobre los datos |
| **Enfoque** | Reportar lo que ya pasó / está pasando | Descubrir patrones ocultos y predecir |
| **No sirve para** | Encontrar patrones nuevos | (no aplica) |

> **Idea clave:** En minería de datos *usamos los datos del ayer y de hoy para tomar mejores decisiones mañana.*

💡 Un **datamart** es un subconjunto temático de un *data warehouse* orientado a un área concreta del negocio (ventas, finanzas, etc.). Es descriptivo; la minería de datos es predictiva y exploratoria.

### El sesgo (bias)

El sesgo se puede atacar en **tres momentos**:

1. **Pre-modelo:** seleccionando qué variables le doy al entrenamiento (calidad de los datos de entrada).
2. **Durante el aprendizaje:** asignando **peso** a las variables dentro de la función de aprendizaje.
3. **Post-modelo:** aplicando **técnicas correctivas** y ajustes al modelo final.

> Hay que entregar **datos balanceados** al modelo.

💡 Un dataset está *desbalanceado* cuando una clase domina sobre las otras (ej.: 95% "buen cliente" vs. 5% "mal cliente"). Esto hace que el modelo aprenda a ignorar la clase minoritaria. Técnicas para corregirlo: *oversampling* (ej. SMOTE), *undersampling* o pesos por clase.

---

## 2. El proceso de minería de datos

```
Fuente de datos
      ↓
   Filtro
      ↓
   Proceso
      ↓
 Transformación      (dar la forma que necesita el algoritmo)
      ↓
 Vista minable       (su construcción depende de lo que el algoritmo pueda encontrar)
      ↓
 Aplicación del algoritmo
      ↓
   Modelo
      ↓
 Conocimiento para el usuario
```

> La forma en que se construya la **vista minable** determina qué puede llegar a encontrar el algoritmo.

### ¿Cómo sé si el modelo está bien construido?

Mediante **métricas de calidad del modelo**: indican qué tanto se equivoca.

- Las métricas **dependen del tipo de técnica** que usemos → cada técnica tiene sus propias métricas.
- Se evalúan pasándole al modelo **datos cuya respuesta ya conocemos** y comparando.

💡 Ejemplos de métricas según la tarea:
- **Clasificación:** accuracy, precisión, recall, F1-score, matriz de confusión, AUC-ROC.
- **Forecasting / regresión:** MAE, MSE, RMSE, MAPE, R².
- **Clustering:** coeficiente de silueta, índice de Davies-Bouldin, inercia.

### Variables predictivas

Se obtienen mediante **ingeniería de características** (*feature engineering*): crear, transformar o seleccionar variables para mejorar el modelo.

---

## 3. Tareas de la minería de datos

Existen dos grandes grupos: **descriptivas** y **predictivas**.

### Tareas predictivas

Se dividen en dos grandes tipos:

#### a) Clasificación
Dado un conjunto de datos, predecir **a qué categoría** pertenece.
- Ejemplo: ¿será un *buen cliente* o un *mal cliente*?
- La salida es una **etiqueta / categoría** (variable cualitativa).

#### b) Forecasting (pronóstico)
Predecir un **número**.
- Ejemplo: cuántas personas con gripe habrá.
- La salida es un **valor numérico** (variable cuantitativa).

**Algoritmos para forecasting:**

- **Redes neuronales**
  - LSTM
  - Recurrentes (RNN)
  - Convolucionales (CNN)
- **Árbol de decisión**
- **Estadística**
  - Regresión lineal
  - ARIMA
  - SARIMA

> ⚠️ **El tipo de variable a usar (cualitativa o cuantitativa) depende del algoritmo** que vamos a utilizar.

💡 Diferencia clave:
- **Clasificación** → variable objetivo *categórica* (clases discretas).
- **Forecasting/Regresión** → variable objetivo *numérica continua*.
- **ARIMA/SARIMA** son específicos de **series de tiempo**; SARIMA añade el componente **estacional** (Seasonal).

### Tareas descriptivas

Describir **patrones** en los datos (sin una respuesta conocida de antemano). Ver detalle en la siguiente sección.

---

## 4. Tareas descriptivas (detalle)

> Cada **tarea** tiene sus **técnicas**, y cada **técnica** tiene su **algoritmo**.

📌 **Importante:** el problema del proyecto tiene que ser algo a lo que se le pueda **aplicar una solución** real.

### a) Asociación

Busca **reglas de asociación**: cuando ocurre A y B, ocurre Z.

- Se basa en **antecedentes** (A, B) para encontrar el **consecuente** (Z).
- Las reglas tienen métricas que dicen **cuánto se cumple** esa regla en el conjunto de datos.

💡 Métricas típicas de las reglas de asociación:
- **Soporte (support):** frecuencia con que aparece el conjunto en los datos.
- **Confianza (confidence):** probabilidad del consecuente dado el antecedente.
- **Lift:** cuánto más probable es el consecuente con el antecedente vs. sin él.
- Algoritmo clásico: **Apriori** y **FP-Growth**. Caso de uso típico: análisis de carrito de compra.

### b) Matriz de correlación

Sirve para ver **qué correlación tienen las variables** entre sí.

- Se usan **coeficientes de correlación** que se mueven entre **+1 y −1**:
  - **+1** → si una sube, la otra sube (correlación positiva).
  - **−1** → si una sube, la otra baja (correlación negativa).
  - **0** → no tienen correlación.
- Coeficientes:
  - **Pearson** → para variables con relación **lineal** y distribución **normal**.
  - **Spearman** → para relaciones monótonas / variables ordinales (no requiere normalidad).
- La matriz de correlación **necesita una cantidad de muestra válida** para que los resultados sean confiables.

> ⚠️ La **técnica requiere ciertos tipos de datos**: primero se escoge la técnica y luego las variables que sirven para aplicarla.
>
> Cada algoritmo **necesita unos supuestos** (ej. normalidad, linealidad, independencia).

> 📝 Nota del curso: *la regresión lineal no es buena para la práctica* (suele ser demasiado simple para problemas reales con relaciones no lineales).

### c) Agrupación / Clustering

Técnicas que **agrupan los datos según sus características**.

- En agrupación **NO se le dan datos previos etiquetados** para que clasifique → es **aprendizaje no supervisado**.
- **Técnica del codo (*elbow method*):** sirve para determinar **cuántos grupos (clusters)** son válidos para el análisis.

💡 Complemento:
- Algoritmo más común: **K-Means** (requiere definir *k* = número de grupos).
- Otros: **DBSCAN** (basado en densidad), **clustering jerárquico**.
- El **método del codo** grafica la inercia vs. número de clusters; el "codo" de la curva indica el *k* óptimo. Alternativa: **coeficiente de silueta**.

> 💡 Diferencia clave **clasificación vs. clustering**:
> - **Clasificación** = supervisado (hay etiquetas conocidas).
> - **Clustering** = no supervisado (el algoritmo descubre los grupos solo).

---

## 5. Evaluación del modelo e hiperparámetros

### Descriptivo vs. Predictivo (entregable)

| Tipo de tarea | Entregable |
|---|---|
| **Descriptivo** | Un **informe** |
| **Predictivo** | Un **sistema** |

- En **clustering**, el **EDA se hace a cada grupo** por separado.
- **Cada tarea debe tener (al menos) dos algoritmos** para poder hacer un análisis **comparativo**.

### Guía CRISP-DM

La **guía CRISP-DM** sirve para basarse en cómo se hace el informe / estructurar el proyecto.

💡 **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*) tiene 6 fases:
1. Comprensión del negocio
2. Comprensión de los datos
3. Preparación de los datos
4. Modelado
5. Evaluación
6. Despliegue

### Métricas de evaluación

- Se escogen **en base a los modelos**, aunque se usen diferentes algoritmos.
- La **técnica de evaluación corresponde al algoritmo** que se escoge.

### Hiperparámetros

- Son **argumentos que se configuran al algoritmo**.
- **Controlan el comportamiento del algoritmo** y permiten **mejorar los resultados**.
- Hay **técnicas para saber qué hiperparámetros** son necesarios para mi algoritmo.
- Ejemplo: la **profundidad del árbol** en un árbol de decisión.

> **Flujo de mejora:** primero **evalúo** el modelo → según los resultados, **ajusto los hiperparámetros** para mejorarlo.
>
> La evaluación/iteración se hace **hasta cumplir el criterio de éxito** definido.

💡 Técnicas para encontrar buenos hiperparámetros:
- **Grid Search** (búsqueda en malla).
- **Random Search** (búsqueda aleatoria).
- **Optimización bayesiana**.
- 📌 Diferencia: los **parámetros** los aprende el modelo solo durante el entrenamiento; los **hiperparámetros** los define el analista *antes* de entrenar.

> 📝 Recordatorio: verificar **si la variable sigue una distribución** (normal u otra), porque muchos algoritmos lo asumen como supuesto.

---

## 6. Flujo completo de un proyecto

```
Datos crudos
     ↓
   EDA          (exploración inicial)
     ↓
   ETL          → aquí se limpian y balancean los datos
     ↓
   EDA 2        (re-explorar para ver cómo quedaron tras el balanceo)
     ↓
 Vista minable
     ↓
 Aplicación del algoritmo   ← aquí se ingresan los hiperparámetros
     ↓
   Modelo
```

### EDA (Análisis Exploratorio de Datos)

💡 **EDA** = *Exploratory Data Analysis*. Sirve para entender los datos antes de modelar: distribuciones, valores faltantes, outliers, correlaciones.

- Se aplica un **segundo EDA (EDA 2)** después del ETL para ver cómo quedaron los datos tras la limpieza y el balanceo.
- En el **EDA 2** se revisan las **condiciones de los datos** para que puedan aplicarse al algoritmo.

### ETL (Extract, Transform, Load)

- El ETL **se tiene que hacer igual** (de forma consistente) para que **no haya sesgo** en los datos.
- Los **problemas de desbalanceo** requieren **técnicas de balanceo**, y lo favorable es **hacerlo en el ETL**.
- Dentro del ETL se puede **forzar a que las variables sigan una distribución** determinada, para poder aplicar el algoritmo que requiere ese supuesto.

💡 **ETL** = *Extract* (extraer de las fuentes), *Transform* (limpiar, normalizar, balancear, transformar), *Load* (cargar al destino / vista minable).

### Vista minable

- Es la tabla final, ya transformada, lista para el algoritmo.
- **Puede haber más de una vista minable**, para **comparar** qué conjunto de datos hace que el algoritmo aprenda mejor.
- Todas las vistas minables probadas **deben registrarse en el informe**.

### Split (división del dataset)

La vista minable se divide en subconjuntos — el proceso se llama **Split**:

- **Dataset de entrenamiento** (*training*) → el modelo aprende.
- **Dataset de validación** (*validation*) → ajustar hiperparámetros.
- **Dataset de test** (*test*) → evaluación final con datos nunca vistos.

> - También se puede dividir solo en **entrenamiento y test** (esto aplica **solo en tareas predictivas**).
> - ⚠️ Cada subgrupo **debe estar igualmente balanceado**.

💡 Proporciones típicas: 70/15/15 o 80/10/10. Técnica avanzada: **validación cruzada (*k-fold cross-validation*)** para aprovechar mejor los datos.

---

## 7. Resumen y glosario

### Mapa mental de tareas

```
MINERÍA DE DATOS
│
├── DESCRIPTIVAS (no supervisado) → entregable: INFORME
│   ├── Asociación (reglas: soporte, confianza, lift)
│   ├── Matriz de correlación (Pearson / Spearman)
│   └── Agrupación / Clustering (K-Means, método del codo)
│
└── PREDICTIVAS (supervisado) → entregable: SISTEMA
    ├── Clasificación (categoría: buen/mal cliente)
    └── Forecasting (número: regresión, ARIMA, SARIMA, redes neuronales)
```

### Glosario rápido

| Término | Significado |
|---|---|
| **Datamart** | Subconjunto temático de datos para monitorear indicadores (descriptivo) |
| **EDA** | Análisis exploratorio de datos |
| **ETL** | Extract, Transform, Load: extraer, transformar (limpiar/balancear) y cargar |
| **Vista minable** | Tabla final preparada para alimentar el algoritmo |
| **Split** | División en entrenamiento / validación / test |
| **Hiperparámetro** | Argumento configurable que controla el comportamiento del algoritmo |
| **Sesgo (bias)** | Error sistemático; se ataca antes, durante o después del modelo |
| **Balanceo** | Equilibrar la cantidad de ejemplos por clase |
| **CRISP-DM** | Metodología estándar de 6 fases para proyectos de minería de datos |
| **Feature engineering** | Ingeniería de características: crear/transformar variables predictivas |

### Ideas clave para no olvidar

- ✅ Usar datos del ayer y hoy para decidir mejor mañana.
- ✅ Entregar **datos balanceados** y hacer el balanceo en el **ETL**.
- ✅ Primero se elige la **técnica**, luego las **variables** (cada técnica exige tipos de datos y supuestos).
- ✅ Cada tarea con **al menos 2 algoritmos** para comparar.
- ✅ Aplicar **EDA antes y después** del ETL (EDA 2).
- ✅ Evaluar → ajustar **hiperparámetros** → repetir hasta el **criterio de éxito**.
- ✅ Mantener **todos los subconjuntos del Split balanceados**.
```
