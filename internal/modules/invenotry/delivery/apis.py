from fastapi import Depends, APIRouter, HTTPException

from internal.domain.interfaces.iuse_case import IUseCase
from internal.modules.invenotry.commands.inventory import ReserveStockCommand
from internal.modules.invenotry.dependencies.inventory import get_reserve_stock_command

router = APIRouter()


@router.patch("/inventory/reserve", response_model=None, )
def reserve(use_case: ReserveStockCommand = Depends(get_reserve_stock_command)):
    query = use_case.execute(sku='test', quantity=2)
    return query
