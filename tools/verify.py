"""verify.py - check files in source/ against MANIFEST.json SHA256.
Usage: python tools/verify.py
Reports, for every file listed in the manifest: OK / MISMATCH / MISSING,
plus any extra files found in source/ that are not in the manifest."""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    man_path = os.path.join(SRC, "MANIFEST.json")
    if not os.path.exists(man_path):
        print("MANIFEST.json not found in source/. Place the package first.")
        return 2
    man = json.load(open(man_path, encoding="utf-8"))
    listed = {e["path"]: e for e in man["files"]}
    ok = miss = bad = 0
    print(f"package: {man.get('package')}  exported: {man.get('exported_at_utc')}")
    print(f"{'STATUS':9} {'SIZE':>9}  FILE")
    for path, e in listed.items():
        full = os.path.join(SRC, path)
        if not os.path.exists(full):
            print(f"{'MISSING':9} {e['size']:>9}  {path}")
            miss += 1
            continue
        got = sha256(full)
        if got == e["sha256"]:
            print(f"{'OK':9} {e['size']:>9}  {path}")
            ok += 1
        else:
            print(f"{'MISMATCH':9} {e['size']:>9}  {path}  (got {got[:12]}...)")
            bad += 1
    present = set(os.listdir(SRC))
    extra = sorted(present - set(listed) - {"MANIFEST.json"})
    for x in extra:
        print(f"{'EXTRA':9} {os.path.getsize(os.path.join(SRC,x)):>9}  {x}")
    print(f"\nsummary: {ok} ok, {miss} missing, {bad} mismatch, "
          f"{len(listed)} in manifest, {len(extra)} extra")
    return 0 if (miss == 0 and bad == 0) else 1

if __name__ == "__main__":
    sys.exit(main())
