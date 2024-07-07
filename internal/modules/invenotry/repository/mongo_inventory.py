from internal.domain.entities.inventory import Inventory
from internal.domain.interfaces.repositories.iinventory import IInventoryCommandRepository


class InventoryMongoCommandRepository(IInventoryCommandRepository):

    def reserve(self, inventory: Inventory) -> Inventory:
        pass

    def create(self, inventory: Inventory) -> Inventory:
        pass

    def increase_soh(self, inventory: Inventory) -> Inventory:
        pass

    def decrease_soh(self, inventory: Inventory) -> Inventory:
        pass

