import uuid

from internal.domain.entities.inventory import InventoryProjection
from internal.domain.interfaces.repositories.iinventory import IInventoryCommandRepository, IInventoryQueryRepository


class InventoryElasticSearchCommandRepository(IInventoryCommandRepository):

    def reserve(self, inventory: InventoryProjection) -> InventoryProjection:
        pass

    def create(self, inventory: InventoryProjection) -> InventoryProjection:
        pass

    def increase_soh(self, inventory: InventoryProjection) -> InventoryProjection:
        pass

    def decrease_soh(self, inventory: InventoryProjection) -> InventoryProjection:
        pass


class InventoryElasticSearchQueryRepository(IInventoryQueryRepository):
    def find_by_id(self, pk: uuid) -> InventoryProjection | None:
        pass

    def find_by_sku(self, sku: str) -> InventoryProjection | None:
        pass
