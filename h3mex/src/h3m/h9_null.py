from . import io


def read_null() -> bytes:
    return io.in_file.read()


def write_null(info: bytes) -> None:
    io.write_raw(info)
