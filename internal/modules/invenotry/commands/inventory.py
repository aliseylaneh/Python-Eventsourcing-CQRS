from uuid import UUID

from internal.domain.commands.commands import BaseCommand
from internal.domain.entities.inventory import Inventory
from internal.domain.exceptions.inventory import (InventoryAlreadyExists,
                                                  InventoryDoesNotExists)

from ..aggregates.inventory import InventoryAggregate


class CreateInventoryCommand(BaseCommand):
    async def execute(
        self, user_id: UUID, sku: str, soh: int, available_quantity: int
    ) -> Inventory:
        # Check if inventory already exists
        events = await self.event_repository.find(sku=sku)
        inventory_aggregate: InventoryAggregate = self.aggregate()
        await inventory_aggregate.apply(events=events)
        if inventory_aggregate.inventory:
            raise InventoryAlreadyExists()
        new_events = await inventory_aggregate.create(
            user_id=user_id, sku=sku, soh=soh, available_quantity=available_quantity
        )
        await self.event_repository.insert(events=new_events)
        return inventory_aggregate.inventory


class ReserveStockCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, quantity: int) -> Inventory:
        events = await self.event_repository.find(sku=sku)
        inventory_aggregate: InventoryAggregate = self.aggregate()
        await inventory_aggregate.apply(events=events)
        if not inventory_aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await inventory_aggregate.reserve_stock(
            user_id=user_id, quantity=quantity
        )
        await self.event_repository.insert(events=new_events)
        return inventory_aggregate.inventory


class CompleteReservedStockCommand(BaseCommand):
    async def execute(self, user_id: UUID, sku: str, quantity: int) -> Inventory:
        events = await self.event_repository.find(sku=sku)
        inventory_aggregate: InventoryAggregate = self.aggregate()
        await inventory_aggregate.apply(events=events)
        if not inventory_aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await inventory_aggregate.complete_reserved_stock(
            user_id=user_id, quantity=quantity
        )
        await self.event_repository.insert(events=new_events)
        return inventory_aggregate.inventory


class UpdateInventoryCommand(BaseCommand):
    async def execute(
        self, user_id: UUID, sku: str, soh: int, available_quantity: int
    ) -> Inventory:
        events = await self.event_repository.find(sku=sku)
        inventory_aggregate: InventoryAggregate = self.aggregate()
        await inventory_aggregate.apply(events=events)
        if not inventory_aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await inventory_aggregate.update(
            user_id=user_id, soh=soh, available_quantity=available_quantity
        )
        await self.event_repository.insert(events=new_events)
        return inventory_aggregate.inventory
