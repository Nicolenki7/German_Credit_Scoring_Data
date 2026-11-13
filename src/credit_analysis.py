"""German Credit: riesgo de impago, segmentos y drivers del modelo.

Fuente: Statlog German Credit (UCI), 1.000 solicitudes, versión limpia del repo.
Ejecuta `python src/credit_analysis.py` y regenera outputs/ y docs/img/.
"""
import pathlib
import sqlite3
import sys

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from svg_chart import AZUL, ROJO, barras

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "german_credit_cleaned.csv"
IMG, OUT = ROOT / "docs" / "img", ROOT / "outputs"
IMG.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)
print(f"1. cargado: {df.shape[0]} filas x {df.shape[1]} columnas")
print("   target:", df["target"].value_counts().to_dict())

# target viene como texto ('good'/'bad'); 1 = buen crédito
df["target"] = (df["target"].astype(str).str.lower() == "good").astype(int)
malo = 1 - df["target"].mean()
print(f"2. tasa de impago: {malo:.1%} ({int((df['target'] == 0).sum())} de {len(df)})")

# ---------- feature engineering en SQL ----------
conn = sqlite3.connect(":memory:")
df.to_sql("credit_data", conn, index=False, if_exists="replace")
sql = """
SELECT *,
  CAST(loan_amt AS REAL) / duration AS Debt_to_Duration_Ratio,
  CASE WHEN age < 25 THEN 'Joven (<25)'
       WHEN age < 45 THEN 'Adulto (25-44)'
       ELSE 'Senior (45+)' END AS Tramo_Edad,
  CASE WHEN duration <= 12 THEN 'Corto (<=12m)'
       WHEN duration <= 36 THEN 'Medio (13-36m)'
       ELSE 'Largo (>36m)' END AS Tramo_Plazo
FROM credit_data;
"""
d = pd.read_sql_query(sql, conn)
conn.close()
print(f"3. SQL: +3 columnas -> {d.shape[1]}")

# ---------- gráficos ----------
ETIQUETA_CUENTA = {"below_0": "sin fondo / <0 DM", "below_200": "0-200 DM",
                  "above:200": ">200 DM", "no_cheking_acc": "sin cuenta"}
riesgo_cuenta = 1 - d.groupby("checking_acc_status")["target"].mean()
orden = ["below_0", "below_200", "above:200", "no_cheking_acc"]
riesgo_cuenta = riesgo_cuenta.reindex([c for c in orden if c in riesgo_cuenta.index])
barras(
    [(ETIQUETA_CUENTA[c], v, ROJO if v > malo else AZUL) for c, v in riesgo_cuenta.items()],
    "Sin cuenta o en números rojos: el doble de riesgo",
    IMG / "credit-cuenta.svg",
    subtitulo=f"Tasa de impago por cuenta corriente · media {malo:.1%}",
    formato="{:.1%}")

riesgo_plazo = 1 - d.groupby("Tramo_Plazo")["target"].mean()
riesgo_plazo = riesgo_plazo.reindex(["Corto (<=12m)", "Medio (13-36m)", "Largo (>36m)"])
barras(
    [(c, v, ROJO if v > malo else AZUL) for c, v in riesgo_plazo.items()],
    "Los plazos largos concentran el impago",
    IMG / "credit-plazo.svg",
    subtitulo=f"Tasa de impago por duración del préstamo · media {malo:.1%}",
    formato="{:.1%}")

# ---------- modelo ----------
X = d.drop(columns=["target", "Tramo_Edad", "Tramo_Plazo"])
y = d["target"]
cat = X.select_dtypes(exclude="number").columns.tolist()
X = pd.get_dummies(X, columns=cat, drop_first=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=.25, random_state=42, stratify=y)

# Las numéricas van estandarizadas: sin escalar, el solver no converge y los
# signos de los coeficientes dejan de tener sentido.
numericas = X.select_dtypes(include="number").columns.tolist()
modelo = Pipeline([
    ("pre", ColumnTransformer([("num", StandardScaler(), numericas)],
                              remainder="passthrough")),
    ("lr", LogisticRegression(max_iter=5000, class_weight="balanced")),
])
modelo.fit(X_tr, y_tr)
prob = modelo.predict_proba(X_te)[:, 1]
auc = roc_auc_score(y_te, prob)
acc = accuracy_score(y_te, prob > .5)
print(f"4. modelo: AUC {auc:.3f} · accuracy {acc:.3f} · train {len(X_tr)} / test {len(X_te)}")

coefs = pd.DataFrame({"feature": X.columns, "coef": modelo.named_steps["lr"].coef_[0]})
coefs["odds_ratio"] = np.exp(coefs["coef"])
coefs = coefs.reindex(coefs["coef"].abs().sort_values(ascending=False).index)
coefs.to_csv(OUT / "credit_feature_importance.csv", index=False)
top = coefs.head(8)[::-1]
print("\nTOP 8:")
print(top.iloc[::-1].to_string(index=False))

barras(
    [(f.replace("_", " ")[:34], c, ROJO if c < 0 else AZUL) for f, c in
     zip(top["feature"], top["coef"])],
    "Qué separa un buen crédito de un impago",
    IMG / "credit-drivers.svg",
    subtitulo="coeficiente logístico sobre P(buen crédito) · rojo = más riesgo",
    formato="{:+.2f}")

d.to_csv(OUT / "german_credit_scored.csv", index=False)
print("\ncuenta corriente:")
print((1 - d.groupby("checking_acc_status")["target"].mean()).round(3).to_string())
print("\ntramo de plazo:")
print((1 - d.groupby("Tramo_Plazo")["target"].mean()).round(3).to_string())
print("\nreporte (0 = impago):")
print(classification_report(y_te, modelo.predict(X_te),
                           target_names=["impago", "bueno"], digits=2))
print("préstamo mediano:", round(df["loan_amt"].median(), 0),
      "· plazo medio:", round(df["duration"].mean(), 1), "meses")
print("\npeores propósitos (tasa de impago):")
print((1 - d.groupby("purpose")["target"].mean()).sort_values(ascending=False).head(4).round(3).to_string())
print("\ntramo de edad:")
print((1 - d.groupby("Tramo_Edad")["target"].mean()).round(3).to_string())
