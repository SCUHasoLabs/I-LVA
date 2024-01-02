import serial
import time
from typing import Dict
from tensorflow import keras
import pandas as pd
import joblib

model = keras.models.load_model("my_model.h5")

channels = {}

for i in range(8):
    channel = float(input(f"channel{i+1}"))
    channels["channel" + str(i + 1)] = channel

df = pd.DataFrame.from_dict(channels)


scaler = joblib.load("scaler.save")
X_test_scaled = scaler.transform(df)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=X_test_scaled.columns)


ser = serial.Serial("COM3", 9600)
time.sleep(2)

classification_result = '0' if model.predict(X_test_scaled_df)[0] % 2 == 0 else '1'

ser.write(classification_result.encode())

ser.close()
