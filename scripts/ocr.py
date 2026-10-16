#!/usr/bin/env python3
import os
import subprocess
import tempfile


def main():
    try:
        geometry = subprocess.check_output(["slurp"]).decode().strip()
    except subprocess.CalledProcessError:
        return
    if not geometry:
        return

    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        subprocess.run(["grim", "-g", geometry, path], check=True)
        text = subprocess.check_output(
            ["tesseract", path, "stdout"], stderr=subprocess.DEVNULL
        ).decode()
    finally:
        os.unlink(path)

    if text.strip():
        subprocess.run(["wl-copy"], input=text.encode())


if __name__ == "__main__":
    main()
