from collections import deque

from ..dto.inventory import InventoryResponse
from ..events.v1.inventory import ReserveQuantityIncreasedEvent, InventoryCreatedEvent
from ....domain.commands.commands import BaseCommand
from ....domain.entities.inventory import Inventory


class ReserveStockCommand(BaseCommand):
    def execute(self, sku: str, quantity: int) -> Inventory:
        with self.aggregate:
            event = ReserveQuantityIncreasedEvent(sku=sku, reserved=quantity)
            self.aggregate.apply(events=deque([event]))
        return self.aggregate.inventory


class CreateInventoryCommand(BaseCommand):
    def execute(self, sku: str, soh: int, available_quantity: int) -> Inventory:
        with self.aggregate:
            event = InventoryCreatedEvent(sku=sku, soh=soh, available_quantity=available_quantity)
            self.aggregate.apply(events=deque([event]))
        return self.aggregate.inventory
