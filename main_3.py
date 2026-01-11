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

# ==================================================
# 🏠 HOME PAGE
# ==================================================
if page == "🏠 Home":
    st.markdown(
        """
        <h1 style="text-align:center;">Bad Debt Prediction</h1>
        <p style="text-align:center; color:grey;">
        A Business-Oriented Machine Learning Credit Risk System
        </p>
        """,
        unsafe_allow_html=True
    )

    st.image(
        "/mnt/data/1d370404-80f0-4f69-9d3a-6428084c043c.png",
        use_column_width=True
    )

    st.markdown("""
    ### About the Project
    This application predicts **Bad Debt Risk** using **credit bureau data**
    combined with a **Machine Learning + Business Rule Engine (BRE)** approach.

    **Key Highlights**
    - Bureau-aligned feature engineering
    - Derived delinquency metrics
    - Recall-focused ML model
    - Rule-based risk overrides
    - Explainable, policy-driven decisions

    **Author:** Sree Varshan
    """)

# ==================================================
# 🧮 CALCULATIONS PAGE
# ==================================================
elif page == "🧮 Calculations":
    st.markdown("## Calculation Logic")

    st.markdown("""
    ### Long-Term / Repeated Delinquency Count
    **Formula**
    ```
    Long_Term_Delinquency =
    30+ DPD (24 Months)
    + max(0, 30+ DPD (12 Months) - 1)
    ```

    **Why this works**
    - 24M captures historical behaviour
    - 12M captures recent stress
    - Prevents double counting
    - Penalizes repeated delinquency
    """)

    st.markdown("""
    ### Credit Score Risk Bands
    | Score Range | Risk Band |
    |------------|-----------|
    | ≤ 500 | Very High Risk |
    | 501 – 607 | High Risk |
    | 608 – 715 | Medium Risk |
    | > 715 | Low Risk |
    """)

    st.markdown(
        "<a href='#input_section'>👉 Go to Input Values</a>",
        unsafe_allow_html=True
    )

# ==================================================
# ⚙️ BUSINESS RULE ENGINE PAGE
# ==================================================
elif page == "⚙️ Business Rule Engine":
    st.markdown("## Business Rule Engine (BRE)")

    st.markdown("""
    ### Credit Score Rules
    ```text
    IF Credit Score ≤ 500 → Very High Risk
    IF Credit Score 501–607 → High Risk
    IF Credit Score 608–715 → Medium Risk
    IF Credit Score > 715 → Low Risk
    ```
    """)

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
    ### Default Override Rules
    ```text
    IF Open Defaults > 0 → Auto Reject
    IF Total Defaults ≥ 2 → Very High Risk
    ```
    """)

    st.markdown("""
    **Why BRE?**
    - Improves recall
    - Controls extreme predictions
    - Ensures policy compliance
    - Provides explainability
    """)

# ==================================================
# MAIN INPUT & PREDICTION SECTION (ALL PAGES)
# ==================================================
st.markdown("<a id='input_section'></a>", unsafe_allow_html=True)

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

st.markdown("### Applicant Profile")

col4, col5, col6 = st.columns(3)

with col4:
    RESIDENTIAL = st.selectbox("Residential Status", ["Owned", "Rented", "Living_With_Family", "Missing"])
    CD_OCCUPATION = st.selectbox("Occupation Type", ["employed", "self_employed", "student", "retired", "unemployed", "Missing"])

with col5:
    EMPLOYED_STATUS = st.selectbox("Employment Status", ["employed", "self_employed", "student", "retired", "unemployed", "benefits", "Missing"])
    APPLICANT_AGE = st.selectbox("Applicant Age Band", ["18-24", "25-29", "30-34", "35-44", "45-54", "54+"])

with col6:
    DOC_TYPE = st.selectbox("Document Type", ["AU Passport", "AU Driver Licence", "Australian Passport", "Intl Passport and Visa", "HAAU 18+ Card", "Missing"])
    BUREAU_DEFAULT = st.selectbox("Bureau Default Category", ["Missing", "1-1000", "1000+"])

st.markdown("### Internal Risk Segmentation")

SCORECARD = st.selectbox("Internal Scorecard", ["TAR1A", "SFJR1A", "HSHSOL", "CTSDP", "INSLV"])
BUREAU_ENQUIRIES_12_MONTHS = st.selectbox("Bureau Enquiries (12M)", ["1-2", "3", "4-5", "6-7", "8-11", "12+", "14+"])

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
        "DEFAULT_OPEN_CNT_CR22": DEFAULT_OPEN_CNT_CR22,
        "RESIDENTIAL": RESIDENTIAL,
        "CD_OCCUPATION": CD_OCCUPATION,
        "DOC_TYPE": DOC_TYPE,
        "EMPLOYED_STATUS": EMPLOYED_STATUS,
        "APPLICANT_AGE": APPLICANT_AGE,
        "BUREAU_DEFAULT": BUREAU_DEFAULT,
        "SCORECARD": SCORECARD,
        "BUREAU_ENQUIRIES_12_MONTHS": BUREAU_ENQUIRIES_12_MONTHS
    }

    prob_bad, decision = predict_risk(user_input)
    band = cr22_risk_band(SCORE_CR22)

    st.markdown("## Prediction Outcome")

    if decision.lower() == "bad":
        st.error(f"Final Decision: {decision}")
    else:
        st.success(f"Final Decision: {decision}")

    st.markdown(
        f"""
        **Credit Score Risk Band:** {band}  
        **Probability of Default:** {prob_bad:.2%}
        """
    )
