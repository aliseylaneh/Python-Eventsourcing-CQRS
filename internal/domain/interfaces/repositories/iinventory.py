import uuid
from abc import ABC, abstractmethod
from collections import deque

from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event


class IInventoryRepository(ABC):
    def __init__(self, collection):
        self._collection = collection

    @abstractmethod
    def create(self, event: Event):
        raise NotImplementedError

    @abstractmethod
    def bulk_insert(self, events: deque[Event]):
        raise NotImplementedError

    @abstractmethod
    def find_by_sku(self, sku: str) -> Inventory | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, pk: uuid) -> Inventory:
        raise NotImplementedError
