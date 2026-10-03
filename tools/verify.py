"""verify.py - check files in source/ against MANIFEST.json SHA256.
Usage: python tools/verify.py
Reports, for every file listed in the manifest: OK / MISMATCH / MISSING,
plus any extra files found in source/ that are not in the manifest."""

import argparse
import hashlib
import json
import os
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="считать неучтённые файлы source/ нарушением целостности",
    )
    args = parser.parse_args()
    man_path = os.path.join(SRC, "MANIFEST.json")
    if not os.path.exists(man_path):
        print("MANIFEST.json not found in source/. Place the package first.")
        return 2
    with open(man_path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    listed = {entry["path"]: entry for entry in manifest["files"]}
    ok = missing = mismatch = 0
    print(f"package: {manifest.get('package')}  exported: {manifest.get('exported_at_utc')}")
    print(f"{'STATUS':9} {'SIZE':>9}  FILE")
    for path, entry in listed.items():
        full = os.path.join(SRC, path)
        if not os.path.exists(full):
            print(f"{'MISSING':9} {entry['size']:>9}  {path}")
            missing += 1
            continue
        actual = sha256(full)
        if actual == entry["sha256"]:
            print(f"{'OK':9} {entry['size']:>9}  {path}")
            ok += 1
        else:
            print(f"{'MISMATCH':9} {entry['size']:>9}  {path}  (got {actual[:12]}...)")
            mismatch += 1
    present = set(os.listdir(SRC))
    extra = sorted(present - set(listed) - {"MANIFEST.json"})
    for name in extra:
        print(f"{'EXTRA':9} {os.path.getsize(os.path.join(SRC, name)):>9}  {name}")
    print(
        f"\nsummary: {ok} ok, {missing} missing, {mismatch} mismatch, "
        f"{len(listed)} in manifest, {len(extra)} extra"
    )
    return 0 if (missing == 0 and mismatch == 0 and (not args.strict or not extra)) else 1


if __name__ == "__main__":
    sys.exit(main())
