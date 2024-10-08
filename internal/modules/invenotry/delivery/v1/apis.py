from fastapi import APIRouter, Depends, HTTPException

from config.otel import tracer
from internal.domain.entities.types.inventory import SKU
from ...commands.inventory import CompleteReservedCommand
from ...commands.inventory import CreateInventoryCommand, ReserveStockCommand, UpdateInventoryCommand
from ...dependencies.inventory import get_complete_reserved_command
from ...dependencies.inventory import get_create_inventory_command, get_inventory_query, get_reserve_stock_command, \
    get_update_inventory_command
from ...dto.inventory import CompleteReservedStock
from ...dto.inventory import CreateInventory, InventoryReserveStock, InventoryResponse, UpdateInventory
from ...queries.inventory import GetInventoryQuery

router = APIRouter()


@router.patch("/inventory/{sku}/reserve")
def reserve(sku: SKU, reserve_stock: InventoryReserveStock,
            use_case: ReserveStockCommand = Depends(get_reserve_stock_command)) -> InventoryResponse:
    """
    This endpoint is used when ever there are available stocks for a specific Inventory and reserving for a given amount is possible.
    """
    try:
        inventory = use_case.execute(sku=sku, quantity=reserve_stock.quantity)
        response = InventoryResponse(sku=inventory.sku,
                                     soh=inventory.soh,
                                     reserved=inventory.reserved,
                                     available_quantity=inventory.available_quantity)
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.patch("/inventory/{sku}/complete")
def complete(sku: SKU, complete_reserved_stock: CompleteReservedStock,
             use_case: CompleteReservedCommand = Depends(get_complete_reserved_command)) -> InventoryResponse:
    """
    This endpoint will process the use case of releasing the amount of reserved for a specific inventory.
    It should be noted which that amount was reserved before using /inventory/{sku}/reserved endpoint.
    """
    try:
        inventory = use_case.execute(sku=sku, quantity=complete_reserved_stock.quantity)
        response = InventoryResponse(sku=inventory.sku,
                                     soh=inventory.soh,
                                     reserved=inventory.reserved,
                                     available_quantity=inventory.available_quantity)
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.post("/inventory/create")
def create(inventory: CreateInventory,
           use_case: CreateInventoryCommand = Depends(get_create_inventory_command)) -> InventoryResponse:
    """
    This endpoint has responsibility of creating a new Inventory if it isn't created before.
    It will raise InventoryDoesExists for already created inventories.
    """
    try:
        inventory = use_case.execute(sku=inventory.sku, soh=inventory.soh, available_quantity=inventory.available_quantity)
        response = InventoryResponse(sku=inventory.sku,
                                     soh=inventory.soh,
                                     reserved=inventory.reserved,
                                     available_quantity=inventory.available_quantity)
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.patch("/inventory/{sku}/update")
def update(sku: SKU, inventory: UpdateInventory,
           use_case: UpdateInventoryCommand = Depends(get_update_inventory_command)) -> InventoryResponse:
    try:
        inventory = use_case.execute(sku=sku,
                                     soh=inventory.soh,
                                     available_quantity=inventory.available_quantity)
        response = InventoryResponse(sku=inventory.sku,
                                     soh=inventory.soh,
                                     reserved=inventory.reserved,
                                     available_quantity=inventory.available_quantity)
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.get("/inventory/{sku}")
def get(sku: SKU, use_case: GetInventoryQuery = Depends(get_inventory_query)) -> InventoryResponse:
    with tracer.start_as_current_span('get-inventory-api') as span:
        try:
            inventory = use_case.execute(sku=sku)
            response = InventoryResponse(sku=inventory.sku,
                                         soh=inventory.soh,
                                         reserved=inventory.reserved,
                                         available_quantity=inventory.available_quantity)
            return response
        except Exception as exception:
            raise HTTPException(status_code=400, detail=str(exception))
