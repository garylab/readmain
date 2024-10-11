import zlib


def int_hash(sentence: str) -> int:
    return zlib.crc32(sentence.encode())
