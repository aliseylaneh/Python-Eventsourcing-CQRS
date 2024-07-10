from fastapi import APIRouter, Depends, HTTPException

from internal.domain.entities.inventory import Inventory
from ...commands.inventory import ReserveStockCommand, CreateInventoryCommand
from ...dependencies.inventory import get_reserve_stock_command, get_create_inventory_command
from ...dto.inventory import InventoryReserveStock, CreateInventory, CreateInventoryResponse

router = APIRouter()


@router.post("/inventory/reserve")
def reserve(reserve_stock: InventoryReserveStock, use_case: ReserveStockCommand = Depends(get_reserve_stock_command)):
    try:
        use_case.execute(sku=reserve_stock.sku, quantity=reserve_stock.quantity)
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.post("/inventory")
def create(inventory: CreateInventory,
           use_case: CreateInventoryCommand = Depends(get_create_inventory_command)) -> CreateInventoryResponse:
    inventory = use_case.execute(sku=inventory.sku, soh=inventory.soh, available_quantity=inventory.available_quantity)
    return inventory
