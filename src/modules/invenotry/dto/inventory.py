from uuid import UUID

from pydantic import BaseModel, PositiveInt


class UserIDDTO(BaseModel):
    user_id: UUID


class InventoryReserveStock(UserIDDTO, BaseModel):
    quantity: PositiveInt


class CompleteReservedStock(UserIDDTO, BaseModel):
    quantity: PositiveInt


class CreateInventory(UserIDDTO, BaseModel):
    sku: str
    soh: PositiveInt
    available_quantity: PositiveInt


class UpdateInventory(UserIDDTO, BaseModel):
    soh: PositiveInt
    available_quantity: PositiveInt


class InventoryResponse(BaseModel):
    sku: str
    soh: int
    reserved: int
    available_quantity: int
