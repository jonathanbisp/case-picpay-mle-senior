from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field


class LoadModelRequest(BaseModel):
    model: str


class PredictRequest(BaseModel):
    model: str
    text: str


class PredicitionEntities(BaseModel):
    money: float | None
    person: str | None
    date: str | None


class PredictionModel(BaseModel):
    id: ObjectId = Field(alias="_id")
    model: str
    text: str
    entities: PredicitionEntities
    timestamp: datetime

    class Config:
        arbitrary_types_allowed = True


class HistoryResponse(BaseModel):
    history: list[PredictionModel]
