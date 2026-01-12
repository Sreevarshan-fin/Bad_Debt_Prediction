

# Bad Debt Prediction System 

**[![Open in Streamlit](https://img.shields.io/badge/Launch%20App-Streamlit-%23FF4B4B?logo=streamlit&logoColor=white&style=for-the-badge&labelColor=FF4B4B)](https://baddebtprediction-5hh99e6ezkuwsp5wlrbchd.streamlit.app/)**


## The Problem

In credit-based businesses, customers are allowed to buy now and pay later. While this helps grow sales, it also creates risk. Some customers repay on time, but others delay payments or default completely. When these unpaid amounts cannot be recovered, they turn into **bad debt**, directly impacting revenue and cash flow.

Although businesses collect large amounts of customer, repayment, and credit bureau data, credit decisions are often made without a clear understanding of default risk. As a result, risky customers get approved, leading to avoidable financial losses.

This project was built to answer one simple question:
**Can we identify risky customers before approving credit?**

---

## How I Approached the Problem

I approached this problem from a **business loss perspective**, not just a modeling perspective. In real credit portfolios, bad customers form only a small portion of the population. Because of this, accuracy alone can be misleading.

For example, if most customers repay on time, a model that predicts everyone as “Good” would still show high accuracy — but it would completely fail to prevent defaults.

To understand the real impact, consider a business facing a potential loss of **₹1 million** due to bad loans. If a model can identify even **50–60% of risky customers in advance**, the business can take preventive actions such as rejection, manual review, or stricter credit terms. This can reduce losses to around **₹0.5 million**, clearly showing why **capturing risk matters more than achieving perfect accuracy**.

Based on this understanding:

* I focused on **early risk identification and ranking**, not just predictions
* Noisy and unreliable features were removed
* Stable predictors were selected using **WoE and IV**, following credit risk best practices
* Models were tuned to **prioritize recall for bad customers**

Instead of using the model as a hard approve/reject system, predictions were combined with a **Business Rule Engine**, ensuring final decisions followed credit policy and remained explainable.

---
##	**Project Architecture**

<img width="1000" height="800" alt="image" src="https://github.com/user-attachments/assets/bc0048b9-121d-4514-b7dd-e959354fabf2" />




---
## What the Project Aimed to Achieve

* Understand what truly separates **good** and **bad** customers
* Predict customer risk **before credit approval**
* Focus on **risk capture over raw accuracy**
* Deliver decisions that are **business-friendly and explainable**
* Support model output with a **Business Rule Engine (BRE)**

---

## The Data Behind the Model

* Around **91,000 customer records**
* **99 features** covering customer profile, repayment behavior, and credit bureau data
* Data from multiple sources merged using **Customer ID** into a single master table

---

## Defining Good vs Bad Customers

* **Good (0):** Customers who paid on time with no defaults
* **Bad (1):** Customers who defaulted or had severe payment delays

Only about **8% of customers were bad**, making this a highly imbalanced problem. This reinforced the need to focus on **recall and ranking metrics** rather than accuracy.

---

## Key Data Decisions

During data understanding and cleaning:

* Poor-quality CR21 credit features were dropped
* Cleaner and more reliable CR22 features were retained
* Redundant and highly correlated variables were removed
* **WoE and IV** were used to retain only meaningful predictors

---

## Feature Engineering Highlights

* Address stability buckets to capture residential consistency
* Life instability flag combining address and employment tenure
* Feature selection based on **IV > 0.04** to ensure stability and interpretability

---

## Modeling Strategy

I tested multiple models:

* Logistic Regression
* Random Forest
* XGBoost
* CatBoost

To handle class imbalance:

* Under-sampling
* SMOTE–Tomek oversampling

The goal was not to maximize recall blindly, but to find a **balanced and deployable solution**.

---

## Final Model Choice

**Random Forest with SMOTE–Tomek oversampling** was selected because it provided the best trade-off between risk detection and business stability.

**Key results:**

* Recall (Bad): ~61%
* Accuracy: ~72%
* ROC–AUC: ~0.74
* Stable performance across training and test data

This model identified a meaningful share of risky customers without rejecting too many good ones.

---

## How Model Performance Was Judged

Instead of focusing only on accuracy, performance was evaluated using **business-relevant metrics**:

* **ROC–AUC:** ~0.74
* **KS Statistic:** ~34
* **Gini Coefficient:** ~0.48

Risk increased consistently across deciles, confirming strong **rank ordering** and clear separation between low-risk and high-risk customers.

---

## What Drives Risk the Most

The strongest risk drivers included:

* Credit score (most important factor)
* Recent payment irregularities
* Bureau derogatories and defaults
* Long-term delinquency history
* Credit card stress indicators
* Residential stability

---

## How the Model Is Used in Practice

* The model predicts **Good / Bad**
* This output is passed through a **Business Rule Engine**
* Final decisions are tagged as:

  * Low Risk
  * Medium Risk
  * High Risk
  * Reject

This adds a **business safety layer** and ensures decisions are explainable and policy-aligned.

---

## Business Impact

* Risky customers are identified **before losses occur**
* Credit approvals become **risk-based**, not rule-only
* Bad debt is reduced without hurting good customer approvals
* The solution is suitable for **real-world credit decision systems**

---

## Challenges Faced

* Severe class imbalance
* Improving recall without over-rejecting good customers
* Cleaning noisy credit bureau data
* Focusing on ranking metrics instead of accuracy
* Translating model output into business rules

---

## Declaration

This project is my original work, developed for learning and demonstration purposes using publicly available resources.

---


