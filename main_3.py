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
def long_term_delinquency_count(dpd_12m: int, dpd_24m: int) -> int:
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
        return "Reject", "Very High Risk due to chronic delinquency"
    elif long_term_delinquency >= 3:
        return "High Risk", "Repeated delinquency behaviour detected"
    elif long_term_delinquency >= 1:
        return "Medium Risk", "Occasional delinquency observed"
    else:
        return "Low Risk", "Clean repayment behaviour"

# ==================================================
# 🏠 HOME
# ==================================================
if page == "🏠 Home":
    st.markdown(
        """
        <h1 style="text-align:center;">Bad Debt Prediction</h1>
        <p style="text-align:center; color:grey;">
        Machine Learning + Business Rule Engine Credit System
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    ### About the Project
    This application predicts **Bad Debt Risk** using **credit bureau data**
    combined with a **Business Rule Engine (BRE)** for explainable decisions.

    **Key Features**
    - Bureau-aligned credit behaviour metrics
    - Long-term delinquency feature engineering
    - ML probability + rule-based interpretation
    - Policy-aligned, explainable output
    """)

# ==================================================
# 🧮 CALCULATIONS
# ==================================================
elif page == "🧮 Calculations":
    st.markdown("## Calculation Logic")

    st.markdown("""
    ### Long-Term / Repeated Delinquency Count

    ```
    Long_Term_Delinquency =
    30+ DPD (24 Months)
    + max(0, 30+ DPD (12 Months) - 1)
    ```

    **Logic**
    - 24M captures historical behaviour
    - 12M captures recent stress
    - Prevents double counting
    - Penalizes repeated delinquency
    """)

    st.markdown(
        "<a href='#input_section'>👉 Go to Input Values</a>",
        unsafe_allow_html=True
    )

# ==================================================
# ⚙️ BUSINESS RULE ENGINE
# ==================================================
elif page == "⚙️ Business Rule Engine":
    st.markdown("## Business Rule Engine (BRE)")

    st.markdown("""
    ### Delinquency Rules
    ```text
    IF Long-Term Delinquency ≥ 5 → Reject
    IF Long-Term Delinquency 3–4 → High Risk
    IF Long-Term Delinquency 1–2 → Medium Risk
    IF Long-Term Delinquency = 0 → Low Risk
    ```
    """)

    st.markdown("""
    ### Credit Score Rules
    ```text
    ≤ 500 → Very High Risk
    501–607 → High Risk
    608–715 → Medium Risk
    > 715 → Low Risk
    ```
    """)

# ==================================================
# INPUT SECTION
# ==================================================
st.markdown("<a id='input_section'></a>", unsafe_allow_html=True)

st.info(
    "All inputs follow credit bureau logic. "
    "Derived metrics are calculated automatically."
)

st.markdown("### Credit Behaviour Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    SCORE_CR22 = st.number_input("Credit Score (0–1200)", -300, 1200, 650)
    DEROGATORIES = st.number_input("Derogatory Records", 0, value=0)
    Late_Payment_30DPD_Last_12M = st.number_input("Late Payments (30+ DPD) – 12M", 0, value=0)

with col2:
    Credit_Card_Payment_Failure_Count = st.number_input("Credit Card Payment Failures", 0, value=0)
    Recent_Payment_Irregularity_Flag = st.number_input("Recent Payment Irregularity (Months)", 0, 25, 0)
    Late_Payment_30DPD_Last_24M = st.number_input("Late Payments (30+ DPD) – 24M", 0, value=0)

with col3:
    CREDIT_CARD_CR22 = st.number_input("Active Credit Cards", 0, value=1)
    DEFAULT_CNT_CR22 = st.number_input("Total Historical Defaults", 0, value=0)
    DEFAULT_OPEN_CNT_CR22 = st.number_input("Open Defaults", 0, value=0)

Long_Term_Payment_Delinquency_Count = long_term_delinquency_count(
    Late_Payment_30DPD_Last_12M,
    Late_Payment_30DPD_Last_24M
)

st.metric(
    "Long-Term / Repeated Delinquency Count",
    Long_Term_Payment_Delinquency_Count
)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
st.markdown("---")
if st.button("Predict Credit Risk", use_container_width=True):

    user_input = {
        "SCORE_CR22": SCORE_CR22,
        "DEROGATORIES": DEROGATORIES,
        "Late_Payment_30DPD_Last_12M": Late_Payment_30DPD_Last_12M,
        "Late_Payment_30DPD_Last_24M": Late_Payment_30DPD_Last_24M,
        "Long_Term_Payment_Delinquency_Count": Long_Term_Payment_Delinquency_Count,
        "Credit_Card_Payment_Failure_Count": Credit_Card_Payment_Failure_Count,
        "Recent_Payment_Irregularity_Flag": Recent_Payment_Irregularity_Flag,
        "CREDIT_CARD_CR22": CREDIT_CARD_CR22,
        "DEFAULT_CNT_CR22": DEFAULT_CNT_CR22,
        "DEFAULT_OPEN_CNT_CR22": DEFAULT_OPEN_CNT_CR22
    }

    prob_bad, decision = predict_risk(user_input)
    band = cr22_risk_band(SCORE_CR22)

    delinq_band, delinq_reason = delinquency_interpretation(
        Long_Term_Payment_Delinquency_Count
    )

    st.markdown("## Prediction Outcome")

    if decision.lower() == "bad":
        st.error(f"ML Decision: {decision}")
    else:
        st.success(f"ML Decision: {decision}")

    st.markdown(
        f"""
        **Credit Score Risk Band:** {band}  
        **Probability of Default (ML):** {prob_bad:.2%}
        """
    )

    st.markdown("### Rule-Based Interpretation")

    st.markdown(
        f"""
        **Delinquency Risk Level:** {delinq_band}  
        **Interpretation:** {delinq_reason}
        """
    )

    if delinq_band == "Reject":
        st.error("Final Rule Decision: ❌ Reject (Delinquency Rule Triggered)")
    elif delinq_band == "High Risk":
        st.warning("Final Rule Decision: ⚠️ High Risk Applicant")
    else:
        st.success("Final Rule Decision: ✅ Acceptable Risk")
