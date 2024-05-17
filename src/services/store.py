import asyncio
import uuid

from infrastructure.repositories.store import StoreCommandRepository, StoreQueryRepository
from infrastructure.services.minio import minio_service
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
        created_store = await self.repository.create(store=store)
        await minio_service.save(file=store.logo, name="Test")
        result = await GetStoreQueryService().handle(pk=created_store.id)
        return result
