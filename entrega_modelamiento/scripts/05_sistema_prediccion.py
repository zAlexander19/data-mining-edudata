# -*- coding: utf-8 -*-
"""
SISTEMA DE PREDICCIÓN DE RIESGO ACADÉMICO — Entregable de la tarea predictiva
(apuntes del curso: tarea descriptiva -> informe; tarea predictiva -> SISTEMA)

Aplica el modelo APROBADO (Naïve Bayes mixto, entrenado balanceado y sin la nota previa)
para predecir la probabilidad de reprobar de uno o más estudiantes A PARTIR DE SUS
HÁBITOS, sin usar ninguna calificación. Además asigna el perfil conductual (K-Means)
y la acción de apoyo sugerida.

MODOS DE USO
------------
1) Interactivo (un estudiante, por consola):
       python scripts/05_sistema_prediccion.py
   El sistema pregunta cada hábito (Enter = valor promedio de la población).

2) Lote (varios estudiantes, desde CSV — puede generarse desde Excel con
   "Guardar como CSV"; la plantilla con las columnas está en
   datos/sistema_plantilla.csv):
       python scripts/05_sistema_prediccion.py --csv entrada.csv salida.csv

3) Demostración (3 estudiantes ficticios de distinto perfil):
       python scripts/05_sistema_prediccion.py --demo

Opcional: --umbral 0.6 cambia el punto de alerta (por defecto 0,5; ver el análisis de
umbral de la sección 8.2 del informe para elegirlo según la capacidad de tutorías).
"""
import argparse
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.special import logsumexp

BASE = Path(__file__).resolve().parents[1]
DATOS, MODELOS, RESULTADOS = BASE / "datos", BASE / "modelos", BASE / "resultados"

PERFILES = {
    0: ("Riesgo por gestión del tiempo deficiente", "Taller de planificación y organización"),
    1: ("Alto desempeño autónomo", "Mantención / mentor par"),
    2: ("Riesgo por calidad de apuntes deficiente", "Técnicas de estudio y toma de apuntes"),
    3: ("Riesgo por desmotivación", "Programa motivacional y consejería"),
}

# Media poblacional (EDA 2, Tabla 53 del informe): default del modo interactivo y
# referencia para detectar los hábitos más débiles de cada estudiante.
MEDIAS = {
    "age": 16.5, "study_hours": 4.50, "attendance": 84.71, "sleep_hours": 6.99,
    "assignments_completed": 7.84, "practice_tests_taken": 4.02, "group_study_hours": 1.53,
    "notes_quality_score": 6.94, "time_management_score": 6.46, "motivation_level": 6.95,
    "mental_health_score": 6.98, "screen_time": 4.02, "social_media_hours": 2.53,
}
ETIQUETAS = {
    "age": "Edad (años)", "study_hours": "Horas de estudio diarias",
    "attendance": "Asistencia (%)", "sleep_hours": "Horas de sueño",
    "assignments_completed": "Tareas completadas (0-10)",
    "practice_tests_taken": "Ensayos/tests de práctica (0-10)",
    "group_study_hours": "Horas de estudio en grupo",
    "notes_quality_score": "Calidad de los apuntes (1-10)",
    "time_management_score": "Gestión del tiempo (1-10)",
    "motivation_level": "Nivel de motivación (1-10)",
    "mental_health_score": "Salud mental autopercibida (1-10)",
    "screen_time": "Tiempo de pantalla diario (h)",
    "social_media_hours": "Horas en redes sociales",
    "gender": "Género", "family_income": "Ingreso familiar",
    "parent_education": "Educación de los padres", "internet_access": "Acceso a internet",
    "device_type": "Dispositivo principal", "school_type": "Tipo de establecimiento",
    "extracurriculars": "Actividad extracurricular",
}
# hábitos accionables sobre los que se reportan las palancas más débiles
ACCIONABLES = ["study_hours", "attendance", "sleep_hours", "assignments_completed",
               "practice_tests_taken", "notes_quality_score", "time_management_score",
               "motivation_level"]

DEMO = [
    {"nombre": "Estudiante A (hábitos sólidos)", "age": 16, "gender": "Female",
     "study_hours": 7.5, "attendance": 95, "sleep_hours": 8,
     "assignments_completed": 9.5, "practice_tests_taken": 7, "group_study_hours": 2,
     "notes_quality_score": 8.5, "time_management_score": 8.5, "motivation_level": 9,
     "mental_health_score": 8, "screen_time": 2.5, "social_media_hours": 1.5,
     "family_income": "Medium", "parent_education": "Bachelor", "internet_access": "Yes",
     "device_type": "Laptop", "school_type": "Public", "extracurriculars": "Sports"},
    {"nombre": "Estudiante B (desmotivado)", "age": 17, "gender": "Male",
     "study_hours": 5.0, "attendance": 85, "sleep_hours": 7,
     "assignments_completed": 8, "practice_tests_taken": 4, "group_study_hours": 1.5,
     "notes_quality_score": 7, "time_management_score": 7, "motivation_level": 2,
     "mental_health_score": 5, "screen_time": 5, "social_media_hours": 3,
     "family_income": "Medium", "parent_education": "Master", "internet_access": "Yes",
     "device_type": "Mobile", "school_type": "Private", "extracurriculars": "None"},
    {"nombre": "Estudiante C (poco estudio y mala organización)", "age": 15, "gender": "Other",
     "study_hours": 1.0, "attendance": 78, "sleep_hours": 6,
     "assignments_completed": 6, "practice_tests_taken": 2, "group_study_hours": 0.5,
     "notes_quality_score": 5, "time_management_score": 3, "motivation_level": 6,
     "mental_health_score": 7, "screen_time": 7, "social_media_hours": 5,
     "family_income": "Low", "parent_education": "High School", "internet_access": "No",
     "device_type": "None", "school_type": "Public", "extracurriculars": "None"},
]


class Sistema:
    """Carga los modelos aprobados y predice riesgo + perfil para un DataFrame de hábitos."""

    def __init__(self):
        nb = joblib.load(MODELOS / "naive_bayes_mixto.joblib")
        km = joblib.load(MODELOS / "kmeans.joblib")
        with open(RESULTADOS / "rangos_normalizacion.json", encoding="utf-8") as f:
            self.rangos = json.load(f)
        self.gnb, self.cnb = nb["gnb"], nb["cnb"]
        self.numericas, self.categoricas = nb["numericas"], nb["categoricas"]
        self.categorias = nb["categorias"]
        self.kmeans, self.cols_cluster = km["modelo"], km["columnas"]

    def validar(self, df):
        faltan = [c for c in self.numericas + self.categoricas if c not in df.columns]
        if faltan:
            raise SystemExit(f"ERROR: faltan columnas en la entrada: {faltan}")
        for c in self.categoricas:
            malos = set(df[c].astype(str)) - set(self.categorias[c])
            if malos:
                raise SystemExit(f"ERROR: valores no reconocidos en '{c}': {sorted(malos)}. "
                                 f"Opciones válidas: {self.categorias[c]}")

    def predecir(self, df, umbral=0.5):
        self.validar(df)
        X_num = df[self.numericas].astype(float).to_numpy()
        X_cat = np.column_stack([
            pd.Categorical(df[c].astype(str), categories=self.categorias[c]).codes
            for c in self.categoricas])
        jll = (self.gnb.predict_log_proba(X_num) + self.cnb.predict_log_proba(X_cat)
               - np.log(self.gnb.class_prior_))
        proba = np.exp(jll - logsumexp(jll, axis=1, keepdims=True))
        p_fail = proba[:, list(self.gnb.classes_).index("Fail")]

        # perfil conductual: normalización Min-Max con los rangos del ETL + centroide más cercano
        Z = np.column_stack([
            (df[c].astype(float) - self.rangos[c]["min"])
            / (self.rangos[c]["max"] - self.rangos[c]["min"]) for c in self.cols_cluster])
        grupo = self.kmeans.predict(Z)

        out = pd.DataFrame({
            "p_reprobar_pct": (p_fail * 100).round(1),
            "alerta": np.where(p_fail >= umbral, "SÍ", "no"),
            "grupo": grupo,
            "perfil": [PERFILES[g][0] for g in grupo],
            "accion_sugerida": [PERFILES[g][1] if p >= umbral else "seguimiento regular"
                                for g, p in zip(grupo, p_fail)],
        }, index=df.index)
        # las 2 palancas accionables más débiles (solo si están realmente bajo la media)
        deficit = pd.DataFrame({c: (df[c].astype(float) - MEDIAS[c]) for c in ACCIONABLES})
        out["habitos_mas_debiles"] = [
            "; ".join(f"{ETIQUETAS[c]}: {df[c].iloc[i]:.1f} (media {MEDIAS[c]:.1f})"
                      for c in deficit.iloc[i].nsmallest(2).index
                      if deficit.iloc[i][c] < -0.3)
            or "(ninguno bajo la media poblacional)"
            for i in range(len(df))]
        return out


def imprimir(nombre, fila_in, fila_out, umbral):
    print("=" * 72)
    print(f" {nombre}")
    print("-" * 72)
    print(f"  Probabilidad de reprobar : {fila_out.p_reprobar_pct:5.1f} %")
    print(f"  Alerta (umbral {umbral:.2f})    : {fila_out.alerta}")
    print(f"  Perfil conductual        : {fila_out.perfil}")
    print(f"  Acción sugerida          : {fila_out.accion_sugerida}")
    print(f"  Hábitos más débiles      : {fila_out.habitos_mas_debiles}")


def modo_interactivo(sis, umbral):
    print("SISTEMA DE PREDICCIÓN DE RIESGO ACADÉMICO — ingreso de un estudiante")
    print("(Enter acepta el valor promedio de la población, mostrado entre corchetes)\n")
    datos = {}
    for c in sis.numericas:
        r = sis.rangos.get(c, {})
        while True:
            txt = input(f"  {ETIQUETAS[c]} [{MEDIAS[c]}]: ").strip().replace(",", ".")
            if not txt:
                datos[c] = MEDIAS[c]
                break
            try:
                v = float(txt)
            except ValueError:
                print("    -> ingrese un número.")
                continue
            if r and not (r["min"] <= v <= r["max"]):
                print(f"    -> fuera de rango [{r['min']}, {r['max']}].")
                continue
            datos[c] = v
            break
    for c in sis.categoricas:
        ops = sis.categorias[c]
        while True:
            txt = input(f"  {ETIQUETAS[c]} {ops} [{ops[0]}]: ").strip()
            if not txt:
                datos[c] = ops[0]
                break
            match = [o for o in ops if o.lower() == txt.lower()]
            if match:
                datos[c] = match[0]
                break
            print(f"    -> opción no válida; elija entre {ops}.")
    df = pd.DataFrame([datos])
    out = sis.predecir(df, umbral).iloc[0]
    print()
    imprimir("RESULTADO", df.iloc[0], out, umbral)


def main():
    ap = argparse.ArgumentParser(description="Sistema de predicción de riesgo académico")
    ap.add_argument("--csv", nargs=2, metavar=("ENTRADA", "SALIDA"),
                    help="modo lote: CSV de entrada y CSV de salida")
    ap.add_argument("--demo", action="store_true", help="3 estudiantes de demostración")
    ap.add_argument("--umbral", type=float, default=0.5,
                    help="umbral de alerta sobre P(reprobar) (defecto 0.5)")
    args = ap.parse_args()

    sis = Sistema()
    if args.demo:
        df = pd.DataFrame(DEMO)
        out = sis.predecir(df, args.umbral)
        for i in range(len(df)):
            imprimir(df.nombre.iloc[i], df.iloc[i], out.iloc[i], args.umbral)
    elif args.csv:
        entrada, salida = args.csv
        # "None" es una categoría válida (device_type / extracurriculars), no un nulo
        df = pd.read_csv(entrada, keep_default_na=False, na_values=[""])
        out = sis.predecir(df, args.umbral)
        res = pd.concat([df, out], axis=1)
        res.to_csv(salida, index=False, encoding="utf-8-sig")
        print(f"{len(res)} estudiantes procesados -> {salida}")
        print(f"  alertas emitidas: {(out.alerta == 'SÍ').sum()} "
              f"({(out.alerta == 'SÍ').mean() * 100:.1f}%) con umbral {args.umbral}")
    else:
        try:
            modo_interactivo(sis, args.umbral)
        except (EOFError, KeyboardInterrupt):
            sys.exit("\n(cancelado)")


if __name__ == "__main__":
    main()
