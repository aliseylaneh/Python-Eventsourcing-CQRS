from fastapi import APIRouter, Depends, HTTPException

from internal.domain.entities.inventory import Inventory
from ...commands.inventory import ReserveStockCommand, CreateInventoryCommand
from ...dependencies.inventory import get_reserve_stock_command, get_create_inventory_command
from ...dto.inventory import InventoryReserveStock, CreateInventory, InventoryResponse

router = APIRouter()


@router.post("/inventory/reserve")
def reserve(reserve_stock: InventoryReserveStock,
            use_case: ReserveStockCommand = Depends(get_reserve_stock_command)) -> InventoryResponse:
    try:
        inventory = use_case.execute(sku=reserve_stock.sku, quantity=reserve_stock.quantity)
        response = InventoryResponse(sku=inventory.sku,
                                     soh=inventory.soh,
                                     reserved=inventory.reserved,
                                     available_quantity=inventory.available_quantity)
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=exception.args)


@router.post("/inventory")
def create(inventory: CreateInventory,
           use_case: CreateInventoryCommand = Depends(get_create_inventory_command)) -> InventoryResponse:
    try:
        inventory = use_case.execute(sku=inventory.sku, soh=inventory.soh, available_quantity=inventory.available_quantity)
        response = InventoryResponse(sku=inventory.sku,
                                     soh=inventory.soh,
                                     reserved=inventory.reserved,
                                     available_quantity=inventory.available_quantity)
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=exception.args)
