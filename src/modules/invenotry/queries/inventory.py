from config.otel import tracer
from src.domain.entities.inventory import Inventory
from src.domain.queries.queries import BaseQuery


class GetInventoryQuery(BaseQuery):
    async def execute(self, sku: str) -> Inventory:
        with tracer.start_as_current_span(f"get-{sku}-inventory-usecase"):
            pass
