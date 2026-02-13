from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class LoadModelRequest(BaseModel):
    model: str


class PredictRequest(BaseModel):
    model: str
    text: str


class PredicitionEntities(BaseModel):
    money: float | None = Field(default=None, alias="money")
    person: str | None = Field(default=None, alias="person")
    date: str | None = Field(default=None, alias="date")


class PredictionModel(BaseModel):
    id: ObjectId = Field(alias="_id")
    model: str
    text: str
    entities: PredicitionEntities
    timestamp: datetime

    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)  # type: ignore


class HistoryResponse(BaseModel):
    history: list[PredictionModel]
