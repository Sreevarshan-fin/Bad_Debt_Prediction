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
    .center-title {
        text-align: center;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
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
# ABOUT SECTION
# --------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    ### 🔍 About This Project
    This project simulates a **real-world credit risk decision system**
    used by banks and financial institutions to predict **bad debt risk**.

    It combines **machine learning–based default probability**
    with **internal risk logic** to deliver **accurate and explainable
    credit decisions**.
    """)

with c2:
    st.markdown("""
    ### 👤 About Me
    **Sree Varshan**  
    Aspiring **Data Scientist & Credit Risk Analyst**  
    Focused on **ML-driven credit risk and decisioning systems**
    """)

st.markdown("---")

# --------------------------------------------------
# BUSINESS LOGIC (INTERNAL)
# --------------------------------------------------
def long_term_delinquency_count(dpd_12m, dpd_24m):
    return dpd_24m + max(0, dpd_12m - 1)

def cr22_risk_band(score):
    if score <= 500:
        return "Very High Risk"
    elif score <= 607:
        return "High Risk"
    elif score <= 715:
        return "Medium Risk"
    else:
        return "Low Risk"

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------
st.markdown("## 🧮 Credit Risk Assessment")

col1, col2, col3 = st.columns(3)

with col1:
    SCORE_CR22 = st.number_input("Credit Score", -300, 1200, 650)
    Late_12M = st.number_input("Late Payments (30+ DPD) – 12M", 0, value=0)
    DEROGATORIES = st.number_input("Derogatory Records", 0, value=0)

with col2:
    Late_24M = st.number_input("Late Payments (30+ DPD) – 24M", 0, value=0)
    CC_Failures = st.number_input("Credit Card Payment Failures", 0, value=0)
    Recent_Irregularity = st.number_input("Recent Payment Irregularity (Months)", 0, 25, 0)

with col3:
    Active_CC = st.number_input("Active Credit Cards", 0, value=1)
    Total_Defaults = st.number_input("Total Defaults", 0, value=0)
    Open_Defaults = st.number_input("Open Defaults", 0, value=0)

# Derived Feature
LTD = long_term_delinquency_count(Late_12M, Late_24M)
st.metric("Long-Term Delinquency Count", LTD)

st.markdown("---")

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
if st.button("🔍 Predict Credit Risk", use_container_width=True):

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

    prob_bad, decision = predict_risk(user_input)
    band = cr22_risk_band(SCORE_CR22)

    st.markdown("## 📈 Prediction Result")

    r1, r2, r3 = st.columns(3)

    r1.metric("Probability of Default", f"{prob_bad:.2%}")
    r2.metric("Credit Risk Band", band)
    r3.metric("Final Decision", decision)

    st.info("Business rules are applied internally to ensure policy-aligned decisions.")
