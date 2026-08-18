from pydantic import BaseModel, ConfigDict

from rocket_sdk_python.types.transaction.sign import Transaction
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


class SubmitTransaction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    SubmitTransaction: Transaction


class RegisterExecuteOnDisconnect(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    RegisterExecuteOnDisconnect: Transaction


class ClearExecuteOnDisconnect(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ClearExecuteOnDisconnect: None = None


ClientMessage = (
    Subscribe
    | Unsubscribe
    | Ping
    | SubmitTransaction
    | RegisterExecuteOnDisconnect
    | ClearExecuteOnDisconnect
)
