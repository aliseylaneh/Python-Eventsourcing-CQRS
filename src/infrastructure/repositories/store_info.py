import uuid
from typing import Any
from sqlalchemy.orm import Session
from ..models.store import Store
from src.presentation.schema import CreateStore, UpdateStore


class StoreCommandRepository:
    def __init__(self):
        self.db = Session()

    async def create(self, store: CreateStore):
        new_store = Store(name=store.name, address=store.address)
        self.db.add(new_store)
        self.db.commit()
        self.db.refresh(new_store)

    async def update(self, store: UpdateStore):
        self.db.query(Store).filter(Store.id == store.id).update(
            {Store.name: store.name, Store.address: store.address})
        self.db.commit()


class StoreQueryRepository:
    def __init__(self):
        self.db = Session()

    async def find_by_id(self, pk: int) -> Store:
        return self.db.query(Store).filter(Store.id == pk).first()

    async def all(self, skip: int = 0, limit: int = 20):
        return self.db.query(Store).offset(skip).limit(limit).all()

    async def filter_by_fields(self, data: dict[str, Any]):
        pass
