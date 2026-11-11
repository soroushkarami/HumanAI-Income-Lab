from pathlib import Path
import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[3]

model_path = BASE_DIR/'Trained Model'/'Pipeline nb'/'NN_model_pipeline.pkl'

class IncomePredictorModel:
    def __init__(self):
        self.model = joblib.load(model_path)


    def predict(self, info: dict):
        df = pd.DataFrame([info])

        both_probs = self.model.predict_proba(df)

        return both_probs
