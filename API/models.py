from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship

from database import Base

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String)
    value = Column(Float)
    classification = Column(Integer, default=False)
    raw_emg_values = Column(JSON) #store raw emg values as a JSON array

    # This approach allows you to store an array of floats as a JSON array in the raw_emg_values column. SQLAlchemy will automatically serialize your Python list into JSON when you save the model and deserialize it back into a Python list when you query the database. This method is very flexible and works with any database supported by SQLAlchemy, not just SQLite.

class VirtualToPhysical(Base):
    __tablename__ = "data2"
    id = Column(Integer, primary_key=True, autoincrement=True)
    diff_x = Column(Integer)
    diff_y = Column(Integer)
