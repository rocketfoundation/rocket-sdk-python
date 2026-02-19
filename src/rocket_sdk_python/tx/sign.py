from rocket_sdk_python.crypto.signer import AccountSigner
from rocket_sdk_python.tx.serialization import serialize
from rocket_sdk_python.types.transaction.sign import (
    RawTransaction,
    SerializationFormat,
    SignatureScheme,
    Transaction,
)


def sign_transaction(
    raw_tx: RawTransaction,
    signer: AccountSigner,
    fmt: SerializationFormat = SerializationFormat.JSON,
    scheme: SignatureScheme = SignatureScheme.EIP191,
) -> Transaction:
    serialized = serialize(raw_tx, fmt)
    signature = signer.sign(serialized, scheme)
    return Transaction(
        data=raw_tx,
        serialization_format=fmt,
        signature_scheme=scheme,
        signature=signature,
    )

