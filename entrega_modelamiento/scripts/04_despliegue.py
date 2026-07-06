# -*- coding: utf-8 -*-
"""
Etapa VIII - Despliegue

Conforme a la pauta del informe, los modelos PREDICTIVOS se aplican mediante lenguaje de
programación sobre datos de ejemplo, y los modelos DESCRIPTIVOS se interpretan.

Este script:
  1. Carga el Naïve Bayes mixto APROBADO (entrenado balanceado, sin previous_grade) y lo
     aplica sobre el conjunto de PRUEBA (25.701 casos jamás vistos en el entrenamiento):
     cada estudiante recibe una probabilidad de reprobar P(Fail).
  2. Extrae casos de ejemplo representativos (percentiles del riesgo) con sus hábitos,
     su alerta (umbral nominal 0,5), su grupo conductual K-Means y la acción sugerida.
  3. Análisis de umbral (acción 4 de la sección 7.3): número de alertas, recall y
     precisión de Fail para distintos umbrales -> la institución elige según sus cupos.
  4. Despliegue descriptivo: tabla operativa de segmentos (perfil, tamaño, % reprobación,
     programa de intervención, prioridad).

Nota sobre P(Fail): el modelo se entrenó con clases balanceadas (50/50), por lo que la
probabilidad está calibrada respecto de ese prior; el umbral 0,5 es el punto de decisión
nominal y el análisis de umbral cubre su ajuste operativo.
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
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parents[1]
DATOS, MODELOS, FIGURAS, RESULTADOS = (BASE / d for d in ("datos", "modelos", "figuras", "resultados"))
SEED = 42

PERFILES = {
    0: ("Riesgo por gestión del tiempo deficiente", "Taller de planificación y organización"),
    1: ("Alto desempeño autónomo", "Mantención / mentor par"),
    2: ("Riesgo por calidad de apuntes deficiente", "Técnicas de estudio y toma de apuntes"),
    3: ("Riesgo por desmotivación", "Programa motivacional y consejería"),
}


def main():
    # ---------------- datos y split (idéntico a 02_clasificacion.py) ----------------
    df = pd.read_csv(DATOS / "vista_minable_clasificacion.csv",
                     keep_default_na=False, na_values=[""])
    y = df["pass_fail"]
    X = df.drop(columns=["pass_fail"])
    idx = np.arange(len(y))
    idx_train, idx_tmp = train_test_split(idx, test_size=0.30, stratify=y, random_state=SEED)
    _, idx_test = train_test_split(idx_tmp, test_size=0.50, stratify=y.iloc[idx_tmp],
                                   random_state=SEED)

    base = pd.read_csv(DATOS / "base_limpia_para_perfilamiento.csv",
                       keep_default_na=False, na_values=[""])
    asig = pd.read_csv(RESULTADOS / "clustering_asignaciones.csv") \
        .set_index("student_id")["cluster_kmeans"]

    # ---------------- modelo aprobado: Naïve Bayes mixto ----------------
    nb = joblib.load(MODELOS / "naive_bayes_mixto.joblib")
    gnb, cnb = nb["gnb"], nb["cnb"]
    X_num = X[nb["numericas"]].to_numpy()
    X_cat = np.column_stack([
        pd.Categorical(X[c], categories=nb["categorias"][c]).codes for c in nb["categoricas"]])

    log_prior = np.log(gnb.class_prior_)
    jll = gnb.predict_log_proba(X_num) + cnb.predict_log_proba(X_cat) - log_prior
    proba = np.exp(jll - logsumexp(jll, axis=1, keepdims=True))
    p_fail = proba[:, list(gnb.classes_).index("Fail")]

    te = pd.DataFrame({
        "student_id": base["student_id"].to_numpy()[idx_test],
        "p_fail": p_fail[idx_test],
        "real": y.to_numpy()[idx_test],
    })
    te["cluster"] = te["student_id"].map(asig)

    # ---------------- 1) casos de ejemplo (percentiles del riesgo) ----------------
    te_orden = te.sort_values("p_fail").reset_index(drop=True)
    filas = []
    for q in (0.02, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 0.98):
        r = te_orden.iloc[int(q * (len(te_orden) - 1))]
        est = base.loc[base.student_id == r.student_id].iloc[0]
        perfil, accion = PERFILES[int(r.cluster)]
        filas.append({
            "student_id": int(r.student_id),
            "habitos": (f"estudio {est.study_hours:.1f} h/d; asistencia {est.attendance:.0f}%; "
                        f"gestión tiempo {est.time_management_score:.1f}; "
                        f"motivación {est.motivation_level:.1f}"),
            "p_reprobar": round(float(r.p_fail) * 100, 1),
            "alerta_05": "SÍ" if r.p_fail >= 0.5 else "no",
            "perfil_conductual": perfil,
            "accion_sugerida": accion if r.p_fail >= 0.5 else "seguimiento regular",
            "resultado_real": "Reprobó" if r.real == "Fail" else "Aprobó",
        })
    casos = pd.DataFrame(filas)
    casos.to_csv(RESULTADOS / "despliegue_casos_ejemplo.csv", index=False)

    # ---------------- 2) análisis de umbral (acción 4 de 7.3) ----------------
    n_fail = int((te.real == "Fail").sum())
    umbrales = []
    for u in (0.30, 0.40, 0.50, 0.60, 0.70):
        al = te[te.p_fail >= u]
        tp = int((al.real == "Fail").sum())
        umbrales.append({
            "umbral": u,
            "alertas": len(al),
            "pct_alumnado": round(len(al) / len(te) * 100, 1),
            "recall_fail": round(tp / n_fail * 100, 1),
            "precision_fail": round(tp / len(al) * 100, 1) if len(al) else None,
        })
    umb = pd.DataFrame(umbrales)
    umb.to_csv(RESULTADOS / "despliegue_umbral_alertas.csv", index=False)

    # ---------------- 3) despliegue descriptivo: tabla de segmentos ----------------
    perf = pd.read_csv(RESULTADOS / "clustering_perfiles_kmeans.csv")
    seg = pd.DataFrame({
        "grupo": [f"G{i} – {PERFILES[i][0]}" for i in perf.cluster],
        "n": perf.n,
        "pct_alumnado": (perf.n / perf.n.sum() * 100).round(1),
        "pct_reprobacion": perf.pct_fail,
        "programa": [PERFILES[i][1] for i in perf.cluster],
    })
    seg.to_csv(RESULTADOS / "despliegue_segmentos.csv", index=False)

    # ---------------- figura: alertas vs umbral ----------------
    plt.rcParams.update({"figure.dpi": 150, "font.size": 9})
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    axes[0].plot(umb.umbral, umb.pct_alumnado, marker="o", color="#2c7fb8")
    axes[0].set_xlabel("Umbral de alerta sobre P(reprobar)")
    axes[0].set_ylabel("% del alumnado alertado")
    axes[0].set_title("Volumen de alertas según umbral")
    axes[1].plot(umb.umbral, umb.recall_fail, marker="o", label="Recall Fail", color="#d95f0e")
    axes[1].plot(umb.umbral, umb.precision_fail, marker="s", label="Precisión Fail", color="#2c7fb8")
    axes[1].set_xlabel("Umbral de alerta sobre P(reprobar)")
    axes[1].set_ylabel("%")
    axes[1].set_title("Calidad de las alertas según umbral")
    axes[1].legend()
    for ax in axes:
        ax.axvline(0.5, color="grey", ls="--", lw=1)
    fig.tight_layout()
    fig.savefig(FIGURAS / "despliegue_umbral.png", bbox_inches="tight")
    plt.close(fig)

    print(json.dumps({"casos_ejemplo": filas, "umbral": umbrales,
                      "aciertos_casos": int((casos.alerta_05 == "SÍ")
                                            .eq(casos.resultado_real == "Reprobó").sum())},
                     indent=2, ensure_ascii=False))
    print("\nListo: despliegue generado (CSVs + figura).")


if __name__ == "__main__":
    main()
