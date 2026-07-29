from collections import deque
from uuid import UUID

from ..events.v1.inventory import (AvailableQuantityReplacedEvent,
                                   InventoryCreatedEvent,
                                   ProcessedReservedDecreasedEvent,
                                   ReserveQuantityIncreasedEvent,
                                   SOHReplacedEvent)
from ....domain.commands.commands import BaseCommand
from ....domain.entities.inventory import Inventory


class CreateInventoryCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, soh: int, available_quantity: int) -> Inventory:
        # Check if inventory already exists
        event = InventoryCreatedEvent(sku=sku, soh=soh, available_quantity=available_quantity)
        await self.aggregate(aggregate_id=user_id).apply(events=deque([event]))
        return self.aggregate.inventory


class ReserveStockCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, quantity: int) -> Inventory:
        event = ReserveQuantityIncreasedEvent(sku=sku, reserved=quantity)
        await self.aggregate(aggregate_id=user_id).apply(events=deque([event]))
        return self.aggregate.inventory


class UpdateInventoryCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, soh: int, available_quantity: int) -> Inventory:
        replace_soh_event = SOHReplacedEvent(sku=sku, soh=soh)
        replace_available_quantity_event = AvailableQuantityReplacedEvent(sku=sku, available_quantity=available_quantity)
        await self.aggregate(aggregate_id=user_id).apply(events=deque([replace_soh_event, replace_available_quantity_event]))
        return self.aggregate.inventory


class CompleteReservedCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, quantity: int) -> Inventory:
        event = ProcessedReservedDecreasedEvent(sku=sku, reserved=quantity)
        await self.aggregate(aggregate_id=user_id).apply(deque([event]))
        return self.aggregate.inventory
