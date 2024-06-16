import enum
import uuid
from dataclasses import dataclass

from internal.domain.events.base import Event


class InventoryEventType(enum.Enum):
    CREATE_INVENTORY = 'CREATE_INVENTORY'
    DELETE_INVENTORY = 'DELETE_INVENTORY'
    RESERVE_INVENTORY_STOCK = 'RESERVE_INVENTORY_STOCK'
    INCREASE_INVENTORY_SOH = 'INCREASE_INVENTORY_SOH'
    DECREASE_INVENTORY_SOH = 'DECREASE_INVENTORY_SOH'


@dataclass
class BaseInventoryDetailEvent(Event):
    sku: uuid


@dataclass
class BaseInventorySOHEvent(Event):
    soh: int


@dataclass
class CreateInventoryEvent(BaseInventoryDetailEvent, BaseInventorySOHEvent):
    event_type = InventoryEventType.CREATE_INVENTORY


@dataclass
class DeleteInventoryEvent(Event):
    reference_id: int
    event_type: str = InventoryEventType.DELETE_INVENTORY


@dataclass
class ReserveStockEvent(BaseInventoryDetailEvent):
    quantity: int
    event_type = InventoryEventType.RESERVE_INVENTORY_STOCK


@dataclass
class IncreaseSOHEvent(BaseInventorySOHEvent):
    event_type: str = InventoryEventType.INCREASE_INVENTORY_SOH


@dataclass
class DecreaseSOHEvent(BaseInventorySOHEvent):
    event_type: str = InventoryEventType.DECREASE_INVENTORY_SOH
