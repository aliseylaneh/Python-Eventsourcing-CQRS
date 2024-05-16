from fastapi import UploadFile, File
from pydantic import BaseModel, Base64Bytes

from domain.models import BaseStore, Store


class CreateStore(BaseStore):
    logo: Base64Bytes


class UpdateStore(Store):
    pass
