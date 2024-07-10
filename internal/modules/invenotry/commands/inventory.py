from collections import deque

from ..events.v1.inventory import ReserveQuantityIncreasedEvent, InventoryCreatedEvent
from ....domain.commands.commands import BaseCommand


class ReserveStockCommand(BaseCommand):
    def execute(self, sku: str, quantity: int):
        with self.aggregate:
            self.aggregate.apply(events=deque([ReserveQuantityIncreasedEvent(sku=sku, quantity=quantity)]))


class CreateInventoryCommand(BaseCommand):
    def execute(self, sku: str, soh: int, available_quantity: int):
        with self.aggregate:
            self.aggregate.apply(events=deque([InventoryCreatedEvent(sku=sku, soh=soh, available_quantity=available_quantity)]))
