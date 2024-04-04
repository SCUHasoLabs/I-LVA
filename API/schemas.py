from pydantic import BaseModel

class BaseData(BaseModel):
    location: str
    value: float
    raw_emg_values: list[float]
    classification: int

    class Config:
        from_attributes = True

class DataModel(BaseModel):
    diff_x: int
    diff_y: int

    class Config:
        from_attributes = True

class Response(BaseData):
    id: int
    is_added: bool

    class Config:
        from_attributes = True

class Message(BaseModel):
    message: str

    class Config:
        from_attributes = True

class DBResponse(BaseModel):
    id: int
    location: str
    value: float
    classification: int
    raw_emg_values: list[float]

    class Config:
        from_attributes = True

class DBResponseVRtoLV(BaseModel):
    id: int
    diff_x: int
    diff_y: int

    class Config:
        from_attributes = True