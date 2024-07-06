import enum
import uuid
from dataclasses import dataclass

from internal.domain.events.base import Event


class InventoryEventType(enum.Enum):
    INVENTORY_CREATED = 'INVENTORY_CREATED'
    INVENTORY_DELETED = 'INVENTORY_DELETED'
    STOCK_RESERVED = 'STOCK_RESERVED'
    SOH_INCREASED = 'SOH_INCREASED'
    SOH_DECREASED = 'SOH_DECREASED'


@dataclass
class BaseInventoryDetailEvent(Event):
    sku: uuid


@dataclass
class BaseInventorySOHEvent(Event):
    soh: int


@dataclass
class InventoryCreatedEvent(BaseInventoryDetailEvent, BaseInventorySOHEvent):
    event_type = InventoryEventType.INVENTORY_CREATED


@dataclass
class InventoryDeletedEvent(Event):
    reference_id: int
    event_type: str = InventoryEventType.INVENTORY_DELETED


@dataclass
class StockReservedEvent(BaseInventoryDetailEvent):
    quantity: int
    event_type = InventoryEventType.STOCK_RESERVED


@dataclass
class SOHIncreasedEvent(BaseInventorySOHEvent):
    event_type: str = InventoryEventType.SOH_INCREASED


@dataclass
class SOHDecreasedEvent(BaseInventorySOHEvent):
    event_type: str = InventoryEventType.SOH_DECREASED