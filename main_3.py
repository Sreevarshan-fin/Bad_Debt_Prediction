import streamlit as st
from prediction_helper import predict_risk

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Bad Debt Prediction Centre",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# STYLE
# --------------------------------------------------
st.markdown(
    """
    <style>
    .center-title { text-align: center; }
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <h1 class="center-title">📊 Bad Debt Prediction Centre</h1>
    <h4 class="center-title" style="color: grey;">
    Machine Learning Project
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------
st.markdown("""
### 🔍 About This Project
This project simulates a **real-world credit risk decision system**
used by financial institutions to identify **bad debt risk** using
credit bureau behaviour and repayment history.

The system applies **machine learning with credit policy logic**
to produce **clear, explainable credit decisions**.

**Developed by:**  
**Sree Varshan**
""")

st.markdown("---")

# --------------------------------------------------
# BUSINESS LOGIC
# --------------------------------------------------
def long_term_delinquency_count(dpd_12m, dpd_24m):
    return dpd_24m + max(0, dpd_12m - 1)

def cr22_risk_band(score):
    if score <= 500:
        return "Very High"
    elif score <= 607:
        return "High"
    elif score <= 715:
        return "Medium"
    else:
        return "Low"

def delinquency_risk_score(ltd):
    if ltd >= 5:
        return "High"
    elif ltd >= 3:
        return "Medium"
    elif ltd >= 1:
        return "Low"
    else:
        return "Clean"

# --------------------------------------------------
# INPUT SECTION (CREDIT BUREAU ONLY)
# --------------------------------------------------
st.markdown("## 🧮 Credit Bureau Inputs")

c1, c2, c3 = st.columns(3)

with c1:
    SCORE_CR22 = st.number_input("Credit Score", -300, 1200, 650)
    DEROGATORIES = st.number_input("Derogatory Records", 0, value=0)
    Late_12M = st.number_input("30+ DPD (Last 12 Months)", 0, value=0)

with c2:
    Late_24M = st.number_input("30+ DPD (Last 24 Months)", 0, value=0)
    CC_Failures = st.number_input("Credit Card Payment Failures", 0, value=0)
    Recent_Irregularity = st.number_input("Recent Payment Irregularity (Months)", 0, 24, 0)

with c3:
    Active_CC = st.number_input("Active Credit Cards", 0, value=1)
    Total_Defaults = st.number_input("Total Historical Defaults", 0, value=0)
    Open_Defaults = st.number_input("Open Defaults", 0, value=0)

# --------------------------------------------------
# DERIVED DELINQUENCY
# --------------------------------------------------
LTD = long_term_delinquency_count(Late_12M, Late_24M)
delinq_score = delinquency_risk_score(LTD)

st.metric("Delinquency-Based Risk Score", delinq_score)

st.markdown("---")

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
if st.button("🔍 Evaluate Credit Risk", use_container_width=True):

    user_input = {
        "SCORE_CR22": SCORE_CR22,
        "DEROGATORIES": DEROGATORIES,
        "Late_Payment_30DPD_Last_12M": Late_12M,
        "Late_Payment_30DPD_Last_24M": Late_24M,
        "Long_Term_Payment_Delinquency_Count": LTD,
        "Credit_Card_Payment_Failure_Count": CC_Failures,
        "Recent_Payment_Irregularity_Flag": Recent_Irregularity,
        "CREDIT_CARD_CR22": Active_CC,
        "DEFAULT_CNT_CR22": Total_Defaults,
        "DEFAULT_OPEN_CNT_CR22": Open_Defaults
    }

    _, decision = predict_risk(user_input)
    band = cr22_risk_band(SCORE_CR22)

    # Convert decision to Good / Bad
    credit_outcome = "Bad" if decision in ["Reject", "High Risk"] else "Good"

    st.markdown("## 📈 Credit Decision Summary")

    r1, r2, r3 = st.columns(3)
    r1.metric("Credit Outcome", credit_outcome)
    r2.metric("Credit Risk Band", band)
    r3.metric("Delinquency Risk", delinq_score)



