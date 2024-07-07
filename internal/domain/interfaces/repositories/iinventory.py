import uuid
from abc import ABC, abstractmethod

from internal.domain.entities.inventory import InventoryProjection


class IInventoryCommandRepository(ABC):

    @abstractmethod
    def create(self, inventory: InventoryProjection) -> InventoryProjection:
        raise NotImplementedError

    @abstractmethod
    def increase_soh(self, inventory: InventoryProjection) -> InventoryProjection:
        raise NotImplementedError

    @abstractmethod
    def decrease_soh(self, inventory: InventoryProjection) -> InventoryProjection:
        raise NotImplementedError

    @abstractmethod
    def reserve(self, inventory: InventoryProjection) -> InventoryProjection:
        raise NotImplementedError


class IInventoryQueryRepository(ABC):

    @abstractmethod
    def find_by_id(self, pk: uuid) -> InventoryProjection | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_sku(self, sku: str) -> InventoryProjection | None:
        raise NotImplementedError
