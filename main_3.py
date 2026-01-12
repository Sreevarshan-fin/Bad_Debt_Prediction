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
    used by financial institutions to predict **bad debt risk**.

    It combines **machine learning–based default probability**
    with **internal business rules** to deliver **accurate,
    policy-compliant, and explainable credit decisions**.
    """)

with c2:
    st.markdown("""
    ### 👤 Name
    **Sree Varshan**
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

# ---------------- CREDIT BEHAVIOUR ----------------
st.markdown("### Credit Behaviour Metrics")
c1, c2, c3 = st.columns(3)

with c1:
    SCORE_CR22 = st.number_input("Credit Score (0–1200)", -300, 1200, 650)
    DEROGATORIES = st.number_input("Derogatory Records", 0, value=0)
    Late_12M = st.number_input("Late Payments (30+ DPD) – Last 12 Months", 0, value=0)

with c2:
    CC_Failures = st.number_input("Credit Card Payment Failures", 0, value=0)
    Recent_Irregularity = st.number_input("Recent Payment Irregularity (Months)", 0, 25, 0)
    Late_24M = st.number_input("Late Payments (30+ DPD) – Last 24 Months", 0, value=0)

with c3:
    Active_CC = st.number_input("Active Credit Cards", 0, value=1)
    Total_Defaults = st.number_input("Total Historical Defaults", 0, value=0)
    Open_Defaults = st.number_input("Open Defaults", 0, value=0)

# ---------------- DERIVED FEATURE ----------------
LTD = long_term_delinquency_count(Late_12M, Late_24M)
st.metric("Long-Term / Repeated Delinquency Count", LTD)

# ---------------- APPLICANT PROFILE ----------------
st.markdown("### Applicant Profile")
a1, a2, a3 = st.columns(3)

with a1:
    RESIDENTIAL = st.selectbox(
        "Residential Status",
        ["Owned", "Rented", "Living_With_Family", "Missing"]
    )
    CD_OCCUPATION = st.selectbox(
        "Occupation Type",
        ["employed", "self_employed", "student", "retired", "unemployed", "Missing"]
    )

with a2:
    EMPLOYED_STATUS = st.selectbox(
        "Employment Status",
        ["employed", "self_employed", "student", "retired", "unemployed", "benefits", "Missing"]
    )
    APPLICANT_AGE = st.selectbox(
        "Applicant Age Band",
        ["18-24", "25-29", "30-34", "35-44", "45-54", "54+"]
    )

with a3:
    DOC_TYPE = st.selectbox(
        "Document Type",
        [
            "AU Passport", "AU Driver Licence", "Australian Passport",
            "Intl Passport and Visa", "HAAU 18+ Card", "Missing"
        ]
    )
    BUREAU_DEFAULT = st.selectbox(
        "Bureau Default Category",
        ["Missing", "1-1000", "1000+"]
    )

# ---------------- INTERNAL SEGMENTATION ----------------
st.markdown("### Internal Risk Segmentation")

SCORECARD = st.selectbox(
    "Internal Scorecard",
    ["TAR1A", "SFJR1A", "HSHSOL", "CTSDP", "INSLV"]
)

BUREAU_ENQUIRIES_12M = st.selectbox(
    "Bureau Enquiries (Last 12 Months)",
    ["1-2", "3", "4-5", "6-7", "8-11", "12+", "14+"]
)

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
        "DEFAULT_OPEN_CNT_CR22": Open_Defaults,
        "RESIDENTIAL": RESIDENTIAL,
        "CD_OCCUPATION": CD_OCCUPATION,
        "EMPLOYED_STATUS": EMPLOYED_STATUS,
        "APPLICANT_AGE": APPLICANT_AGE,
        "DOC_TYPE": DOC_TYPE,
        "BUREAU_DEFAULT": BUREAU_DEFAULT,
        "SCORECARD": SCORECARD,
        "BUREAU_ENQUIRIES_12_MONTHS": BUREAU_ENQUIRIES_12M
    }

    prob_bad, decision = predict_risk(user_input)
    band = cr22_risk_band(SCORE_CR22)

    st.markdown("## 📈 Prediction Result")

    r2, r3 = st.columns(3)
    r2.metric("Credit Risk Band", band)
    r3.metric("Final Decision", decision)

    st.info("Business rules are applied internally to ensure policy-aligned decisions.")

