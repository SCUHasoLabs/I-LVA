from typing import List
from fastapi import HTTPException
import numpy as np
import tensorflow as tf
from joblib import load
import pandas as pd
# Load the ml model here

model = tf.keras.models.load_model('new_model.h5')
# model = tf.saved_model.load('./my_saved_model')
scaler = load('scaler1.joblib')  # Load the scaler from disk


def conduct_classification(raw_emg_values: List[float]) -> int:
    try:
        # Preprocess the data
        raw_data = np.array([raw_emg_values])  # Convert to DataFrame with feature names
        input_data = scaler.transform(raw_data)
        

        # Convert input data to a tensor
        input_tensor = tf.convert_to_tensor(input_data, dtype=tf.float32)
        
        print(input_tensor)

        # Make prediction
        prediction = model.predict(input_tensor)
        
        print(prediction)

        # Check the prediction output
        predicted_class = 1 if prediction[0][0] > 0.5 else 0

        return predicted_class
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during classification: {e}")
