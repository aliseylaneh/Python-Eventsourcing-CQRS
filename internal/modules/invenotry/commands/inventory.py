from collections import deque
from uuid import UUID

from ..events.v1.inventory import (AvailableQuantityReplacedEvent,
                                   InventoryCreatedEvent,
                                   ProcessedReservedDecreasedEvent,
                                   ReserveQuantityIncreasedEvent,
                                   SOHReplacedEvent, AvailableQuantityDecreasedEvent, ProcessedReservedSOHDecreasedEvent)
from ....domain.commands.commands import BaseCommand
from ....domain.entities.inventory import Inventory
from ....domain.exceptions.inventory import InventoryAlreadyExists, InventoryDoesNotExists


class CreateInventoryCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, soh: int, available_quantity: int) -> Inventory:
        # Check if inventory already exists
        events = await self.event_repository.find(sku=sku)
        inventory_aggregate = self.aggregate(aggregate_id=user_id)
        await inventory_aggregate.apply(events=events)
        if inventory_aggregate.inventory:
            raise InventoryAlreadyExists()
        new_events = await inventory_aggregate.create(sku=sku, soh=soh, available_quantity=available_quantity)
        await self.event_repository.insert(events=new_events)
        return inventory_aggregate.inventory


class ReserveStockCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, quantity: int) -> Inventory:
        events = await self.event_repository.find(sku=sku)
        inventory_aggregate = self.aggregate(aggregate_id=user_id)
        await inventory_aggregate.apply(events=events)
        if not inventory_aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await inventory_aggregate.reserve_stock(quantity=quantity)
        await self.event_repository.insert(events=new_events)
        return inventory_aggregate.inventory


class CompleteReservedStockCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, quantity: int) -> Inventory:
        events = await self.event_repository.find(sku=sku)
        inventory_aggregate = self.aggregate(aggregate_id=user_id)
        await inventory_aggregate.apply(events=events)
        if not inventory_aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await inventory_aggregate.complete_reserved_stock(quantity=quantity)
        await self.event_repository.insert(events=new_events)
        return inventory_aggregate.inventory


class UpdateInventoryCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, soh: int, available_quantity: int) -> Inventory:
        events = await self.event_repository.find(sku=sku)
        inventory_aggregate = self.aggregate(aggregate_id=user_id)
        await inventory_aggregate.apply(events=events)
        if not inventory_aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await inventory_aggregate.update(soh=soh, available_quantity=available_quantity)
        await self.event_repository.insert(events=new_events)
        return inventory_aggregate.inventory
