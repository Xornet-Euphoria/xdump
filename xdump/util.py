from struct import unpack


def is_unpackable(data):
    return  len(data) == 8 or len(data) == 4


def upk(data, endian="little"):
    if not is_unpackable:
        raise ValueError("data length must be 4 or 8")

    if endian != "little" and endian != "big":
        raise ValueError("little or big endian are allowed")

    fmt = "<" if endian == "little" else ">"
    fmt += "Q" if len(data) == 8 else "L"

    return unpack(fmt, data)[0]
