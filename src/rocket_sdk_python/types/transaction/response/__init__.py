from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives.account_address import AccountAddress
from rocket_sdk_python.types.primitives.asset import AssetRow
from rocket_sdk_python.types.primitives.instrument import InstrumentRow
from rocket_sdk_python.types.transaction.response.oracle_settings import (
    OraclePriceScale,
    OracleSettingsMap,
    OracleState,
    SourceId,
)
from rocket_sdk_python.types.transaction.response.order import (
    OrderEvent,
    OrderEventCanceledData,
    OrderEventData,
    OrderEventFillData,
    OrderEventModifiedData,
    OrderEventPlacedData,
    OrderEventRejectedData,
    PlaceOrderErr,
    PlaceOrderResult,
    PlaceOrderSuccess,
)


class PlaceOrderTransactionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["PlaceOrder"] = "PlaceOrder"
    results: list[PlaceOrderResult]


class CreateVaultTransactionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["CreateVault"] = "CreateVault"
    vault_address: AccountAddress = Field(alias="vaultAddress")


class VaultDepositTransactionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["VaultDeposit"] = "VaultDeposit"
    vault_address: AccountAddress = Field(alias="vaultAddress")
    deposited_amount: str = Field(alias="depositedAmount")
    minted_shares: str = Field(alias="mintedShares")


class VaultWithdrawTransactionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["VaultWithdraw"] = "VaultWithdraw"
    vault_address: AccountAddress = Field(alias="vaultAddress")
    burned_shares: str = Field(alias="burnedShares")
    payout_quantity: str = Field(alias="payoutQuantity")


class DelegateManagerTransactionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["DelegateManager"] = "DelegateManager"
    delegator: AccountAddress
    manager: AccountAddress


class UpdateOracleConfigResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["UpdateOracleConfig"] = "UpdateOracleConfig"
    new_quote_symbol_pattern: str | None = Field(
        default=None, alias="newQuoteSymbolPattern"
    )
    updated_oracle_settings: OracleSettingsMap | None = Field(
        default=None, alias="updatedOracleSettings"
    )


class ListAssetsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["ListAssets"] = "ListAssets"
    assets: list[AssetRow]


class ListInstrumentsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["ListInstruments"] = "ListInstruments"
    instruments: list[InstrumentRow]


class OkResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Ok"] = "Ok"


class ErrResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Err"] = "Err"
    message: str


TransactionResponse = Annotated[
    PlaceOrderTransactionResponse
    | CreateVaultTransactionResponse
    | VaultDepositTransactionResponse
    | VaultWithdrawTransactionResponse
    | DelegateManagerTransactionResponse
    | UpdateOracleConfigResponse
    | ListAssetsResponse
    | ListInstrumentsResponse
    | OkResponse
    | ErrResponse,
    Field(discriminator="type"),
]


__all__ = [
    "CreateVaultTransactionResponse",
    "DelegateManagerTransactionResponse",
    "ErrResponse",
    "ListAssetsResponse",
    "ListInstrumentsResponse",
    "OkResponse",
    "OraclePriceScale",
    "OracleSettingsMap",
    "OracleState",
    "OrderEvent",
    "OrderEventCanceledData",
    "OrderEventData",
    "OrderEventFillData",
    "OrderEventModifiedData",
    "OrderEventPlacedData",
    "OrderEventRejectedData",
    "PlaceOrderErr",
    "PlaceOrderResult",
    "PlaceOrderSuccess",
    "PlaceOrderTransactionResponse",
    "SourceId",
    "TransactionResponse",
    "UpdateOracleConfigResponse",
    "VaultDepositTransactionResponse",
    "VaultWithdrawTransactionResponse",
]
