# -*- coding: utf-8 -*-
"""
Etapa V - Preparación de Datos (ETL)
Proyecto Data Mining - EduData Analytics (dataset sintético Kaggle, 300.000 estudiantes)

Replica el proceso ETL documentado en la sección V del informe:
  1. Extracción del CSV crudo.
  2. Selección de registros: filtro de edad 15-18 años (población escolar).
  3. Limpieza: eliminación de registros erróneos (final_grade = 0 con grade_category vacía).
  4. Transformación:
     - Vista de clasificación: escalas originales, categóricas nominales, objetivo pass_fail.
       previous_grade se EXCLUYE de los predictores (feedback del profesor): la nota del año
       anterior domina la predicción y sesga el análisis; el objetivo del modelo es medir el
       impacto de los HÁBITOS. La nota solo se usa para definir la etiqueta (pass_fail
       proviene de final_grade), no como variable de entrada.
     - Vista de clustering: numéricas normalizadas Min-Max [0,1], ordinales/binarias
       codificadas, nominales One-Hot, sin variable objetivo.
  5. Carga: exportación a CSV (y ARFF para Weka en el caso de la clasificación).

Nota técnica: en device_type y extracurriculars el valor "None" es una CATEGORÍA real
("sin dispositivo" / "sin actividad"), no un dato faltante; por eso se lee el CSV con
keep_default_na=False. Los únicos faltantes reales son 4 celdas vacías de grade_category.
"""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[1]
CSV_CRUDO = BASE.parent / "student_performance_prediction_dataset-2.csv"
DATOS = BASE / "datos"
RESULTADOS = BASE / "resultados"

NUMERICAS = [
    "age", "study_hours", "attendance", "sleep_hours", "previous_grade",
    "assignments_completed", "practice_tests_taken", "group_study_hours",
    "notes_quality_score", "time_management_score", "motivation_level",
    "mental_health_score", "screen_time", "social_media_hours",
]
ORDINALES = {
    "family_income": {"Low": 0, "Medium": 1, "High": 2},
    "parent_education": {"High School": 0, "Bachelor": 1, "Master": 2, "PhD": 3},
}
BINARIAS = {
    "internet_access": {"No": 0, "Yes": 1},
    "school_type": {"Public": 0, "Private": 1},
}
NOMINALES_ONEHOT = ["gender", "device_type", "extracurriculars"]


def extraer() -> pd.DataFrame:
    # keep_default_na=False evita que pandas convierta la categoría "None" en NaN;
    # las celdas realmente vacías ('') se marcan como faltantes.
    df = pd.read_csv(CSV_CRUDO, keep_default_na=False, na_values=[""])
    assert df.shape == (300000, 25), f"Formato inesperado del CSV: {df.shape}"
    return df


def seleccionar_y_limpiar(df: pd.DataFrame) -> pd.DataFrame:
    n0 = len(df)
    df = df[df["age"].between(15, 18)]                 # población escolar
    n1 = len(df)
    df = df[df["final_grade"] > 0]                     # registros erróneos (nota 0, categoría vacía)
    n2 = len(df)
    print(f"Registros: {n0} -> filtro edad 15-18: {n1} -> limpieza nota 0: {n2}")
    assert n1 == 171336 and n2 == 171334, "Conteos distintos a los documentados en el informe"
    assert df.isna().sum().sum() == 0, "Quedan valores faltantes tras la limpieza"
    assert df["student_id"].duplicated().sum() == 0, "Hay estudiantes duplicados"
    return df.reset_index(drop=True)


def vista_clasificacion(df: pd.DataFrame) -> pd.DataFrame:
    # Escalas originales; se eliminan identificador y variables con fuga de información.
    # previous_grade se excluye como predictor: la nota solo etiqueta (pass_fail), no entra
    # al modelo, para que la clasificación se base en los hábitos (feedback del profesor).
    return df.drop(columns=["student_id", "final_grade", "grade_category", "previous_grade"])


def vista_clustering(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    vista = pd.DataFrame(index=df.index)
    rangos = {}
    for col in NUMERICAS:                              # normalización Min-Max [0,1]
        vmin, vmax = float(df[col].min()), float(df[col].max())
        rangos[col] = {"min": vmin, "max": vmax}
        vista[col] = (df[col] - vmin) / (vmax - vmin)
    for col, mapa in ORDINALES.items():                # ordinales: preservan el orden
        vista[col] = df[col].map(mapa)
    for col, mapa in BINARIAS.items():                 # binarias 0/1
        vista[col] = df[col].map(mapa)
    for col in NOMINALES_ONEHOT:                       # One-Hot para nominales sin orden
        dummies = pd.get_dummies(df[col], prefix=col, dtype=int)
        vista = pd.concat([vista, dummies], axis=1)
    assert vista.notna().all().all(), "Codificación incompleta en la vista de clustering"
    return vista, rangos


def exportar_arff(df: pd.DataFrame, ruta: Path) -> None:
    """Exporta la vista de clasificación a ARFF para replicar los modelos en Weka."""
    lineas = ["@relation estudiantes_pass_fail", ""]
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            lineas.append(f"@attribute {col} numeric")
        else:
            cats = ",".join(f"'{c}'" for c in sorted(df[col].unique()))
            lineas.append(f"@attribute {col} {{{cats}}}")
    lineas += ["", "@data"]
    # newline="" evita la doble traducción \r\r\n de Windows; se fuerza \n uniforme.
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lineas) + "\n")
        df_out = df.copy()
        for col in df_out.select_dtypes(exclude="number").columns:
            df_out[col] = "'" + df_out[col].astype(str) + "'"
        df_out.to_csv(f, header=False, index=False, lineterminator="\n")


def main():
    DATOS.mkdir(exist_ok=True)
    RESULTADOS.mkdir(exist_ok=True)

    df = seleccionar_y_limpiar(extraer())

    clasif = vista_clasificacion(df)
    clasif.to_csv(DATOS / "vista_minable_clasificacion.csv", index=False)
    exportar_arff(clasif, DATOS / "vista_minable_clasificacion.arff")
    print(f"vista_minable_clasificacion: {clasif.shape[0]} x {clasif.shape[1]} "
          f"(objetivo pass_fail: {dict(clasif.pass_fail.value_counts(normalize=True).round(4)*100)})")

    clust, rangos = vista_clustering(df)
    clust.to_csv(DATOS / "vista_minable_clustering.csv", index=False)
    print(f"vista_minable_clustering: {clust.shape[0]} x {clust.shape[1]}")

    # Los rangos Min-Max se guardan para poder aplicar el modelo a datos nuevos (despliegue).
    with open(RESULTADOS / "rangos_normalizacion.json", "w", encoding="utf-8") as f:
        json.dump(rangos, f, indent=2, ensure_ascii=False)

    # Se conservan las variables originales junto a la vista de clustering para el
    # EDA por grupo (perfilamiento de clusters en la escala original del negocio).
    df.to_csv(DATOS / "base_limpia_para_perfilamiento.csv", index=False)


if __name__ == "__main__":
    main()
