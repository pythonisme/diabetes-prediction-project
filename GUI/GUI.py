import tkinter as tk
from   tkinter import ttk, messagebox
import joblib
import pandas as pd
import os

# Load Model:
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'lr_final_for_diabetes.joblib')
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    messagebox.showerror('Error', f'Model not found!\nExpected: {MODEL_PATH}')
    exit()

# Main Window:
root = tk.Tk()
root.title('Diabetes Prediction')
root.resizable(False, False)

ttk.Label(root, text='Diabetes Risk Prediction', font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)

labels = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
          'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

entries = {}
for i, text in enumerate(labels, 1):
    ttk.Label(root, text=text + ' :').grid(row=i, column=0, sticky='e', padx=10, pady=5)
    entry = ttk.Entry(root, width=20)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[text] = entry

# Result label:
result_label = ttk.Label(root, text='', font=('Helvetica', 14), foreground='navy')
result_label.grid(row=10, column=0, columnspan=2, pady=15)

prob_label = ttk.Label(root, text='', font=('Helvetica', 11), foreground='gray')
prob_label.grid(row=11, column=0, columnspan=2)

# Function for prediction:
def predict():
    try:
        
        values = []
        for col in labels:
            val = entries[col].get().strip()
            if not val:
                raise ValueError(f'{col} is empty!')
            values.append(float(val))

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
       
        input_df    = pd.DataFrame([values], columns=labels)
        prediction  = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]

        
        result     = 'Diabetes' if prediction == 1 else 'No Diabetes'
        confidence = max(probability) * 100

        result_label.config(
            text=result,
            foreground='red' if prediction == 1 else 'green'
        )
        prob_label.config(
            text=f'Confidence: {confidence:.1f}% (Diabetes risk: {probability[1]*100:.1f}%)'
        )

    except ValueError as e:
        messagebox.showerror('Invalid Input', str(e))
    except Exception as e:
        messagebox.showerror('Error', f'Something went wrong:\n{e}')

ttk.Button(root, text='Predict', command=predict).grid(row=9, column=0, columnspan=2, pady=20)

root.mainloop()