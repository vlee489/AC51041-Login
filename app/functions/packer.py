"""Handles msgpack functions"""
import datetime
import msgpack


def __decode(obj):
    if '__datetime__' in obj:
        obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
    return obj


def __encode(obj):
    if isinstance(obj, datetime.datetime):
        return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj


def pack(message: dict) -> bytes:
    return msgpack.packb(message, default=__encode, use_bin_type=True)


def unpack(message: bytes):
    return msgpack.unpackb(message, object_hook=__decode, raw=False)

