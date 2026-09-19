import asyncio

from adapter.mongo import db, event_collection, outbox_collection
from src.modules.invenotry.projections.inventory_projector import \
    InventoryProjection
from src.modules.invenotry.repositories.inventory_mongo_repository import (
    INVENTORY_PROJECTION_COLLECTION, InventoryReadRepository,
    InventoryWriteRepository)


def _build_projection() -> InventoryProjection:
    """
    Build a projector that writes into the inventory projection collection.
    :return: InventoryProjection
    """
    read_repository = InventoryReadRepository(
        db=db,
        projection_store=INVENTORY_PROJECTION_COLLECTION,
    )
    return InventoryProjection(repository=read_repository)


def _build_outbox_repository() -> InventoryWriteRepository:
    """
    Build the write repository used to read and acknowledge unpublished outbox events.
    :return: InventoryWriteRepository
    """
    return InventoryWriteRepository(
        db=db,
        event_collection=event_collection,
        outbox_collection=outbox_collection,
    )


async def project_unpublished_events() -> int:
    """
    Load unpublished outbox events, project each one into the read model, then mark it published.
    Projection happens before mark_published so a crash can replay the same event.
    Version guards on the read repository keep that replay idempotent.
    :return: number of events that were projected in this cycle
    """
    event_repository = _build_outbox_repository()
    projector = _build_projection()
    unpublished = await event_repository.find_unpublished()
    for event in unpublished:
        await projector.project(event)
        await event_repository.mark_published(event.event_id)
    return len(unpublished)


async def run_inventory_projection_worker(poll_interval: float = 1.0) -> None:
    """
    Continuously drain the inventory outbox into the projection store.
    :param poll_interval: seconds to wait after each projection cycle
    :return:
    """
    while True:
        await project_unpublished_events()
        await asyncio.sleep(poll_interval)
