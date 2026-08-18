from fastapi import APIRouter, Depends, HTTPException

from config.otel import tracer
from src.domain.entities.types.inventory import SKU

from ...commands.inventory_commands import (CompleteReservedStockCommand,
                                            CreateInventoryCommand,
                                            ReserveStockCommand,
                                            UpdateInventoryCommand)
from ...dependencies.inventory_dependencies import (
    get_complete_reserved_command, get_create_inventory_command,
    get_inventory_query, get_reserve_stock_command,
    get_update_inventory_command)
from ...dto.inventory_dto import (CompleteReservedStock, CreateInventory,
                                  InventoryReserveStock, InventoryResponse,
                                  UpdateInventory)
from ...queries.inventory_queries import GetInventoryQuery

router = APIRouter()


@router.patch("/inventory/{sku}/reserve")
async def reserve(
    sku: SKU,
    reserve_stock: InventoryReserveStock,
    command: ReserveStockCommand = Depends(get_reserve_stock_command),
) -> InventoryResponse:
    """
    This endpoint is used when ever there are available stocks for a
    specific Inventory and reserving for a given amount is possible.
    """
    try:
        inventory = await command.execute(
            user_id=reserve_stock.user_id, sku=sku, quantity=reserve_stock.quantity
        )
        response = InventoryResponse(
            sku=inventory.sku,
            soh=inventory.soh,
            reserved=inventory.reserved,
            available_quantity=inventory.available_quantity,
        )
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.patch("/inventory/{sku}/complete")
async def complete(
    sku: SKU,
    complete_reserved_stock: CompleteReservedStock,
    command: CompleteReservedStockCommand = Depends(get_complete_reserved_command),
) -> InventoryResponse:
    """
    This endpoint will process the use case of releasing the amount of reserved for a specific inventory.
    It should be noted which that amount was reserved before using /inventory/{sku}/reserved endpoint.
    """
    try:
        inventory = await command.execute(
            user_id=complete_reserved_stock.user_id,
            sku=sku,
            quantity=complete_reserved_stock.quantity,
        )
        response = InventoryResponse(
            sku=inventory.sku,
            soh=inventory.soh,
            reserved=inventory.reserved,
            available_quantity=inventory.available_quantity,
        )
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.post("/inventory/create")
async def create(
    inventory: CreateInventory,
    command: CreateInventoryCommand = Depends(get_create_inventory_command),
) -> InventoryResponse:
    """
    This endpoint has responsibility of creating a new Inventory if it isn't created before.
    It will raise InventoryDoesExists for already created inventories.
    """
    try:
        inventory = await command.execute(
            user_id=inventory.user_id,
            sku=inventory.sku,
            soh=inventory.soh,
            available_quantity=inventory.available_quantity,
        )
        response = InventoryResponse(
            sku=inventory.sku,
            soh=inventory.soh,
            reserved=inventory.reserved,
            available_quantity=inventory.available_quantity,
        )
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.patch("/inventory/{sku}/update")
async def update(
    sku: SKU,
    inventory: UpdateInventory,
    command: UpdateInventoryCommand = Depends(get_update_inventory_command),
) -> InventoryResponse:
    try:
        inventory = await command.execute(
            user_id=inventory.user_id,
            sku=sku,
            soh=inventory.soh,
            available_quantity=inventory.available_quantity,
        )
        response = InventoryResponse(
            sku=inventory.sku,
            soh=inventory.soh,
            reserved=inventory.reserved,
            available_quantity=inventory.available_quantity,
        )
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.get("/inventory/{sku}")
async def get(
    sku: SKU, command: GetInventoryQuery = Depends(get_inventory_query)
) -> InventoryResponse:
    with tracer.start_as_current_span("get-inventory-api"):
        try:
            response = await command.execute(sku=sku)
            return response
        except Exception as exception:
            raise HTTPException(status_code=400, detail=str(exception))
