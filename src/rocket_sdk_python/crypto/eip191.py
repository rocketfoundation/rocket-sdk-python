from eth_account import Account
from eth_account.messages import encode_defunct
from eth_hash.auto import keccak


def eip191_hash(message: bytes) -> bytes:
    prefix = f"\x19Ethereum Signed Message:\n{len(message)}"
    return keccak(prefix.encode("utf-8") + message)


def sign_eip191(message: bytes, private_key: str) -> str:
    signable = encode_defunct(primitive=message)
    signed = Account.sign_message(signable, private_key=private_key)
    return "0x" + signed.signature.hex()
