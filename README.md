# Diabetes Prediction Project

A complete machine learning project on the Pima Indians Diabetes dataset: from exploratory data analysis and model training to multiple deployment options.

## Project Structure
- **EDA/**: Jupyter notebook for data exploration and cleaning.
- **ML/**: Jupyter notebook for model training, handling class imbalance (SMOTE), hyperparameter tuning, and saving the final Logistic Regression model.
- **GUI/**: Desktop application using Tkinter.
- **STREAMLIT/**: Web version of the prediction app using Streamlit.

## Usage

### 1. Exploratory Data Analysis
Open and run `EDA/Diabetes EDA.ipynb` in Jupyter.  
Explores distributions, correlations, missing values, removes outliers, and creates the cleaned dataset.

### 2. Machine Learning
Open and run `ML/Diabetes ML.ipynb`.  
Trains several models, applies SMOTE for imbalance, tunes Logistic Regression, and saves the final model (`lr_final_for_diabetes.joblib`).

Fully reproducible with fixed seeds and stable library versions.

### 3. Desktop GUI App (Tkinter)
```bash
cd GUI
python "Diabetes GUI.py"

A window opens where you can enter patient details and get an instant prediction.

#### Optional: Build a standalone executable (Windows)
Place Diabetes GUI.spec, Diabetes GUI.py, and lr_final_for_diabetes.joblib in the GUI folder.
Install PyInstaller: pip install pyinstaller==6.17.0
Run:Bashcd GUI
pyinstaller "Diabetes GUI.spec" --onefile --windowed --name="Diabetes Predictor" --add-data "lr_final_for_diabetes.joblib;." --clean
Find Diabetes Predictor.exe in GUI/dist (~350 MB).

### 4. Web App (Streamlit)
Live demo: https://streamlit.app

#### Run locally:
Bashcd STREAMLIT
streamlit run STREAMLIT.py
Enter patient details in the browser and get the diabetes risk prediction instantly.


### Notes

Model: Logistic Regression (chosen for interpretability and strong performance on this dataset).
All code uses stable library versions for maximum reproducibility.
This Project which is my first, was a great challenge for me covering the full ML pipeline: EDA → Modeling → Multiple Deployment Options (Desktop + Web).
I myself Learned so many things in this project by experimenting. I hope it can help you!

Feel free to fork, experiment, or improve (e.g., try different models in the ML notebook)!