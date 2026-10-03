"""Read-only consistency route for the FTS project.

The default invocation executes every mandatory existing check without
rebuilding a graph, export, or source artifact.  A non-zero exit means that at
least one mandatory check failed or could not be run.  P2 lines emitted by the
existing audit are preserved as documented limitations, not upgraded to a
failure by this wrapper.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Check:
    identifier: str
    title: str
    script: str
    arguments: tuple[str, ...]


@dataclass
class Result:
    identifier: str
    title: str
    command: list[str]
    status: str
    exit_code: int | None
    summary: str
    limitations: list[str]
    output: str


CHECKS: tuple[Check, ...] = (
    Check(
        "canon_manifest",
        "активный канон: MANIFEST, SHA256 и неучтённые файлы",
        "tools/verify.py",
        ("--strict",),
    ),
    Check(
        "claim_graph",
        "граф утверждений: источники, направленные рёбра и идемпотентность",
        "tools/claim_graph.py",
        ("validate", "--idempotent"),
    ),
    Check(
        "formal_suite",
        "формальные предикаты статьи C01–C62",
        "work/v14_rebuild/verification.py",
        (),
    ),
    Check(
        "audit",
        "аудит схемы, трассируемости, статических формальных и исторических артефактов",
        "work/v14_rebuild/audit/run_audit.py",
        ("all",),
    ),
    Check(
        "research_export",
        "исследовательская выгрузка: побайтовая воспроизводимость",
        "tools/build_research_export.py",
        ("--check",),
    ),
)


def concise_output(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    for prefix in ("summary:", "CLAIM GRAPH validate:", "PASS verification:", "AUDIT all:", "PASS выгрузка", "FAIL выгрузка"):
        matching = [line for line in lines if line.startswith(prefix)]
        if matching:
            return matching[-1]
    return lines[-1] if lines else "нет вывода"


def documented_limitations(output: str) -> list[str]:
    return [line.strip() for line in output.splitlines() if line.lstrip().startswith("P2 ")]


def run_check(check: Check, workspace: Path) -> Result:
    script = workspace / check.script
    command = [sys.executable, "-X", "utf8", str(script), *check.arguments]
    try:
        completed = subprocess.run(
            command,
            cwd=workspace,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return Result(
            identifier=check.identifier,
            title=check.title,
            command=command,
            status="NOT_RUN",
            exit_code=None,
            summary=f"не удалось запустить: {exc}",
            limitations=[],
            output="",
        )

    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part).strip()
    limits = documented_limitations(output)
    if completed.returncode:
        status = "FAIL"
    elif limits:
        status = "PASS_WITH_DOCUMENTED_LIMITATIONS"
    else:
        status = "PASS"
    return Result(
        identifier=check.identifier,
        title=check.title,
        command=command,
        status=status,
        exit_code=completed.returncode,
        summary=concise_output(output),
        limitations=limits,
        output=output,
    )


def render_text(results: Sequence[Result], full: bool, verbose: bool) -> None:
    for result in results:
        exit_text = "not run" if result.exit_code is None else f"exit {result.exit_code}"
        print(f"{result.status} {result.identifier} [{exit_text}] — {result.summary}")
        for limitation in result.limitations:
            print(f"  DOCUMENTED_LIMITATION {limitation}")
        if verbose or result.status in {"FAIL", "NOT_RUN"}:
            detail = result.output or "нет дополнительного вывода"
            for line in detail.splitlines():
                print(f"  {line}")
    failed = [result for result in results if result.status in {"FAIL", "NOT_RUN"}]
    limited = [result for result in results if result.limitations]
    scope = "full" if full else "partial"
    print(
        f"PROJECT CONSISTENCY {scope}: {len(results) - len(failed)}/{len(results)} checks passed; "
        f"failures={len(failed)}; documented_limitations={sum(len(result.limitations) for result in limited)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=ROOT,
        help="проверяемый checkout (по умолчанию корень этого проекта); полезно для изолированной копии",
    )
    parser.add_argument(
        "--only",
        choices=[check.identifier for check in CHECKS],
        action="append",
        help="запустить только названную проверку; это частичная диагностика, не полный verdict",
    )
    parser.add_argument("--verbose", action="store_true", help="показать полный вывод каждой проверки")
    parser.add_argument("--json", action="store_true", help="вывести собранный результат JSON вместо краткого текста")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    selected = tuple(check for check in CHECKS if not args.only or check.identifier in args.only)
    results = [run_check(check, workspace) for check in selected]
    full = len(selected) == len(CHECKS)
    failed = [result for result in results if result.status in {"FAIL", "NOT_RUN"}]

    if args.json:
        payload = {
            "workspace": str(workspace),
            "scope": "full" if full else "partial",
            "checks": [asdict(result) for result in results],
            "failed_mandatory_checks": [result.identifier for result in failed],
            "documented_limitations": [limitation for result in results for limitation in result.limitations],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        render_text(results, full=full, verbose=args.verbose)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
