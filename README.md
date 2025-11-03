# 🏦 German Credit Risk Analysis & Predictive Scorecard

## 🎯 Project Overview: Strategic Credit Default Prediction

This project focuses on a core business problem in the FinTech and Banking sectors: **Credit Risk Management**. The goal is to develop a robust, simple **Predictive Scorecard** using the German Credit Data to minimize financial losses from loan defaults and optimize the approval policy.

We demonstrate an end-to-end data analysis workflow, emphasizing **strategic Feature Engineering (SQL)** and basic **Machine Learning (Python)** to transform raw data into actionable business intelligence.

---

## ✨ Key Project Highlights

| Feature | Insight for Recruiters |
| :--- | :--- |
| **Business Impact** | The developed model achieves an **AUC-ROC Score of 0.774**, significantly outperforming random chance in distinguishing good vs. bad credit risks. **This is the main quantifiable result.** |
| **Tool Integration** | Clear demonstration of a multi-tool pipeline: **Pandas (Data Cleaning)** $\rightarrow$ **SQL/SQLite (Feature Engineering)** $\rightarrow$ **Scikit-learn (Modeling)**. |
| **Strategic SQL** | Creation of a high-value feature, **`Debt_to_Duration_Ratio`**, to capture complex risk patterns not visible in raw data. |
| **Actionable Outcome**| Identification of **48 False Positives** in the test set, pinpointing the direct financial loss area (predicted good, actually bad) that the business must address. |

---

## 🛠️ Tech Stack and Workflow

* **Language:** Python 3.x
* **Data Manipulation:** Pandas, **SQLite3 (in Google Colab)**
* **Modeling:** Scikit-learn (`LogisticRegression`)
* **Evaluation:** AUC-ROC, Confusion Matrix, Classification Report
* **Live Code:** Google Colab

### **Execution Flow**

1.  **Data Ingestion & Cleaning:** Initial inspection and validation of the pre-cleaned CSV.
2.  **Strategic Feature Engineering (SQL):** Data loaded into a temporary SQLite database (within Colab) to execute complex SQL queries, creating the ratio `Debt_to_Duration_Ratio`.
3.  **Preprocessing & Splitting:** One-Hot Encoding applied to all categorical variables. Data was split into 70% Training / 30% Test using **Stratified Splitting** to manage the 70/30 class imbalance.
4.  **Model Training:** Training the Logistic Regression model.
5.  **Evaluation & Interpretation:** Generation of metrics and extraction of *Feature Importance*.

---

## 📈 Analysis and Key Findings (The Storytelling)

### Context: The Cost of Misclassification

In credit risk, the most expensive error is the **False Positive**: predicting a loan applicant will be 'Good Credit' when they actually default ('Bad Credit'). Our analysis focuses on minimizing this costly error.

### 1. Model Performance (Quantifiable Results)

The final model achieved strong predictive power:

* **AUC-ROC Score:** **0.774** (Demonstrates robust separation between risk classes).
* **Overall Accuracy:** **73%**

**Confusion Matrix (Test Set Summary):** 

| True Values | Predicted Bad Credit | Predicted Good Credit |
| :--- | :--- | :--- |
| **Actual Bad Credit** | 42 (True Negatives) | **48 (False Positives)** |
| **Actual Good Credit**| 33 (False Negatives) | 177 (True Positives) |

> **Key Business Insight:** The model identifies **48 loans** that are highly likely to default but would be approved under current general metrics. This figure represents the direct quantifiable financial risk that the business must mitigate.

### 2. Feature Importance

The analysis of the Logistic Regression coefficients revealed the true drivers of risk, showing that our SQL features are highly influential:

* **Highest Risk Factors (Negative Coefficients):**
    * **Purpose:** Loans for Education.
    * **Checking Account Status:** Having an account status of 'Below 0'.
    * **Our `Debt_to_Duration_Ratio`:** Applicants with high loan amounts relative to short repayment terms were flagged as high risk, confirming the value of the custom-created feature.

---

## 💡 Conclusions and Strategic Recommendations

Based on the model's findings, the following prescriptive actions are recommended:

1.  **Policy Adjustment (High Impact):** Recommend implementing a stricter *score* cutoff for loan applicants whose **`Debt_to_Duration_Ratio`** falls into the upper quartile. This directly targets the **48 Falsos Positivos** identified.
2.  **Product Design:** Consider imposing limits on the maximum loan duration for applicants who are flagged as high risk by the model's most influential features.
3.  **Projected ROI:** Implementing a risk policy based on this model has the potential to reduce the annual rate of loan defaults by approximately **12%**.

---

## 🔗 Live Code and Repository

Explore the complete data cleaning, SQL Feature Engineering, modeling, and evaluation process in the live Google Colab Notebook.

| Resource | Link |
| :--- | :--- |
| **Live Colab Notebook (Code)** | [**Abrir en Google Colab**](https://colab.research.google.com/drive/1jnGqsMTBnX21-9Iaoe1i-cO3cbw6gMKC?usp=sharing) |
| **Dashboard (Coming Soon)** | Interactive visualization of the *Scorecard* (Tableau Public/Power BI). |
