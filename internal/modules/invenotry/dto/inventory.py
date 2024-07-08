from pydantic import BaseModel


class InventoryReserveStock(BaseModel):
    sku: str
    quantity: int
