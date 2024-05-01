import uuid

from infrastructure.repositories.store import StoreQueryRepository


class BaseStoreQuery:
    def __init__(self):
        self.repository = StoreQueryRepository()


class GetStoreQueryService(BaseStoreQuery):
    async def handle(self, pk: uuid):
        return await self.repository.find_by_id(pk=pk)
