# -*- coding: utf-8 -*-
"""
oq_anchor.py — миграция: стабильные якоря {#oq-...} пунктам OPEN_QUESTIONS.md.

Зачем: #NN позиционны и ДРЕЙФУЮТ при закрытии/добавлении пунктов. OQ_TRIAGE
эпохи 44 ссылался на #32/#38/#41 (политика проб) и #19 (свидетель чётности) —
после закрытий и перенумерации эти #NN указывают в другие пункты. Якорь =
постоянная идентичность строки, переживающая перенумерацию.

Дисциплина: якорь ставится КАЖДОМУ пункту (открытому и закрытому) в порядке
файла. Список PLAN — пары (ожидаемый_статус, slug) 1:1 с пунктами; при любом
рассинхроне (число/статус) скрипт ПАДАЕТ и ничего не пишет (guard против
молчаливого дрейфа). Идемпотентно: пункт с уже проставленным {#...} не трогается,
но его slug сверяется с PLAN.

Запуск:  python -X utf8 tools/oq_anchor.py [--write]
  без --write — сухой прогон (печать соответствия строка→slug), файл не меняется.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OQ = ROOT / "work" / "OPEN_QUESTIONS.md"

# (ожидаемый статус, slug) — СТРОГО в порядке появления в файле.
PLAN = [
    (" ", "oq-ce-canon"),
    ("x", "oq-machine-check-done"),
    (" ", "oq-kappa-provenance"),
    ("~", "oq-o20-missing-benchmark"),
    ("x", "oq-formulas-7-11-done"),
    ("x", "oq-upper-12-17-done"),
    ("x", "oq-chi-ladder-done"),
    (" ", "oq-phase-causal-u9"),
    # ## Новые (после пересборки v14, 2026-06-11)
    (" ", "oq-node11-asymmetry"),
    (" ", "oq-pi-projection-above-u7"),
    ("x", "oq-export-refs-done"),
    (" ", "oq-u8-u10-optests"),
    (" ", "oq-dict-d-completeness"),
    (" ", "oq-arity-window-13-14"),
    (" ", "oq-passport-u14-u15"),
    ("x", "oq-redteam-f3-done"),
    (" ", "oq-u12-radius-r"),
    (" ", "oq-u12-antimode-gate"),
    (" ", "oq-redteam-dependent-guards"),
    (" ", "oq-d11-branch-bit-test"),
    (" ", "oq-forms8plus-ratio"),
    (" ", "oq-tot-groups-8-11"),
    (" ", "oq-o3-twolists"),
    (" ", "oq-third-boundary"),
    ("x", "oq-parity-witness-done"),
    (" ", "oq-const-statistics-code"),
    (" ", "oq-unit-circle-z15"),
    (" ", "oq-u13-boundary-union-op"),
    (" ", "oq-u14-worlds-agg-op"),
    (" ", "oq-u12-antimode-authorfix"),
    (" ", "oq-d10-phase-test"),
    # ## Перенос канона в v14
    (" ", "oq-ce-weights-proof"),
    (" ", "oq-mprime-audit"),
    (" ", "oq-ddelta-weights"),
    (" ", "oq-canon-star-fate"),
    # ## Кандидат: колонка неопределённости
    (" ", "oq-d2-half-overlay"),
    (" ", "oq-d4-column-precision"),
    ("x", "oq-witnesses-verif-done"),
    ("x", "oq-8plus-only-refuted"),
    (" ", "oq-synthesis-c-assembly"),
    ("~", "oq-d2-sign-retrieval-remainder"),
    (" ", "oq-roots-of-unity-z368"),
    ("~", "oq-pentad-role-cycle"),
    # ## Кандидат: слой χ_E
    (" ", "oq-sphere-u6-carrier"),
    ("x", "oq-txp-verif-done"),
    (" ", "oq-fourier-questiongain"),
    ("~", "oq-zero-classes-chi-e"),
    # ## Кандидат: ЦПТ
    ("x", "oq-clt-verif-done"),
    (" ", "oq-divorce-cases-genre"),
    (" ", "oq-levy-world"),
    (" ", "oq-edgeworth-u9"),
]

ITEM = re.compile(r"^- \[([ x~])\] (.*)$")
ANCHOR = re.compile(r"\{#(oq-[a-z0-9-]+)\}")


def main():
    write = "--write" in sys.argv
    lines = io.open(OQ, encoding="utf-8").read().split("\n")

    # индексы строк-пунктов
    idx = [i for i, ln in enumerate(lines) if ITEM.match(ln)]
    if len(idx) != len(PLAN):
        print(f"ABORT: пунктов в файле {len(idx)}, в PLAN {len(PLAN)} — рассинхрон.")
        for k, i in enumerate(idx):
            exp = PLAN[k][1] if k < len(PLAN) else "—"
            print(f"  {k:02d} стр.{i+1} [{ITEM.match(lines[i]).group(1)}] {lines[i][6:56]}  → {exp}")
        sys.exit(1)

    changed = 0
    for k, i in enumerate(idx):
        m = ITEM.match(lines[i])
        status, body = m.group(1), m.group(2)
        exp_status, slug = PLAN[k]
        if status != exp_status:
            print(f"ABORT стр.{i+1}: статус '{status}' ≠ ожид. '{exp_status}' (slug {slug}).")
            print(f"  текст: {body[:70]}")
            sys.exit(1)
        have = ANCHOR.search(body)
        if have:
            if have.group(1) != slug:
                print(f"ABORT стр.{i+1}: якорь '{have.group(1)}' ≠ PLAN '{slug}'.")
                sys.exit(1)
            mark = "ok  "
        else:
            lines[i] = lines[i].rstrip() + f" {{#{slug}}}"
            changed += 1
            mark = "ADD "
        print(f"{mark}#{k+1:02d} стр.{i+1} [{status}] {{#{slug}}}  {body[:44]}")

    print(f"\nВсего пунктов {len(idx)}; проставлено новых {changed}.")
    if write and changed:
        io.open(OQ, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
        print(f"[written] {OQ}")
    elif not write:
        print("(сухой прогон; для записи добавь --write)")


if __name__ == "__main__":
    main()
