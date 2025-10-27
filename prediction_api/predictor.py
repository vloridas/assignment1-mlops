import json
import os
import pandas as pd
from flask import jsonify
from keras.models import load_model
import logging
from io import StringIO

class BanknotePredictor:
    def __init__(self):
        self.model = None
    
    def predict_single_record(self, prediction_input):
        logging.debug(prediction_input)
        
        if self.model is None:
            try:
                model_repo = os.environ['MODEL_REPO']
                file_path = os.path.join(model_repo, "model.keras")
                self.model = load_model(file_path)
            except KeyError:
                print("MODEL_REPO is undefined")
                self.model = load_model('model.keras')
        
       
        REQUIRED_COLS = ["variance", "skewness", "curtosis", "entropy"]

        def _to_df(payload):
    # Accept either a single dict or a list of dicts
            if isinstance(payload, dict):
                df = pd.DataFrame([payload])
            elif isinstance(payload, list):
                df = pd.DataFrame(payload)
            else:
                raise ValueError("Payload must be a dict or list of dicts")

    # Enforce column order & types
            missing = [c for c in REQUIRED_COLS if c not in df.columns]
            if missing:
                raise ValueError(f"Missing required keys: {missing}")

            df = df[REQUIRED_COLS].astype(float)
            return df
        df = _to_df(prediction_input)
        y_pred = self.model.predict(df)
        logging.info(y_pred[0])
        
        status = (y_pred[0] > 0.5)
        logging.info(type(status[0]))
        
        # Convert numpy boolean to Python int (0 or 1)
        result = int(status[0])
        
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': str(result)}), 200