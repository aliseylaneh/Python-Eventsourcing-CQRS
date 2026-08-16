from typing import Type

from fastapi import Depends
from pymongo import AsyncMongoClient

from adapter.mongo import db, event_collection, outbox_collection
from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.interfaces.repositories.iinventory import \
    IInventoryRepository
from internal.modules.invenotry.aggregates.inventory import InventoryAggregate
from internal.modules.invenotry.commands.inventory import (
    CompleteReservedStockCommand, CreateInventoryCommand, ReserveStockCommand,
    UpdateInventoryCommand)
from internal.modules.invenotry.queries.inventory import GetInventoryQuery
from internal.modules.invenotry.repositories.mongo_inventory import \
    InventoryMongoRepository


async def get_mongo_inventory_db():
    return db


async def inventory_event_repository(
    mongo_inventory_db: AsyncMongoClient = Depends(get_mongo_inventory_db),
) -> IInventoryRepository:
    return InventoryMongoRepository(
        db=mongo_inventory_db,
        event_store=event_collection,
        outbox_store=outbox_collection,
    )


async def inventory_aggregate() -> InventoryAggregate:
    return InventoryAggregate


async def get_reserve_stock_command(
    aggregate: Type[AggregateRoot] = Depends(inventory_aggregate),
    event_repository: IInventoryRepository = Depends(inventory_event_repository),
) -> ReserveStockCommand:
    return ReserveStockCommand(aggregate=aggregate, event_repository=event_repository)


async def get_create_inventory_command(
    aggregate: Type[AggregateRoot] = Depends(inventory_aggregate),
    event_repository: IInventoryRepository = Depends(inventory_event_repository),
) -> CreateInventoryCommand:
    return CreateInventoryCommand(
        aggregate=aggregate, event_repository=event_repository
    )


async def get_update_inventory_command(
    aggregate: Type[AggregateRoot] = Depends(inventory_aggregate),
    event_repository: IInventoryRepository = Depends(inventory_event_repository),
) -> UpdateInventoryCommand:
    return UpdateInventoryCommand(
        aggregate=aggregate, event_repository=event_repository
    )


async def get_complete_reserved_command(
    aggregate: Type[AggregateRoot] = Depends(inventory_aggregate),
    event_repository: IInventoryRepository = Depends(inventory_event_repository),
) -> CompleteReservedStockCommand:
    return CompleteReservedStockCommand(
        aggregate=aggregate, event_repository=event_repository
    )


async def get_inventory_query(
    repository: IInventoryRepository = Depends(inventory_event_repository),
) -> GetInventoryQuery:
    return GetInventoryQuery(repository=repository)
