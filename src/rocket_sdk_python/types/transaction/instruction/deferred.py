from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.transaction.instruction.order import OrderRequestSet


class DeferredData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    expires_at_ms: int = Field(alias="expiresAtMs")
    orders: OrderRequestSet


class DeferredInstruction(BaseModel):
    Deferred: DeferredData
