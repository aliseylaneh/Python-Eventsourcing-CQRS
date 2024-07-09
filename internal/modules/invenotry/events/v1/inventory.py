from enum import Enum
import uuid
from dataclasses import dataclass, field

from .....domain.events.base import Event


class InventoryEventType(Enum):
    INVENTORY_CREATED = 'INVENTORY_CREATED'
    INVENTORY_DELETED = 'INVENTORY_DELETED'
    STOCK_RESERVED = 'STOCK_RESERVED'
    SOH_INCREASED = 'SOH_INCREASED'
    SOH_DECREASED = 'SOH_DECREASED'
    AVAILABLE_QUANTITY_DECREASED = 'AVAILABLE_QUANTITY_DECREASED'


@dataclass
class BaseInventoryDetailEvent(Event):
    sku: uuid = field(default=0)
    event_type: InventoryEventType


@dataclass
class BaseInventorySOHEvent(Event):
    soh: int = field(default=0)


@dataclass
class QuantityEvent(BaseInventoryDetailEvent):
    quantity: int = field(default=0)


# OPERATIONAL EVENTS
@dataclass
class ReserveQuantityIncreasedEvent(QuantityEvent):
    event_type: InventoryEventType = InventoryEventType.STOCK_RESERVED


@dataclass
class AvailableQuantityDecreasedEvent(QuantityEvent):
    event_type: InventoryEventType = InventoryEventType.AVAILABLE_QUANTITY_DECREASED
