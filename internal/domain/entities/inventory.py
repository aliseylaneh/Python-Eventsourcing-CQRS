import uuid
from dataclasses import dataclass, field

from internal.domain.exceptions.inventory import OutOfStock


@dataclass
class Inventory:
    reference: uuid = field(default='')
    sku: str = field(default='')
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = field(default=0)
