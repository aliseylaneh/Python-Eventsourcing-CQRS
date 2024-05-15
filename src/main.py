from fastapi import FastAPI

from presentation.apis import router as store_router

app = FastAPI()

app.include_router(store_router)
