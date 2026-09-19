from abc import ABC
from uuid import UUID

from src.domain.commands.commands import BaseCommand
from src.domain.entities.inventory import Inventory
from src.domain.exceptions.inventory import (InventoryAlreadyExists,
                                             InventoryDoesNotExists)
from src.domain.interfaces.repositories.iinventory import \
    IMongoInventoryWriteRepository
from src.modules.invenotry.aggregates.inventory_aggregate import \
    InventoryAggregate


class InventoryCommand(BaseCommand, ABC):
    """
    Shared write-side command that loads an InventoryAggregate and an event repository.
    Each execute first rebuilds aggregate state from the event stream, then appends new events.
    """

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
        """
        Create a new inventory stream when no events exist for the sku.
        Existing reconstructed inventory raises InventoryAlreadyExists.
        :param user_id: user that initiated the command
        :param sku: sku
        :param soh: initial stock on hand
        :param available_quantity: initial available quantity
        :return: created inventory state
        """
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
        """
        Reserve quantity from an existing inventory and persist the generated events.
        :param user_id: user that initiated the command
        :param sku: sku
        :param quantity: quantity to reserve
        :return: inventory state after reservation
        """
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
        """
        Complete previously reserved stock and persist the generated events.
        Reserved is decreased and soh is decreased, available quantity stays as it was after reserve.
        :param user_id: user that initiated the command
        :param sku: sku
        :param quantity: reserved quantity to complete
        :return: inventory state after completion
        """
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
        """
        Replace soh and available quantity of an existing inventory and persist the generated events.
        :param user_id: user that initiated the command
        :param sku: sku
        :param soh: new stock on hand
        :param available_quantity: new available quantity
        :return: inventory state after update
        """
        events = await self.event_repository.find(sku=sku)
        await self._aggregate.apply(events=events)
        if not self._aggregate.inventory:
            raise InventoryDoesNotExists()
        new_events = await self._aggregate.update(
            user_id=user_id, soh=soh, available_quantity=available_quantity
        )
        await self.event_repository.insert(events=new_events)
        return self._aggregate.inventory
