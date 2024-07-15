from abc import ABC, abstractmethod
from collections import deque

from internal.domain.events.base import Event


class IInventoryRepository(ABC):
    def __init__(self, collection):
        self._collection = collection

    @abstractmethod
    def insert(self, events: deque[Event]):
        raise NotImplementedError

    @abstractmethod
    def find(self, sku: str) -> deque[dict]:
        raise NotImplementedError
