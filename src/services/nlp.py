from asyncio import Lock
from datetime import datetime, timezone

from fastapi.exceptions import HTTPException
from spacy import Language, load
from spacy.cli import download
from spacy.util import is_package

from core.settings import AppSettings
from models import HistoryResponse, PredicitionEntities, PredictionModel
from repositories import BaseRepository

from .base import BaseNLPService


class NLPService(BaseNLPService):
    def __init__(self, settings: AppSettings, repository: BaseRepository) -> None:
        self.repository = repository
        self.models_collection = settings.MONGO_COLLECTION_MODELS
        self.predictions_collection = settings.MONGO_COLLECTION_PREDICTIONS
        self.models: dict[str, Language] = {}
        self._lock = Lock()

    async def extract_entities(self, model_name: str, text: str) -> PredicitionEntities:
        nlp = await self.load_model(model_name=model_name)
        doc = nlp(text)
        entities = {}
        for ent in doc.ents:
            entities[ent.label_.lower()] = ent.text
        pred = PredicitionEntities.model_validate(entities)  # type: ignore
        await self.repository.write(
            collection=self.predictions_collection,
            data={
                "model": model_name,
                "text": text,
                "entities": pred.model_dump(),
                "timestamp": datetime.now(timezone.utc),
            },
        )
        return pred

    async def add_model(self, model_name: str) -> None:
        if not await self.repository.find(
            collection=self.models_collection, query={"model": model_name}
        ):
            await self.repository.write(
                collection=self.models_collection, data={"model": model_name}
            )
            await self.load_model(model_name=model_name)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{model_name}' already exists in repository.",
            )

    async def load_model(self, model_name: str) -> Language:
        if not await self.repository.find(
            collection=self.models_collection, query={"model": model_name}
        ):
            # Remove do cache se o modelo não estiver mais no repositório
            if model_name in self.models:
                del self.models[model_name]
            raise HTTPException(
                status_code=404,
                detail=f"Model '{model_name}' not found in repository. Please add it first.",
            )

        if model_name in self.models:
            return self.models[model_name]

        async with self._lock:
            if model_name not in self.models:
                if not is_package(model_name):
                    try:
                        download(model_name)
                    except SystemExit as e:
                        await self.delete_model(model_name=model_name)
                        raise HTTPException(
                            status_code=500,
                            detail=f"Failed to download model '{model_name}': {str(e)}",
                        )
                self.models[model_name] = load(model_name)
                # Desabilita pipes desnecessários para otimizar performance
                for pipe_name in list(self.models[model_name].pipe_names):
                    if pipe_name != "ner":
                        self.models[model_name].disable_pipe(pipe_name)

        return self.models[model_name]

    async def get_models(self) -> list[str]:
        models = await self.repository.list(collection=self.models_collection, query={})
        return [model["model"] for model in models]

    async def delete_model(self, model_name: str) -> None:
        if await self.repository.find(
            collection=self.models_collection, query={"model": model_name}
        ):
            await self.repository.delete(
                collection=self.models_collection, query={"model": model_name}
            )
            if model_name in self.models:
                del self.models[model_name]

        else:
            raise HTTPException(
                status_code=404,
                detail=f"Model '{model_name}' not found in repository.",
            )

    async def history(self) -> HistoryResponse:
        return HistoryResponse.model_validate(
            {
                "history": [
                    PredictionModel.model_validate(prediction)
                    for prediction in await self.repository.list(
                        collection=self.predictions_collection, query={}
                    )
                ]
            }
        )
