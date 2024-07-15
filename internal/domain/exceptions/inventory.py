from enum import Enum


class QuantityError(Exception):
    pass


class OutOfStock(Exception):
    def __init__(self, *args, **kwargs):
        super(OutOfStock, self).__init__("Out of stock!!.")


class InvalidRelatedEventType(Exception):

    def __init__(self, event_type: Enum, aggregate):
        super(InvalidRelatedEventType, self).__init__(f"Event type {event_type} isn't related to aggregate {aggregate.__class__}.")


class InventoryDoesNotExists(Exception):
    def __init__(self, *args, **kwargs):
        super(InventoryDoesNotExists, self).__init__("Inventory does not exists!!")


class InventoryAlreadyExists(Exception):
    def __init__(self, *args, **kwargs):
        super(InventoryAlreadyExists, self).__init__("Inventory exists!!")


class AvailableQuantityError(Exception):
    def __init__(self, *args, **kwargs):
        super(AvailableQuantityError, self).__init__("Available Quantity is more than soh.")


class ReservedStockInProcess(Exception):
    def __init__(self, *args, **kwargs):
        super(ReservedStockInProcess, self).__init__("Update is unavailable due to reserved stock.")


class InvalidReservedAmount(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidReservedAmount, self).__init__("Amount is more than reserved quantity.")


class InvalidAvailableQuantityUpdate(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidAvailableQuantityUpdate, self).__init__(
            "Available quantity update is not available due to zero or negative value.")


class InvalidSOHUpdate(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidSOHUpdate, self).__init__(
            "SOH update is not available due to zero or negative value.")
