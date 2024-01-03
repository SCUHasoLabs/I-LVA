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

# make sure the serial port and baud rates are consistent with the arduino
ser = serial.Serial("COM3", 9600)
time.sleep(2)

# hand movement was detected
classification_result = "1" if np.argmax(model.predict(X_test_scaled_df), axis=-1)[0] in [0, 2, 3, 4, 5, 6, 7] else "0"

# will write 0 or 1 to the serial port of the arduino
ser.write(classification_result.encode())

ser.close()
