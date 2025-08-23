from .h3m import h3m


def read_raw(length: int) -> bytes:
    return map.read(length)


def read_int(length: int) -> int:
    return int.from_bytes(map.read(length), "little")


def read_str(length: int) -> str:
    return map.read(length).decode("latin-1")


def read_bits(length: int) -> list:
    temp_bits = []
    raw_data = read_raw(length)

    for c in raw_data:
        bits = format(int(c), "#010b").removeprefix("0b")[::-1]
        for b in bits:
            temp_bits.append(1 if b == "1" else 0)

    return temp_bits


def write_raw(data: bytes):
    global h3m
    h3m.write(data)


def write_int(data: int, length: int) -> None:
    global h3m
    h3m.write(data.to_bytes(length, "little"))


def write_str(data: str) -> None:
    global h3m
    h3m.write(data.encode("latin-1"))


def write_bits(data: list) -> None:
    for i in range(0, len(data), 8):
        s = ""
        for b in range(8):
            s += "1" if data[i + b] else "0"
        write_int(int(s[::-1], 2), 1)


def seek(length: int) -> None:
    h3m.seek(length, 1)
