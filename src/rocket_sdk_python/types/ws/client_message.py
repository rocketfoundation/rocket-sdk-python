from pydantic import BaseModel, ConfigDict

from rocket_sdk_python.types.ws.subscription_kind import SubscriptionKind


class Subscribe(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Subscribe: SubscriptionKind


class Unsubscribe(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Unsubscribe: SubscriptionKind


class Ping(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Ping: None = None


ClientMessage = Subscribe | Unsubscribe | Ping
