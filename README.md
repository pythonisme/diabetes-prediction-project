Usage

1. Exploratory Data Analysis.
Open and run EDA/Diabetes EDA.ipynb in Jupyter.
Explores distributions, correlations, missing values, cuts outliers and creates the cleaned dataset.


2. Machine Learning.
Open and run ML/Diabetes ML.ipynb.
Trains multiple models, handles imbalance (SMOTE), tunes Logistic Regression, and saves the final model (lr_final_for_diabetes.joblib).

Fully reproducible with identical results on every run.
Easy experimentation: Swap models or change scoring metrics via the provided custom scorer functions.


3. Run the Desktop GUI App.
Bash cd GUI
python "Diabetes GUI.py"

A window opens.
Enter patient values (Pregnancies, Glucose, etc.).
Click Predict → Shows "Diabetes" or "No Diabetes" with confidence and risk percentage.


you can Build Standalone Executable (Optional – Windows)
To create a single .exe (no Python needed for end users):

download and locate all files in a folder name it GUI:
1- "Diabetes GUI.spec"
2- Diabetes GUI.py
3- lr_final_for_diabetes.joblib
(you can download them from repository/GUI)


Install PyInstaller:Bash pip install pyinstaller==6.17.0

cd GUI: pyinstaller "Diabetes GUI.spec" --onefile --windowed --name="Diabetes Predictor" --add-data "lr_final_for_diabetes.joblib;." --clean


Find Diabetes Predictor.exe in folder GUI/dist. (300 MB normal due to pandas/scikit-learn).


Notes

Model: Logistic Regression (interpretable, strong performance on this dataset).
All code uses stable, established library versions for maximum reproducibility.
Perfect starter project for learning the full ML pipeline: EDA → Modeling → Deployment.

Feel free to fork, experiment, or improve (e.g., try different models in the ML notebook or add a web version with Streamlit)!