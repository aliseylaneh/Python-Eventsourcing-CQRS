from fastapi import FastAPI

from invenotry.delivery.apis import router as inventory_router

app = FastAPI()

app.include_router(inventory_router)
