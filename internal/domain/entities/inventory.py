import uuid
from dataclasses import dataclass


@dataclass
class Inventory:
    reference: uuid
    sku: int
    available_quantity: int
    reserved: int

    def reserve(self, quantity: int):
        if self.available_quantity < quantity:
            raise Exception("Out of Stock")
        self.reserved += quantity


inventory_database: set[Inventory] = set()


class InventoryRepository:
    def find_by_sku(self, sku: int) -> Inventory:
        for i in inventory_database:
            if i.sku != sku:
                continue
            return i

    def update(self, inventory: Inventory):
        pass


class ReserveInventoryUseCase:
    def __init__(self):
        self.repository = InventoryRepository()

    def reserve(self, sku: int, quantity: int) -> Inventory:
        inventory = self.repository.find_by_sku(sku=sku)
        inventory.reserve(quantity=quantity)
        self.repository.update(inventory)
        return inventory
