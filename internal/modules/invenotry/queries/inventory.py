from typing import Any

from internal.domain.entities.inventory import Inventory
from internal.domain.entities.types.inventory import SKU
from internal.domain.exceptions.inventory import InventoryDoesNotExists
from internal.domain.queries.queries import BaseQuery
from internal.es.services.inventory_utility import MongoDBInventoryUtility


class GetInventoryQuery(BaseQuery):
    def execute(self, sku: str) -> Inventory:
        inventory = MongoDBInventoryUtility.recreate_state(repository=self.repository, sku=sku)
        if not inventory:
            raise InventoryDoesNotExists()
        return inventory
