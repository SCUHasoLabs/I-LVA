from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import models, database, schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session

import json

app = FastAPI()
scheduler = AsyncIOScheduler()
scheduler.start()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clear_database():
    with Session() as session:
        session.query(models.Data).delete()
        session.commit()

scheduler.add_job(clear_database, 'interval', minutes=5)


@app.post("/", response_model=schemas.Response)
def create_entry(data: schemas.BaseData, db: Session = Depends(get_db)):
    db_data = db.query(models.Data).filter(models.Data.value == data.value).first()
    if (db_data):
        raise HTTPException(status_code=400, detail="Value already in db")
    new_data = models.Data(location=data.location, value=data.value, result=data.result)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    response = schemas.Response(
        id=new_data.id,
        location=new_data.location, 
        is_added=True,
        result=new_data.result,
        value=new_data.value
    )
    return response

@app.get("/show/", response_model=list[schemas.DBResponse])
def show_db(db: Session = Depends(get_db)):
    data = db.query(models.Data).all()
    return data