#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue - entry program.

Copies the shipped meme image (entry.png, rendered deterministically by
generate_meme.py) to /output/entry.png.

Stdlib only, no network, no randomness, no API key: the output is a
byte-for-byte copy of entry.png, so every run produces identical bytes.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1

    out_dir = os.environ.get("OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "entry.png")
        shutil.copyfile(src, dst)
    except OSError:
        # /output not writable (local runs): fall back to ./output
        out_dir = os.path.join(here, "output")
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "entry.png")
        shutil.copyfile(src, dst)

    print("wrote " + dst + " (" + str(os.path.getsize(dst)) + " bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
