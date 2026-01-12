import streamlit as st
from prediction_helper import predict_risk

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Bad Debt Risk Prediction",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# STYLE (PROFESSIONAL LOOK)
# ==================================================
st.markdown("""
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
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<h1 style="text-align:center;">Bad Debt Risk Prediction</h1>
<p style="text-align:center; color:grey;">
Machine Learning + Business Rule Engine
</p>
""", unsafe_allow_html=True)

st.info(
    "All inputs follow credit bureau risk-score logic. "
    "Derived features are calculated automatically to match the ML pipeline."
)

# ==================================================
# BUSINESS LOGIC
# ==================================================
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

def delinquency_risk_band(long_term_delinquency):
    if long_term_delinquency >= 5:
        return "Very High Risk (Reject)"
    elif long_term_delinquency >= 3:
        return "High Risk"
    elif long_term_delinquency >= 1:
        return "Medium Risk"
    else:
        return "Low Risk"

# ==================================================
# INPUT SECTION (DESIGNED)
# ==================================================
with st.container():
    st.markdown("## Credit Behaviour & Applicant Profile")

    left, right = st.columns([2, 1])

    # ---------------- CREDIT BEHAVIOUR ----------------
    with left:
        st.markdown("### Credit Behaviour Metrics")
        c1, c2, c3 = st.columns(3)

        with c1:
            SCORE_CR22 = st.number_input("Credit Score (0–1200)", -300, 1200, 650)
            DEROGATORIES = st.number_input("Derogatory Records", 0, value=0)
            Late_12M = st.number_input("Late Payments (30+ DPD) – 12M", 0, value=0)

        with c2:
            CC_Failures = st.number_input("Credit Card Payment Failures", 0, value=0)
            Recent_Irregularity = st.number_input("Recent Payment Irregularity (Months)", 0, 25, 0)
            Late_24M = st.number_input("Late Payments (30+ DPD) – 24M", 0, value=0)

        with c3:
            Active_CC = st.number_input("Active Credit Cards", 0, value=1)
            Total_Defaults = st.number_input("Total Historical Defaults", 0, value=0)
            Open_Defaults = st.number_input("Open Defaults", 0, value=0)

    # ---------------- APPLICANT PROFILE ----------------
    with right:
        st.markdown("### Applicant Profile")
        RESIDENTIAL = st.selectbox("Residential Status", ["Owned", "Rented", "Living_With_Family", "Missing"])
        CD_OCCUPATION = st.selectbox("Occupation Type", ["employed", "self_employed", "student", "retired", "unemployed", "Missing"])
        EMPLOYED_STATUS = st.selectbox("Employment Status", ["employed", "self_employed", "student", "retired", "unemployed", "benefits", "Missing"])
        APPLICANT_AGE = st.selectbox("Applicant Age Band", ["18-24", "25-29", "30-34", "35-44", "45-54", "54+"])
        DOC_TYPE = st.selectbox(
            "Document Type",
            ["AU Passport", "AU Driver Licence", "Australian Passport",
             "Intl Passport and Visa", "HAAU 18+ Card", "Missing"]
        )
        BUREAU_DEFAULT = st.selectbox("Bureau Default Category", ["Missing", "1-1000", "1000+"])

# ==================================================
# DERIVED METRIC (KPI STYLE)
# ==================================================
with st.container():
    st.markdown("## Derived Credit Indicator")

    LTD = long_term_delinquency_count(Late_12M, Late_24M)

    st.metric(
        "Long-Term / Repeated Delinquency Count",
        LTD
    )

# ==================================================
# INTERNAL SEGMENTATION
# ==================================================
with st.container():
    st.markdown("## Internal Risk Segmentation")

    s1, s2 = st.columns(2)

    with s1:
        SCORECARD = st.selectbox("Internal Scorecard", ["TAR1A", "SFJR1A", "HSHSOL", "CTSDP", "INSLV"])

    with s2:
        BUREAU_ENQUIRIES_12M = st.selectbox(
            "Bureau Enquiries (Last 12 Months)",
            ["1-2", "3", "4-5", "6-7", "8-11", "12+", "14+"]
        )

# ==================================================
# PREDICT BUTTON
# ==================================================
st.markdown("---")
btn_col = st.columns([1, 2, 1])[1]
with btn_col:
    predict_btn = st.button("🔍 Predict Credit Risk", use_container_width=True)

# ==================================================
# PREDICTION & DECISION
# ==================================================
if predict_btn:

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

    score_band = cr22_risk_band(SCORE_CR22)
    delinquency_risk = delinquency_risk_band(LTD)

    # ---------------- FINAL DECISION CARD ----------------
    st.markdown("## Final Credit Decision")

    d1, d2, d3 = st.columns(3)

    with d1:
        st.metric("Credit Score Band", score_band)

    with d2:
        st.metric("Delinquency Risk", delinquency_risk)

    with d3:
        st.metric("Decision", decision.upper())

    if decision.lower() == "bad" or delinquency_risk.startswith("Very High"):
        st.error("❌ Application Classified as High Risk")
    else:
        st.success("✅ Application Classified as Acceptable Risk")

    # ---------------- INTERPRETATION ----------------
    st.markdown("### Decision Interpretation")

    st.write(f"""
    - Credit score places the applicant in **{score_band}**
    - Long-term delinquency count = **{LTD}**, indicating **{delinquency_risk}**
    """)

