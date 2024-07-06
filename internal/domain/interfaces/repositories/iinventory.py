import uuid
from abc import ABC, abstractmethod

from internal.domain.entities.inventory import Inventory


class IInventoryCommandRepository(ABC):

    @abstractmethod
    def create(self, inventory: Inventory) -> Inventory:
        raise NotImplementedError

    @abstractmethod
    def increase_soh(self, inventory: Inventory) -> Inventory:
        raise NotImplementedError

    @abstractmethod
    def decrease_soh(self, inventory: Inventory) -> Inventory:
        raise NotImplementedError

    @abstractmethod
    def reserve(self, inventory: Inventory) -> Inventory:
        raise NotImplementedError


class IInventoryQueryRepository(ABC):

    @abstractmethod
    def find_by_id(self, pk: uuid) -> Inventory | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_sku(self, sku: str) -> Inventory | None:
        raise NotImplementedError
