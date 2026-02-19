from eth_account import Account
from eth_keys import keys

from rocket_sdk_python.crypto.eip191 import sign_eip191
from rocket_sdk_python.crypto.eip712 import sign_eip712
from rocket_sdk_python.types.primitives import AccountAddress
from rocket_sdk_python.types.transaction.sign import SignatureScheme


class AccountSigner:
    _private_key: str
    _address: AccountAddress

    def __init__(self, private_key: str):
        key = private_key.strip()
        if key.startswith("0x"):
            key = key[2:]
        self._private_key = key
        pk = keys.PrivateKey(bytes.fromhex(key))
        self._address = AccountAddress(pk.public_key.to_checksum_address())

    @classmethod
    def from_private_key(cls, private_key: str) -> "AccountSigner":
        return cls(private_key)

    @classmethod
    def dummy(cls) -> "AccountSigner":
        return cls("0x1111111111111111111111111111111111111111111111111111111111111111")

    @property
    def address(self) -> AccountAddress:
        return self._address

    def sign(self, message: bytes, scheme: SignatureScheme = SignatureScheme.EIP191) -> str:
        if scheme == SignatureScheme.EIP191:
            return sign_eip191(message, self._private_key)
        elif scheme == SignatureScheme.EIP712:
            return sign_eip712(message, self._private_key)
        else:
            raise ValueError(f"Unsupported signature scheme: {scheme}")

