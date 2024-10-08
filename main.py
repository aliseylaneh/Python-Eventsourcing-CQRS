from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from config.otel import *  # noqa
from internal.modules.invenotry.delivery.v1.apis import router as inventory_router

app = FastAPI()
RequestsInstrumentor().instrument()
FastAPIInstrumentor().instrument_app(app=app, excluded_urls="/docs,/openapi.json,/")
app.include_router(inventory_router)
