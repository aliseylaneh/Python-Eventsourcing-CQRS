from typing import Type, NewType

from fastapi import APIRouter, Depends, HTTPException

from ...commands.inventory import CreateInventoryCommand, ReserveStockCommand, UpdateInventoryCommand
from ...dependencies.inventory import get_create_inventory_command, get_reserve_stock_command, get_update_inventory_command
from ...dto.inventory import CreateInventory, InventoryReserveStock, InventoryResponse, UpdateInventory

router = APIRouter()
Sku = NewType(name='sku', tp=str)


@router.patch("/inventory/{sku}/reserve")
def reserve(sku: Sku, reserve_stock: InventoryReserveStock,
            use_case: ReserveStockCommand = Depends(get_reserve_stock_command)) -> InventoryResponse:
    try:
        inventory = use_case.execute(sku=sku, quantity=reserve_stock.quantity)
        response = InventoryResponse(sku=inventory.sku,
                                     soh=inventory.soh,
                                     reserved=inventory.reserved,
                                     available_quantity=inventory.available_quantity)
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.post("/inventory/create")
def create(sku: Sku, inventory: CreateInventory,
           use_case: CreateInventoryCommand = Depends(get_create_inventory_command)) -> InventoryResponse:
    try:
        inventory = use_case.execute(sku=sku, soh=inventory.soh, available_quantity=inventory.available_quantity)
        response = InventoryResponse(sku=inventory.sku,
                                     soh=inventory.soh,
                                     reserved=inventory.reserved,
                                     available_quantity=inventory.available_quantity)
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@router.patch("/inventory/{sku}/update")
def update(inventory: UpdateInventory,
           use_case: UpdateInventoryCommand = Depends(get_update_inventory_command)) -> InventoryResponse:
    try:
        inventory = use_case.execute(sku=inventory.sku,
                                     soh=inventory.soh,
                                     available_quantity=inventory.available_quantity)
        response = InventoryResponse(sku=inventory.sku,
                                     soh=inventory.soh,
                                     reserved=inventory.reserved,
                                     available_quantity=inventory.available_quantity)
        return response
    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))