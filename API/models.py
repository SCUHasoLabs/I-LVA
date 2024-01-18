from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True)
    location = Column(String)
    value = Column(Float)
    result = Column(Integer, default=False)
