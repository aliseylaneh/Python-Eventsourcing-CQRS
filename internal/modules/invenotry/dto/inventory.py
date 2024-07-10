import uuid

from pydantic import BaseModel, validator
from pydantic_core import ValidationError

from internal.domain.exceptions.inventory import QuantityError


class InventoryReserveStock(BaseModel):
    sku: str
    quantity: int

    @validator('quantity', )
    def non_zero_negative(cls, v):
        if v <= 0:
            raise QuantityError()
        return v


class CreateInventory(BaseModel):
    sku: str
    soh: int
    available_quantity: int


class CreateInventoryResponse(BaseModel):
    sku: str
    soh: int
    reserved: int
    available_quantity: int
