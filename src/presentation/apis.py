from fastapi import Depends, APIRouter, HTTPException
from domain.models import Store
from services.store import GetStoreQueryService

router = APIRouter()


@router.get("/store/{pk}", response_model=Store, )
async def get_store(pk: int, service: GetStoreQueryService = Depends(GetStoreQueryService)):
    query = await service.handle(pk=pk)
    if not query:
        raise HTTPException(status_code=400, detail="Given id store not found!!")
    return query
