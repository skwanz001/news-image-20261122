#!/usr/bin/env python3
"""Entry for news-image-20261122: write the day's poster to the output.

The poster (entry.png, drawn by draw.py from the real news of Sunday
22 November 2026) ships in the repository; this program copies it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library
only — the grading sandbox installs nothing, so the entry must not
import PIL or any other third-party package.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(dst, "written", os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
