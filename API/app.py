from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import models, database, schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
scheduler = AsyncIOScheduler()
scheduler.start()

models.Base.metadata.create_all(bind=engine)

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
@app.post("/", response_model=schemas.Response, status_code=200)
def create_entry(data: schemas.BaseData, db: Session = Depends(get_db)):
    db_data = db.query(models.Data).filter(models.Data.value == data.value).first()
    if (db_data):
        raise HTTPException(status_code=400, detail="Value already in db")
    new_data = models.Data(location=data.location, value=data.value, classification=data.classification, raw_emg_values=data.raw_emg_values)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    response = schemas.Response(
        id=new_data.id,
        location=new_data.location, 
        is_added=True,
        result=new_data.classification,
        value=new_data.value,
        raw_emg_values=new_data.raw_emg_values
    )
    return response

# retrieve all entries in the database
@app.get("/show/", response_model=list[schemas.DBResponse], status_code=200)
def show_db(db: Session = Depends(get_db)):
    data = db.query(models.Data).all()
    return data