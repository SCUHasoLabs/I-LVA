from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import models, database, schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy import delete
from datetime import timezone, datetime as dt
from classify import conduct_classification
import uvicorn
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()
scheduler = AsyncIOScheduler()
scheduler.start()

models.Base.metadata.create_all(bind=engine)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

#load the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#clear database function
def clear_database():
    with Session() as session:
        session.query(models.Data).delete()
        session.commit()

#clear database every 5 minutes to not get it cluttered
scheduler.add_job(clear_database, 'interval', minutes=5)

# create an entry into the database for emg data
# post 
@app.post("/", response_model=schemas.Response, status_code=200)
def create_entry(data: schemas.BaseData, db: Session = Depends(get_db)):
    # db_data = db.query(models.Data).filter(models.Data.value == data.value).first()
    # if db_data:
    #     raise HTTPException(status_code=400, detail="Value already in db")
    # for the classifcation, need to write function that classifies and then call it to get the classification
    classification = conduct_classification(data.raw_emg_values)
    if classification is None:
        raise HTTPException(status_code=500, detail="Classification failed")
    # print(classification)
    new_data = models.Data(classification=classification, timestamp=str(dt.now(timezone.utc)), heart_rate=data.heart_rate, raw_emg_values=data.raw_emg_values)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    response = schemas.Response(
        id=new_data.id,
        is_added=True,
        classification=new_data.classification,
        heart_rate=new_data.heart_rate,
        raw_emg_values=new_data.raw_emg_values,
        timestamp=new_data.timestamp,
    )
    return response

@app.put("/api/vr_to_lv", response_model=schemas.Message, status_code=200)
def put_entry(data: schemas.DataModel, db: Session = Depends(get_db)):
    old_data = db.query(models.VirtualToPhysical).first()
    if not old_data:
        entry = models.VirtualToPhysical(**data.dict())
        db.add(entry)

        message = "New entry created successfully"
    else:
        old_data.diff_x = data.diff_x
        old_data.diff_y = data.diff_y

        message = "Entry was updated successfully"

    db.commit()

    return schemas.Message(
        message=message
    )



#retrieve current entry for virtual to physical
# originally had response model which was DBResponseVRtoLV
@app.get("/api/vr_to_lv", status_code=200)
def get_entry(db: Session = Depends(get_db)):
    data = db.query(models.VirtualToPhysical).all()
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="database is empty")
    return {"raw data": data}

# retrieve all entries in the database
@app.get("/", response_model=list[schemas.DBResponse], status_code=200)
def show_db(db: Session = Depends(get_db)):
    data = db.query(models.Data).all()
    return data

@app.delete("/", response_model=schemas.Message, status_code=200)
def del_db(db: Session = Depends(get_db)):
    table_name: str = models.Data.__tablename__
    db.query(models.Data).delete()
    db.commit()

    return schemas.Message(
        message=f"Successful deletion of all entries in {table_name}"
    )

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)