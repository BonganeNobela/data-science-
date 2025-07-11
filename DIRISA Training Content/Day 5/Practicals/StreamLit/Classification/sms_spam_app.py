
import streamlit as st
import joblib
from datetime import datetime
import pandas as pd
import os

# Set up the Streamlit page
st.set_page_config(page_title="📨 SMS Spam Classifier", layout="centered")
st.title("📨 SMS Spam Classification App")

# Load the trained model pipeline
model = joblib.load("spam_classifier_pipeline.pkl")

# Create input box
st.subheader("✉️ Enter your SMS message:")
message = st.text_area("Message", height=150)

# Predict and display result
if st.button("Classify"):
    prediction = model.predict([message])[0]
    label = "📢 Spam" if prediction == 1 else "✅ Ham (Not Spam)"
    st.success(f"Prediction: {label}")

    # Save result to Excel
    result_row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Message": message,
        "Prediction": label
    }

    file_path = "spam_predictions_results.xlsx"

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
        st.info("📄 Prediction saved to spam_predictions_results.xlsx")

    except Exception as e:
        st.error(f"❌ Error saving to Excel: {e}")
