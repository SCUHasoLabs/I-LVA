from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from models import ExampleItem, SessionLocal
import atexit
from tensorflow.keras.models import load_model
import numpy as np

# Load the ml model here
model = load_model('my_model.h5')

# Use the python to arduino code, which does the pre-processing, just add that here
def preprocess_data(data):
    processed_data = np.array(data).reshape(1, -1)
    return processed_data

# This is just a template, can change depending on the model
def classify_data(data):
    processed_data = preprocess_data(data)
    prediction = model.predict(processed_data)
    predicted_class = np.argmax(prediction)
    return predicted_class

def classify_and_update_db():
    db = SessionLocal()
    try:
        # Query for unclassified items
        unclassified_items = db.query(ExampleItem).filter(ExampleItem.classification == None).all()
        for item in unclassified_items:
            # Perform classification
            classification_result = classify_data(item.data)
            # Update the item with the classification result
            item.classification = classification_result
            db.add(item)
        db.commit()
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(func=classify_and_update_db, trigger="interval", seconds=5)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
