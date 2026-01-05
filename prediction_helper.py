import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
model_data = joblib.load(os.path.join(BASE_DIR, "model_data_final.joblib"))

model = model_data["model"]
features = model_data["features"]
scaler = model_data["scaler"]
cols_to_scale = model_data["cols_to_scale"]

BAD_CLASS = 1  # Bad = 1, Good = 0
THRESHOLD = 0.3 # business rule


def prepare_input(user_input: dict):

    df = pd.DataFrame([user_input])

    # Same encoding as training
    df = pd.get_dummies(df, drop_first=True)

    # Add missing columns
    for col in features:
        if col not in df.columns:
            df[col] = 0

    # Keep training order
    df = df[features]

    # Scale numeric columns
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    return df


def predict_risk(user_input: dict):

    df = prepare_input(user_input)

    prob_bad = float(model.predict_proba(df)[0][BAD_CLASS])

    decision = "Bad" if prob_bad >= THRESHOLD else "Good"

    return   prob_bad , decision


#-----sree varshan----#