from enum import Enum
from typing import Type


class OutOfStock(Exception):
    pass


class NotAvailable(Exception):
    pass


class InvalidRelatedEventType(Exception):

    def __init__(self, event_type: Enum, aggregate):
        super(InvalidRelatedEventType, self).__init__(f"Event type {event_type} isn't related to aggregate {aggregate.__class__}")
