from typing import Type

from fastapi import Depends

from adapter.mongo import db
from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.aggregates.inventory import InventoryAggregate
from internal.modules.invenotry.commands.inventory import CompleteReservedCommand, CreateInventoryCommand, ReserveStockCommand, \
    UpdateInventoryCommand
from internal.modules.invenotry.queries.inventory import GetInventoryQuery
from internal.modules.invenotry.repositories.mongo_inventory import InventoryMongoRepository


async def get_inventory_events_collection():
    return db['inventory_events']


async def inventory_repository(collection=Depends(get_inventory_events_collection)) -> IInventoryRepository:
    return InventoryMongoRepository(collection=collection)


async def inventory_aggregate() -> InventoryAggregate:
    return InventoryAggregate


async def get_reserve_stock_command(aggregate: Type[AggregateRoot] = Depends(inventory_aggregate)) -> ReserveStockCommand:
    return ReserveStockCommand(aggregate=aggregate)


async def get_create_inventory_command(aggregate: Type[AggregateRoot] = Depends(inventory_aggregate)) -> CreateInventoryCommand:
    return CreateInventoryCommand(aggregate=aggregate)


async def get_update_inventory_command(aggregate: Type[AggregateRoot] = Depends(inventory_aggregate)) -> UpdateInventoryCommand:
    return UpdateInventoryCommand(aggregate=aggregate)


async def get_complete_reserved_command(aggregate: Type[AggregateRoot] = Depends(inventory_aggregate)) -> CompleteReservedCommand:
    return CompleteReservedCommand(aggregate=aggregate)


async def get_inventory_query(repository: IInventoryRepository = Depends(inventory_repository)) -> GetInventoryQuery:
    return GetInventoryQuery(repository=repository)
