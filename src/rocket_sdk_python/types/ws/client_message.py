from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.ws.subscription_kind import SubscriptionKind


class Subscribe(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Subscribe"] = "Subscribe"
    subscription: SubscriptionKind


class Unsubscribe(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Unsubscribe"] = "Unsubscribe"
    subscription: SubscriptionKind


class Ping(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Ping"] = "Ping"


ClientMessage = Annotated[
    Subscribe | Unsubscribe | Ping,
    Field(discriminator="type"),
]

