from sqlalchemy import BinaryExpression, select
from sqlalchemy.ext.asyncio import AsyncSession

from presentation.schema import CreateStore, UpdateStore
from ..models.store import Store
from ..settings.database import get_db_session


class StoreCommandRepository:
    def __init__(self):
        self.db_session: AsyncSession = get_db_session()

    async def create(self, store: CreateStore) -> Store:
        new_store = Store(name=store.name, address=store.address, logo=store.logo)
        self.db_session.add(new_store)
        await self.db_session.commit()
        await self.db_session.refresh(new_store)
        return new_store

    async def update(self, store: UpdateStore):
        await self.db_session.query(Store).filter(Store.id == store.id).update(
            {Store.name: store.name, Store.address: store.address})
        await self.db_session.commit()


class StoreQueryRepository:
    def __init__(self):
        self.db_session = get_db_session()

    async def find_by_id(self, pk: int) -> Store:
        result = await self.db_session.execute(select(Store).where(pk == Store.id))
        store = result.scalars().first()
        return store

    async def all(self, skip: int = 0, limit: int = 20):
        results = await self.db_session.execute(select(Store).offset(skip).limit(limit))
        return results.scalars().all()

    async def filter_by_fields(self, *expressions: BinaryExpression):
        query = select(Store)
        if expressions:
            query = query.where(*expressions)
        return list(await self.db_session.scalars(query))
