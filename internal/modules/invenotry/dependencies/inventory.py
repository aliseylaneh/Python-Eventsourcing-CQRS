from fastapi import Depends

from adapter.mongo import mongo_db_connection
from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.aggregates.inventory import InventoryAggregate
from internal.modules.invenotry.commands.inventory import CompleteReservedCommand, CreateInventoryCommand, ReserveStockCommand, \
    UpdateInventoryCommand
from internal.modules.invenotry.queries.inventory import GetInventoryQuery
from internal.modules.invenotry.repositories.mongo_inventory import InventoryMongoRepository


def get_inventory_collection():
    return mongo_db_connection()['inventory']


def inventory_repository(collection=Depends(get_inventory_collection)) -> IInventoryRepository:
    return InventoryMongoRepository(collection=collection)


def inventory_aggregate(repository: IInventoryRepository = Depends(inventory_repository)) -> InventoryAggregate:
    return InventoryAggregate(repository=repository)


def get_reserve_stock_command(aggregate: AggregateRoot = Depends(inventory_aggregate)) -> ReserveStockCommand:
    return ReserveStockCommand(aggregate=aggregate)


def get_create_inventory_command(aggregate: AggregateRoot = Depends(inventory_aggregate)) -> CreateInventoryCommand:
    return CreateInventoryCommand(aggregate=aggregate)


def get_update_inventory_command(aggregate: AggregateRoot = Depends(inventory_aggregate)) -> UpdateInventoryCommand:
    return UpdateInventoryCommand(aggregate=aggregate)


def get_complete_reserved_command(aggregate: AggregateRoot = Depends(inventory_aggregate)) -> CompleteReservedCommand:
    return CompleteReservedCommand(aggregate=aggregate)


def get_inventory_query(repository: IInventoryRepository = Depends(inventory_repository)) -> GetInventoryQuery:
    return GetInventoryQuery(repository=repository)
