from abc import ABC, abstractmethod
from collections import deque

from pymongo.asynchronous.database import AsyncDatabase

from internal.domain.events.base import Event


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
