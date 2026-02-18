from enum import Enum
from typing import Union

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, Signature
from rocket_sdk_python.types.transaction.instruction import (
    CreateVaultInstruction,
    PlaceOrderInstruction,
    SetLeverageInstruction,
    VaultDepositInstruction,
    VaultWithdrawInstruction,
    WithdrawInstruction,
)


class SerializationFormat(str, Enum):
    JSON = "JSON"
    MESSAGE_PACK = "MessagePack"


class SignatureScheme(str, Enum):
    EIP191 = "EIP191"
    EIP712 = "EIP712"


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

