from enum import Enum
from typing import Type


class QuantityError(Exception):
    def __init__(self):
        super(QuantityError, self).__init__('Quantity must not be less than or equal to zero')


class OutOfStock(Exception):
    pass


class NotAvailable(Exception):
    pass


class InvalidRelatedEventType(Exception):

    def __init__(self, event_type: Enum, aggregate):
        super(InvalidRelatedEventType, self).__init__(f"Event type {event_type} isn't related to aggregate {aggregate.__class__}")


class InventoryDoesNotExists(Exception):
    def __init__(self):
        super(InventoryDoesNotExists, self).__init__("Inventory does not exists")
