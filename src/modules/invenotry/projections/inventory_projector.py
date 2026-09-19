from src.domain.interfaces.repositories.iinventory import \
    IMongoInventoryReadRepository
from src.modules.invenotry.events.v1.inventory_events import (
    InventoryEventDTO, InventoryEventType)


class InventoryProjection:
    """
    Maps inventory events onto the read-model repository.
    Each event type updates a different projection field and always forwards event version
    so the read store can ignore already applied or older events.
    """

    def __init__(
        self,
        repository: IMongoInventoryReadRepository,
    ):
        self.repository = repository

    async def project(self, event: InventoryEventDTO):
        """
        Apply one unpublished event to the inventory projection.
        :param event: inventory event loaded from the outbox
        :return:
        """

        match event.event_type:
            case InventoryEventType.INVENTORY_CREATED:
                await self.repository.create(
                    {
                        "sku": event.sku,
                        "soh": event.soh,
                        "available_quantity": event.available_quantity,
                        "reserved": event.reserved,
                        "last_applied_version": event.version,
                    }
                )
            case InventoryEventType.STOCK_RESERVED:
                await self.repository.increase_reserved(
                    sku=event.sku,
                    amount=event.reserved,
                    version=event.version,
                )

            case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                await self.repository.decrease_available_quantity(
                    sku=event.sku,
                    amount=event.available_quantity,
                    version=event.version,
                )

            case InventoryEventType.PROCESSED_RESERVED_DECREASED:
                await self.repository.decrease_reserved(
                    sku=event.sku,
                    amount=event.reserved,
                    version=event.version,
                )

            case InventoryEventType.PROCESSED_RESERVED_SOH_DECREASED:
                await self.repository.decrease_soh(
                    sku=event.sku,
                    amount=event.soh,
                    version=event.version,
                )

            case InventoryEventType.SOH_REPLACED:
                await self.repository.set_soh(
                    sku=event.sku,
                    soh=event.soh,
                    version=event.version,
                )

            case InventoryEventType.AVAILABLE_QUANTITY_REPLACED:
                await self.repository.set_available_quantity(
                    sku=event.sku,
                    available_quantity=event.available_quantity,
                    version=event.version,
                )
