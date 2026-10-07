"""Stop: если source/ изменён и не закоммичен — не завершать ход, пока verify.py --strict не даст 0 mismatch."""
import json
import os
import subprocess
import sys

data = json.load(sys.stdin)
if data.get("stop_hook_active"):
    sys.exit(0)

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dirty = subprocess.run(["git", "status", "--porcelain", "--", "source"], cwd=root,
                       capture_output=True, text=True).stdout.strip()
if not dirty:
    sys.exit(0)

r = subprocess.run([sys.executable, "-X", "utf8", "tools/verify.py", "--strict"], cwd=root,
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
if r.returncode != 0:
    tail = (r.stdout + r.stderr).strip()[-1500:]
    sys.stderr.write("source/ изменён, но verify.py --strict не проходит. "
                     "Выполните tools/rebuild_canon.py и повторите проверку.\n" + tail + "\n")
    sys.exit(2)
