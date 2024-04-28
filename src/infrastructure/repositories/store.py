from presentation.schema import CreateStore, UpdateStore
from sqlalchemy import BinaryExpression, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.store import Store
from ..settings.database import get_db_session


class StoreCommandRepository:
    def __init__(self):
        self.db_session: AsyncSession = get_db_session()

    async def create(self, store: CreateStore):
        new_store = Store(name=store.name, address=store.address)
        self.db_session.add(new_store)
        await self.db_session.commit()
        await self.db_session.refresh(new_store)

    async def update(self, store: UpdateStore):
        await self.db_session.query(Store).filter(Store.id == store.id).update(
            {Store.name: store.name, Store.address: store.address})
        await self.db_session.commit()


class StoreQueryRepository:
    def __init__(self):
        self.db_session: AsyncSession = get_db_session()

    async def find_by_id(self, pk: int) -> Store:
        return await self.db_session.query(Store).filter(Store.id == pk).first()

    async def all(self, skip: int = 0, limit: int = 20):
        return await self.db_session.query(Store).offset(skip).limit(limit).all()

    async def filter_by_fields(self, *expressions: BinaryExpression):
        query = select(Store)
        if expressions:
            query = query.where(*expressions)
        return list(await self.db_session.scalars(query))
