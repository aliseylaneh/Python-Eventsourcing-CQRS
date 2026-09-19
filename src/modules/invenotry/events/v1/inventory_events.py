from dataclasses import dataclass, field
from enum import Enum

from src.domain.events.base import Event


class InventoryEventType(str, Enum):
    """
    Inventory event names stored on the event stream and used by aggregate and projector match handlers.
    """

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
    """
    Shared inventory event fields. sku is the aggregate identity of the event stream.
    """

    sku: str = field(default="")
    event_type: InventoryEventType


@dataclass(frozen=True, kw_only=True)
class BaseInventorySOHEvent(Event):
    """
    Event payload that carries a soh value, either an absolute replacement or a signed delta.
    """

    soh: int = field(default=0)


@dataclass(frozen=True, kw_only=True)
class BaseReservedEvent(BaseInventoryDetailEvent):
    """
    Event payload that carries a reserved quantity.
    """

    reserved: int = field(default=0)


@dataclass(frozen=True, kw_only=True)
class InventoryEventDTO(Event):
    """
    Common DTO used when events are loaded from Mongo.
    Missing payload fields default to 0 so replay and projection can use one type for every event.
    """

    event_type: InventoryEventType
    sku: str = field(default="")
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = 0


# OPERATIONAL EVENTS
@dataclass(frozen=True, kw_only=True)
class ReserveQuantityIncreasedEvent(BaseReservedEvent):
    """
    Reserved quantity increased. Available quantity is decreased by a following event in the same command.
    """

    event_type: InventoryEventType = InventoryEventType.STOCK_RESERVED


@dataclass(frozen=True, kw_only=True)
class AvailableQuantityDecreasedEvent(BaseInventoryDetailEvent):
    """
    Available quantity changed by a signed delta. Reserve stock writes a negative available_quantity.
    """

    event_type: InventoryEventType = InventoryEventType.AVAILABLE_QUANTITY_DECREASED
    available_quantity: int = field(default=0)


@dataclass(frozen=True, kw_only=True)
class ProcessedReservedDecreasedEvent(BaseReservedEvent):
    """
    Reserved quantity decreased after a reservation is completed. Amount is positive and subtracted from reserved.
    """

    event_type: InventoryEventType = InventoryEventType.PROCESSED_RESERVED_DECREASED


@dataclass(frozen=True, kw_only=True)
class ProcessedReservedSOHDecreasedEvent(
    BaseInventoryDetailEvent, BaseInventorySOHEvent
):
    """
    Stock on hand changed after a reservation is completed. Amount is a negative soh delta.
    """

    event_type: InventoryEventType = InventoryEventType.PROCESSED_RESERVED_SOH_DECREASED


# CRUD EVENTS
@dataclass(frozen=True, kw_only=True)
class InventoryCreatedEvent(Event):
    """
    First event of an inventory stream. reserved defaults to 0.
    """

    sku: str = field(default="")
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = 0
    event_type: InventoryEventType = InventoryEventType.INVENTORY_CREATED


@dataclass(frozen=True, kw_only=True)
class SOHReplacedEvent(BaseInventoryDetailEvent, BaseInventorySOHEvent):
    """
    Replace stock on hand with an absolute value.
    """

    event_type: InventoryEventType = InventoryEventType.SOH_REPLACED


@dataclass(frozen=True, kw_only=True)
class AvailableQuantityReplacedEvent(BaseInventoryDetailEvent):
    """
    Replace available quantity with an absolute value.
    """

    available_quantity: int = field(default=0)
    event_type: InventoryEventType = InventoryEventType.AVAILABLE_QUANTITY_REPLACED
