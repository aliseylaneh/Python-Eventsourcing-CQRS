import uuid
from abc import ABC, abstractmethod

from internal.domain.entities.inventory import Inventory


class IInventoryRepository(ABC):

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
