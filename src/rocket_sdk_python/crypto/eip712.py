from eth_account import Account
from eth_hash.auto import keccak

ROCKET_CHAIN_DOMAIN = {
    "name": "RocketChain",
    "version": "1",
}

EIP712_DOMAIN_TYPE = [
    {"name": "name", "type": "string"},
    {"name": "version", "type": "string"},
]

ROCKET_CHAIN_MESSAGE_TYPE = [
    {"name": "contents", "type": "bytes32"},
]


def _encode_type(type_name: str, type_fields: list[dict]) -> bytes:
    fields_str = ",".join(f"{f['type']} {f['name']}" for f in type_fields)
    return f"{type_name}({fields_str})".encode("utf-8")


def _hash_type(type_name: str, type_fields: list[dict]) -> bytes:
    return keccak(_encode_type(type_name, type_fields))


def _encode_data(type_fields: list[dict], data: dict) -> bytes:
    encoded = b""
    for field in type_fields:
        value = data[field["name"]]
        if field["type"] == "string":
            encoded += keccak(value.encode("utf-8"))
        elif field["type"] == "bytes32":
            if isinstance(value, bytes):
                encoded += value
            else:
                encoded += bytes.fromhex(value.replace("0x", ""))
        else:
            raise ValueError(f"Unsupported type: {field['type']}")
    return encoded


def _hash_struct(type_name: str, type_fields: list[dict], data: dict) -> bytes:
    type_hash = _hash_type(type_name, type_fields)
    encoded_data = _encode_data(type_fields, data)
    return keccak(type_hash + encoded_data)


def _domain_separator() -> bytes:
    return _hash_struct("EIP712Domain", EIP712_DOMAIN_TYPE, ROCKET_CHAIN_DOMAIN)


def eip712_signing_hash(message: bytes) -> bytes:
    contents_hash = keccak(message)
    struct_hash = _hash_struct(
        "RocketChainMessage",
        ROCKET_CHAIN_MESSAGE_TYPE,
        {"contents": contents_hash},
    )
    return keccak(b"\x19\x01" + _domain_separator() + struct_hash)


def sign_eip712(message: bytes, private_key: str) -> str:
    digest = eip712_signing_hash(message)
    signed = Account.unsafe_sign_hash(digest, private_key=private_key)
    return "0x" + signed.signature.hex()

