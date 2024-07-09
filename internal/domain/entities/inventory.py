import uuid
from dataclasses import dataclass

from internal.domain.exceptions.inventory import OutOfStock


@dataclass
class Inventory:
    reference: uuid
    sku: str
    soh: int
    available_quantity: int
    reserved: int
