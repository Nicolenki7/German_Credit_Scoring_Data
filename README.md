# 📊 Proyecto de Credit Scoring 360: Rendimiento del Modelo y Control de Falsos Positivos

Este repositorio documenta el proceso de *Credit Scoring* y la implementación de un dashboard ejecutivo de *Business Intelligence (BI)* para la toma de decisiones basada en el riesgo. El objetivo del proyecto es balancear el crecimiento (Tasa de Aprobación) con la minimización de errores de alto impacto financiero.

## Resumen Ejecutivo del Proyecto

El análisis se centró en la creación de un modelo predictivo robusto y en la cuantificación precisa del **Error de Mayor Costo**: el **Falso Positivo** (aprobar un cliente que resulta ser de Mal Crédito).

A través del dashboard ejecutivo, se logra:

1.  **Validar la Robustez del Modelo:** Demostrando la capacidad de separación de clases (AUC superior a 80%).
2.  **Cuantificar el Riesgo:** Aislamos y medimos el impacto de los **145 Falsos Positivos** a través de la Matriz de Confusión y formatos condicionales.
3.  **Justificar el Análisis de *Features*:** Se comprueba que la ingeniería de variables clave, como el ratio de endeudamiento, es un predictor fundamental del *default*.

## Abordaje y Robustez de la Solución

El proyecto abordó y corrigió activamente inconsistencias críticas en la fuente de datos (errores de tipo de dato y ambigüedad en la definición de métricas), garantizando que las métricas financieras clave sean precisas y confiables.

### 1. Cuantificación del Riesgo y Costo Financiero (Matriz de Confusión)

* **Enfoque:** La Matriz de Confusión fue etiquetada explícitamente y configurada para que la celda de **Falsos Positivos (145)** se destaque visualmente, aislando el error de máximo impacto financiero para la junta directiva.

### 2. Validación de la Capacidad Predictiva

* **Análisis:** El gráfico de Distribución del Score demuestra que el modelo agrupa consistentemente a los clientes de **Mal Crédito** en los *scores* bajos y a los de **Buen Crédito** en los *scores* altos, confirmando la robustez de la predicción.

### 3. Ingeniería y Validación de Variables

* **Validación Clave:** Se implementó el **Binning (Agrupación)** para la variable de ratio de endeudamiento (`Debt_Risk_Group`). El análisis demuestra que los clientes en el **Nivel 5 (Alto)** de endeudamiento tienen la **Tasa Default Real más alta**, justificando la inclusión de esta variable en el modelo.

## Herramientas y Enlaces del Proyecto

| Recurso | Enlace |
| :--- | :--- |
| **Dashboard Ejecutivo (Looker Studio)** | [https://lookerstudio.google.com/s/iw0qzisBiFk](https://lookerstudio.google.com/s/iw0qzisBiFk) |
| **Código y Scripts de Análisis (GitHub)** | [https://github.com/Nicolenki7/German-Credit-Data---Feature-Importance](https://github.com/Nicolenki7/German-Credit-Data---Feature-Importance) |

| Herramienta | Uso en el Proyecto |
| :--- | :--- |
| **Looker Studio** | Visualización ejecutiva y *storytelling* de datos. |
| **Python / Jupyter** | Preprocesamiento de datos y entrenamiento de modelo. |
| **GitHub** | Control de versiones y divulgación profesional. |

---
*Este proyecto es un testimonio de la capacidad de transformar modelos de Machine Learning en soluciones de Business Intelligence accionables.*
