from collections import deque

from ..events.v1.inventory import (AvailableQuantityReplacedEvent,
                                   InventoryCreatedEvent,
                                   ProcessedReservedDecreasedEvent,
                                   ReserveQuantityIncreasedEvent,
                                   SOHReplacedEvent)
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


class UpdateInventoryCommand(BaseCommand):
    def execute(self, sku: str, soh: int, available_quantity: int) -> Inventory:
        with self.aggregate:
            replace_soh_event = SOHReplacedEvent(sku=sku, soh=soh)
            replace_available_quantity_event = AvailableQuantityReplacedEvent(sku=sku, available_quantity=available_quantity)
            self.aggregate.apply(events=deque([replace_soh_event, replace_available_quantity_event]))
        return self.aggregate.inventory


class CompleteReservedCommand(BaseCommand):
    def execute(self, sku: int, quantity: int) -> Inventory:
        with self.aggregate:
            event = ProcessedReservedDecreasedEvent(sku=sku, reserved=quantity)
            self.aggregate.apply(deque([event]))
        return self.aggregate.inventory
