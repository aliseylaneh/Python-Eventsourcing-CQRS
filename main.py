from contextlib import asynccontextmanager

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from adapter.mongo import close_client, ensure_indexes
from config.otel import *  # noqa
from internal.modules.invenotry.delivery.v1.apis import \
    router as inventory_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_indexes()
    yield
    await close_client()


app = FastAPI(lifespan=lifespan)

RequestsInstrumentor().instrument()
FastAPIInstrumentor().instrument_app(app=app, excluded_urls="/docs,/openapi.json,/")
app.include_router(inventory_router)
