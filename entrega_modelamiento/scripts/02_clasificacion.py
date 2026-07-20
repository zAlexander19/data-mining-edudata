# -*- coding: utf-8 -*-
"""
Etapa VI/VII - Modelamiento y Evaluación: TAREA PREDICTIVA (Clasificación de pass_fail)

Algoritmos comparados (equivalentes en Python/scikit-learn a los declarados en Weka):
  1. Árbol de Decisión con criterio de entropía / ganancia de información
     (DecisionTreeClassifier, equivalente conceptual de J48/C4.5).
  2. Naïve Bayes mixto: Gaussiano para atributos numéricos + Categórico para nominales
     (equivalente al NaiveBayes de Weka, que modela numéricas con gaussianas y
     nominales con tablas de frecuencia).

Decisiones metodológicas incorporadas tras la revisión con el profesor:
  a) previous_grade NO es predictor. La nota del año anterior domina la correlación con
     el objetivo y sesga el modelo; como el objetivo del estudio es medir el impacto de
     los HÁBITOS, la nota solo se usa para etiquetar (pass_fail proviene de final_grade)
     y queda fuera de la ecuación predictiva. El modelo debe poder clasificar a un
     estudiante por sus hábitos sin conocer su nota.
  b) Balanceo de clases (la base viene ~60% Pass / ~40% Fail). Se comparan cuatro
     estrategias, aplicadas SIEMPRE solo al conjunto de entrenamiento (validación y
     prueba conservan la distribución real):
       - original:      sin balanceo (referencia, base sesgada 60/40).
       - ponderacion:   class_weight='balanced' (costos, sin re-muestrear; solo árbol).
       - sobremuestreo: muestreo CON reemplazo de la clase minoritaria hasta 50/50.
       - submuestreo:   eliminación aleatoria de la clase mayoritaria hasta 50/50.
     No se generan datos sintéticos (recomendación explícita del profesor: no "inventar"
     datos; usar muestreo con reemplazo o submuestreo).
     El MODELO FINAL se elige entre las estrategias de re-muestreo (50/50); la versión
     "original" se reporta solo como referencia para discutir el sesgo de clase.
  c) La validación cruzada re-muestrea DENTRO de cada fold (solo la parte de
     entrenamiento del fold): si se balanceara antes de partir, las copias de la clase
     minoritaria caerían a la vez en train y test del fold y las métricas saldrían
     optimistas (fuga de información).

Diseño de test: split estratificado 70/15/15 (entrenamiento / validación / prueba),
validado por el profesor para bases de datos grandes. Cada fila es una persona única
(el ETL verifica que no haya student_id duplicados). Los hiperparámetros y la estrategia
de balanceo se eligen con el conjunto de VALIDACIÓN; el conjunto de PRUEBA solo se usa
al final. Semilla fija (42) para reproducibilidad.

Criterios de éxito (sección 3.2 del informe):
  - accuracy >= 80% en el conjunto de prueba
  - recall de la clase "Fail" (Reprueba) >= 75%
"""
import json
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.special import logsumexp
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report, cohen_kappa_score,
                             confusion_matrix, roc_auc_score)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.naive_bayes import CategoricalNB, GaussianNB
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

BASE = Path(__file__).resolve().parents[1]
DATOS, MODELOS, FIGURAS, RESULTADOS = (BASE / d for d in ("datos", "modelos", "figuras", "resultados"))
SEED = 42

# previous_grade EXCLUIDA de los predictores (ver decisión metodológica (a) del docstring).
NUMERICAS = [
    "age", "study_hours", "attendance", "sleep_hours",
    "assignments_completed", "practice_tests_taken", "group_study_hours",
    "notes_quality_score", "time_management_score", "motivation_level",
    "mental_health_score", "screen_time", "social_media_hours",
]
ORDINALES = {
    "family_income": ["Low", "Medium", "High"],
    "parent_education": ["High School", "Bachelor", "Master", "PhD"],
}
BINARIAS = {"internet_access": ["No", "Yes"], "school_type": ["Public", "Private"]}
NOMINALES = ["gender", "device_type", "extracurriculars"]
CATEGORICAS = list(ORDINALES) + list(BINARIAS) + NOMINALES

ESTRATEGIAS_REMUESTREO = ("sobremuestreo", "submuestreo")


# ----------------------------------------------------------------------------- Naïve Bayes mixto
class NaiveBayesMixto:
    """Combina GaussianNB (numéricas) y CategoricalNB (categóricas) compartiendo el prior.

    log P(c|x) ∝ log P(c) + Σ log N(x_num; μ_c, σ_c) + Σ log P(x_cat|c)
    """

    def __init__(self, var_smoothing=1e-9, alpha=1.0):
        self.var_smoothing = var_smoothing
        self.alpha = alpha

    def fit(self, X_num, X_cat, y):
        self.gnb = GaussianNB(var_smoothing=self.var_smoothing).fit(X_num, y)
        self.cnb = CategoricalNB(alpha=self.alpha).fit(X_cat, y)
        self.classes_ = self.gnb.classes_
        return self

    def _joint(self, X_num, X_cat):
        log_prior = np.log(self.gnb.class_prior_)
        jll_g = self.gnb.predict_log_proba(X_num)   # posterior normalizado (incluye prior)
        jll_c = self.cnb.predict_log_proba(X_cat)
        return jll_g + jll_c - log_prior            # el prior queda contado una sola vez

    def predict_proba(self, X_num, X_cat):
        jll = self._joint(X_num, X_cat)
        return np.exp(jll - logsumexp(jll, axis=1, keepdims=True))

    def predict(self, X_num, X_cat):
        return self.classes_[np.argmax(self._joint(X_num, X_cat), axis=1)]


# ----------------------------------------------------------------------------- preparación
def cargar():
    df = pd.read_csv(DATOS / "vista_minable_clasificacion.csv",
                     keep_default_na=False, na_values=[""])
    y = df["pass_fail"]
    X = df.drop(columns=["pass_fail"])

    # Codificación para el árbol: One-Hot en nominales (splits binarios interpretables),
    # códigos ordinales en las variables con orden natural.
    X_arbol = X.copy()
    for col, cats in {**ORDINALES, **BINARIAS}.items():
        X_arbol[col] = X_arbol[col].map({c: i for i, c in enumerate(cats)})
    X_arbol = pd.get_dummies(X_arbol, columns=NOMINALES, dtype=int)

    # Codificación para Naïve Bayes: numéricas tal cual + códigos de categoría.
    X_num = X[NUMERICAS].to_numpy()
    X_cat = np.column_stack([X[c].astype("category").cat.codes.to_numpy() for c in CATEGORICAS])

    return X, y, X_arbol, X_num, X_cat


def dividir(y):
    """Split estratificado 70/15/15; devuelve índices para reutilizarlos en ambas codificaciones."""
    idx = np.arange(len(y))
    idx_train, idx_tmp = train_test_split(idx, test_size=0.30, stratify=y, random_state=SEED)
    idx_valid, idx_test = train_test_split(idx_tmp, test_size=0.50, stratify=y.iloc[idx_tmp],
                                           random_state=SEED)
    return idx_train, idx_valid, idx_test


def remuestrear(idx, y, estrategia, rng):
    """Re-muestrea SOLO los índices dados (entrenamiento); nunca toca validación/prueba.

    - sobremuestreo: repite casos reales de la clase minoritaria (muestreo con reemplazo)
      hasta igualar 50/50. No se inventan datos: solo se repiten filas existentes.
    - submuestreo: descarta al azar casos de la clase mayoritaria (sin reemplazo) hasta 50/50.
    Cualquier otra estrategia devuelve los índices sin cambios.
    """
    if estrategia not in ESTRATEGIAS_REMUESTREO:
        return idx
    etiquetas = y.iloc[idx].to_numpy()
    clases, conteos = np.unique(etiquetas, return_counts=True)
    if conteos.min() == conteos.max():
        return idx
    minoritaria = clases[conteos.argmin()]
    idx_min, idx_may = idx[etiquetas == minoritaria], idx[etiquetas != minoritaria]
    if estrategia == "sobremuestreo":
        extra = rng.choice(idx_min, size=len(idx_may) - len(idx_min), replace=True)
        out = np.concatenate([idx_may, idx_min, extra])
    else:  # submuestreo
        out = np.concatenate([rng.choice(idx_may, size=len(idx_min), replace=False), idx_min])
    rng.shuffle(out)
    return out


def metricas(y_true, y_pred, y_score=None):
    rep = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    out = {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision_Fail": round(rep["Fail"]["precision"], 4),
        "recall_Fail": round(rep["Fail"]["recall"], 4),
        "f1_Fail": round(rep["Fail"]["f1-score"], 4),
        "precision_Pass": round(rep["Pass"]["precision"], 4),
        "recall_Pass": round(rep["Pass"]["recall"], 4),
        "f1_Pass": round(rep["Pass"]["f1-score"], 4),
        "kappa": round(cohen_kappa_score(y_true, y_pred), 4),
        "matriz_confusion": confusion_matrix(y_true, y_pred, labels=["Fail", "Pass"]).tolist(),
    }
    if y_score is not None:
        out["auc_roc"] = round(roc_auc_score((y_true == "Pass").astype(int), y_score), 4)
    return out


def elegir(grid_df, estrategias, claves_orden):
    """Regla de selección sobre VALIDACIÓN dentro de las estrategias indicadas:
    cumplir recall(Fail)>=0.75 y maximizar accuracy; desempates por claves_orden
    (mayor recall de Fail / menos hojas) y, si el empate persiste, el orden de la
    malla (sort estable => se queda la configuración más simple, determinista)."""
    pool = grid_df[grid_df.estrategia.isin(estrategias)]
    ok = pool[pool.recall_fail_valid >= 0.75]
    pool = ok if len(ok) else pool
    ascending = [k == "hojas" for k in claves_orden]
    return pool.sort_values(claves_orden, ascending=ascending, kind="stable").iloc[0]


def cv5_con_remuestreo(fit_predict, y, idx_pool, estrategia):
    """Validación cruzada 5-fold sobre idx_pool re-muestreando DENTRO de cada fold.

    El re-muestreo se aplica únicamente a la parte de entrenamiento del fold; el fold de
    evaluación queda intacto. Así las filas repetidas por el sobremuestreo jamás aparecen
    a la vez en entrenamiento y evaluación (sin fuga de información).
    """
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    accs = []
    for f, (tr, te) in enumerate(cv.split(idx_pool, y.iloc[idx_pool])):
        idx_tr = remuestrear(idx_pool[tr], y, estrategia, np.random.default_rng(SEED + f))
        idx_te = idx_pool[te]
        accs.append(round(accuracy_score(y.iloc[idx_te], fit_predict(idx_tr, idx_te)), 4))
    return accs


# ----------------------------------------------------------------------------- main
def main():
    for d in (MODELOS, FIGURAS, RESULTADOS):
        d.mkdir(exist_ok=True)

    X, y, X_arbol, X_num, X_cat = cargar()
    idx_train, idx_valid, idx_test = dividir(y)
    y_tr, y_va, y_te = (y.iloc[i] for i in (idx_train, idx_valid, idx_test))
    print("Split:", {k: len(v) for k, v in
                     zip(("train", "valid", "test"), (idx_train, idx_valid, idx_test))})
    print("Proporción Fail por subconjunto:",
          [round((s == 'Fail').mean(), 4) for s in (y_tr, y_va, y_te)])

    resultados = {"split": {
        "train": len(idx_train), "valid": len(idx_valid), "test": len(idx_test),
        "pct_fail": {n: round(float((s == 'Fail').mean()), 4)
                     for n, s in zip(("train", "valid", "test"), (y_tr, y_va, y_te))},
    }}
    resultados["balanceo"] = {
        "distribucion_train_original": {c: int(n) for c, n in y_tr.value_counts().items()},
        "distribucion_train_por_estrategia": {},
        "nota": "El balanceo se aplica SOLO al entrenamiento; validación y prueba "
                "conservan la distribución real (~60/40).",
    }
    for est in ESTRATEGIAS_REMUESTREO:
        idx_b = remuestrear(idx_train, y, est, np.random.default_rng(SEED))
        resultados["balanceo"]["distribucion_train_por_estrategia"][est] = \
            {c: int(n) for c, n in y.iloc[idx_b].value_counts().items()}
    print("Balanceo del train:", json.dumps(resultados["balanceo"], indent=2, ensure_ascii=False))

    Xa_va, Xa_te = X_arbol.iloc[idx_valid], X_arbol.iloc[idx_test]

    # ---------------- 1) Árbol: malla hiperparámetros x estrategia de balanceo ----------------
    grid = []
    for estrategia in ("original", "ponderacion") + ESTRATEGIAS_REMUESTREO:
        idx_bal = remuestrear(idx_train, y, estrategia, np.random.default_rng(SEED))
        Xb, yb = X_arbol.iloc[idx_bal], y.iloc[idx_bal]
        cw = "balanced" if estrategia == "ponderacion" else None
        for max_depth in (4, 6, 8, 10, 12, 16, None):
            for min_leaf in (1, 50, 200, 500):
                m = DecisionTreeClassifier(criterion="entropy", max_depth=max_depth,
                                           min_samples_leaf=min_leaf, class_weight=cw,
                                           random_state=SEED).fit(Xb, yb)
                pred = m.predict(Xa_va)
                rep = classification_report(y_va, pred, output_dict=True, zero_division=0)
                grid.append({"estrategia": estrategia, "max_depth": max_depth,
                             "min_samples_leaf": min_leaf,
                             "accuracy_valid": round(accuracy_score(y_va, pred), 4),
                             "recall_fail_valid": round(rep["Fail"]["recall"], 4),
                             "hojas": int(m.get_n_leaves())})
        print(f"  árbol / {estrategia}: {len(grid)} configuraciones acumuladas")
    grid_df = pd.DataFrame(grid)
    grid_df.to_csv(RESULTADOS / "grid_search_arbol.csv", index=False)

    # Modelo final: mejor configuración ENTRE LAS ESTRATEGIAS DE RE-MUESTREO (50/50).
    best = elegir(grid_df, ESTRATEGIAS_REMUESTREO,
                  ["accuracy_valid", "recall_fail_valid", "hojas"])
    # Referencia: mejor configuración sin balancear (base sesgada 60/40), para el informe.
    best_ref = elegir(grid_df, ["original"], ["accuracy_valid", "recall_fail_valid", "hojas"])
    print("\nMejor árbol balanceado (validación):\n", best.to_dict())
    print("Mejor árbol sin balancear - referencia (validación):\n", best_ref.to_dict())

    idx_trva = np.concatenate([idx_train, idx_valid])

    def ajustar_arbol(fila, idx_entrena):
        md = None if pd.isna(fila.max_depth) else int(fila.max_depth)
        cw = "balanced" if fila.estrategia == "ponderacion" else None
        m = DecisionTreeClassifier(criterion="entropy", max_depth=md,
                                   min_samples_leaf=int(fila.min_samples_leaf),
                                   class_weight=cw, random_state=SEED)
        return m.fit(X_arbol.iloc[idx_entrena], y.iloc[idx_entrena])

    def resumen_arbol(fila):
        # Modelo final: reentrenado con train+validación re-muestreados con la misma estrategia
        # (práctica estándar tras fijar hiperparámetros; el test sigue intacto).
        idx_bal = remuestrear(idx_trva, y, fila.estrategia, np.random.default_rng(SEED))
        m = ajustar_arbol(fila, idx_bal)
        proba = m.predict_proba(Xa_te)[:, list(m.classes_).index("Pass")]
        md = None if pd.isna(fila.max_depth) else int(fila.max_depth)
        return m, {
            "estrategia_balanceo": fila.estrategia,
            "hiperparametros": {"criterion": "entropy", "max_depth": md,
                                "min_samples_leaf": int(fila.min_samples_leaf),
                                "class_weight": "balanced" if fila.estrategia == "ponderacion" else None},
            "hojas": int(m.get_n_leaves()), "profundidad": int(m.get_depth()),
            "validacion": {"accuracy": float(fila.accuracy_valid),
                           "recall_Fail": float(fila.recall_fail_valid)},
            "test": metricas(y_te, m.predict(Xa_te), proba),
        }

    arbol, res_arbol = resumen_arbol(best)
    _, res_arbol_ref = resumen_arbol(best_ref)
    # Robustez: CV 5-fold sobre train+valid, re-muestreando dentro de cada fold (sin fuga).
    res_arbol["cv5_accuracy_remuestreo_por_fold"] = cv5_con_remuestreo(
        lambda i_tr, i_te: ajustar_arbol(best, i_tr).predict(X_arbol.iloc[i_te]),
        y, idx_trva, best.estrategia)
    resultados["arbol"] = {"final_balanceado": res_arbol,
                           "referencia_sin_balancear": res_arbol_ref}

    # ---------------- 2) Naïve Bayes mixto: malla x estrategia de balanceo ----------------
    Xn_va, Xn_te = X_num[idx_valid], X_num[idx_test]
    Xc_va, Xc_te = X_cat[idx_valid], X_cat[idx_test]
    grid_nb = []
    for estrategia in ("original",) + ESTRATEGIAS_REMUESTREO:
        idx_bal = remuestrear(idx_train, y, estrategia, np.random.default_rng(SEED))
        Xn_b, Xc_b, y_b = X_num[idx_bal], X_cat[idx_bal], y.iloc[idx_bal]
        for vs in (1e-9, 1e-7, 1e-5):
            for alpha in (0.1, 1.0, 10.0):
                nb = NaiveBayesMixto(var_smoothing=vs, alpha=alpha).fit(Xn_b, Xc_b, y_b)
                pred = nb.predict(Xn_va, Xc_va)
                rep = classification_report(y_va, pred, output_dict=True, zero_division=0)
                grid_nb.append({"estrategia": estrategia, "var_smoothing": vs, "alpha": alpha,
                                "accuracy_valid": round(accuracy_score(y_va, pred), 4),
                                "recall_fail_valid": round(rep["Fail"]["recall"], 4)})
        print(f"  naive bayes / {estrategia}: {len(grid_nb)} configuraciones acumuladas")
    grid_nb_df = pd.DataFrame(grid_nb)
    grid_nb_df.to_csv(RESULTADOS / "grid_search_naive_bayes.csv", index=False)

    best_nb = elegir(grid_nb_df, ESTRATEGIAS_REMUESTREO, ["accuracy_valid", "recall_fail_valid"])
    best_nb_ref = elegir(grid_nb_df, ["original"], ["accuracy_valid", "recall_fail_valid"])
    print("\nMejor NB balanceado (validación):\n", best_nb.to_dict())
    print("Mejor NB sin balancear - referencia (validación):\n", best_nb_ref.to_dict())

    def resumen_nb(fila):
        idx_bal = remuestrear(idx_trva, y, fila.estrategia, np.random.default_rng(SEED))
        m = NaiveBayesMixto(var_smoothing=float(fila.var_smoothing),
                            alpha=float(fila.alpha)).fit(X_num[idx_bal], X_cat[idx_bal],
                                                         y.iloc[idx_bal])
        proba = m.predict_proba(Xn_te, Xc_te)[:, list(m.classes_).index("Pass")]
        return m, {
            "estrategia_balanceo": fila.estrategia,
            "hiperparametros": {"var_smoothing": float(fila.var_smoothing),
                                "alpha": float(fila.alpha)},
            "validacion": {"accuracy": float(fila.accuracy_valid),
                           "recall_Fail": float(fila.recall_fail_valid)},
            "test": metricas(y_te, m.predict(Xn_te, Xc_te), proba),
        }

    nb, res_nb = resumen_nb(best_nb)
    _, res_nb_ref = resumen_nb(best_nb_ref)

    def fp_nb(i_tr, i_te):
        m = NaiveBayesMixto(var_smoothing=float(best_nb.var_smoothing),
                            alpha=float(best_nb.alpha)).fit(X_num[i_tr], X_cat[i_tr], y.iloc[i_tr])
        return m.predict(X_num[i_te], X_cat[i_te])

    res_nb["cv5_accuracy_remuestreo_por_fold"] = cv5_con_remuestreo(
        fp_nb, y, idx_trva, best_nb.estrategia)
    resultados["naive_bayes"] = {"final_balanceado": res_nb,
                                 "referencia_sin_balancear": res_nb_ref}

    # Baseline de referencia: clase mayoritaria
    resultados["baseline_clase_mayoritaria"] = round(float((y_te == "Pass").mean()), 4)

    # ---------------- persistencia de modelos y descripciones ----------------
    joblib.dump({"modelo": arbol, "columnas": list(X_arbol.columns),
                 "estrategia_balanceo": best.estrategia},
                MODELOS / "arbol_decision_c45.joblib")
    joblib.dump({"gnb": nb.gnb, "cnb": nb.cnb, "numericas": NUMERICAS,
                 "categoricas": CATEGORICAS,
                 "estrategia_balanceo": best_nb.estrategia,
                 "categorias": {c: list(X[c].astype("category").cat.categories) for c in CATEGORICAS}},
                MODELOS / "naive_bayes_mixto.joblib")

    # Reglas del árbol (patrones) y descripción del modelo NB (medias por clase)
    (RESULTADOS / "arbol_reglas.txt").write_text(
        export_text(arbol, feature_names=list(X_arbol.columns), max_depth=4), encoding="utf-8")
    pd.DataFrame({"variable": list(X_arbol.columns),
                  "importancia": arbol.feature_importances_.round(4)}) \
        .sort_values("importancia", ascending=False) \
        .to_csv(RESULTADOS / "arbol_importancia_variables.csv", index=False)
    pd.DataFrame(nb.gnb.theta_, index=nb.classes_, columns=NUMERICAS).round(3) \
        .to_csv(RESULTADOS / "naive_bayes_medias_por_clase.csv")

    with open(RESULTADOS / "metricas_clasificacion.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print("\n", json.dumps(resultados, indent=2, ensure_ascii=False))

    # ---------------- figuras ----------------
    plt.rcParams.update({"figure.dpi": 150, "font.size": 9})

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    for ax, (nombre, res, pred) in zip(axes, [
            (f"Árbol de Decisión ({best.estrategia})", res_arbol, arbol.predict(Xa_te)),
            (f"Naïve Bayes mixto ({best_nb.estrategia})", res_nb, nb.predict(Xn_te, Xc_te))]):
        cm = confusion_matrix(y_te, pred, labels=["Fail", "Pass"])
        ConfusionMatrixDisplay(cm, display_labels=["Fail (Reprueba)", "Pass (Aprueba)"]) \
            .plot(ax=ax, colorbar=False, values_format=",d", cmap="Blues")
        for t in ax.texts:  # separador de miles con punto (convención del informe)
            t.set_text(t.get_text().replace(",", "."))
        ax.set_title((f"{nombre}\naccuracy={res['test']['accuracy']:.3f} · "
                      f"recall Fail={res['test']['recall_Fail']:.3f}").replace(".", ","))
    fig.suptitle("Matrices de confusión — conjunto de prueba (n=%s), modelos balanceados"
                 % f"{len(y_te):,}".replace(",", "."))
    fig.tight_layout()
    fig.savefig(FIGURAS / "clasificacion_matrices_confusion.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(21, 8))
    plot_tree(arbol, feature_names=list(X_arbol.columns), class_names=arbol.classes_,
              filled=True, max_depth=3, fontsize=8, impurity=False, proportion=True, ax=ax)
    ax.set_title(f"Árbol de decisión (entropía, balanceo por {best.estrategia}) — primeros 3 niveles")
    fig.savefig(FIGURAS / "clasificacion_arbol_decision.png", bbox_inches="tight")
    plt.close(fig)

    imp = pd.DataFrame({"variable": list(X_arbol.columns),
                        "importancia": arbol.feature_importances_}) \
        .sort_values("importancia").tail(12)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(imp.variable, imp.importancia, color="#2c7fb8")
    ax.set_xlabel("Importancia (reducción de entropía normalizada)")
    ax.set_title("Árbol de decisión — importancia de variables (sin previous_grade)")
    fig.tight_layout()
    fig.savefig(FIGURAS / "clasificacion_importancia_variables.png", bbox_inches="tight")
    plt.close(fig)

    print("\nListo: modelos, métricas y figuras generados.")


if __name__ == "__main__":
    main()
