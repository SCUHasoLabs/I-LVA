import serial
import time
from tensorflow import keras
import pandas as pd
import joblib
import numpy as np

model = keras.models.load_model("my_model.h5")

channels = {}

for i in range(8):
    print(f"channel{i+1}")
    channel = float(input())
    channels["channel" + str(i + 1)] = channel

df = pd.DataFrame([channels])
print(df.head())

scaler = joblib.load("scaler.save")
X_test_scaled = scaler.transform(df)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=df.columns)


ser = serial.Serial("COM3", 9600)
time.sleep(2)

classification_result = '0' if np.argmax(model.predict(X_test_scaled_df), axis=-1) % 2 == 0 else '1'

ser.write(classification_result.encode())

ser.close()
