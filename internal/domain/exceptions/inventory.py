from enum import Enum


class QuantityError(Exception):
    pass


class OutOfStock(Exception):
    pass


class NotAvailable(Exception):
    pass


class InvalidRelatedEventType(Exception):

    def __init__(self, event_type: Enum, aggregate):
        super(InvalidRelatedEventType, self).__init__(f"Event type {event_type} isn't related to aggregate {aggregate.__class__}")


class InventoryDoesNotExists(Exception):
    def __init__(self, *args, **kwargs):
        super(InventoryDoesNotExists, self).__init__("Inventory does not exists")


class InventoryAlreadyExists(Exception):
    def __init__(self, *args, **kwargs):
        super(InventoryAlreadyExists, self).__init__("Inventory exists")
