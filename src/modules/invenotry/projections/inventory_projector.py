from src.domain.interfaces.repositories.iinventory import \
    IMongoInventoryReadRepository
from src.modules.invenotry.events.v1.inventory_events import (
    InventoryEventDTO, InventoryEventType)


class InventoryProjection:

    def __init__(
        self,
        repository: IMongoInventoryReadRepository,
    ):
        self.repository = repository

    async def project(self, event: InventoryEventDTO):

        match event.event_type:
            case InventoryEventType.INVENTORY_CREATED:
                await self.repository.create(
                    {
                        "sku": event.sku,
                        "soh": event.soh,
                        "available_quantity": event.available_quantity,
                        "reserved": event.reserved,
                    }
                )
            case InventoryEventType.STOCK_RESERVED:
                await self.repository.increase_reserved(
                    sku=event.sku,
                    amount=event.reserved,
                )

            case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                await self.repository.decrease_available_quantity(
                    sku=event.sku,
                    amount=event.available_quantity,
                )

            case InventoryEventType.PROCESSED_RESERVED_DECREASED:
                await self.repository.decrease_reserved(
                    sku=event.sku,
                    amount=event.reserved,
                )

            case InventoryEventType.PROCESSED_RESERVED_SOH_DECREASED:
                await self.repository.decrease_soh(
                    sku=event.sku,
                    amount=event.soh,
                )

            case InventoryEventType.SOH_REPLACED:
                await self.repository.set_soh(
                    sku=event.sku,
                    soh=event.soh,
                )

            case InventoryEventType.AVAILABLE_QUANTITY_REPLACED:
                await self.repository.set_available_quantity(
                    sku=event.sku,
                    available_quantity=event.available_quantity,
                )
