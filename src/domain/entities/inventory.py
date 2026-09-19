from dataclasses import dataclass, field

from src.domain.exceptions.inventory import (
    AvailableQuantityError,
    InvalidAvailableQuantityUpdate,
    InvalidReservedAmount,
    InvalidSOHUpdate,
    OutOfStock,
    ReservedStockInProcess,
    ReserveMoreThanStock,
)


@dataclass
class Inventory:
    """
    Current in-memory state of an inventory item reconstructed by the aggregate.
    """

    sku: str = field(default="")
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = field(default=0)

    async def set_soh(self, soh: int):
        """
        Replace stock on hand with an absolute value.
        Update is rejected when reserved quantity is greater than or equal to the new soh.
        :param soh: new stock on hand value
        :return:
        """
        if self.reserved >= soh:
            raise ReservedStockInProcess()
        if soh >= 0:
            self.soh = soh

    async def set_available_quantity(self, available_quantity: int):
        """
        Replace available quantity with an absolute value.
        Available quantity can not be greater than stock on hand.
        :param available_quantity: new available quantity
        :return:
        """
        if self.soh < available_quantity:
            raise AvailableQuantityError()
        if available_quantity >= 0:
            self.available_quantity = available_quantity

    async def decrease_reserved(self, amount: int):
        """
        Decrease only the reserved quantity by a positive amount.
        Stock on hand is not changed here, completing a reservation decreases soh with a separate event.
        :param amount: reserved quantity that should be released from reservation
        :return:
        """
        if self.reserved < amount:
            raise InvalidReservedAmount()
        self.reserved -= amount

    async def update_soh(self, amount: int):
        """
        Update stock on hand with a signed delta.
        Completing reserved stock uses a negative amount so soh is decreased after reservation is processed.
        :param amount: positive or negative soh delta
        :return:
        """
        next_soh = self.soh + amount
        if next_soh < 0:
            raise InvalidSOHUpdate()
        self.soh = next_soh

    async def update_available_quantity(self, amount: int):
        """
        Update available quantity with a signed delta.
        Reserving stock uses a negative amount so available quantity is decreased.
        :param amount: positive or negative available quantity delta
        :return:
        """
        next_quantity = self.available_quantity + amount
        if next_quantity < 0:
            raise InvalidAvailableQuantityUpdate()
        self.available_quantity = next_quantity

    async def increase_reserved(self, amount: int):
        """
        Increase reserved quantity when there is enough available stock.
        Available quantity is decreased by a separate event in the same reserve action.
        :param amount: quantity that should be reserved
        :return:
        """
        if self.soh <= 0:
            raise OutOfStock()
        if self.available_quantity < amount:
            raise ReserveMoreThanStock()
        self.reserved += amount
