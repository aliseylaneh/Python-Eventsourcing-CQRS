from typing import Type

from internal.domain.aggregates.inventory import AggregateRoot


class OutOfStock(Exception):
    pass


class NotAvailable(Exception):
    pass


class InvalidRelatedEventType(Exception):
    def __init__(self, event_type: str, aggregate: Type[AggregateRoot]):
        super(InvalidRelatedEventType, self).__init__(f"Event type {event_type} isn't related to aggregate {aggregate.__class__}")
