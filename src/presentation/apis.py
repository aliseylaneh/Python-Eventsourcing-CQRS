from fastapi import Depends, APIRouter, HTTPException, UploadFile
from domain.models import Store
from presentation.schema import CreateStore
from services.store import GetStoreQueryService, CreateStoreCommandService

router = APIRouter()


@router.get("/store/{pk}", response_model=Store, )
async def get_store(pk: int, service: GetStoreQueryService = Depends(GetStoreQueryService)):
    query = await service.handle(pk=pk)
    if not query:
        raise HTTPException(status_code=400, detail="Given id store not found!!")
    return query


@router.post("/store", response_model=Store, )
async def create_store(store: CreateStore,
                       service: CreateStoreCommandService = Depends(CreateStoreCommandService)):
    query = await service.handle(store=store)
    return query
