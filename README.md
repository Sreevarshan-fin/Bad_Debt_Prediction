<p align="center">
  <img src="assets/title.png" alt="Bad Debt Prediction" width="100%">
</p>

<p align="center">
  <b>
    End-to-end machine learning system for predicting credit risk in BNPL environments.<br>
    Designed to identify high-risk borrowers and reduce bad debt exposure.<br>
    Enables data-driven, risk-aware lending decisions at scale.
  </b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white">
  <img src="https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white">
  <img src="https://img.shields.io/badge/AWS%20SageMaker-FF9900?style=flat-square&logo=amazonaws&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/WoE%20%2F%20IV-6A0DAD?style=flat-square">
  <img src="https://img.shields.io/badge/PSI%20%2F%20CSI-D32F2F?style=flat-square">
</p>

<hr>


---

## 🚀 Key Highlights

* Built an **end-to-end Bad Debt Prediction system** for BNPL lending to identify high-risk borrowers and enable **data-driven credit decisions**

* Achieved **60% recall**, detecting **3/5 defaulters before approval**, demonstrating a potential ~60% reduction in bad-debt exposure (₹1M → ₹0.4M) through model-driven decision simulation
  
* Designed a **risk-based decision framework (threshold ~0.3)** to minimize **high-cost errors (false negatives)**

* Applied **WoE–IV feature engineering** for **risk-aligned transformation and feature selection**, improving interpretability and maintaining performance across models

* Addressed **severe class imbalance** using **SMOTE–Tomek**, improving minority class detection while preserving data distribution

* Selected **Random Forest** for its optimal balance between **recall, stability, and generalisation**, avoiding overfitting

* Evaluated model performance using **KS (34%)**, **Gini (0.48)**, and **ROC-AUC**, ensuring strong separation of good vs bad customers

* Built a **model monitoring framework** using **PSI (0.39), CSI, and OOT validation** to detect data drift and ensure model stability

* Designed a **scalable ML pipeline** using **AWS SageMaker, FastAPI, Streamlit, and MLflow (EC2)** for real-time inference, experiment tracking, and lifecycle management.

  
-----------------

![Project Architecture](assets/projectworkflow.gif)

![Project Architecture](assets/bdp_1.png)

----

## 🔎 Problem Statement

Credit Business Operating **Buy Now, Pay Later (BNPL)** faces a trade-off between **revenue growth** and **credit risk**. Approving customers without **structured risk assessment** leads to **payment defaults**, causing **bad debts** and **financial losses**. This lack of **predictive evaluation** impacts **cash flow**, **profitability**, and **risk management**.

This project builds a **machine learning classification model** to label customers as **Good (0) / Bad (1)**, enabling **data-driven credit decisions**.

----

## 💹 Business Impact & Decision Framework

> This model improves credit approval by identifying high-risk customers early.It helps reduce bad debt by preventing risky approvals before they happen.The system prioritizes risk
> reduction over approval speed, accepting small operational costs to avoid large financial losses


####  🔸 Business Impact

* Achieved **60% recall**, identifying **3 out of 5 defaulters before approval**, improving early risk detection
* Reduced simulated bad-debt exposure from **₹1M → ₹0.4M (~60% reduction)** using model-driven decision policies


#### 🔸 Approach & Strategy

* **High Recall Focus:** Missing a defaulter (false negative) leads to **direct financial loss**, so the model prioritizes detecting risky applicants
* **ML over Rule-Based:** Traditional methods rely on limited variables, while ML leverages **multi-feature relationships** to capture complex risk patterns
* **Optimized threshold (~0.3)** based on recall–precision trade-off, prioritizing reduction of high-cost false negatives and improving detection of high-risk customers


#### 🔸 Risk & Cost Strategy 

* Allows a **controlled increase in false positives** (manual review effort)
* Strong focus on **reducing false negatives**, which have higher financial impact

| Error Type     | Business Impact                |
| -------------- | ------------------------------ |
| False Negative | High financial loss (critical) |
| False Positive | Lower cost (review / delay)    |

➡️ Focus is on **minimizing high-cost risk**, not just improving accuracy


#### 🔸 Decision Enablement

* **High-risk customers** → Reject or approve with stricter terms (higher interest, lower limits)
* **Low-risk customers** → Fast-track approvals with better offers, improving customer experience


#### 🔸 Model Performance & Reliability

* **Recall:** 60%
* **ROC-AUC:** 0.74
* **KS Score:** 34%
* **Gini:** 0.48
* **Overfitting:** Not observed

✔️ Strong ability to **separate good vs bad customers**
✔️ Metrics aligned with **credit risk standards**

#### 🔸 Monitoring & Stability 

* **PSI (0.39):** Customer behavior has shifted → risk of **wrong credit decisions**
* **CSI Stable:** Core risk drivers still valid → model logic remains usable

👉 **Impact:**
Without updates, the model may **approve risky customers or reject good ones**, leading to **higher losses or missed revenue**.
Requires **regular retraining and monitoring** to keep decisions accurate.





-----

## 📊 Data Overview

Real-world credit dataset (~100K customers, 99 features) collected under NDA, structured based on key risk dimensions:

* **Customer Behaviour**
* **Credit Behaviour**
* **Credit Bureau Data**

Includes credit bureau scores from two providers — **CR21** and **CR22** — enabling comparative analysis of their effectiveness in identifying high-risk customers.

⚠️ Dataset cannot be shared due to confidentiality constraints.

----

## ⚙️ Model Development & Validation

<details>
<summary><b>1. Data Preprocessing & EDA</b></summary>

Handled **missing values**, removed **duplicates**, and validated **financial variables** to ensure data consistency and reliability.
Performed **exploratory data analysis (EDA)** to analyse **repayment behaviour**, **delinquency trends**, and **outliers** using statistical plots and correlation analysis.

👉  **Insight:** **Credit score**, **repayment behaviour**, and **delinquency patterns** showed strong differentiation between **defaulters** and **non-defaulters**.

</details>

---

<details>
<summary><b>2. Feature Engineering</b></summary>


#### 🔸 CR21 vs CR22 Analysis

* Compared **CR21 and CR22**, two **credit bureau score providers**, using box plots to analyze **median separation, distribution spread, and outliers** across good vs bad customers
* **CR22 showed stronger class separation** with reduced overlap, making it a more reliable predictor of default risk

---

#### 🔸 WoE–IV Feature Engineering & Selection

* Applied **Weight of Evidence (WoE)** binning to transform variables into **monotonic, risk-aligned categories**, improving interpretability and ensuring a stable relationship with default probability

* Performed **feature selection using Information Value (IV)** to retain high-predictive variables:

  * **IV < 0.02** → Not predictive (excluded)
  * **0.02 – 0.1** → Weak
  * **0.1 – 0.3** → Medium
  * **> 0.3** → Strong

* Used **WoE–IV for feature selection** in a highly imbalanced dataset to identify variables with strong class separation

* Removed **highly correlated features** to reduce multicollinearity and improve **model robustness and generalisation**

---

👉 **Key Insight**

> The combination of **CR22 selection, WoE transformation, and IV-based filtering** produced **high-quality, risk-aligned features**, improving **interpretability, class separation, and overall model performance**.

</details>
  
---


<details>
<summary><b>3. Class Imbalance Handling</b></summary>


**To address severe class imbalance, two strategies were evaluated:**


🔹**Attempt 1: Under-Sampling**

Reduced the majority class to balance the dataset.

**Observations:**
- Loss of critical information due to removal of majority samples  
- Poor model generalisation, especially in precision  
- Overfitting observed across multiple models  
- ROC-AUC remained moderate (~0.74–0.84), but imbalance in precision-recall reduced reliability  

👉 **Conclusion:** Under-sampling failed to capture full data distribution and degraded performance.

---

🔹 **Attempt 2: SMOTE-Tomek**

Applied SMOTE for synthetic minority generation and Tomek Links for noise removal.

**Improvements:**
- Better class representation without information loss  
- Reduction in class overlap and noise  
- More consistent model performance  

**Model Comparison (Test Performance)**

| Model | Recall | Precision | AUC | Overfitting | Insight |
|------|--------|----------|-----|------------|--------|
| Logistic Regression | 0.91 | 0.09 | 0.69 | Yes | High recall but excessive false positives |
| CatBoost | 0.82 | 0.10 | 0.70 | Yes | Strong recall but unstable |
| XGBoost | 0.47 | 0.15 | 0.70 | No | Stable but lower detection |
| **Random Forest** | **0.61** | **0.16** | **0.74** | **No** | ✅ Best trade-off between detection and stability |


👉 **Final Choice:** SMOTE-Tomek retained as the optimal resampling strategy  

👉 **Decision Logic:** Prioritised a model that balances **risk detection (high recall)** with **stability and generalisation**, rather than maximising accuracy  

👉 **Insight:** Enabled reliable identification of **high-risk customers** while maintaining **robust and consistent model performance**

</details>

---

<details>
<summary><b>4. Model Selection</b></summary>

Evaluated multiple models to identify the most reliable performer on balanced data.

**Final Model:** Random Forest — selected for its consistent performance and ability to generalise well without overfitting.

👉 **Insight:** Ensemble tree-based models effectively capture complex, non-linear relationships, leading to stable predictions on unseen data.

</details>

---

<details>
<summary><b>5. Model Evaluation</b></summary>

Evaluated using key **credit risk metrics**:

* **ROC-AUC (0.74)** → Good class discrimination
* **Gini (0.48)** → Moderate predictive power
* **KS (34%)** → Strong separation
* **Recall (60%)** → Majority of defaulters identified

Maintained consistent performance across **train**, **test**, and **OOT datasets**.
Threshold tuning (e.g., **0.3**) used to prioritise **risk detection**.

Accuracy was not used as the primary metric due to class imbalance. Business risk is better captured through Recall, KS, and Gini.

**Precision is intentionally lower due to recall prioritization. In credit risk, false positives lead to additional manual review costs, whereas false negatives result in direct financial loss. The model is therefore optimized to minimize high-cost errors (false negatives).**

👉  **Insight:** Model is optimised for **high recall**, ensuring early detection of **risky customers**.

</details>

---

<details>
<summary><b>6. Performance Analysis</b></summary>

Focused on **classification errors** and **feature contribution**.
Special attention on **False Negatives**, as they represent the highest **financial risk**.
Used **feature importance** to identify key drivers of default.

👉 **Insight:** Strong **risk separation** and clear **driver identification** validate model reliability.

</details>

---

<details>
<summary><b>7. PSI & CSI Monitoring</b></summary>


Used **PSI** and **CSI** with **Out-of-Time (OOT) validation** to track data drift and ensure model stability.

* PSI (0.39) → Significant shift in data distribution
* CSI (Stable) → Feature importance remains consistent

Requires periodic retraining using recent data to maintain decision accuracy.

Currently, drift is monitored using **PSI and CSI with OOT validation**; future enhancements will extend this to **real-time production monitoring** using tools like **Evidently AI**.

👉  **Insight:** **High PSI indicates the model may degrade over time, requiring **continuous monitoring, periodic retraining, and threshold recalibration** to maintain reliable performance. **

</details>

---


## 🧰 Tech Stack

* **Programming & Libraries:** Python, Pandas, NumPy
* **Machine Learning:** Scikit-learn, XGBoost, CatBoost, Random Forest
* **Experiment Tracking & Deployment:** MLflow, AWS SageMaker, Streamlit
* **Monitoring & Risk Analytics:** PSI, CSI
* **Feature Engineering & Techniques:** WoE, Information Value (IV), SMOTE-Tomek, OOT Validation
* **Evaluation Techniques:** KS Statistic, Gini Coefficient, ROC-AUC, with prioritisation of Recall to ensure effective detection of high-risk customers

---------

## 🌩️ Deployment

### SageMaker Deployment (Design & Implementation)

Designed and validated a scalable deployment pipeline using AWS SageMaker for real-time inference.

* Uploaded trained model artifacts to Amazon S3
* Developed a custom inference script for prediction handling
* Configured and deployed a real-time SageMaker endpoint using the SDK
* Successfully tested end-to-end inference using the SageMaker runtime client

**Note:** Designed and validated a scalable deployment pipeline using AWS SageMaker; endpoint tested but not kept live due to cost constraints.

-------

### **Streamlit UI**


![UI](assets/streamlit_ui.png)

-----------



## ⚡ Challenges

- **Severe class imbalance** — bad customers were a tiny minority, requiring careful resampling strategy selection and metric prioritisation
- **Misleading accuracy** — shifted evaluation entirely toward recall, KS, and Gini to reflect true business risk
- **Feature selection complexity** — noisy, correlated, and leakage-prone variables addressed using WoE/IV filtering and stability checks
- **Recall vs precision trade-off** — SMOTE-Tomek improved bad customer detection but increased overfitting risk in some models, requiring careful validation

---

##  🚀 Future Improvements

* Implement automated retraining pipelines triggered by drift thresholds (PSI-based alerts)
  
  *(Currently, drift is monitored using **PSI and CSI with OOT validation**; future work will extend this to real-time production data.)*

* Implement **A/B testing** to compare multiple models in real-world scenarios and select the best-performing model based on **business metrics**

* Introduce a **dynamic decision threshold** based on **business risk appetite**, replacing a fixed cutoff

* Build a **feedback loop** using actual repayment/default outcomes to continuously improve model performance over time


---

## 🔬 Experiment Tracking & Model Registry (MLflow on AWS)


#### 🔹 MLflow Tracking Server (AWS EC2)
Deployed an MLflow Tracking Server on AWS EC2 to log experiments, parameters, metrics, and artifacts.


![MLflow EC2](assets/EC2_Instance.png)

---

#### 🔹 Experiment Run Tracking
Tracked multiple model runs with parameters and performance metrics, enabling reproducible comparison and model selection.

![Experiment Tracking](assets/Experimental_Tracking_Table_EC2.png)

![Model Comparison](assets/Comparision_2.png)

---

#### 🔹 Model Registry
Registered and versioned models using MLflow Model Registry for structured model management and version control.

![Model Registry](assets/Model_Register.png)


-------------------

**Author:** Sree Varshan  
**Open to ML engineering / Data Scientist/ Credit Risk Analyst opportunities**  

-----
