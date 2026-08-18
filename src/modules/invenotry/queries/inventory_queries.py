from typing import Dict, Any

from config.otel import tracer
from src.domain.queries.queries import BaseQuery


class GetInventoryQuery(BaseQuery):
    async def execute(self, sku: str) -> Dict[str, Any]:
        with tracer.start_as_current_span(f"get-{sku}-inventory-usecase"):
            return self._repository.find(sku=sku)
