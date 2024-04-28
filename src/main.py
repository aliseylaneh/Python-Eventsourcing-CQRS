from fastapi import Depends
from fastapi import FastAPI
from domain.models import Store

from services.store import GetStoreQueryService

app = FastAPI()


@app.get("/store/{id}", response_model=Store)
async def get_store(pk: int, service: GetStoreQueryService = Depends(GetStoreQueryService)):
    query = await service.handle(pk=pk)
    return Store(store_name="Dolce & Gabbana")
