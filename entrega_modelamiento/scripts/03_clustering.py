# -*- coding: utf-8 -*-
"""
Etapa VI/VII - Modelamiento y Evaluación: TAREA DESCRIPTIVA (Agrupamiento de estudiantes)

Algoritmos comparados:
  1. K-Means (scikit-learn, init k-means++, n_init=10).
  2. K-Medoids mediante el esquema CLARA (Kaufman & Rousseeuw): se ejecuta PAM
     (intercambio alternado) sobre varias muestras aleatorias, se elige el conjunto de
     medoides con menor costo sobre una muestra de evaluación grande y se asignan
     TODOS los registros al medoide más cercano. Esto hace viable K-Medoids sobre
     171.334 registros (PAM puro es O(n^2) e intratable a esta escala).

Vistas minables evaluadas (los apuntes del curso piden registrar todas las vistas probadas):
  A) vista completa: 31 atributos (14 numéricas normalizadas + categóricas codificadas).
  B) vista numérica: las 14 numéricas normalizadas (incluye age y previous_grade).
  C) vista conductual: 12 numéricas normalizadas, SOLO HÁBITOS (se excluyen age y
     previous_grade). Decisión metodológica del feedback del profesor: si la nota entra
     al clustering, los grupos se parten por rendimiento académico y no por
     comportamiento; la segmentación debe basarse únicamente en hábitos y la nota se
     agrega DESPUÉS, para validar la coherencia de los perfiles encontrados.

Resultado del análisis comparativo (documentado en la sección VI del informe):
  - La vista A produce grupos definidos solo por las combinaciones one-hot (género,
    dispositivo, actividad), con perfiles numéricos idénticos y % de reprobación plano:
    sin valor de negocio.
  - En la vista B el atributo age domina la partición (variable discreta uniforme con
    la mayor varianza tras el Min-Max) pese a tener correlación 0,00 con la nota, y
    previous_grade mete el rendimiento previo en la definición de los grupos
    (exactamente lo que el profesor pidió evitar): descartada.
  - La vista C produce segmentos definidos por los hábitos de estudio, interpretables
    y con % de reprobación diferenciado. ES LA VISTA SELECCIONADA.

Número de grupos: método del codo (inercia) + coeficiente de silueta para k = 2..10.
Cuando la silueta resulta casi plana y el codo no es concluyente, k se decide por
interpretabilidad y utilidad de negocio (k=4: un grupo de alto desempeño y grupos de
riesgo diferenciados por su hábito débil).
Semilla fija (42). Ni pass_fail, ni final_grade, ni previous_grade entran al modelo:
las notas se usan SOLO a posteriori para caracterizar los grupos y validar su coherencia
("¿el grupo con mejores hábitos es efectivamente el de mejores notas?") mediante el %
de reprobación y los terciles de rendimiento (Bajo/Medio/Alto) por grupo.
"""
import json
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (adjusted_rand_score, davies_bouldin_score,
                             pairwise_distances, silhouette_score)

BASE = Path(__file__).resolve().parents[1]
DATOS, MODELOS, FIGURAS, RESULTADOS = (BASE / d for d in ("datos", "modelos", "figuras", "resultados"))
SEED = 42
RNG = np.random.default_rng(SEED)

NUMERICAS = [
    "age", "study_hours", "attendance", "sleep_hours", "previous_grade",
    "assignments_completed", "practice_tests_taken", "group_study_hours",
    "notes_quality_score", "time_management_score", "motivation_level",
    "mental_health_score", "screen_time", "social_media_hours",
]
# Vista C: SOLO hábitos. Se excluyen age (r=0,00 con la nota; fragmenta los grupos) y
# previous_grade (la nota no debe definir los grupos, se agrega a posteriori — feedback profesor).
CONDUCTUALES = [c for c in NUMERICAS if c not in ("age", "previous_grade")]


# --------------------------------------------------------------------- K-Medoids (CLARA)
def pam_muestra(X, k, rng, max_iter=25):
    """PAM 'alternado' sobre una muestra: asignación + actualización de medoides."""
    n = len(X)
    D = pairwise_distances(X, X)          # matriz de distancias de la muestra
    # inicialización tipo k-means++ sobre distancias
    medoids = [int(rng.integers(n))]
    for _ in range(k - 1):
        d2 = D[:, medoids].min(axis=1) ** 2
        p = d2 / d2.sum()
        medoids.append(int(rng.choice(n, p=p)))
    medoids = np.array(medoids)

    for _ in range(max_iter):
        labels = D[:, medoids].argmin(axis=1)
        nuevos = medoids.copy()
        for c in range(k):
            idx = np.where(labels == c)[0]
            if len(idx) == 0:
                continue
            # medoide = punto de la muestra que minimiza la suma de distancias intra-cluster
            nuevos[c] = idx[D[np.ix_(idx, idx)].sum(axis=1).argmin()]
        if np.array_equal(nuevos, medoids):
            break
        medoids = nuevos
    costo = D[:, medoids].min(axis=1).mean()
    return medoids, costo


def clara(X, k, n_muestras=5, tam_muestra=4000, tam_eval=30000):
    """CLARA: PAM en muestras; el mejor conjunto de medoides se elige por costo global."""
    idx_eval = RNG.choice(len(X), size=min(tam_eval, len(X)), replace=False)
    X_eval = X[idx_eval]
    mejor = None
    for s in range(n_muestras):
        rng = np.random.default_rng(SEED + s)
        idx_m = rng.choice(len(X), size=tam_muestra, replace=False)
        med_local, _ = pam_muestra(X[idx_m], k, rng)
        med_global = idx_m[med_local]
        costo = pairwise_distances(X_eval, X[med_global]).min(axis=1).mean()
        if mejor is None or costo < mejor["costo"]:
            mejor = {"medoids_idx": med_global, "costo": costo, "muestra": s}
    labels = pairwise_distances(X, X[mejor["medoids_idx"]]).argmin(axis=1)
    return mejor["medoids_idx"], labels, mejor["costo"]


def silueta(X, labels, n=10000):
    idx = RNG.choice(len(X), size=min(n, len(X)), replace=False)
    return round(float(silhouette_score(X[idx], labels[idx])), 4)


def main():
    for d in (MODELOS, FIGURAS, RESULTADOS):
        d.mkdir(exist_ok=True)

    vista = pd.read_csv(DATOS / "vista_minable_clustering.csv")
    base = pd.read_csv(DATOS / "base_limpia_para_perfilamiento.csv",
                       keep_default_na=False, na_values=[""])
    X_full = vista.to_numpy(dtype=float)                 # Vista A: 31 atributos
    X_num = vista[NUMERICAS].to_numpy(dtype=float)       # Vista B: 14 numéricas
    X_cond = vista[CONDUCTUALES].to_numpy(dtype=float)   # Vista C: 12 conductuales (solo hábitos)

    # Terciles de rendimiento para la validación a posteriori (feedback del profesor):
    # los grupos se forman SOLO con hábitos y después se les "agrega" la nota para
    # comprobar coherencia. La nota jamás participa en la formación de los grupos.
    base["rendimiento"] = pd.qcut(base["final_grade"], q=3, labels=["Bajo", "Medio", "Alto"])
    vista[CONDUCTUALES].to_csv(DATOS / "vista_minable_clustering_conductual.csv", index=False)
    resultados = {}

    # ---------------- selección de k: codo + silueta, en las tres vistas ----------------
    barrido = []
    for nombre, X in (("A_completa_31", X_full), ("B_numerica_14", X_num),
                      ("C_conductual_12", X_cond)):
        for k in range(2, 11):
            km = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X)
            barrido.append({"vista": nombre, "k": k,
                            "inercia": round(float(km.inertia_), 1),
                            "silueta": silueta(X, km.labels_)})
            print(barrido[-1])
    barrido_df = pd.DataFrame(barrido)
    barrido_df.to_csv(RESULTADOS / "clustering_barrido_k.csv", index=False)
    resultados["barrido_k"] = barrido

    # Evidencia del descarte de las vistas A y B (perfiles planos / partición por edad):
    km_a = KMeans(n_clusters=3, n_init=10, random_state=SEED).fit(X_full)
    km_b = KMeans(n_clusters=2, n_init=10, random_state=SEED).fit(X_num)
    ev = {}
    for nombre, lab in (("A_completa_31_k3", km_a.labels_), ("B_numerica_14_k2", km_b.labels_)):
        df_ev = base.copy(); df_ev["c"] = lab
        pf = (df_ev.groupby("c")["pass_fail"].apply(lambda s: (s == "Fail").mean() * 100)).round(1)
        edad = df_ev.groupby("c")["age"].mean().round(2)
        ev[nombre] = {"pct_fail_por_grupo": pf.tolist(), "edad_media_por_grupo": edad.tolist()}
    resultados["vistas_descartadas"] = ev

    # Vista y k seleccionados (justificación en el docstring y en la sección VI del informe):
    # silueta casi plana y codo no concluyente => decide la interpretabilidad de negocio;
    # k=4 sobre la vista conductual C (solo hábitos, sin nota ni edad).
    VISTA_SEL, K = "C_conductual_12", 4
    X_sel, cols_sel = X_cond, CONDUCTUALES
    sil_k = {int(r.k): float(r.silueta) for _, r in
             barrido_df[barrido_df.vista == VISTA_SEL].iterrows()}
    resultados["seleccion"] = {"vista": VISTA_SEL, "k": K, "silueta_por_k": sil_k,
                               "criterio": "silueta casi plana y codo no concluyente; k=4 "
                               "maximiza la interpretabilidad y la diferenciación del % de "
                               "reprobación entre grupos; la vista usa SOLO hábitos: la "
                               "nota no participa en la formación de los grupos"}
    print(f"\n>> Vista seleccionada: {VISTA_SEL}, k={K}")

    # ---------------- modelos finales ----------------
    km = KMeans(n_clusters=K, n_init=10, random_state=SEED).fit(X_sel)
    lab_km = km.labels_
    med_idx, lab_kmed, costo = clara(X_sel, K)

    resultados["kmeans"] = {
        "silueta": silueta(X_sel, lab_km),
        "davies_bouldin": round(float(davies_bouldin_score(X_sel, lab_km)), 4),
        "inercia": round(float(km.inertia_), 1),
        "tamanos": np.bincount(lab_km).tolist(),
    }
    resultados["kmedoids"] = {
        "silueta": silueta(X_sel, lab_kmed),
        "davies_bouldin": round(float(davies_bouldin_score(X_sel, lab_kmed)), 4),
        "costo_medio": round(float(costo), 4),
        "tamanos": np.bincount(lab_kmed).tolist(),
        "medoides_student_id": base.loc[med_idx, "student_id"].tolist(),
    }
    resultados["concordancia_ARI"] = round(float(adjusted_rand_score(lab_km, lab_kmed)), 4)
    print(json.dumps({k: v for k, v in resultados.items() if k != "barrido_k"},
                     indent=2, ensure_ascii=False))

    # ---------------- EDA por grupo (perfilamiento en escala original) ----------------
    # Validación a posteriori: recién aquí se "agrega" la nota (final_grade, pass_fail,
    # previous_grade y terciles de rendimiento) para comprobar la coherencia de los
    # perfiles conductuales. Ninguna de estas variables participó en el clustering.
    perfiles, coherencias = {}, {}
    for alg, lab in (("kmeans", lab_km), ("kmedoids", lab_kmed)):
        df = base.copy()
        df["cluster"] = lab
        agg = df.groupby("cluster")[NUMERICAS + ["final_grade"]].mean().round(2)
        agg["n"] = df.groupby("cluster").size()
        agg["pct_fail"] = (df.groupby("cluster")["pass_fail"]
                           .apply(lambda s: (s == "Fail").mean() * 100).round(1))
        for c in ("family_income", "internet_access", "device_type"):
            agg[f"moda_{c}"] = df.groupby("cluster")[c].agg(lambda s: s.mode().iloc[0])
        perfiles[alg] = agg
        agg.to_csv(RESULTADOS / f"clustering_perfiles_{alg}.csv")

        # % de estudiantes de cada tercil de rendimiento dentro de cada grupo
        coher = (pd.crosstab(df["cluster"], df["rendimiento"], normalize="index") * 100).round(1)
        coherencias[alg] = coher
        coher.to_csv(RESULTADOS / f"clustering_coherencia_rendimiento_{alg}.csv")

    resultados["coherencia_rendimiento_kmeans"] = {
        f"grupo_{c}": {str(r): float(coherencias["kmeans"].loc[c, r])
                       for r in coherencias["kmeans"].columns}
        for c in coherencias["kmeans"].index}

    # etiquetas por estudiante (entregable de despliegue/anexo)
    pd.DataFrame({"student_id": base.student_id, "cluster_kmeans": lab_km,
                  "cluster_kmedoids": lab_kmed}) \
        .to_csv(RESULTADOS / "clustering_asignaciones.csv", index=False)

    joblib.dump({"modelo": km, "columnas": cols_sel, "vista": VISTA_SEL},
                MODELOS / "kmeans.joblib")
    joblib.dump({"medoides": X_sel[med_idx], "medoides_student_id":
                 resultados["kmedoids"]["medoides_student_id"],
                 "columnas": cols_sel, "vista": VISTA_SEL},
                MODELOS / "kmedoids_clara.joblib")

    with open(RESULTADOS / "metricas_clustering.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    # ---------------- figuras ----------------
    plt.rcParams.update({"figure.dpi": 150, "font.size": 9})

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for nombre, marker in (("A_completa_31", "o"), ("B_numerica_14", "s"),
                           ("C_conductual_12", "^")):
        sub = barrido_df[barrido_df.vista == nombre]
        axes[0].plot(sub.k, sub.inercia / sub.inercia.max(), marker=marker,
                     label=f"vista {nombre[0]} ({nombre.split('_')[-1]} attrs)")
        axes[1].plot(sub.k, sub.silueta, marker=marker, label=f"vista {nombre[0]}")
    axes[0].set_xlabel("k (número de grupos)"); axes[0].set_ylabel("Inercia (normalizada)")
    axes[0].set_title("Método del codo"); axes[0].legend()
    axes[1].set_xlabel("k"); axes[1].set_ylabel("Coeficiente de silueta")
    axes[1].set_title("Silueta según k (muestra de 10.000)"); axes[1].legend()
    axes[1].axvline(K, color="grey", ls="--", lw=1)
    fig.tight_layout()
    fig.savefig(FIGURAS / "clustering_codo_silueta.png", bbox_inches="tight")
    plt.close(fig)

    # perfiles z-score (qué distingue a cada grupo)
    agg = perfiles["kmeans"][NUMERICAS]
    z = (agg - base[NUMERICAS].mean()) / base[NUMERICAS].std()
    fig, ax = plt.subplots(figsize=(9, 0.6 * K + 2))
    im = ax.imshow(z, cmap="RdBu_r", vmin=-1.2, vmax=1.2, aspect="auto")
    ax.set_xticks(range(len(NUMERICAS)), NUMERICAS, rotation=45, ha="right")
    ax.set_yticks(range(K), [f"Grupo {i}\n(n={resultados['kmeans']['tamanos'][i]:,})".replace(",", ".")
                             for i in range(K)])
    for i in range(K):
        for j in range(len(NUMERICAS)):
            ax.text(j, i, f"{z.iloc[i, j]:+.1f}".replace(".", ","), ha="center", va="center",
                    fontsize=7, color="white" if abs(z.iloc[i, j]) > 0.75 else "black")
    ax.set_title("Perfil de cada grupo (K-Means) — desviación de la media global (z-score)")
    fig.colorbar(im, shrink=0.8)
    fig.tight_layout()
    fig.savefig(FIGURAS / "clustering_perfiles_heatmap.png", bbox_inches="tight")
    plt.close(fig)

    # dispersión PCA con ambos algoritmos
    idx = RNG.choice(len(X_sel), size=20000, replace=False)
    P = PCA(n_components=2, random_state=SEED).fit_transform(X_sel[idx])
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharex=True, sharey=True)
    for ax, lab, nombre in ((axes[0], lab_km[idx], "K-Means"),
                            (axes[1], lab_kmed[idx], "K-Medoids (CLARA)")):
        sc = ax.scatter(P[:, 0], P[:, 1], c=lab, s=2, cmap="tab10", alpha=.5)
        ax.set_title(nombre); ax.set_xlabel("Componente principal 1")
    axes[0].set_ylabel("Componente principal 2")
    fig.suptitle(f"Grupos proyectados en 2 componentes principales (muestra de 20.000, k={K})")
    fig.tight_layout()
    fig.savefig(FIGURAS / "clustering_pca_scatter.png", bbox_inches="tight")
    plt.close(fig)

    # tamaños y % de reprobación por grupo
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    p = perfiles["kmeans"]
    axes[0].bar([f"G{i}" for i in p.index], p.n, color="#2c7fb8")
    axes[0].set_title("Tamaño de cada grupo (K-Means)"); axes[0].set_ylabel("estudiantes")
    axes[1].bar([f"G{i}" for i in p.index], p.pct_fail, color="#d95f0e")
    axes[1].axhline((base.pass_fail == "Fail").mean() * 100, color="grey", ls="--",
                    label="promedio global")
    axes[1].set_title("% de reprobación por grupo"); axes[1].set_ylabel("% Fail")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(FIGURAS / "clustering_tamanos_reprobacion.png", bbox_inches="tight")
    plt.close(fig)

    # validación a posteriori: terciles de rendimiento dentro de cada grupo conductual
    coher_km = coherencias["kmeans"]
    fig, ax = plt.subplots(figsize=(7, 3.8))
    fondo = np.zeros(len(coher_km))
    colores = {"Bajo": "#d95f0e", "Medio": "#fec44f", "Alto": "#2c7fb8"}
    for cat in ("Bajo", "Medio", "Alto"):
        vals = coher_km[cat].to_numpy(dtype=float)
        ax.bar([f"G{i}" for i in coher_km.index], vals, bottom=fondo,
               label=cat, color=colores[cat])
        fondo += vals
    ax.set_ylabel("% de estudiantes del grupo")
    ax.set_title("Validación a posteriori (K-Means): terciles de rendimiento por grupo\n"
                 "(la nota NO participó en la formación de los grupos)")
    ax.legend(title="Rendimiento")
    fig.tight_layout()
    fig.savefig(FIGURAS / "clustering_coherencia_rendimiento.png", bbox_inches="tight")
    plt.close(fig)

    print("\nListo: clustering completado.")


if __name__ == "__main__":
    main()
