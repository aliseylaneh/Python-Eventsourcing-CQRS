from internal.domain.entities.inventory import Inventory
from internal.domain.events.v1.inventory import StockReservedEvent, SOHDecreasedEvent, SOHIncreasedEvent, InventoryCreatedEvent
from internal.domain.interfaces.repositories.iinventory import IInventoryCommandRepository


class InventoryMongoCommandRepository(IInventoryCommandRepository):

    def create(self, inventory: Inventory) -> Inventory:
        pass

    def increase_soh(self, inventory: Inventory) -> Inventory:
        pass

    def decrease_soh(self, inventory: Inventory) -> Inventory:
        pass

    def reserve(self, event: StockReservedEvent) -> Inventory:
        pass
