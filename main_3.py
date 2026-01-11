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
# Header
# --------------------------------------------------
st.markdown(
    """
    <h1 style="text-align:center;">Bad Debt Risk Prediction</h1>
    <p style="text-align:center; color:grey;">
    Credit Bureau–Driven Risk Assessment Dashboard
    </p>
    """,
    unsafe_allow_html=True
)

st.info(
    "All inputs follow credit bureau risk-score logic. "
    "Derived features are calculated automatically to match the ML pipeline."
)

# --------------------------------------------------
# BUSINESS LOGIC (ML PIPELINE CONSISTENT)
# --------------------------------------------------
def long_term_delinquency_count(dpd_12m: int, dpd_24m: int) -> int:
    """
    Long-term or repeated delinquency calculation
    """
    return dpd_24m + max(0, dpd_12m - 1)

# --------------------------------------------------
# INPUTS
# --------------------------------------------------
st.markdown("### Credit Behaviour Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    SCORE_CR22 = st.number_input(
        "Credit Score (0 – 1200)", min_value=-300, max_value=1200, value=650
    )

    DEROGATORIES = st.number_input(
        "Derogatory Records", min_value=0, value=0
    )

    Late_Payment_30DPD_Last_12M = st.number_input(
        "Late Payments (30+ DPD) – Last 12 Months", min_value=0, value=0
    )

with col2:
    Credit_Card_Payment_Failure_Count = st.number_input(
        "Credit Card Payment Failures", min_value=0, value=0
    )

    Recent_Payment_Irregularity_Flag = st.number_input(
        "Recent Payment Irregularity (Months)", min_value=0, max_value=25, value=0
    )

    Late_Payment_30DPD_Last_24M = st.number_input(
        "Late Payments (30+ DPD) – Last 24 Months", min_value=0, value=0
    )

with col3:
    CREDIT_CARD_CR22 = st.number_input(
        "Active Credit Cards", min_value=0, value=1
    )

    DEFAULT_CNT_CR22 = st.number_input(
        "Total Historical Defaults", min_value=0, value=0
    )

    DEFAULT_OPEN_CNT_CR22 = st.number_input(
        "Open Defaults", min_value=0, value=0
    )

# --------------------------------------------------
# AUTO-DERIVED FEATURE (READ-ONLY)
# --------------------------------------------------
Long_Term_Payment_Delinquency_Count = long_term_delinquency_count(
    Late_Payment_30DPD_Last_12M,
    Late_Payment_30DPD_Last_24M
)

st.text_input(
    "Long-Term / Repeated Delinquency Count (Auto-calculated)",
    value=Long_Term_Payment_Delinquency_Count,
    disabled=True
)

# --------------------------------------------------
# APPLICANT PROFILE
# --------------------------------------------------
st.markdown("### Applicant Profile")

col4, col5, col6 = st.columns(3)

with col4:
    RESIDENTIAL = st.selectbox(
        "Residential Status",
        ["Owned", "Rented", "Living_With_Family", "Missing"]
    )

    CD_OCCUPATION = st.selectbox(
        "Occupation Type",
        ["employed", "self_employed", "student", "retired", "unemployed", "Missing"]
    )

with col5:
    EMPLOYED_STATUS = st.selectbox(
        "Employment Status",
        ["employed", "self_employed", "student", "retired",
         "unemployed", "benefits", "Missing"]
    )

    APPLICANT_AGE = st.selectbox(
        "Applicant Age Band",
        ["18-24", "25 - 29", "30-34", "35-44", "45-54", "54+"]
    )

with col6:
    DOC_TYPE = st.selectbox(
        "Document Type",
        [
            "AU Passport", "AU Driver Licence", "Australian Passport",
            "Intl Passport and Visa", "HAAU 18+ Card",
            "Fire Arms Licence", "Defence Force ID(picture card)",
            "AU Birth Certificate", "Missing"
        ]
    )

    BUREAU_DEFAULT = st.selectbox(
        "Bureau Default Category",
        ["Missing", "1-1000", "1000+"]
    )

# --------------------------------------------------
# INTERNAL SEGMENTATION
# --------------------------------------------------
st.markdown("### Internal Risk Segmentation")

SCORECARD = st.selectbox(
    "Internal Scorecard",
    ["TAR1A", "SFJR1A", "HSHSOL", "CTSDP", "INSLV"]
)

BUREAU_ENQUIRIES_12_MONTHS = st.selectbox(
    "Bureau Enquiries (Last 12 Months)",
    ["1-2", "3", "4-5", "6-7", "8-11", "12+", "14+"]
)

# --------------------------------------------------
# RISK BAND LOGIC
# --------------------------------------------------
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
# PREDICTION
# --------------------------------------------------
st.markdown("---")
center_col = st.columns([1, 2, 1])[1]

with center_col:
    predict_btn = st.button("Predict Credit Risk", use_container_width=True)

if predict_btn:
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
        Credit Score Risk Band: **{band}**  
        Probability of Default: **{prob_bad:.2%}**
        """
    )

