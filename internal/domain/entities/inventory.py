import uuid
from dataclasses import dataclass, field

from internal.domain.exceptions.inventory import OutOfStock


@dataclass
class Inventory:
    sku: str = field(default='')
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = field(default=0)

    def update_available_quantity(self, amount: int):
        self.available_quantity += amount

    def increase_reserved(self, amount: int):
        if self.soh <= 0:
            raise OutOfStock()
        if self.available_quantity < amount:
            raise OutOfStock()
        self.reserved += amount
