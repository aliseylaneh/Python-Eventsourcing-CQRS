import uuid
from typing import Any

from src.domain.models import Store


class StoreCommandRepository:
    async def create(self, store: Store):
        pass

    async def update(self, pk: uuid):
        pass


class StoreQueryRepository:
    async def find_by_id(self, pk: uuid) -> Store:
        pass

    async def filter_by_fields(self, data: dict[str, Any]):
        pass
