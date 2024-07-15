import uuid
from dataclasses import dataclass, field
from enum import Enum

from .....domain.events.base import Event


class InventoryEventType(str, Enum):
    # OPERATIONAL
    STOCK_RESERVED = 'STOCK_RESERVED'
    SOH_INCREASED = 'SOH_INCREASED'
    SOH_DECREASED = 'SOH_DECREASED'
    AVAILABLE_QUANTITY_DECREASED = 'AVAILABLE_QUANTITY_DECREASED'
    # CRUD
    SOH_REPLACED = 'SOH_REPLACED'
    AVAILABLE_QUANTITY_REPLACED = 'AVAILABLE_QUANTITY_REPLACED'
    INVENTORY_CREATED = 'INVENTORY_CREATED'
    INVENTORY_DELETED = 'INVENTORY_DELETED'


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
class ReserveQuantityIncreasedEvent(BaseInventoryDetailEvent):
    event_type: InventoryEventType = InventoryEventType.STOCK_RESERVED
    reserved: int = field(default=0)


@dataclass
class AvailableQuantityDecreasedEvent(BaseInventoryDetailEvent):
    event_type: InventoryEventType = InventoryEventType.AVAILABLE_QUANTITY_DECREASED
    available_quantity: int = field(default=0)


# CRUD EVENTS
@dataclass
class InventoryCreatedEvent(Event):
    sku: str = field(default='')
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = 0
    event_type: InventoryEventType = InventoryEventType.INVENTORY_CREATED


@dataclass
class SOHReplacedEvent(BaseInventoryDetailEvent):
    soh: int = field(default=0)
    event_type: InventoryEventType = InventoryEventType.SOH_REPLACED


@dataclass
class AvailableQuantityReplacedEvent(BaseInventoryDetailEvent):
    available_quantity: int = field(default=0)
    event_type = InventoryEventType = InventoryEventType.AVAILABLE_QUANTITY_REPLACED
