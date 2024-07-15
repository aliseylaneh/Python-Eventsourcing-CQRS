from dataclasses import dataclass, field

from internal.domain.exceptions.inventory import AvailableQuantityError, InvalidAvailableQuantityUpdate, InvalidReservedAmount, \
    InvalidSOHUpdate, OutOfStock, \
    ReservedStockInProcess


@dataclass
class Inventory:
    sku: str = field(default='')
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = field(default=0)

    def set_soh(self, soh: int):
        if self.reserved >= soh:
            raise ReservedStockInProcess()
        if soh >= 0:
            self.soh = soh

    def set_available_quantity(self, available_quantity: int):
        if self.soh < available_quantity:
            raise AvailableQuantityError()
        if available_quantity >= 0:
            self.available_quantity = available_quantity

    def decrease_reserved(self, amount: int):
        if self.reserved < amount:
            raise InvalidReservedAmount()
        self.reserved -= amount

    def update_soh(self, amount: int):
        """
        Updating soh can be done with positive and negative values.
        """
        if self.soh <= 0:
            raise InvalidSOHUpdate()
        self.soh += amount

    def update_available_quantity(self, amount: int):
        """
        Updating available quantity can be done with positive and negative values.
        """
        if self.available_quantity <= 0:
            raise InvalidAvailableQuantityUpdate()
        self.available_quantity += amount

    def increase_reserved(self, amount: int):
        if self.soh <= 0:
            raise OutOfStock()
        if self.available_quantity < amount:
            raise OutOfStock()
        self.reserved += amount
