import uuid
from abc import ABC, abstractmethod

from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event


class IInventoryRepository(ABC):
    def __init__(self, collection, events_collection):
        self._collection = collection
        self._events_collection = events_collection

    @abstractmethod
    def save_events(self, event: list[Event]):
        raise NotImplementedError

    @abstractmethod
    def create(self, inventory: Inventory) -> Inventory:
        raise NotImplementedError

    @abstractmethod
    def update_soh(self, inventory: Inventory) -> Inventory:
        raise NotImplementedError

    @abstractmethod
    def reserve(self, inventory: Inventory) -> Inventory:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, pk: uuid) -> Inventory | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_sku(self, sku: str) -> Inventory | None:
        raise NotImplementedError
