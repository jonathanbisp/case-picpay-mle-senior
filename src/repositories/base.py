from abc import ABC, abstractmethod
from typing import Any, List


class BaseRepository(ABC):
    @abstractmethod
    async def find(self, collection: str, query: dict) -> Any | None: ...

    @abstractmethod
    async def write(self, collection: str, data: dict) -> dict: ...

    @abstractmethod
    async def update(self, collection: str, query: dict, data: dict) -> Any | None: ...

    @abstractmethod
    async def delete(self, collection: str, query: dict) -> Any | None: ...

    @abstractmethod
    async def list(self, collection: str, query: dict) -> List[dict]: ...

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def is_healthy(self) -> bool: ...
