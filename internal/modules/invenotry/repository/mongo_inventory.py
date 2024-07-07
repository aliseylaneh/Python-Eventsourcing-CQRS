from internal.domain.entities.inventory import InventoryProjection
from internal.domain.interfaces.repositories.iinventory import IInventoryCommandRepository


class InventoryMongoCommandRepository(IInventoryCommandRepository):

    def reserve(self, inventory: InventoryProjection) -> InventoryProjection:
        pass

    def create(self, inventory: InventoryProjection) -> InventoryProjection:
        pass

    def increase_soh(self, inventory: InventoryProjection) -> InventoryProjection:
        pass

    def decrease_soh(self, inventory: InventoryProjection) -> InventoryProjection:
        pass

