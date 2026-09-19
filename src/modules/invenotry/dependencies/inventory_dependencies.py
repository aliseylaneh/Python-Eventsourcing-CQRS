import asyncio

from fastapi import Depends
from pymongo.asynchronous.database import AsyncDatabase

from adapter.mongo import db, event_collection, outbox_collection
from src.domain.interfaces.repositories.iinventory import (
    IMongoInventoryReadRepository, IMongoInventoryWriteRepository)
from src.modules.invenotry.aggregates.inventory_aggregate import \
    InventoryAggregate
from src.modules.invenotry.commands.inventory_commands import (
    CompleteReservedStockCommand, CreateInventoryCommand, ReserveStockCommand,
    UpdateInventoryCommand)
from src.modules.invenotry.queries.inventory_queries import GetInventoryQuery
from src.modules.invenotry.repositories.inventory_mongo_repository import (
    INVENTORY_PROJECTION_COLLECTION, InventoryReadRepository,
    InventoryWriteRepository)
from src.modules.invenotry.tasks.inventory_workers import \
    run_inventory_projection_worker

_projection_worker: asyncio.Task | None = None


def _ensure_projection_worker() -> None:
    """
    Start the outbox projection worker once on the first inventory request.
    FastAPI Depends is used instead of app lifespan because this module lives under src.
    :return:
    """
    global _projection_worker
    if _projection_worker is None or _projection_worker.done():
        _projection_worker = asyncio.create_task(run_inventory_projection_worker())


async def get_mongo_inventory_db() -> AsyncDatabase:
    """
    Return the shared Mongo database and make sure the projection worker is running.
    :return: inventory AsyncDatabase
    """
    _ensure_projection_worker()
    return db


async def inventory_event_repository(
    mongo_inventory_db: AsyncDatabase = Depends(get_mongo_inventory_db),
) -> IMongoInventoryWriteRepository:
    """
    Build the write repository that talks to event store and outbox collections.
    :param mongo_inventory_db: inventory database
    :return: IMongoInventoryWriteRepository
    """
    return InventoryWriteRepository(
        db=mongo_inventory_db,
        event_collection=event_collection,
        outbox_collection=outbox_collection,
    )


async def inventory_read_repository(
    mongo_inventory_db: AsyncDatabase = Depends(get_mongo_inventory_db),
) -> IMongoInventoryReadRepository:
    """
    Build the read repository that talks to the inventory projection collection.
    :param mongo_inventory_db: inventory database
    :return: IMongoInventoryReadRepository
    """
    return InventoryReadRepository(
        db=mongo_inventory_db,
        projection_store=INVENTORY_PROJECTION_COLLECTION,
    )


async def inventory_aggregate() -> InventoryAggregate:
    """
    Create a new InventoryAggregate instance per request so command state is not shared.
    :return: InventoryAggregate
    """
    return InventoryAggregate()


async def get_reserve_stock_command(
    aggregate: InventoryAggregate = Depends(inventory_aggregate),
    event_repository: IMongoInventoryWriteRepository = Depends(
        inventory_event_repository
    ),
) -> ReserveStockCommand:
    """
    Wire ReserveStockCommand with a fresh aggregate and the event repository.
    :param aggregate: inventory aggregate
    :param event_repository: event store
    :return: ReserveStockCommand
    """
    return ReserveStockCommand(
        aggregate=aggregate, event_repository=event_repository
    )


async def get_create_inventory_command(
    aggregate: InventoryAggregate = Depends(inventory_aggregate),
    event_repository: IMongoInventoryWriteRepository = Depends(
        inventory_event_repository
    ),
) -> CreateInventoryCommand:
    """
    Wire CreateInventoryCommand with a fresh aggregate and the event repository.
    :param aggregate: inventory aggregate
    :param event_repository: event store
    :return: CreateInventoryCommand
    """
    return CreateInventoryCommand(
        aggregate=aggregate, event_repository=event_repository
    )


async def get_update_inventory_command(
    aggregate: InventoryAggregate = Depends(inventory_aggregate),
    event_repository: IMongoInventoryWriteRepository = Depends(
        inventory_event_repository
    ),
) -> UpdateInventoryCommand:
    """
    Wire UpdateInventoryCommand with a fresh aggregate and the event repository.
    :param aggregate: inventory aggregate
    :param event_repository: event store
    :return: UpdateInventoryCommand
    """
    return UpdateInventoryCommand(
        aggregate=aggregate, event_repository=event_repository
    )


async def get_complete_reserved_command(
    aggregate: InventoryAggregate = Depends(inventory_aggregate),
    event_repository: IMongoInventoryWriteRepository = Depends(
        inventory_event_repository
    ),
) -> CompleteReservedStockCommand:
    """
    Wire CompleteReservedStockCommand with a fresh aggregate and the event repository.
    :param aggregate: inventory aggregate
    :param event_repository: event store
    :return: CompleteReservedStockCommand
    """
    return CompleteReservedStockCommand(
        aggregate=aggregate, event_repository=event_repository
    )


async def get_inventory_query(
    repository: IMongoInventoryReadRepository = Depends(inventory_read_repository),
) -> GetInventoryQuery:
    """
    Wire GetInventoryQuery with the projection repository, not the event store.
    :param repository: inventory read repository
    :return: GetInventoryQuery
    """
    return GetInventoryQuery(repository=repository)
