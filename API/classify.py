from typing import List
import numpy as np
import tensorflow as tf
from joblib import load
# Load the ml model here
model = tf.saved_model.load('./EMG_binary_classification')
scaler = load('scaler.joblib')  # Load the scaler from disk

def conduct_classification(raw_emg_values: []) -> int: # type: ignore
    try:
        # Preprocess the data
        input_data = np.array(raw_emg_values).reshape(1, -1)  # Reshape data for the model
        input_data = scaler.transform(input_data)  # Scale the data using the loaded scaler
        
        # Make prediction
        prediction = model.predict(input_data)
        prediction_class = int(np.argmax(prediction, axis=1)[0])
        
        return prediction_class
    except Exception as e:
        return None
