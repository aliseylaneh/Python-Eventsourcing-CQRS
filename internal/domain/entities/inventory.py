import uuid
from dataclasses import dataclass

from internal.domain.exceptions.inventory import OutOfStock


@dataclass
class Inventory:
    reference: uuid
    sku: int
    soh: int
    available_quantity: int
    reserved: int

    def reserve_stock(self, quantity: int) -> int:
        if self.soh <= 0:
            raise OutOfStock()
        if self.available_quantity < quantity:
            raise OutOfStock()
        self.reserved += quantity
        return self.available_quantity
