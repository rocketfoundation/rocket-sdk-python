from enum import Enum
from typing import Union

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.base import (
    AccountAddress,
    AssetId,
    InstrumentId,
    Signature,
)
from rocket_sdk_python.types.orders import OrderRequestSet


class SerializationFormat(str, Enum):
    JSON = "JSON"
    MESSAGE_PACK = "MessagePack"


class SignatureScheme(str, Enum):
    EIP191 = "EIP191"
    EIP712 = "EIP712"


class WithdrawData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asset_id: AssetId = Field(alias="assetId")
    amount: str
    to: str


class CreateVaultData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    deposit_asset: AssetId = Field(alias="depositAsset")
    initial_deposit: str = Field(alias="initialDeposit")


class VaultDepositData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault: AccountAddress
    amount: str


class VaultWithdrawData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault: AccountAddress
    shares: str


class SetLeverageData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    to: AccountAddress
    instrument_id: InstrumentId = Field(alias="instrumentId")
    leverage: int


class PlaceOrderInstruction(BaseModel):
    PlaceOrder: OrderRequestSet


class WithdrawInstruction(BaseModel):
    Withdraw: WithdrawData


class CreateVaultInstruction(BaseModel):
    CreateVault: CreateVaultData


class VaultDepositInstruction(BaseModel):
    VaultDeposit: VaultDepositData


class VaultWithdrawInstruction(BaseModel):
    VaultWithdraw: VaultWithdrawData


class SetLeverageInstruction(BaseModel):
    SetLeverage: SetLeverageData


TransactionInstruction = Union[
    PlaceOrderInstruction,
    WithdrawInstruction,
    CreateVaultInstruction,
    VaultDepositInstruction,
    VaultWithdrawInstruction,
    SetLeverageInstruction,
]


class RawTransaction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sender: AccountAddress
    instruction: TransactionInstruction
    nonce: int


class Transaction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: RawTransaction
    serialization_format: SerializationFormat = Field(alias="serializationFormat")
    signature_scheme: SignatureScheme = Field(
        default=SignatureScheme.EIP191, alias="signatureScheme"
    )
    signature: Signature
