from abc import ABC, abstractmethod

from spacy import Language

from models import HistoryResponse, PredicitionEntities


class BaseNLPService(ABC):
    @abstractmethod
    async def extract_entities(
        self, model_name: str, text: str
    ) -> PredicitionEntities: ...

    @abstractmethod
    async def add_model(self, model_name: str) -> None: ...

    @abstractmethod
    async def load_model(self, model_name: str) -> Language: ...

    @abstractmethod
    async def get_models(self) -> list[str]: ...

    @abstractmethod
    async def delete_model(self, model_name: str) -> None: ...

    @abstractmethod
    async def history(self) -> HistoryResponse: ...
