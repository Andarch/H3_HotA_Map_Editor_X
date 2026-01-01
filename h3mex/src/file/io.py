import sys
from typing import BinaryIO, Optional

in_file: Optional[BinaryIO] = None
out_file: Optional[BinaryIO] = None
bytes_read: int = 0


def get_position() -> int:
    """Get the current byte position in the file."""
    return bytes_read


def reset_position() -> None:
    """Reset the byte position counter (call when opening a new file)."""
    global bytes_read
    bytes_read = 0


def seek(length: int) -> None:
    global bytes_read
    in_file.seek(length, 1)
    bytes_read += length


def read_raw(length: int) -> bytes:
    global bytes_read
    data = in_file.read(length)
    bytes_read += len(data)
    return data


def read_int(length: int) -> int:
    global bytes_read
    data = in_file.read(length)
    bytes_read += len(data)
    return int.from_bytes(data, "little")


def read_str(length: int) -> str:
    global bytes_read
    data = in_file.read(length)
    bytes_read += len(data)
    return data.decode("latin-1")


def read_bits(length: int) -> list:
    temp_bits = []
    raw_data = read_raw(length)

    for c in raw_data:
        bits = format(int(c), "#010b").removeprefix("0b")[::-1]
        for b in bits:
            temp_bits.append(1 if b == "1" else 0)

    return temp_bits


def write_raw(data: bytes):
    global out_file
    out_file.write(data)


def write_int(data: int, length: int) -> None:
    global out_file
    out_file.write(data.to_bytes(length, "little"))


def write_str(data: str) -> None:
    global out_file
    out_file.write(data.encode("latin-1"))


def write_bits(data: list) -> None:
    for i in range(0, len(data), 8):
        s = ""
        for b in range(8):
            s += "1" if data[i + b] else "0"
        write_int(int(s[::-1], 2), 1)


def with_position_tracking(func):
    """Decorator that catches exceptions and adds byte position information."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            position = get_position()
            print(f"\n{'='*60}", file=sys.stderr)
            print(f"ERROR at byte position: {position} (0x{position:X})", file=sys.stderr)
            print(f"{'='*60}\n", file=sys.stderr)
            raise

    return wrapper
