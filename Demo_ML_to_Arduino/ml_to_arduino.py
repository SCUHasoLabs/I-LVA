import serial
import time
from tensorflow import keras
import pandas as pd
import joblib
import numpy as np

model = keras.models.load_model("Demo_ML_to_Arduino/my_model.h5")

channels = {}



df = pd.read_csv("Demo_ML_to_Arduino/data.csv")
df = df.sample(frac=1).reset_index(drop=True)
df2 = df.copy()
df.drop("time", axis=1, inplace=True)
df.drop("class", axis=1, inplace=True)


for i in range(50):
    for j in range(1,9):
        channel = df.iloc[i][f'channel{j}']
        if not channels.get(f'channel{j}'):
            channels['channel' + str(j)] = []
        channels['channel' + str(j)].append(channel)

df = pd.DataFrame(channels)

scaler = joblib.load("Demo_ML_to_Arduino/scaler.save")
X_test_scaled = scaler.transform(df)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=df.columns)

# make sure the serial port and baud rates are consistent with the arduino
ser = serial.Serial("COM3", 9600)
time.sleep(2)

# hand movement was detected
for i in range(len(50)):
    classification_result = "1" if np.argmax(model.predict(X_test_scaled_df), axis=-1)[i] in [0, 2, 3, 4, 5, 6, 7] else "0"
    ser.write(classification_result.encode())
    # send classification result every 3 seconds
    time.sleep(3)

# will write 0 or 1 to the serial port of the arduino
ser.close()