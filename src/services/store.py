import uuid

from src.infrastructure.store_info_respository import StoreQueryRepository


class BaseStoreQuery:
    def __init__(self):
        self.repository = StoreQueryRepository()


class GetStoreQueryService(BaseStoreQuery):
    async def handle(self, pk: uuid):
        return await self.repository.find_by_id(pk=pk)
