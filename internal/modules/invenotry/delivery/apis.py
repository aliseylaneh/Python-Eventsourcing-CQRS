from fastapi import APIRouter, Depends, HTTPException

from internal.domain.entities.inventory import Inventory
from ..commands.inventory import ReserveStockCommand
from ..dependencies.inventory import get_reserve_stock_command
from ..dto.inventory import InventoryReserveStock

router = APIRouter()


@router.post("/inventory/reserve")
def reserve(reserve_stock: InventoryReserveStock, use_case: ReserveStockCommand = Depends(get_reserve_stock_command)):
    try:
        query = use_case.execute(sku=reserve_stock.sku, quantity=reserve_stock.quantity)
        return query
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))
