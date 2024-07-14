from typing import Any

from internal.domain.entities.types.inventory import SKU
from internal.domain.queries.queries import BaseQuery


class GetInventoryQuery(BaseQuery):
    def execute(self, sku: str) -> Any:
        pass
