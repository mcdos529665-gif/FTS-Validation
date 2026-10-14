"""Фиксированная команда запуска экспериментов OpenResearch (orx).

Запуск из корня проекта: py -3.11 -X utf8 experiments/run.py
Читает experiments/ACTIVE, проверяет границу записи ветки orx/* и запускает
experiments/<ACTIVE>/run.py тем же интерпретатором. Контракт — experiments/AGENTS.md.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments"
BASE_BRANCH = "master"
SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def git(*args):
    r = subprocess.run(["git", "-C", str(ROOT), *args],
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout.strip()


def check_scope():
    """Ветка orx/* может менять только experiments/. Без .git (архив прогона) — пропуск."""
    code, branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if code != 0:
        print("scope: git недоступен (архив прогона) — проверка пропущена")
        return
    if not branch.startswith("orx/"):
        print(f"scope: ветка {branch} — не orx/*, проверка не требуется")
        return
    code, base = git("merge-base", "HEAD", BASE_BRANCH)
    if code != 0:
        sys.exit(f"scope: FAIL — нет общей базы с {BASE_BRANCH}")
    _, committed = git("diff", "--name-only", f"{base}..HEAD")
    _, worktree = git("status", "--porcelain", "--untracked-files=all")
    paths = set(filter(None, committed.splitlines()))
    paths |= {line[3:].split(" -> ")[-1] for line in worktree.splitlines() if line}
    bad = sorted(p for p in paths if not p.startswith("experiments/"))
    if bad:
        sys.exit("scope: FAIL — ветка orx/* затрагивает пути вне experiments/:\n  "
                 + "\n  ".join(bad))
    print(f"scope: OK ({len(paths)} путей, все в experiments/)")


def main():
    active_file = EXP / "ACTIVE"
    if not active_file.is_file():
        sys.exit("run: нет experiments/ACTIVE")
    slug = active_file.read_text(encoding="utf-8").strip()
    if not SLUG_RE.match(slug):
        sys.exit(f"run: недопустимое имя эксперимента в ACTIVE: {slug!r}")
    entry = EXP / slug / "run.py"
    if not entry.is_file():
        sys.exit(f"run: нет точки входа {entry.relative_to(ROOT).as_posix()}")
    check_scope()
    print(f"run: эксперимент {slug}", flush=True)
    r = subprocess.run([sys.executable, "-X", "utf8", str(entry)], cwd=ROOT)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
