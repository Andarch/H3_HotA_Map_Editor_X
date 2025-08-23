from . import io


def read_null() -> bytes:
    return io.read_raw(124)


def write_null(info: bytes) -> None:
    io.write_raw(info)
