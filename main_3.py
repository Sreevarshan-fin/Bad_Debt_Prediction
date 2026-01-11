import streamlit as st
from prediction_helper import predict_risk

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Bad Debt Prediction",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Section",
    ["🏠 Home", "🧮 Calculations", "⚙️ Business Rule Engine"]
)

# --------------------------------------------------
# STYLE OVERRIDES
# --------------------------------------------------
st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 600;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #555555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# BUSINESS LOGIC
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

def delinquency_interpretation(long_term_delinquency):
    if long_term_delinquency >= 5:
        return "Reject", "Chronic delinquency detected"
    elif long_term_delinquency >= 3:
        return "High Risk", "Repeated delinquency behaviour"
    elif long_term_delinquency >= 1:
        return "Medium Risk", "Occasional delinquency"
    else:
        return "Low Risk", "Clean repayment behaviour"

# ==================================================
# 🏠 HOME — ABOUT (NO INPUTS)
# ==================================================
if page == "🏠 Home":

    st.markdown(
        """
        <h1 style="text-align:center;">Bad Debt Prediction System</h1>
        <p style="text-align:center; color:grey;">
        Machine Learning + Business Rule Engine
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    ### About This Project
    This application simulates a **real-world credit risk decision system**
    used by banks and financial institutions to identify **bad debt risk**.

    The system combines:
    - Credit bureau features
    - Derived delinquency metrics
    - Machine learning probability models
    - Business Rule Engine (BRE)

    ### About Me
    **Sree Varshan**  
    Aspiring Data Scientist & Credit Risk Analyst  
    Focused on **ML-driven financial risk systems** with explainability.
    """)

# ==================================================
# 🧮 CALCULATIONS — INPUTS + PREDICTION
# ==================================================
elif page == "🧮 Calculations":

    st.markdown("## Credit Behaviour Inputs")

    col1, col2, col3 = st.columns(3)

    with col1:
        SCORE_CR22 = st.number_input("Credit Score (0–1200)", -300, 1200, 650)
        DEROGATORIES = st.number_input("Derogatory Records", 0, value=0)
        Late_12M = st.number_input("Late Payments (30+ DPD) – 12M", 0, value=0)

    with col2:
        CC_Failures = st.number_input("Credit Card Payment Failures", 0, value=0)
        Recent_Irregularity = st.number_input("Recent Payment Irregularity (Months)", 0, 25, 0)
        Late_24M = st.number_input("Late Payments (30+ DPD) – 24M", 0, value=0)

    with col3:
        Active_CC = st.number_input("Active Credit Cards", 0, value=1)
        Total_Defaults = st.number_input("Total Historical Defaults", 0, value=0)
        Open_Defaults = st.number_input("Open Defaults", 0, value=0)

    # Derived Metric
    LTD = long_term_delinquency_count(Late_12M, Late_24M)

    st.metric("Long-Term / Repeated Delinquency Count", LTD)

    # Prediction
    st.markdown("---")
    if st.button("Predict Credit Risk", use_container_width=True):

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
        delinq_band, delinq_reason = delinquency_interpretation(LTD)

        st.markdown("## Prediction Result")

        st.write(f"**ML Decision:** {decision}")
        st.write(f"**Credit Score Band:** {band}")
        st.write(f"**Probability of Default:** {prob_bad:.2%}")

        st.markdown("### Rule-Based Interpretation")
        st.write(f"**Delinquency Level:** {delinq_band}")
        st.write(f"**Reason:** {delinq_reason}")

# ==================================================
# ⚙️ BUSINESS RULE ENGINE — LOGIC ONLY
# ==================================================
elif page == "⚙️ Business Rule Engine":

    st.markdown("## Business Rule Engine (BRE)")

    st.markdown("""
    ### Delinquency Rules
    ```text
    Long-Term Delinquency ≥ 5  → Reject
    Long-Term Delinquency 3–4  → High Risk
    Long-Term Delinquency 1–2  → Medium Risk
    Long-Term Delinquency = 0  → Low Risk
    ```
    """)

    st.markdown("""
    ### Credit Score Rules
    ```text
    ≤ 500      → Very High Risk
    501–607    → High Risk
    608–715    → Medium Risk
    > 715      → Low Risk
    ```
    """)

    st.markdown("""
    ### Why BRE Exists
    - Overrides extreme ML predictions
    - Improves recall for bad debt
    - Ensures regulatory explainability
    - Aligns decisions with credit policy
    """)
