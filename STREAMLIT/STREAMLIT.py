import streamlit as st
import joblib
import pandas as pd
import os


MODEL_PATH = os.path.join(os.path.dirname(__file__), 'lr_final_for_diabetes.joblib')
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error(f'Model not found! Please ensure "{MODEL_PATH}" is in the app directory.')
    st.stop()

st.title('Diabetes Risk Prediction')

st.markdown("""
Enter the patient's details below to predict the risk of diabetes using a trained logistic regression model  
(based on the Pima Indians Diabetes dataset).
""")

# Input fields
pregnancies    = st.number_input('Pregnancies', min_value=0, max_value=20, value=1, step=1,
                              help='Number of times pregnant (0-20 typical)')

glucose        = st.number_input('Glucose (mg/dL)', min_value=50.0, max_value=400.0, value=100.0, step=1.0,
                                 help='Plasma glucose concentration (0-400, typical 70-200)')

blood_pressure = st.number_input('Blood Pressure (mmHg)', min_value=.0, max_value=200.0, value=70.0, step=1.0,
                                 help='Diastolic blood pressure (typical 60-120)')

skin_thickness = st.number_input('Skin Thickness (mm)', min_value=10.0, max_value=100.0, value=20.0, step=1.0,
                                 help='Triceps skinfold thickness (typical 0-99, 0 often missing)')

insulin        = st.number_input('Insulin (mu U/ml)', min_value=20.0, max_value=900.0, value=80.0, step=1.0,
                                 help='2-Hour serum insulin (typical 0-846, 0 often missing)')

bmi            = st.number_input('BMI (kg/m²)', min_value=15.0, max_value=70.0, value=30.0, step=0.1,
                                 help='Body mass index (typical 18-67)')

dpf            = st.number_input('Diabetes Pedigree Function', min_value=0.1, max_value=3.0, value=0.5, step=0.01,
                                 help='Diabetes pedigree score (typical 0.07-2.42)')

age           = st.number_input('Age (years)', min_value=10, max_value=120, value=30, step=1,
                                help='Age in years (minimum 21 in original dataset)')

if st.button('Predict'):
    try:
        # Collect inputs into a list (order must match model training)
        values = [
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            dpf,
            age
        ]

        
        if any(v < 0 for v in values):
            raise ValueError("All values must be non-negative.")



        VALID_RANGES = [
        #   (index, name, min_val, max_val, metric)
            (1, 'Glucose',                  50,  400, 'mg/dL'),
            (2, 'BloodPressure',            25,  200, 'mmHg'),
            (3, 'SkinThickness',            10,  100, 'mm'),
            (4, 'Insulin',                  20,  140, 'mu U/ml'),
            (5, 'BMI',                      15,   70, 'kg/m²'),
            (6, 'DiabetesPedigreeFunction', 0.1, 3.0, 'score'),
            (7, 'Age',                      10,  120, 'years')
        ]
        for idx, name, min_val, max_val, metric in VALID_RANGES:
        
            val = values[idx]
            if not (min_val <= val <= max_val):
                raise ValueError(f'{name} Should be between {min_val} - {max_val} {metric}')

        
        input_df    = pd.DataFrame([values],
                                   columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                                            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'])

        prediction  = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]

        result = 'Diabetes' if prediction == 1 else 'No Diabetes'
        confidence = max(probability) * 100
        diabetes_risk = probability[1] * 100

        st.markdown(f"### **Prediction: {result}**")
        if prediction == 1:
            st.error(result)  # Red emphasis
        else:
            st.success(result)  # Green emphasis

        st.markdown(f"**Confidence:** {confidence:.1f}%  \n"
                    f"**Diabetes Risk Probability:** {diabetes_risk:.1f}%")

    except ValueError as e:
        st.error(f"Invalid Input: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Note: This is a demonstration tool based on a logistic regression model trained on the Pima Indians Diabetes dataset. "
           "It is not a substitute for professional medical diagnosis.")