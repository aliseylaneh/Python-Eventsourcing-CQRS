from typing import Any, Dict

from config.otel import tracer
from src.domain.exceptions.inventory import InventoryDoesNotExists
from src.domain.queries.queries import BaseQuery


class GetInventoryQuery(BaseQuery):
    async def execute(self, sku: str) -> Dict[str, Any]:
        """
        Read one inventory from the projection store, not from the event stream.
        The result can lag behind a recent write until the outbox worker projects the events.
        :param sku: sku
        :return: projected inventory document
        """
        with tracer.start_as_current_span(f"get-{sku}-query"):
            inventory = await self._repository.find(sku=sku)
            if inventory is None:
                raise InventoryDoesNotExists()
            return inventory
