
import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
from datetime import datetime

# Set up the page
st.set_page_config(page_title="Boston Housing Price Predictor", layout="wide")
st.title("🏡 Boston House Price Prediction App")

# Load model
model = joblib.load("regression_pipeline.pkl")

st.header("📋 Enter House Features Below:")

# Create 3-column layout
col1, col2, col3 = st.columns(3)

with col1:
    CRIM = st.number_input("CRIM: Crime rate", 0.0)
    NOX = st.number_input("NOX: Nitric oxides concentration", 0.0)
    AGE = st.number_input("AGE: % built before 1940", 0.0)
    TAX = st.number_input("TAX: Property-tax rate", 0.0)
    LSTAT = st.number_input("LSTAT: % lower status population", 0.0)

with col2:
    ZN = st.number_input("ZN: Proportion of large lots", 0.0)
    RM = st.number_input("RM: Avg number of rooms", 0.0)
    DIS = st.number_input("DIS: Distance to employment centers", 0.0)
    PTRATIO = st.number_input("PTRATIO: Pupil-teacher ratio", 0.0)

with col3:
    INDUS = st.number_input("INDUS: Non-retail business acres", 0.0)
    CHAS = st.selectbox("CHAS: Borders Charles River?", [0, 1])
    RAD = st.number_input("RAD: Access to highways", 0.0)
    B = st.number_input("B: Proportion of Black residents", 0.0)

result_row = []
# Predict and log
if st.button("Predict"):
    input_data = np.array([[CRIM, ZN, INDUS, CHAS, NOX, RM, AGE,
                            DIS, RAD, TAX, PTRATIO, B, LSTAT]])

    prediction = model.predict(input_data)[0]
    price = round(prediction * 1000, 2)

    st.success(f"💰 Predicted House Price: ${price:,.2f}")

    # Prepare row for Excel
    result_row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "CRIM": CRIM, "ZN": ZN, "INDUS": INDUS, "CHAS": CHAS, "NOX": NOX,
        "RM": RM, "AGE": AGE, "DIS": DIS, "RAD": RAD, "TAX": TAX,
        "PTRATIO": PTRATIO, "B": B, "LSTAT": LSTAT,
        "Predicted_Price": price
    }

file_path = "regression_predictions_results.xlsx"

try:
    if os.path.exists(file_path):
        try:
            existing_data = pd.read_excel(file_path, engine='openpyxl')
        except Exception:
            os.remove(file_path)
            st.warning("⚠️ Corrupted Excel file removed. Creating new one.")
            existing_data = pd.DataFrame()
        updated_data = pd.concat([existing_data, pd.DataFrame([result_row])], ignore_index=True)
    else:
        updated_data = pd.DataFrame([result_row])

    updated_data.to_excel(file_path, index=False, engine='openpyxl')
    st.info("📄 Prediction saved to regression_predictions_results.xlsx")

except Exception as e:
    st.error(f"❌ Error saving to Excel: {e}")
