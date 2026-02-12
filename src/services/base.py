from abc import ABC, abstractmethod

from spacy import Language


class BaseNLPService(ABC):
    @abstractmethod
    async def extract_entities(self, model_name: str, text: str) -> dict: ...

    @abstractmethod
    async def load_model(self, model_name: str) -> Language: ...

    @abstractmethod
    async def delete_model(self, model_name: str) -> None: ...
