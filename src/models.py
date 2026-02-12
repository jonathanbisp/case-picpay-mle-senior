from pydantic import BaseModel


class LoadModelRequest(BaseModel):
    model: str


class PredictRequest(BaseModel):
    model: str
    text: str
