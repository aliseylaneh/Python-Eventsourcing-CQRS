from abc import ABC
from uuid import UUID

from domain.interfaces.repositories.iinventory import \
    IMongoInventoryWriteRepository
from src.domain.commands.commands import BaseCommand
from src.domain.entities.inventory import Inventory
from src.domain.exceptions.inventory import (InventoryAlreadyExists,
                                             InventoryDoesNotExists)
from src.modules.invenotry.aggregates.inventory_aggregate import \
    InventoryAggregate


class InventoryCommand(BaseCommand, ABC):
    def __init__(
        self,
        aggregate: InventoryAggregate,
        event_repository: IMongoInventoryWriteRepository,
    ):
        super(InventoryCommand, self).__init__(event_repository=event_repository)
        self._aggregate: InventoryAggregate = aggregate


class CreateInventoryCommand(InventoryCommand):
    async def execute(
        self, user_id: UUID, sku: str, soh: int, available_quantity: int
    ) -> Inventory:
        # Check if inventory already exists
        events = await self.event_repository.find(sku=sku)
        await self._aggregate.apply(events=events)
        if self._aggregate.inventory:
            raise InventoryAlreadyExists()
        new_events = await self._aggregate.create(
            user_id=user_id, sku=sku, soh=soh, available_quantity=available_quantity
        )
        await self.event_repository.insert(events=new_events)
        return self._aggregate.inventory


class ReserveStockCommand(InventoryCommand):
    async def execute(self, user_id: UUID, sku: str, quantity: int) -> Inventory:
        events = await self.event_repository.find(sku=sku)
        await self._aggregate.apply(events=events)
        if not self._aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await self._aggregate.reserve_stock(
            user_id=user_id, quantity=quantity
        )
        await self.event_repository.insert(events=new_events)
        return self._aggregate.inventory


class CompleteReservedStockCommand(InventoryCommand):
    async def execute(self, user_id: UUID, sku: str, quantity: int) -> Inventory:
        events = await self.event_repository.find(sku=sku)
        await self._aggregate.apply(events=events)
        if not self._aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await self._aggregate.complete_reserved_stock(
            user_id=user_id, quantity=quantity
        )
        await self.event_repository.insert(events=new_events)
        return self._aggregate.inventory


class UpdateInventoryCommand(InventoryCommand):
    async def execute(
        self, user_id: UUID, sku: str, soh: int, available_quantity: int
    ) -> Inventory:
        events = await self.event_repository.find(sku=sku)

        await self._aggregate.apply(events=events)
        if not self._aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await self._aggregate.update(
            user_id=user_id, soh=soh, available_quantity=available_quantity
        )
        await self.event_repository.insert(events=new_events)
        return self._aggregate.inventory
