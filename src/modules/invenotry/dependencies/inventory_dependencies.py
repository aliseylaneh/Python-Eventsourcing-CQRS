from typing import Type

from fastapi import Depends
from pymongo import AsyncMongoClient

from adapter.mongo import db, event_collection
from domain.interfaces.repositories.iinventory import \
    IMongoInventoryReadRepository
from src.domain.aggregates.base import AggregateRoot
from src.domain.interfaces.repositories.iinventory import \
    IMongoInventoryWriteRepository
from src.modules.invenotry.aggregates.inventory_aggregate import \
    InventoryAggregate
from src.modules.invenotry.commands.inventory_commands import (
    CompleteReservedStockCommand, CreateInventoryCommand, ReserveStockCommand,
    UpdateInventoryCommand)
from src.modules.invenotry.queries.inventory_queries import GetInventoryQuery
from src.modules.invenotry.repositories.inventory_mongo_repository import \
    InventoryWriteRepository


async def get_mongo_inventory_db():
    return db


async def inventory_event_repository(
    mongo_inventory_db: AsyncMongoClient = Depends(get_mongo_inventory_db),
) -> IMongoInventoryWriteRepository:
    return InventoryWriteRepository(
        db=mongo_inventory_db,
        event_collection=event_collection,
    )


async def inventory_aggregate() -> InventoryAggregate:
    return InventoryAggregate


async def get_reserve_stock_command(
    event_repository: IMongoInventoryWriteRepository = Depends(
        inventory_event_repository
    ),
) -> ReserveStockCommand:
    return ReserveStockCommand(event_repository=event_repository)


async def get_create_inventory_command(
    event_repository: IMongoInventoryWriteRepository = Depends(
        inventory_event_repository
    ),
) -> CreateInventoryCommand:
    return CreateInventoryCommand(event_repository=event_repository)


async def get_update_inventory_command(
    aggregate: Type[AggregateRoot] = Depends(inventory_aggregate),
    event_repository: IMongoInventoryWriteRepository = Depends(
        inventory_event_repository
    ),
) -> UpdateInventoryCommand:
    return UpdateInventoryCommand(event_repository=event_repository)


async def get_complete_reserved_command(
    event_repository: IMongoInventoryWriteRepository = Depends(
        inventory_event_repository
    ),
) -> CompleteReservedStockCommand:
    return CompleteReservedStockCommand(event_repository=event_repository)


async def get_inventory_query(
    repository: IMongoInventoryReadRepository = Depends(inventory_event_repository),
) -> GetInventoryQuery:
    return GetInventoryQuery(repository=repository)
