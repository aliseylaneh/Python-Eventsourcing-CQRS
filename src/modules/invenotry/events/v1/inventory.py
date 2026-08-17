from dataclasses import dataclass, field
from enum import Enum

from .....domain.events.base import Event


class InventoryEventType(str, Enum):
    # OPERATIONAL
    STOCK_RESERVED = "STOCK_RESERVED"
    AVAILABLE_QUANTITY_DECREASED = "AVAILABLE_QUANTITY_DECREASED"
    PROCESSED_RESERVED_SOH_DECREASED = "PROCESSED_RESERVED_SOH_DECREASED"
    PROCESSED_RESERVED_DECREASED = "PROCESSED_RESERVED_DECREASED"

    # CRUD
    SOH_REPLACED = "SOH_REPLACED"
    AVAILABLE_QUANTITY_REPLACED = "AVAILABLE_QUANTITY_REPLACED"
    INVENTORY_CREATED = "INVENTORY_CREATED"


# SCHEMA EVENTS
@dataclass(frozen=True, kw_only=True)
class BaseInventoryDetailEvent(Event):
    sku: str = field(default=0)
    event_type: InventoryEventType


@dataclass(frozen=True, kw_only=True)
class BaseInventorySOHEvent(Event):
    soh: int = field(default=0)


@dataclass(frozen=True, kw_only=True)
class BaseReservedEvent(BaseInventoryDetailEvent):
    reserved: int = field(default=0)


@dataclass(frozen=True, kw_only=True)
class InventoryEventDTO(Event):
    event_type: InventoryEventType
    sku: str = field(default="")
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = 0


# OPERATIONAL EVENTS
@dataclass(frozen=True, kw_only=True)
class ReserveQuantityIncreasedEvent(BaseReservedEvent):
    event_type: InventoryEventType = InventoryEventType.STOCK_RESERVED


@dataclass(frozen=True, kw_only=True)
class AvailableQuantityDecreasedEvent(BaseInventoryDetailEvent):
    event_type: InventoryEventType = InventoryEventType.AVAILABLE_QUANTITY_DECREASED
    available_quantity: int = field(default=0)


@dataclass(frozen=True, kw_only=True)
class ProcessedReservedDecreasedEvent(BaseReservedEvent):
    event_type: InventoryEventType = InventoryEventType.PROCESSED_RESERVED_DECREASED


@dataclass(frozen=True, kw_only=True)
class ProcessedReservedSOHDecreasedEvent(
    BaseInventoryDetailEvent, BaseInventorySOHEvent
):
    event_type: InventoryEventType = InventoryEventType.PROCESSED_RESERVED_SOH_DECREASED


# CRUD EVENTS
@dataclass(frozen=True, kw_only=True)
class InventoryCreatedEvent(Event):
    sku: str = field(default="")
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = 0
    event_type: InventoryEventType = InventoryEventType.INVENTORY_CREATED


@dataclass(frozen=True, kw_only=True)
class SOHReplacedEvent(BaseInventoryDetailEvent, BaseInventorySOHEvent):
    event_type: InventoryEventType = InventoryEventType.SOH_REPLACED


@dataclass(frozen=True, kw_only=True)
class AvailableQuantityReplacedEvent(BaseInventoryDetailEvent):
    available_quantity: int = field(default=0)
    event_type: InventoryEventType = InventoryEventType.AVAILABLE_QUANTITY_REPLACED
