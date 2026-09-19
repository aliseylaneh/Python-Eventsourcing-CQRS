# Python Event Sourcing + CQRS

A FastAPI inventory service that stores **events**, not current state. Commands write to an event store. Queries read a projection that is built asynchronously from those events.

## How it works

```text
API  →  Command  →  Aggregate  →  Event store + outbox
                                      ↓
GET  ←  Query    ←  Projection  ←  outbox worker
```

1. A command loads the event stream for a SKU and rebuilds `InventoryAggregate`.
2. New events are written in one transaction to `inventory_events` and `inventory_outbox`.
3. A background worker projects unpublished outbox events into `inventory_projections`.
4. `GET /inventory/{sku}` reads the projection. It can lag a moment behind a write.

Inventory actions: **create**, **reserve**, **complete reserved stock**, **update**, **get**.

## Layout

```text
src/domain/                 shared contracts, entity, aggregate base
src/modules/invenotry/      inventory use cases
  aggregates/               event handlers and new-event factories
  commands/                 write use cases
  queries/                  read use cases
  repositories/             Mongo event store, outbox, projection
  projections/              event → read model
  tasks/                    outbox worker
  delivery/v1/              HTTP API
adapter/                    Mongo client
config/                     Mongo and tracing settings
main.py                     FastAPI app
```

## Run

```bash
docker compose up -d
uvicorn main:app --reload
```

App: http://localhost:8000  
Docs: http://localhost:8000/docs  
Mongo Express: http://localhost:8081  
Jaeger: http://localhost:16686  

Mongo defaults: `localhost:27017`, database `inventory`, user `admin`, password `1234`.

## Upcoming

- **Observability** — tracing, metrics, and clearer request/event correlation
- **Caching** — faster reads on the projection without hitting Mongo every time
- **Snapshotting** — avoid replaying the full event stream as aggregates grow
- **Deployment and scalability** — how to run, split, and scale the write path, read path, and workers
