#!/usr/bin/env python3
"""Deliver the front-page artwork for news-image-20261126.

The finished newspaper page ships inside this repository two ways:
as ``entry.png`` itself, and as ``entry.png.b64``, the same bytes in
base64 text. The grading sandbox checks out text only, so there the
program takes the base64 copy, decodes it in memory, and writes the
picture to the output folder. A full checkout uses ``entry.png``
directly when it is present.

Before anything is delivered, the PNG is checked the way the
competition gate describes a whole image: the signature, then every
chunk in order with its CRC verified, an IHDR first with dimensions
of at most 1024 by 1024, an IEND at the end, and at most 1 MiB in
total. Anything that fails is refused, never delivered.

Standard library only. No network. Every run writes the same bytes.
"""

import base64
import os
import sys
import zlib
from pathlib import Path

PICTURE = "entry.png"
EMBEDDED = "entry.png.b64"
OUT_NAME = "entry.png"

BYTE_LIMIT = 1024 * 1024
SIDE_LIMIT = 1024
SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


class PictureError(Exception):
    """The artwork failed one of the delivery checks."""


def check_png(blob, label):
    """Walk a whole PNG; return (width, height) or raise PictureError."""
    if len(blob) > BYTE_LIMIT:
        raise PictureError(f"{label} is {len(blob)} bytes, over the {BYTE_LIMIT} limit")
    if not blob.startswith(SIGNATURE):
        raise PictureError(f"{label} does not start with a PNG signature")
    pos = len(SIGNATURE)
    width = height = None
    while True:
        if pos + 8 > len(blob):
            raise PictureError(f"{label} ends mid-chunk, with no IEND")
        size = int.from_bytes(blob[pos:pos + 4], "big")
        kind = blob[pos + 4:pos + 8]
        body_end = pos + 8 + size
        if body_end + 4 > len(blob):
            raise PictureError(f"{label} has a truncated {kind!r} chunk")
        body = blob[pos + 8:body_end]
        stored_crc = int.from_bytes(blob[body_end:body_end + 4], "big")
        if zlib.crc32(kind + body) & 0xFFFFFFFF != stored_crc:
            raise PictureError(f"{label} has a bad CRC in its {kind!r} chunk")
        if width is None:
            if kind != b"IHDR" or size != 13:
                raise PictureError(f"{label} does not open with a 13-byte IHDR")
            width = int.from_bytes(body[0:4], "big")
            height = int.from_bytes(body[4:8], "big")
            if width > SIDE_LIMIT or height > SIDE_LIMIT:
                raise PictureError(f"{label} is {width}x{height}, over the {SIDE_LIMIT} side limit")
        pos = body_end + 4
        if kind == b"IEND":
            break
    if pos != len(blob):
        raise PictureError(f"{label} has bytes after its IEND chunk")
    return width, height


def obtain(script_dir):
    """Return (blob, width, height) from the best source at hand.

    When both copies are present they must agree byte for byte: a
    stale base64 copy beside a newer picture is refused, not quietly
    delivered in the picture's place.
    """
    plain = script_dir / PICTURE
    packed = script_dir / EMBEDDED
    blob = None
    if plain.is_file():
        blob = plain.read_bytes()
        check_png(blob, PICTURE)
    if packed.is_file():
        try:
            decoded = base64.b64decode(packed.read_bytes().strip(), validate=True)
        except ValueError as exc:
            raise PictureError(f"{EMBEDDED} is not valid base64: {exc}")
        check_png(decoded, EMBEDDED)
        if blob is not None and decoded != blob:
            raise PictureError(f"{EMBEDDED} does not match {PICTURE}")
        blob = decoded
    if blob is None:
        raise PictureError(f"no {PICTURE} or {EMBEDDED} beside this script")
    width, height = check_png(blob, PICTURE)
    return blob, width, height


def run():
    script_dir = Path(__file__).resolve().parent
    try:
        blob, width, height = obtain(script_dir)
    except PictureError as problem:
        print(f"refusing to deliver: {problem}", file=sys.stderr)
        return 1
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / OUT_NAME
    target.write_bytes(blob)
    print(f"delivered {OUT_NAME} ({width}x{height}, {len(blob)} bytes) to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
