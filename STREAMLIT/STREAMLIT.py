import streamlit as st
import joblib
import pandas as pd
import os

# --- Load Model ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), "lr_final_for_diabetes.joblib")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error("Model file not found! Upload 'lr_final_for_diabetes.joblib'.")
    st.stop()

# --- UI ---
st.title("Diabetes Risk Prediction")
st.markdown("""
Predict diabetes risk using a Logistic Regression model trained on the Pima Indians Diabetes dataset.  
**Use sliders for quick adjustment or type exact values – they sync automatically!**
""")

st.info("💡 Slider and number input are fully synchronized for precise control.")

# --- Synced Slider + Number Input ---
def synced_slider(label: str, min_val, max_val, default, step=1.0, format_str=None, help_text=""):
    key = f"{label.lower().replace(' ', '_')}_synced"
    
    if key not in st.session_state:
        st.session_state[key] = float(default) if step < 1 else int(default)
    
    col_slider, col_input = st.columns([4, 1])
    
    with col_slider:
        slider_val = st.slider(
            label, min_value=min_val, max_value=max_val,
            value=st.session_state[key], step=step,
            key=f"{key}_slider", help=help_text
        )
    
    with col_input:
        input_val = st.number_input(
            "", min_value=min_val, max_value=max_val,
            value=st.session_state[key], step=step,
            format=format_str if format_str else ("%d" if step >= 1 else "%.2f"),
            key=f"{key}_input", label_visibility="collapsed"
        )
    
    current_val = st.session_state[key]
    if slider_val != current_val:
        st.session_state[key] = type(current_val)(slider_val)
    if input_val != current_val:
        st.session_state[key] = type(current_val)(input_val)
    
    return st.session_state[key]

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    pregnancies    = synced_slider("Pregnancies",            0,  15,   0, step=1, help_text="Number of times pregnant")
    glucose        = synced_slider("Glucose (mg/dL)",       50, 200, 100, step=1, help_text="Key diabetes indicator")
    blood_pressure = synced_slider("Blood Pressure (mmHg)", 30, 140,  70, step=1, help_text="Diastolic")
    skin_thickness = synced_slider("Skin Thickness (mm)",    0,  99,  20, step=1, help_text="Triceps skinfold")

with col2:
    insulin = synced_slider("Insulin (μU/ml)",               0,  900,   80, step=5,     help_text="2-Hour serum insulin")
    bmi     = synced_slider("BMI (kg/m²)",                15.0, 70.0, 30.0, step=0.1,  format_str="%.1f", help_text="Major risk factor")
    dpf     = synced_slider("Diabetes Pedigree Function", 0.07, 2.50, 0.50, step=0.01, format_str="%.3f", help_text="Genetic score")
    age     = synced_slider("Age (years)",                  20,  120,   30, step=1,     help_text="Patient age")

# --- Prediction ---
if st.button("Predict Risk", type="primary", use_container_width=True):
    try:
        input_data = [pregnancies, glucose, blood_pressure, skin_thickness,
                      insulin, bmi, dpf, age]

        input_df = pd.DataFrame([input_data], columns=[
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ])

        prediction = model.predict(input_df)[0]
        proba      = model.predict_proba(input_df)[0]
        risk_prob  = proba[1] * 100
        confidence = max(proba) * 100

        result     = "Diabetes" if prediction == 1 else "No Diabetes"

        st.markdown(f"### Prediction: **{result}**")
        if prediction == 1:
            st.error("⚠️ High Risk Detected")
        else:
            st.success("✅ Low Risk")
            
        st.markdown("#### Results")
        st.markdown(f"##### Diabetes Risk Probability: {risk_prob:.1f}%", )
        st.markdown(f"##### Model Confidence: {confidence:.1f}%")

        st.progress(risk_prob / 100)

    except Exception as e:
        st.error(f"Error: {e}")

# --- Disclaimer ---
st.markdown("---")
st.warning("""
***Disclaimer: ⚠️***  
This tool is for educational purposes only and is not a medical diagnosis.  
Consult a healthcare professional for real medical advice.
""")


