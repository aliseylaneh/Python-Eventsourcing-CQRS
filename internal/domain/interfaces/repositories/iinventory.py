import uuid
from abc import ABC, abstractmethod

from internal.domain.entities.inventory import Inventory


class IInventoryRepository(ABC):

    @abstractmethod
    def find_by_id(self, pk: uuid) -> Inventory | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_sku(self, sku: str) -> Inventory | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, new_inventory: Inventory) -> Inventory:
        raise NotImplementedError

    @abstractmethod
    def update(self, inventory: Inventory) -> Inventory:
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk: uuid) -> Inventory:
        raise NotImplementedError

    @abstractmethod
    def search(self, reference: str) -> list[Inventory]:
        raise NotImplementedError
