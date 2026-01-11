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
    """)

# ==================================================
# 🧮 CALCULATIONS
# ==================================================
elif page == "🧮 Calculations":
    st.markdown("## Calculation Logic")

    st.markdown("""
    ```
    Long_Term_Delinquency =
    30+ DPD (24 Months)
    + max(0, 30+ DPD (12 Months) - 1)
    ```
    """)

    st.markdown("<a href='#input_section'>👉 Go to Input Values</a>", unsafe_allow_html=True)

# ==================================================
# ⚙️ BUSINESS RULE ENGINE
# ==================================================
elif page == "⚙️ Business Rule Engine":
    st.markdown("""
    ## Business Rule Engine (BRE)

    **Delinquency Rules**
    ```
    ≥5  → Reject
    3–4 → High Risk
    1–2 → Medium Risk
    0   → Low Risk
    ```

    **Credit Score Rules**
    ```
    ≤500      → Very High Risk
    501–607   → High Risk
    608–715   → Medium Risk
    >715      → Low Risk
    ```
    """)

# ==================================================
# INPUT SECTION
# ==================================================
st.markdown("<a id='input_section'></a>", unsafe_allow_html=True)

st.info("All inputs follow credit bureau logic. Derived features are auto-calculated.")

# ---------------- CREDIT BEHAVIOUR ----------------
st.markdown("### Credit Behaviour Metrics")

c1, c2, c3 = st.columns(3)

with c1:
    SCORE_CR22 = st.number_input("Credit Score (0–1200)", -300, 1200, 650)
    DEROGATORIES = st.number_input("Derogatory Records", 0, value=0)
    Late_Payment_30DPD_Last_12M = st.number_input("Late Payments (30+ DPD) – 12M", 0, value=0)

with c2:
    Credit_Card_Payment_Failure_Count = st.number_input("Credit Card Payment Failures", 0, value=0)
    Recent_Payment_Irregularity_Flag = st.number_input("Recent Payment Irregularity (Months)", 0, 25, 0)
    Late_Payment_30DPD_Last_24M = st.number_input("Late Payments (30+ DPD) – 24M", 0, value=0)

with c3:
    CREDIT_CARD_CR22 = st.number_input("Active Credit Cards", 0, value=1)
    DEFAULT_CNT_CR22 = st.number_input("Total Historical Defaults", 0, value=0)
    DEFAULT_OPEN_CNT_CR22 = st.number_input("Open Defaults", 0, value=0)

Long_Term_Payment_Delinquency_Count = long_term_delinquency_count(
    Late_Payment_30DPD_Last_12M, Late_Payment_30DPD_Last_24M
)

st.metric("Long-Term / Repeated Delinquency Count", Long_Term_Payment_Delinquency_Count)

# ---------------- APPLICANT PROFILE ----------------
st.markdown("### Applicant Profile")

a1, a2, a3 = st.columns(3)

with a1:
    RESIDENTIAL = st.selectbox("Residential Status", ["Owned", "Rented", "Living_With_Family", "Missing"])
    CD_OCCUPATION = st.selectbox("Occupation Type", ["employed", "self_employed", "student", "retired", "unemployed", "Missing"])

with a2:
    EMPLOYED_STATUS = st.selectbox("Employment Status", ["employed", "self_employed", "student", "retired", "unemployed", "benefits", "Missing"])
    APPLICANT_AGE = st.selectbox("Applicant Age Band", ["18-24", "25-29", "30-34", "35-44", "45-54", "54+"])

with a3:
    DOC_TYPE = st.selectbox("Document Type", ["AU Passport", "AU Driver Licence", "Australian Passport", "Intl Passport and Visa", "Missing"])
    BUREAU_DEFAULT = st.selectbox("Bureau Default Category", ["Missing", "1-1000", "1000+"])

# ---------------- INTERNAL SEGMENT ----------------
st.markdown("### Internal Risk Segmentation")

SCORECARD = st.selectbox("Internal Scorecard", ["TAR1A", "SFJR1A", "HSHSOL", "CTSDP", "INSLV"])
BUREAU_ENQUIRIES_12_MONTHS = st.selectbox(
    "Bureau Enquiries (12 Months)",
    ["1-2", "3", "4-5", "6-7", "8-11", "12+", "14+"]
)

# ==================================================
# PREDICTION
# ==================================================
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
        "EMPLOYED_STATUS": EMPLOYED_STATUS,
        "APPLICANT_AGE": APPLICANT_AGE,
        "DOC_TYPE": DOC_TYPE,
        "BUREAU_DEFAULT": BUREAU_DEFAULT,
        "SCORECARD": SCORECARD,
        "BUREAU_ENQUIRIES_12_MONTHS": BUREAU_ENQUIRIES_12_MONTHS
    }

    prob_bad, decision = predict_risk(user_input)
    band = cr22_risk_band(SCORE_CR22)
    delinq_band, delinq_reason = delinquency_interpretation(Long_Term_Payment_Delinquency_Count)

    st.markdown("## Prediction Outcome")

    st.write(f"**ML Decision:** {decision}")
    st.write(f"**Credit Score Risk Band:** {band}")
    st.write(f"**Probability of Default:** {prob_bad:.2%}")

    st.markdown("### Rule-Based Interpretation")
    st.write(f"**Delinquency Risk Level:** {delinq_band}")
    st.write(f"**Interpretation:** {delinq_reason}")

