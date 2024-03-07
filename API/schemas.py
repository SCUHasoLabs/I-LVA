from pydantic import BaseModel

class BaseData(BaseModel):
    location: str
    value: float
    raw_emg_values: list[float]
    result: int

    class Config:
        orm_mode = True

class Response(BaseData):
    id: int
    is_added: bool

    class Config:
        orm_mode = True

class DBResponse(BaseModel):
    id: int
    location: str
    value: float
    result: int
    raw_emg_values: list[float]

    class Config:
        orm_mode = True