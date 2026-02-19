import msgpack

from rocket_sdk_python.types.transaction.sign import (
    RawTransaction,
    SerializationFormat,
)


def serialize_json(raw_tx: RawTransaction) -> bytes:
    return raw_tx.model_dump_json(by_alias=True).encode("utf-8")


def serialize_msgpack(raw_tx: RawTransaction) -> bytes:
    data = raw_tx.model_dump(by_alias=True, mode="json")
    return msgpack.packb(data, use_bin_type=True)


def serialize(raw_tx: RawTransaction, fmt: SerializationFormat) -> bytes:
    if fmt == SerializationFormat.JSON:
        return serialize_json(raw_tx)
    elif fmt == SerializationFormat.MESSAGE_PACK:
        return serialize_msgpack(raw_tx)
    else:
        raise ValueError(f"Unsupported serialization format: {fmt}")


def deserialize_json(data: bytes) -> RawTransaction:
    return RawTransaction.model_validate_json(data)


def deserialize_msgpack(data: bytes) -> RawTransaction:
    unpacked = msgpack.unpackb(data, raw=False)
    return RawTransaction.model_validate(unpacked)


def deserialize(data: bytes, fmt: SerializationFormat) -> RawTransaction:
    if fmt == SerializationFormat.JSON:
        return deserialize_json(data)
    elif fmt == SerializationFormat.MESSAGE_PACK:
        return deserialize_msgpack(data)
    else:
        raise ValueError(f"Unsupported serialization format: {fmt}")

