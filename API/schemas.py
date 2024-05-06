from pydantic import BaseModel

class BaseData(BaseModel):
    raw_emg_values: list[float]
    heart_rate: int

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
    timestamp: str
    classification: int

    class Config:
        from_attributes = True

class Message(BaseModel):
    message: str

    class Config:
        from_attributes = True

class DBResponse(BaseModel):
    id: int
    classification: int
    raw_emg_values: list[float]
    heart_rate: int
    timestamp: str

    class Config:
        from_attributes = True

class DBResponseVRtoLV(BaseModel):
    id: int
    diff_x: int
    diff_y: int

    class Config:
        from_attributes = True