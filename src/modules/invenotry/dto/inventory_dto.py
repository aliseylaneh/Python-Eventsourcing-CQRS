from uuid import UUID

from pydantic import BaseModel, PositiveInt


class UserIDDTO(BaseModel):
    """
    Shared request field for the user that initiated an inventory command.
    """

    user_id: UUID


class InventoryReserveStock(UserIDDTO, BaseModel):
    """
    Request body for reserving a positive quantity from an inventory.
    """

    quantity: PositiveInt


class CompleteReservedStock(UserIDDTO, BaseModel):
    """
    Request body for completing a previously reserved positive quantity.
    """

    quantity: PositiveInt


class CreateInventory(UserIDDTO, BaseModel):
    """
    Request body for creating a new inventory stream.
    """

    sku: str
    soh: PositiveInt
    available_quantity: PositiveInt


class UpdateInventory(UserIDDTO, BaseModel):
    """
    Request body for replacing soh and available quantity.
    """

    soh: PositiveInt
    available_quantity: PositiveInt


class InventoryResponse(BaseModel):
    """
    API response for inventory state.
    Identity is sku, so a separate id field is not required.
    """

    sku: str
    soh: int
    reserved: int
    available_quantity: int
