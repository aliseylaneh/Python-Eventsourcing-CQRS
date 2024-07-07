import uuid

from internal.domain.entities.inventory import Inventory
from internal.domain.interfaces.repositories.iinventory import IInventoryCommandRepository, IInventoryQueryRepository


class InventoryElasticSearchCommandRepository(IInventoryCommandRepository):

    def reserve(self, inventory: Inventory) -> Inventory:
        pass

    def create(self, inventory: Inventory) -> Inventory:
        pass

    def increase_soh(self, inventory: Inventory) -> Inventory:
        pass

    def decrease_soh(self, inventory: Inventory) -> Inventory:
        pass


class InventoryElasticSearchQueryRepository(IInventoryQueryRepository):
    def find_by_id(self, pk: uuid) -> Inventory | None:
        pass

    def find_by_sku(self, sku: str) -> Inventory | None:
        pass
