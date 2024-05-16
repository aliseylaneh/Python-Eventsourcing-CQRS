import uuid

from infrastructure.repositories.store import StoreQueryRepository, StoreCommandRepository
from presentation.schema import CreateStore


class BaseStoreCommand:
    def __init__(self):
        self.repository = StoreCommandRepository()


class BaseStoreQuery:
    def __init__(self):
        self.repository = StoreQueryRepository()


class GetStoreQueryService(BaseStoreQuery):
    async def handle(self, pk: uuid):
        return await self.repository.find_by_id(pk=pk)


class CreateStoreCommandService(BaseStoreCommand):
    async def handle(self, store: CreateStore):
        return await self.repository.create(store=store)
