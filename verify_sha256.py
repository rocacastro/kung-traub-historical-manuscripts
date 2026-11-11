#!/usr/bin/env python3
"""Verify archived historical files using the SHA-256 manifest.

This check requires only Python 3 and does not change any files.
"""
from hashlib import sha256
from pathlib import Path

root = Path(__file__).resolve().parent
failed = False
for item in (root / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    if not item.strip() or item.startswith("#"):
        continue
    expected, relative = item.split("  ", 1)
    path = root / relative
    if not path.is_file():
        print(f"MISSING:  {relative}")
        failed = True
        continue
    actual = sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        print(f"MISMATCH: {relative}")
        failed = True
    else:
        print(f"OK:       {relative}")
print("Verification failed." if failed else "All archived files match their SHA-256 hashes.")
raise SystemExit(1 if failed else 0)
