# -*- coding: utf-8 -*-
"""
Genera la DEMO WEB del modelo de predicción (demo_web/index.html).

Exporta los parámetros de los modelos aprobados (Naïve Bayes mixto y K-Means) a JSON
y los inyecta en la plantilla HTML (demo_web/plantilla_core.html). El resultado es un
único archivo autocontenido que replica el modelo en JavaScript: se abre con doble
clic, sin servidor ni instalación.

Cada preset incluye la predicción esperada calculada aquí con el modelo REAL de
scikit-learn; la página ejecuta un autotest al cargar y avisa si el cálculo en
JavaScript se desvía del original.
"""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.special import logsumexp

BASE = Path(__file__).resolve().parents[1]
DATOS, MODELOS, RESULTADOS, DEMO_DIR = (BASE / d for d in
                                        ("datos", "modelos", "resultados", "demo_web"))

# etiqueta, etiqueta corta, paso del slider, unidad (sufijo del valor) y significado
# (unidades y definiciones según la Tabla 45 del informe, sección 4.3.2).
VARIABLES = {
    "age": ("Edad", "Edad", 1, "años",
            "edad del estudiante, en años cumplidos"),
    "study_hours": ("Horas de estudio", "Horas de estudio", 0.1, "h/día",
                    "horas DIARIAS dedicadas al estudio individual, fuera de clases"),
    "attendance": ("Asistencia", "Asistencia", 1, "%",
                   "porcentaje de asistencia a clases en el período"),
    "sleep_hours": ("Horas de sueño", "Sueño", 0.1, "h/día",
                    "horas de sueño diarias (promedio por noche)"),
    "assignments_completed": ("Cumplimiento de tareas", "Tareas", 0.1, "/ 10",
                              "escala 0–10: nivel de entrega de tareas y trabajos "
                              "(0 = ninguna · 10 = todas)"),
    "practice_tests_taken": ("Ensayos de práctica", "Ensayos", 0.1, "/ 10",
                             "escala 0–10: cantidad e intensidad de ensayos o tests "
                             "de práctica rendidos"),
    "group_study_hours": ("Estudio en grupo", "Estudio en grupo", 0.1, "h/día",
                          "horas diarias de estudio en grupo (además del individual)"),
    "notes_quality_score": ("Calidad de apuntes", "Apuntes", 0.1, "/ 10",
                            "escala 1–10: calidad de los apuntes propios "
                            "(1 = deficientes · 10 = excelentes)"),
    "time_management_score": ("Gestión del tiempo", "Gestión del tiempo", 0.1, "/ 10",
                              "escala 1–10: capacidad de organizar y planificar el "
                              "tiempo (autoevaluación)"),
    "motivation_level": ("Motivación", "Motivación", 0.1, "/ 10",
                         "escala 1–10: nivel de motivación declarado por el estudiante"),
    "mental_health_score": ("Salud mental", "Salud mental", 0.1, "/ 10",
                            "escala 1–10: estado de salud mental autopercibido"),
    "screen_time": ("Tiempo de pantalla", "Pantalla", 0.1, "h/día",
                    "horas diarias frente a pantallas, uso general (estudio y ocio)"),
    "social_media_hours": ("Redes sociales", "Redes sociales", 0.1, "h/día",
                           "horas diarias en redes sociales (parte del tiempo de pantalla)"),
    "gender": ("Género", "Género", None, None, "género autoidentificado"),
    "family_income": ("Ingreso familiar", "Ingreso", None, None,
                      "nivel de ingreso del hogar (bajo / medio / alto)"),
    "parent_education": ("Educación de los padres", "Educ. padres", None, None,
                         "máximo nivel educativo alcanzado por los padres"),
    "internet_access": ("Acceso a internet", "Internet", None, None,
                        "disponibilidad de internet en el hogar"),
    "device_type": ("Dispositivo principal", "Dispositivo", None, None,
                    "dispositivo principal con el que estudia"),
    "school_type": ("Tipo de establecimiento", "Establecimiento", None, None,
                    "establecimiento público o privado"),
    "extracurriculars": ("Actividad extracurricular", "Extracurricular", None, None,
                         "actividad extracurricular principal del estudiante"),
}
OPCIONES_ES = {  # texto mostrado en los selectores (el valor interno no cambia)
    "gender": {"Female": "Femenino", "Male": "Masculino", "Other": "Otro"},
    "family_income": {"Low": "Bajo", "Medium": "Medio", "High": "Alto"},
    "parent_education": {"High School": "Educación secundaria", "Bachelor": "Pregrado",
                         "Master": "Magíster", "PhD": "Doctorado"},
    "internet_access": {"No": "No", "Yes": "Sí"},
    "device_type": {"Laptop": "Notebook", "Mobile": "Celular", "Tablet": "Tablet",
                    "None": "Sin dispositivo propio"},
    "school_type": {"Public": "Público", "Private": "Privado"},
    "extracurriculars": {"Arts": "Arte", "Coding Club": "Club de programación",
                         "Debate": "Debate", "Music": "Música", "Sports": "Deportes",
                         "None": "Ninguna"},
}
MEDIAS = {"age": 16.5, "study_hours": 4.5, "attendance": 84.7, "sleep_hours": 7.0,
          "assignments_completed": 7.8, "practice_tests_taken": 4.0,
          "group_study_hours": 1.5, "notes_quality_score": 6.9,
          "time_management_score": 6.5, "motivation_level": 7.0,
          "mental_health_score": 7.0, "screen_time": 4.0, "social_media_hours": 2.5}
GRUPOS_FORM = [
    {"titulo": "Hábitos de estudio",
     "campos": ["study_hours", "assignments_completed", "practice_tests_taken",
                "group_study_hours", "notes_quality_score"]},
    {"titulo": "Organización y ánimo",
     "campos": ["time_management_score", "motivation_level", "mental_health_score"]},
    {"titulo": "Rutina diaria",
     "campos": ["attendance", "sleep_hours", "screen_time", "social_media_hours"]},
    {"titulo": "Contexto",
     "campos": ["age", "gender", "family_income", "parent_education",
                "internet_access", "device_type", "school_type", "extracurriculars"]},
]
ACCIONABLES = ["study_hours", "attendance", "sleep_hours", "assignments_completed",
               "practice_tests_taken", "notes_quality_score", "time_management_score",
               "motivation_level"]
PERFILES = {
    0: {"nombre": "Riesgo por gestión del tiempo deficiente",
        "accion": "taller de planificación y organización",
        "pct_alumnado": "25,5%", "pct_fail": "46,7%", "critico": True},
    1: {"nombre": "Alto desempeño autónomo", "accion": "mantención / mentor par",
        "pct_alumnado": "26,4%", "pct_fail": "18,0%", "critico": False},
    2: {"nombre": "Riesgo por calidad de apuntes deficiente",
        "accion": "técnicas de estudio y toma de apuntes",
        "pct_alumnado": "24,2%", "pct_fail": "44,7%", "critico": True},
    3: {"nombre": "Riesgo por desmotivación",
        "accion": "programa motivacional y consejería",
        "pct_alumnado": "24,0%", "pct_fail": "51,7%", "critico": True},
}
PRESETS_BASE = [
    ("Promedio", dict(MEDIAS, age=16, gender="Female", family_income="Medium",
                      parent_education="Bachelor", internet_access="Yes",
                      device_type="Laptop", school_type="Public", extracurriculars="None")),
    ("A · hábitos sólidos",
     {"age": 16, "gender": "Female", "study_hours": 7.5, "attendance": 95,
      "sleep_hours": 8, "assignments_completed": 9.5, "practice_tests_taken": 7,
      "group_study_hours": 2, "notes_quality_score": 8.5, "time_management_score": 8.5,
      "motivation_level": 9, "mental_health_score": 8, "screen_time": 2.5,
      "social_media_hours": 1.5, "family_income": "Medium", "parent_education": "Bachelor",
      "internet_access": "Yes", "device_type": "Laptop", "school_type": "Public",
      "extracurriculars": "Sports"}),
    ("B · desmotivado",
     {"age": 17, "gender": "Male", "study_hours": 5.0, "attendance": 85,
      "sleep_hours": 7, "assignments_completed": 8, "practice_tests_taken": 4,
      "group_study_hours": 1.5, "notes_quality_score": 7, "time_management_score": 7,
      "motivation_level": 2, "mental_health_score": 5, "screen_time": 5,
      "social_media_hours": 3, "family_income": "Medium", "parent_education": "Master",
      "internet_access": "Yes", "device_type": "Mobile", "school_type": "Private",
      "extracurriculars": "None"}),
    ("C · desorganizado",
     {"age": 15, "gender": "Other", "study_hours": 1.0, "attendance": 78,
      "sleep_hours": 6, "assignments_completed": 6, "practice_tests_taken": 2,
      "group_study_hours": 0.5, "notes_quality_score": 5, "time_management_score": 3,
      "motivation_level": 6, "mental_health_score": 7, "screen_time": 7,
      "social_media_hours": 5, "family_income": "Low", "parent_education": "High School",
      "internet_access": "No", "device_type": "None", "school_type": "Public",
      "extracurriculars": "None"}),
]
UMBRAL_STATS = [  # de resultados/despliegue_umbral_alertas.csv (conjunto de prueba)
    {"umbral": 0.3, "recall": "95.9", "precision": "56.6", "alumnado": "67.4"},
    {"umbral": 0.4, "recall": "90.2", "precision": "64.7", "alumnado": "55.6"},
    {"umbral": 0.5, "recall": "81.2", "precision": "72.4", "alumnado": "44.7"},
    {"umbral": 0.6, "recall": "68.5", "precision": "79.7", "alumnado": "34.2"},
    {"umbral": 0.7, "recall": "52.9", "precision": "86.6", "alumnado": "24.3"},
]


def main():
    nb = joblib.load(MODELOS / "naive_bayes_mixto.joblib")
    km = joblib.load(MODELOS / "kmeans.joblib")
    with open(RESULTADOS / "rangos_normalizacion.json", encoding="utf-8") as f:
        rangos = json.load(f)
    gnb, cnb = nb["gnb"], nb["cnb"]

    def predecir(valores):
        """Predicción con el modelo real (referencia para el autotest de la página)."""
        x_num = np.array([[float(valores[c]) for c in nb["numericas"]]])
        x_cat = np.array([[nb["categorias"][c].index(str(valores[c]))
                           for c in nb["categoricas"]]])
        jll = (gnb.predict_log_proba(x_num) + cnb.predict_log_proba(x_cat)
               - np.log(gnb.class_prior_))
        p = np.exp(jll - logsumexp(jll, axis=1, keepdims=True))
        p_fail = float(p[0, list(gnb.classes_).index("Fail")])
        z = np.array([[(float(valores[c]) - rangos[c]["min"])
                       / (rangos[c]["max"] - rangos[c]["min"]) for c in km["columnas"]]])
        return p_fail, int(km["modelo"].predict(z)[0])

    presets = []
    for nombre, valores in PRESETS_BASE:
        p, g = predecir(valores)
        presets.append({"nombre": nombre, "valores": valores,
                        "esperado_pct": round(p * 100, 2), "esperado_grupo": g})
        print(f"  preset {nombre!r}: P(reprobar)={p*100:.1f}%  grupo={g} "
              f"({PERFILES[g]['nombre']})")

    variables = {}
    for col, (larga, corta, paso, unidad, desc) in VARIABLES.items():
        v = {"etiqueta": larga, "corta": corta, "desc": desc}
        if paso is not None:
            r = rangos[col]
            v.update({"min": r["min"], "max": r["max"], "paso": paso,
                      "media": MEDIAS[col], "unidad": unidad})
        variables[col] = v

    modelo = {
        "clases": [str(c) for c in gnb.classes_],
        "prior": gnb.class_prior_.tolist(),
        "numericas": nb["numericas"],
        "categoricas": nb["categoricas"],
        "theta": gnb.theta_.tolist(),
        "varianza": gnb.var_.tolist(),
        "cat_logprob": [flp.tolist() for flp in cnb.feature_log_prob_],
        "categorias": nb["categorias"],
        "centroides": km["modelo"].cluster_centers_.tolist(),
        "cols_cluster": km["columnas"],
        "rangos": {c: rangos[c] for c in set(nb["numericas"]) | set(km["columnas"])},
        "variables": variables,
        "opciones_es": OPCIONES_ES,
        "grupos_form": GRUPOS_FORM,
        "accionables": ACCIONABLES,
        "perfiles": {str(k): v for k, v in PERFILES.items()},
        "presets": presets,
        "umbral_stats": UMBRAL_STATS,
    }
    # los índices de perfiles llegan como enteros al JS
    modelo["perfiles"] = [PERFILES[i] for i in range(4)]

    core = (DEMO_DIR / "plantilla_core.html").read_text(encoding="utf-8")
    core = core.replace("__MODELO_JSON__", json.dumps(modelo, ensure_ascii=False))

    html = ("<!doctype html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "</head>\n<body>\n" + core + "\n</body>\n</html>\n")
    (DEMO_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"\nGenerado: demo_web/index.html "
          f"({len(html)//1024} KB, autocontenido — abrir con doble clic)")


if __name__ == "__main__":
    main()
