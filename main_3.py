import streamlit as st
from prediction_helper import predict_risk

st.set_page_config(page_title="Bad Debt Prediction", layout="wide")
st.title("Bad Debt Prediction")

st.markdown(
"""
ℹ️ **Note:**  
All inputs follow **credit bureau risk-score logic**.  
Some combinations may be technically valid but **logically inconsistent** in real-world credit systems.
"""
)

# -----------------------------
# NUMERIC INPUTS
# -----------------------------
SCORE_CR22 = st.number_input(
    "Credit Score (0 – 1200)",
    min_value=-300,
    max_value=1200,
    value=650,
    help="""
Represents bureau risk score.
• Higher score = lower credit risk  
• <300 = very high risk  
• 650+ = good  
• 900+ = excellent
"""
)

DEROGATORIES = st.number_input(
    "Derogatory Records",
    min_value=0,
    value=0,
    help="""
Count of severe negative credit events.
Examples:
• Charge-offs
• Bankruptcy
• Legal defaults

Higher value = higher risk
"""
)

Late_Payment_30DPD_Last_12M = st.number_input(
    "Late Payments (30+ DPD) – Last 12 Months",
    min_value=0,
    value=0,
    help="Number of payments overdue by 30+ days in last 12 months."
)

Credit_Card_Payment_Failure_Count = st.number_input(
    "Credit Card Payment Failures",
    min_value=0,
    value=0,
    help="Number of missed or failed credit card payments."
)

Recent_Payment_Irregularity_Flag = st.number_input(
    "Recent Payment Irregularity Flag",
    min_value=0,
    max_value=25,
    value=0,
    help="""
Number of recent periods (months) where payment behavior was irregular.   

• 0 = No irregular payments
• Higher value = frequent payment issues
• 10+ = very risky behavior
"""
)

Late_Payment_30DPD_Last_24M = st.number_input(
    "Late Payments (30+ DPD) – Last 24 Months",
    min_value=0,
    value=0,
    help="Total late payments in last 24 months."
)

Long_Term_Payment_Delinquency_Count = st.number_input(
    "Long-Term Delinquencies",
    min_value=0,
    value=0,
    help="Count of long-standing unresolved delinquencies."
)

CREDIT_CARD_CR22 = st.number_input(
    "Number of Active Credit Cards",
    min_value=0,
    value=1,
    help="Total number of active credit cards."
)

DEFAULT_CNT_CR22 = st.number_input(
    "Number of Total Defaults",
    min_value=0,
    value=0,
    help="Total number of historical defaults. Not Amount how many defaults [Count] example : 1,2,3,...n"
)

DEFAULT_OPEN_CNT_CR22 = st.number_input(
    "Open Defaults",
    min_value=0,
    value=0,
    help="Number of defaults that are still unresolved."
)

# -----------------------------
# CATEGORICAL INPUTS
# -----------------------------
RESIDENTIAL = st.selectbox(
    "Residential Status",
    ["Owned", "Rented", "Living_With_Family", "Missing"],
    help="Applicant’s current housing status."
)

CD_OCCUPATION = st.selectbox(
    "Occupation Type",
    ["employed", "self_employed", "student", "retired", "unemployed", "Missing"],
    help="Primary occupation of the applicant."
)

DOC_TYPE = st.selectbox(
    "Document Type",
    [
        "AU Passport", "AU Driver Licence", "Australian Passport",
        "Intl Passport and Visa", "HAAU 18+ Card", "Fire Arms Licence",
        "Defence Force ID(picture card)", "AU Birth Certificate", "Missing"
    ],
    help="Identity document provided by applicant."
)

EMPLOYED_STATUS = st.selectbox(
    "Employment Status",
    ["employed", "self_employed", "student", "retired", "unemployed", "benefits", "Missing"],
    help="Current employment status."
)

APPLICANT_AGE = st.selectbox(
    "Applicant Age Band",
    ["18-24", "25 - 29", "30-34", "35-44", "45-54", "54+"],
    help="Age group of applicant."
)

BUREAU_DEFAULT = st.selectbox(
    "Bureau Default Category",
    ["Missing", "1-1000", "1000+"],
    help="""
Indicates severity of bureau-recorded defaults.
• 1000+ = very high default exposure
"""
)

SCORECARD = st.selectbox(
    "Internal Scorecard",
    ["TAR1A", "SFJR1A", "HSHSOL", "CTSDP", "INSLV"],
    help="Internal lender scorecard segment."
)

BUREAU_ENQUIRIES_12_MONTHS = st.selectbox(
    "Bureau Enquiries (Last 12 Months)",
    ["1-2", "3", "4-5", "6-7", "8-11", "12+", "14+"],
    help="Number of credit enquiries in last 12 months."
)



def cr22_risk_band(score):
    if score <= 500:
        return "Very High Risk"
    elif 501 <= score <= 607:
        return "High Risk"
    elif 608 <= score <= 715:
        return "Medium Risk"
    else:
        return "Low Risk"


# -----------------------------
# BUTTON
# -----------------------------
if st.button("Predict Risk"):

    user_input = {
        "SCORE_CR22": SCORE_CR22,
        "DEROGATORIES": DEROGATORIES,
        "Late_Payment_30DPD_Last_12M": Late_Payment_30DPD_Last_12M,
        "Credit_Card_Payment_Failure_Count": Credit_Card_Payment_Failure_Count,
        "Recent_Payment_Irregularity_Flag": Recent_Payment_Irregularity_Flag,
        "Late_Payment_30DPD_Last_24M": Late_Payment_30DPD_Last_24M,
        "Long_Term_Payment_Delinquency_Count": Long_Term_Payment_Delinquency_Count,
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
    result = predict_risk(user_input)

    st.subheader("Prediction Result")
    st.success(f"Final Decision: {decision}")


    # CR22 interpretation
    band = cr22_risk_band(SCORE_CR22)

    st.subheader("Interpretation to Review the Result")

    st.markdown(f"""
    **Probability of Default (PD):** `{prob_bad:.2%}`  
    **Credit Score Risk Band:** `{band}`  
    """)