from fastapi import Depends, APIRouter
from domain.models import Store
from services.store import GetStoreQueryService

router = APIRouter()


@router.get("/store/{id}", response_model=Store)
async def get_store(pk: int, service: GetStoreQueryService = Depends(GetStoreQueryService)):
    query = await service.handle(pk=pk)
    return query
