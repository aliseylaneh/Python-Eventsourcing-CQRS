import uuid

from src.infrastructure.repositories.store_info import StoreQueryRepository


class BaseStoreQuery:
    def __init__(self):
        self.repository = StoreQueryRepository()


class GetStoreQueryService(BaseStoreQuery):
    async def handle(self, pk: uuid):
        return await self.repository.find_by_id(pk=pk)
