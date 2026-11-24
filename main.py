#!/usr/bin/env python3
"""make.fun entry: news-image-20261124 (magazine cover).

Writes the pre-rendered 1024x1024 image of Tuesday 24 November 2026's world
news to the output directory. Standard library only.

Before copying, the PNG header is validated (signature + IHDR dimensions must
be exactly 1024x1024 and the file at most 1 MiB), so a corrupt or wrong-sized
image fails loudly instead of being submitted. After copying, the destination
size is verified against the source.
"""
import os
import shutil
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
EXPECT_W, EXPECT_H = 1024, 1024


def validate_png(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != PNG_SIGNATURE:
        raise SystemExit(f"not a PNG file: {path}")
    if len(head) < 33 or head[12:16] != b"IHDR":
        raise SystemExit(f"missing IHDR chunk: {path}")
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (EXPECT_W, EXPECT_H):
        raise SystemExit(f"expected {EXPECT_W}x{EXPECT_H}, got {width}x{height}")
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB limit")
    return size


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    size = validate_png(src)
    shutil.copyfile(src, dst)
    copied = os.path.getsize(dst)
    if copied != size:
        raise SystemExit(f"copy size mismatch: {copied} != {size}")
    print(f"wrote {dst} ({copied} bytes, validated {EXPECT_W}x{EXPECT_H})")


if __name__ == "__main__":
    sys.exit(main())
