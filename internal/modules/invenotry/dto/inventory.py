from pydantic import BaseModel, PositiveInt


class InventoryReserveStock(BaseModel):
    sku: str
    quantity: PositiveInt


class CreateInventory(BaseModel):
    sku: str
    soh: PositiveInt
    available_quantity: PositiveInt


class UpdateInventory(BaseModel):
    sku: str
    soh: PositiveInt
    available_quantity: PositiveInt


class InventoryResponse(BaseModel):
    sku: str
    soh: int
    reserved: int
    available_quantity: int
