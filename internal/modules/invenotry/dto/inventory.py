from pydantic import BaseModel, validator

from internal.domain.exceptions.inventory import QuantityError


class InventoryReserveStock(BaseModel):
    sku: str
    quantity: int

    @validator('quantity', )
    def non_zero_negative(cls, v):
        if v <= 0:
            raise QuantityError('Quantity must not be less than or equal to zero')
        return v


class CreateInventory(BaseModel):
    sku: str
    soh: int
    available_quantity: int


class InventoryResponse(BaseModel):
    sku: str
    soh: int
    reserved: int
    available_quantity: int
