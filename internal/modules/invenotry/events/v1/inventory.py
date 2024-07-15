import uuid
from dataclasses import dataclass, field
from enum import Enum

from .....domain.events.base import Event


class InventoryEventType(str, Enum):
    # OPERATIONAL
    STOCK_RESERVED = 'STOCK_RESERVED'
    AVAILABLE_QUANTITY_DECREASED = 'AVAILABLE_QUANTITY_DECREASED'
    PROCESSED_RESERVED_SOH_DECREASED = 'PROCESSED_RESERVED_SOH_DECREASED'
    PROCESSED_RESERVED_DECREASED = 'PROCESSED_RESERVED_DECREASED'

    # CRUD
    SOH_REPLACED = 'SOH_REPLACED'
    AVAILABLE_QUANTITY_REPLACED = 'AVAILABLE_QUANTITY_REPLACED'
    INVENTORY_CREATED = 'INVENTORY_CREATED'


@dataclass
class BaseInventoryDetailEvent(Event):
    sku: uuid = field(default=0)
    event_type: InventoryEventType


@dataclass
class BaseInventorySOHEvent(Event):
    soh: int = field(default=0)


@dataclass
class BaseReservedEvent(BaseInventoryDetailEvent):
    reserved: int = field(default=0)


# OPERATIONAL EVENTS
@dataclass
class ReserveQuantityIncreasedEvent(BaseReservedEvent):
    event_type: InventoryEventType = InventoryEventType.STOCK_RESERVED


@dataclass
class AvailableQuantityDecreasedEvent(BaseInventoryDetailEvent):
    event_type: InventoryEventType = InventoryEventType.AVAILABLE_QUANTITY_DECREASED
    available_quantity: int = field(default=0)


@dataclass
class ProcessedReservedDecreasedEvent(BaseReservedEvent):
    event_type: InventoryEventType = InventoryEventType.PROCESSED_RESERVED_DECREASED


@dataclass
class ProcessedReservedSOHDecreasedEvent(BaseInventoryDetailEvent, BaseInventorySOHEvent):
    event_type: InventoryEventType = InventoryEventType.PROCESSED_RESERVED_SOH_DECREASED


# CRUD EVENTS
@dataclass
class InventoryCreatedEvent(Event):
    sku: str = field(default='')
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = 0
    event_type: InventoryEventType = InventoryEventType.INVENTORY_CREATED


@dataclass
class SOHReplacedEvent(BaseInventoryDetailEvent, BaseInventorySOHEvent):
    event_type: InventoryEventType = InventoryEventType.SOH_REPLACED


@dataclass
class AvailableQuantityReplacedEvent(BaseInventoryDetailEvent):
    available_quantity: int = field(default=0)
    event_type: InventoryEventType = InventoryEventType.AVAILABLE_QUANTITY_REPLACED
