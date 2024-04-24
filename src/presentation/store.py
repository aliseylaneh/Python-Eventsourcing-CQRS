from fastapi import Depends

from src.domain.models import Store
from src.main import app
from src.services.store import GetStoreQueryService


@app.get("/store/{id}", response_model=Store)
async def get_store(pk: int, service: GetStoreQueryService = Depends(GetStoreQueryService)):
    query = await service.handle(pk=pk)
    return Store(store_name="Dolce & Gabbana")
