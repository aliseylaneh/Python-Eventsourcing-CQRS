from typing import BinaryIO

from minio import Minio

from infrastructure.settings.minio_settings import MINIO_STORAGE_ACCESS_KEY, MINIO_STORAGE_ENDPOINT, MINIO_STORAGE_MEDIA_BUCKET_NAME, \
    MINIO_STORAGE_SECRET_KEY


class MinioImageOpsService:
    def __init__(self, bucket_name: str):
        self.client = Minio(endpoint=MINIO_STORAGE_ENDPOINT,
                            secret_key=MINIO_STORAGE_SECRET_KEY,
                            access_key=MINIO_STORAGE_ACCESS_KEY)
        self.bucket_name = bucket_name

    async def save(self, file: BinaryIO, name: str):
        result = self.client.put_object(bucket_name=self.bucket_name, object_name=name, data=file, length=-1)
        return result

    async def find(self, name: str):
        result = self.client.get_object(bucket_name=self.bucket_name, object_name=name)
        return result


minio_service = MinioImageOpsService(bucket_name=MINIO_STORAGE_MEDIA_BUCKET_NAME)
