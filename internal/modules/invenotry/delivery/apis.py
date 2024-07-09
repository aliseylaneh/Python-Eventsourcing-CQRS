from fastapi import APIRouter, Depends

from internal.domain.entities.inventory import Inventory
from ..commands.inventory import ReserveStockCommand
from ..dependencies.inventory import get_reserve_stock_command
from ..dto.inventory import InventoryReserveStock

router = APIRouter()


@router.post("/inventory/reserve")
def reserve(reserve_stock: InventoryReserveStock, use_case: ReserveStockCommand = Depends(get_reserve_stock_command)):
    query = use_case.execute(sku=reserve_stock.sku, quantity=reserve_stock.quantity)
    return query
