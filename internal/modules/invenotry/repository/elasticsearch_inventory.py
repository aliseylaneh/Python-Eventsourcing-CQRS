import uuid

from internal.domain.entities.inventory import Inventory
from internal.domain.events.v1.inventory import StockReservedEvent, SOHDecreasedEvent, SOHIncreasedEvent, InventoryCreatedEvent
from internal.domain.interfaces.repositories.iinventory import IInventoryCommandRepository, IInventoryQueryRepository


class InventoryElasticSearchCommandRepository(IInventoryCommandRepository):
    def create(self, event: InventoryCreatedEvent) -> Inventory:
        pass

    def increase_soh(self, event: SOHIncreasedEvent) -> Inventory:
        pass

    def decrease_soh(self, event: SOHDecreasedEvent) -> Inventory:
        pass

    def reserve(self, event: StockReservedEvent) -> Inventory:
        pass


class InventoryElasticSearchQueryRepository(IInventoryQueryRepository):
    def find_by_id(self, pk: uuid) -> Inventory | None:
        pass

    def find_by_sku(self, sku: str) -> Inventory | None:
        pass
