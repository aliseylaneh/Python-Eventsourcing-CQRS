from internal.domain.interfaces.repositories.iinventory import \
    IInventoryProjectionRepository
from internal.modules.invenotry.events.v1.inventory import (InventoryEventDTO,
                                                            InventoryEventType)


class InventoryProjection:

    def __init__(
        self,
        repository: IInventoryProjectionRepository,
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
                    event.sku,
                    event.reserved,
                )

            case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                await self.repository.decrease_available_quantity(
                    event.sku,
                    event.available_quantity,
                )

            case InventoryEventType.PROCESSED_RESERVED_DECREASED:
                await self.repository.decrease_reserved(
                    event.sku,
                    event.reserved,
                )

            case InventoryEventType.PROCESSED_RESERVED_SOH_DECREASED:
                await self.repository.decrease_reserved_and_soh(
                    event.sku,
                    event.soh,
                )

            case InventoryEventType.SOH_REPLACED:
                await self.repository.replace_soh(
                    event.sku,
                    event.soh,
                )

            case InventoryEventType.AVAILABLE_QUANTITY_REPLACED:
                await self.repository.replace_available_quantity(
                    event.sku,
                    event.available_quantity,
                )
