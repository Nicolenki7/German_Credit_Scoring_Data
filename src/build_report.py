"""Construye docs/report.html del scoring de crédito alemán.

Uso: python src/build_report.py
"""
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report import escribir, num

ROOT = pathlib.Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "german_credit_FINAL_FOR_BI.csv")
bien = "target_good"
PROP = {"purpose_car_new": "Coche nuevo", "purpose_car_used": "Coche usado",
        "purpose_radio_tv": "Radio y TV", "purpose_furniture_equipment": "Muebles",
        "purpose_domestic_applience": "Electrodomésticos", "purpose_repairs": "Reformas",
        "purpose_education": "Educación", "purpose_retraining": "Reciclaje",
        "purpose_business": "Negocio", "purpose_others": "Otros"}

filas = []
for col, etiqueta in PROP.items():
    if col in d:
        filas.append({"a": "todos", "g": "proposito", "k": etiqueta,
                      "v": round(100 * d.loc[d[col] == 1, bien].mean(), 1), "u": "%"})
for col, etiqueta in (("age_risk_category_B. Adulto (25-44)", "Adulto 25-44"),
                      ("age_risk_category_C. Senior (45+)", "Senior 45+")):
    if col in d:
        filas.append({"a": "todos", "g": "edad", "k": etiqueta,
                      "v": round(100 * d.loc[d[col] == 1, bien].mean(), 1), "u": "%"})
base = d[(d.get("age_risk_category_B. Adulto (25-44)") != 1) & (d.get("age_risk_category_C. Senior (45+)") != 1)]
if len(base):
    filas.append({"a": "todos", "g": "edad", "k": "Joven hasta 24", "v": round(100 * base[bien].mean(), 1), "u": "%"})
for col, etiqueta in (("duration_risk_category_Medio Plazo (13-36m)", "13-36 m"),
                      ("duration_risk_category_Largo Plazo (>36m)", "más de 36 m")):
    if col in d:
        filas.append({"a": "todos", "g": "plazo", "k": etiqueta,
                      "v": round(100 * d.loc[d[col] == 1, bien].mean(), 1), "u": "%"})

tabla = [[e, num(len(s), 0), f"{num(100 * s[bien].mean(), 1)} %", num(s.loan_amt.mean(), 0)]
         for e, s in ((e, d[d[c] == 1]) for c, e in PROP.items() if c in d)]
tabla.sort(key=lambda r: float(r[2].replace(" %", "").replace(",", ".")), reverse=True)

escribir(
    ROOT / "docs" / "report.html",
    eyebrow="Riesgo de crédito · German Credit",
    titulo="Crédito: para qué se pide y quién devuelve",
    pregunta=("Mil solicitudes de crédito con su resultado real. La pregunta del negocio no es "
              "«quién es buen pagador» en abstracto, sino en qué combinaciones de propósito, edad y "
              "plazo el riesgo se dispara, porque ahí se pone el límite o se pide garantía."),
    kpis=[("Solicitudes", num(len(d)), "con resultado conocido"),
          ("Buenos pagadores", f"{num(100 * d[bien].mean(), 1)} %", "target_good = 1"),
          ("Importe medio", f"{num(d.loan_amt.mean(), 0)} DM", "préstamo solicitado"),
          ("Edad media", f"{num(d.age.mean(), 0)} años", "del solicitante")],
    filtros=None,
    graficos=[
        {"id": "p", "grupo": "proposito", "titulo": "Buen pagador por propósito del crédito",
         "subtitulo": "% de solicitudes devueltas según para qué se pidió", "unidad": "%"},
        {"id": "e", "grupo": "edad", "titulo": "Buen pagador por tramo de edad",
         "subtitulo": "los tres tramos del dataset alemán", "unidad": "%"},
        {"id": "z", "grupo": "plazo", "titulo": "Buen pagador por plazo",
         "subtitulo": "a más plazo, más exposición", "unidad": "%"},
    ],
    filas=filas,
    tabla={"titulo": "Propósito, importe y resultado",
           "subtitulo": "ordenado por tasa de devolución",
           "cabeceras": ["Propósito", "Solicitudes", "Buen pagador", "Importe medio"],
           "filas": tabla},
    metodo=["Cada fila es una solicitud; target_good vale 1 si el crédito se devolvió.",
            "Los propósitos se leen de las columnas one-hot originales, no de una agrupación posterior.",
            "El tramo joven se deriva por exclusión: ni adulto (25-44) ni senior (45+).",
            "Se informa la tasa bruta por grupo; no hay modelo ni ajuste por otras variables."],
    limitaciones=["Mil casos son pocos: un grupo de 50 solicitudes mueve la tasa varios puntos con un caso más.",
                  "Es una tasa bruta, sin controlar confusores: el propósito y la edad están correlacionados.",
                  "El dataset es de 1994 y en marcos alemanes; no describe el crédito actual.",
                  "No hay importe recuperado ni pérdida: solo se sabe si devolvió o no."],
    fuente="german_credit_FINAL_FOR_BI.csv",
    metodo_sub="Una fila por solicitud; cada gráfico aísla una sola dimensión.",
    lim_sub="Qué no se puede concluir con mil solicitudes.")
print("docs/report.html:", (ROOT / "docs" / "report.html").stat().st_size, "bytes")
