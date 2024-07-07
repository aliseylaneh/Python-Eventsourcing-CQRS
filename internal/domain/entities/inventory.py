import uuid
from dataclasses import dataclass

from internal.domain.exceptions.inventory import OutOfStock


@dataclass
class InventoryProjection:
    reference: uuid
    sku: int
    soh: int
    available_quantity: int
    reserved: int

    def __init__(self):
        self._update_soh(soh=self.soh)

    def _update_available_quantity(self):
        self.available_quantity = self.soh - self.reserved

    def _update_soh(self, soh: int):
        self.soh = self.soh - soh

    def reserve_stock(self, quantity: int):
        if self.soh <= 0:
            raise OutOfStock()
        if self.available_quantity < quantity:
            raise OutOfStock()
        self.reserved += quantity
        self._update_available_quantity()
