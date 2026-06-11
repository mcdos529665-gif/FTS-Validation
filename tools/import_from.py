"""import_from.py - copy the FTS package files from a folder into source/ and verify.

Use this after you download the uploaded files from the chat into any folder.
It copies every file listed in source/MANIFEST.json (matching by name) from the
given folder, overwrites whatever is in source/, then runs the SHA256 check.

It also copies a few non-manifest extras if present: дополнение.txt

Usage (from project root):
  python tools/import_from.py "C:\\Users\\Mcdos\\Downloads"
"""
import json, os, shutil, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source")
EXTRAS = ["дополнение.txt"]


def main():
    if len(sys.argv) < 2:
        sys.exit('usage: python tools/import_from.py "<folder with the uploaded files>"')
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        sys.exit(f"not a folder: {folder}")
    man = json.load(open(os.path.join(SRC, "MANIFEST.json"), encoding="utf-8"))
    wanted = [e["path"] for e in man["files"]] + EXTRAS
    copied, absent = [], []
    for name in wanted:
        src = os.path.join(folder, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(SRC, name))
            copied.append(name)
        else:
            absent.append(name)
    print(f"copied {len(copied)} file(s) from {folder}")
    if absent:
        print("not found in that folder:", ", ".join(absent))
    print("-" * 40)
    subprocess.run([sys.executable, "-X", "utf8", os.path.join(ROOT, "tools", "verify.py")])


if __name__ == "__main__":
    main()
