from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Dict

from pymongo.asynchronous.database import AsyncDatabase

from src.domain.events.base import Event


class IInventoryRepository(ABC):
    def __init__(self, db, event_store):
        self._db: AsyncDatabase = db
        self._event_store = event_store

    @abstractmethod
    async def insert(self, events: deque[Event]):
        raise NotImplementedError

    @abstractmethod
    async def find(self, sku: str) -> deque[dict] | None:
        raise NotImplementedError


class IInventoryProjectionRepository(ABC):
    def __init__(self, db: AsyncDatabase, project_store: str):
        self._db: AsyncDatabase = db
        self._projection_store = project_store

    @abstractmethod
    async def create(self, inventory: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find(self, sku: str) -> Dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def set_soh(self, sku: str, soh: int, ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_available_quantity(self, sku: str, available_quantity: int, ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def increase_reserved(self, sku: str, amount: int, ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def decrease_reserved(self, sku: str, amount: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def decrease_soh(self, sku: str, amount: int, ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def decrease_available_quantity(self, sku: str, amount: int, ) -> None:
        raise NotImplementedError
