#!/usr/bin/env python3
"""Сборка и проверка реестра кандидатных предложений ФТС (2026-10-15).

Источники (редактируются руками):
  src/G*.tsv            строки реестра, по одному файлу на группу
  groups.tsv            группы: куда относятся и на что ссылаются
  axes.tsv              ось авторского принятия для каждой строки
  canon_families.tsv    семейства карточек канона со статусом кандидата
  excluded_files.tsv    файлы, где слово «кандидат» значит не предложение ФТС
  REGISTER_head.md / REGISTER_tail.md   вводная и заключительная части

Производные (не править): candidates.tsv, REGISTER.md.

  py -3.11 -X utf8 build_register.py           # проверить и пересобрать
  py -3.11 -X utf8 build_register.py --check   # только проверить: ссылки, покрытие, актуальность производных

Скрипт ничего не повышает и не меняет в source/. Проверки касаются адресов
(карточки, OQ, DN, проверки, файлы) и покрытия, а не истинности содержания.
"""
import argparse
import collections
import json
import os
import pathlib
import re
import sys
import urllib.parse

PKG = pathlib.Path(__file__).resolve().parent
WORK = PKG.parents[1]
ROOT = WORK.parent
V14 = WORK / "v14_rebuild"

CAND_COLS = ["id", "group", "ladder", "levels", "claim", "kind", "origin", "status",
             "cards", "checks", "oq", "dn", "source", "also"]
KINDS = {"form", "reading", "operator", "protocol", "bridge", "prediction", "observation", "method"}
ORIGINS = {"author", "author_delegated", "mixed", "assistant", "assistant_accepted_text",
           "other_model", "external"}
AXES = ["authored", "mixed", "delegated", "working_accepted", "text_accepted",
        "not_accepted", "needs_author"]
AXIS_RU = {
    "authored": "сформулировано автором",
    "mixed": "тезис автора + формализация ассистента",
    "delegated": "выбор делегирован ассистенту",
    "working_accepted": "принято автором как рабочее чтение",
    "text_accepted": "принят текст ответа ассистента",
    "not_accepted": "не принято автором",
    "needs_author": "ждёт решения автора",
}
AXIS_SHORT = {"authored": "авт.", "mixed": "смеш.", "delegated": "делег.",
              "working_accepted": "раб.", "text_accepted": "текст",
              "not_accepted": "нет", "needs_author": "ждёт"}
ORIGIN_RU = {
    "author": "автор",
    "author_delegated": "выбор делегирован",
    "mixed": "автор + ассистент",
    "assistant": "ассистент",
    "assistant_accepted_text": "ответ ассистента (текст принят)",
    "other_model": "другая модель",
    "external": "внешнее [внешнее]",
}
KIND_RU = {"form": "форма", "reading": "чтение", "operator": "оператор", "protocol": "протокол",
           "bridge": "внешний мост", "prediction": "предсказание", "observation": "наблюдение",
           "method": "методика"}
SKIP_PARTS = ("_history", "canon_history", "/export/", "graphify-out", "instruction_history", "/inputs/")
GENERIC_NAMES = {"REVIEW.md", "PROTOCOL.md", "README.md", "RESULTS.md", "SOURCES.md", "INDEX.md"}
# слишком часто упоминаются в OQ: сверка по имени файла для них шумит и не делается
NO_AUTO_NAMES = {"FTS_v14_paper.md", "DECISIONS.md", "STATE.md", "PATTERN_ATLAS.md", "notation.md",
                 "OPEN_QUESTIONS.md", "GROUPED_OPEN_2026-10-08.md", "ANSWERS_60.md", "AUTHOR_ANSWERS_60.md"}


def read_tsv(path, cols=None):
    lines = [l for l in path.read_text(encoding="utf-8").split("\n") if l.strip()]
    head = lines[0].split("\t")
    if cols is not None and head != cols:
        raise SystemExit(f"{path.name}: заголовок {head} != {cols}")
    rows = []
    for n, l in enumerate(lines[1:], 2):
        cells = l.split("\t")
        if len(cells) < len(head):
            # редакторы срезают хвостовые табуляции: пустые последние ячейки допустимы
            cells += [""] * (len(head) - len(cells))
        if len(cells) != len(head):
            raise SystemExit(f"{path.name}:{n}: столбцов {len(cells)} вместо {len(head)}: {l[:80]}")
        rows.append({h: c.strip() for h, c in zip(head, cells)})
    return head, rows


def split_list(s, sep=","):
    return [x.strip() for x in s.split(sep) if x.strip()]


def parse_levels(s):
    s = s.strip()
    if s in ("", "-"):
        return []
    out = []
    for tok in split_list(s):
        m = re.fullmatch(r"(m1|\d+)(?:-(\d+))?", tok)
        if not m:
            raise ValueError(f"плохой уровень {tok!r}")
        a = -1 if m.group(1) == "m1" else int(m.group(1))
        b = int(m.group(2)) if m.group(2) else a
        out.extend(range(a, b + 1))
    return sorted(set(out))


def fmt_levels(lv):
    if not lv:
        return "без номера"
    runs, start, prev = [], lv[0], lv[0]
    for x in lv[1:]:
        if x == prev + 1:
            prev = x
            continue
        runs.append((start, prev))
        start = prev = x
    runs.append((start, prev))
    return ", ".join(str(a) if a == b else f"{a}–{b}" for a, b in runs)


def load_canon():
    cards = {}
    order = []
    with open(ROOT / "source" / "fts_cards.jsonl", encoding="utf-8") as f:
        for line in f:
            c = json.loads(line)
            cards[c["id"]] = c
            order.append(c["id"])
    return cards, order


CAND_STATUS_RE = re.compile(r"candidate|speculative|reserved|projected|overlay|not_adopted")


def oq_info():
    text = (WORK / "OPEN_QUESTIONS.md").read_text(encoding="utf-8")
    lines = text.split("\n")
    anchors = {}
    blocks = []
    cur = None
    for i, l in enumerate(lines):
        if re.match(r"^- \[[ x~]\]", l) or l.startswith("#"):
            if cur:
                blocks.append(cur)
            cur = {"anchors": [], "lines": [l]}
        elif cur is not None:
            cur["lines"].append(l)
        for a in re.findall(r"\{#(oq-[\w\-]+)\}", l):
            anchors[a] = re.sub(r"\s*\{#oq-[\w\-]+\}", "", re.sub(r"^- \[[ x~]\]\s*", "", l)).strip()
            if cur is not None:
                cur["anchors"].append(a)
    if cur:
        blocks.append(cur)
    for b in blocks:
        b["text"] = "\n".join(b["lines"])
    return anchors, blocks


def known_checks():
    c_ids = set()
    for p in V14.glob("verification*.py"):
        for m in re.findall(r"\bC-?(\d{2,3})\b", p.read_text(encoding="utf-8", errors="replace")):
            c_ids.add(int(m))
    wolf = (V14 / "audit" / "WOLFRAM_CHECKS.md").read_text(encoding="utf-8")
    wf = set(re.findall(r"WF-\d{3}", wolf))
    g60 = set(re.findall(r"G60-\d{2}",
                         (V14 / "e5_literature_review" / "undermind_60_oq_2026-09-30" / "verification_g60.py")
                         .read_text(encoding="utf-8")))
    return c_ids, wf, g60


def resolve_file(tok):
    cand = pathlib.Path(tok)
    base = cand.name
    hits = [p for p in V14.rglob(base) if p.as_posix().endswith(tok)]
    if hits:
        return hits[0]
    p = WORK / tok
    return p if p.exists() else None


def dn_ids():
    ids = set()
    for n in ("DIALOGUE_NUANCE_SOURCES.md", "DIALOGUE_NUANCE_JOURNAL.md"):
        ids |= set(re.findall(r"DN-\d{4}", (WORK / n).read_text(encoding="utf-8")))
    return ids


def mention_files():
    out = set()
    pat = re.compile("кандидат", re.I)
    for p in WORK.rglob("*.md"):
        s = p.as_posix()
        if any(k in s for k in SKIP_PARTS) or PKG in p.resolve().parents:
            continue
        if pat.search(p.read_text(encoding="utf-8", errors="replace")):
            out.add(p.relative_to(WORK).as_posix())
    return out


def rel_link(target_rel, anchor=""):
    target = WORK / target_rel
    rp = os.path.relpath(target, PKG).replace("\\", "/")
    rp = urllib.parse.quote(rp, safe="/._-~")
    return rp + (f"#{anchor}" if anchor else "")


def split_src(s):
    if "#" in s:
        p, a = s.split("#", 1)
        return p, a
    return s, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="не писать файлы, сверить производные")
    args = ap.parse_args()
    errors, warns = [], []

    cards, card_order = load_canon()
    c_ids, wf_ids, g60_ids = known_checks()
    oq_anchors, oq_blocks = oq_info()
    dns = dn_ids()

    _, groups = read_tsv(PKG / "groups.tsv", ["group", "title", "belongs_to", "refs_to", "note"])
    group_ids = [g["group"] for g in groups]
    gmap = {g["group"]: g for g in groups}

    rows = []
    for p in sorted((PKG / "src").glob("G*.tsv")):
        _, rr = read_tsv(p, CAND_COLS)
        rows.extend(rr)
    _, axes_rows = read_tsv(PKG / "axes.tsv", ["id", "author_axis"])
    axes = {r["id"]: r["author_axis"] for r in axes_rows}

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("повторяющиеся id: " + ", ".join(i for i, n in collections.Counter(ids).items() if n > 1))
    rows.sort(key=lambda r: int(r["id"].split("-")[1]))
    for i, r in enumerate(rows, 1):
        if r["id"] != f"CP-{i:03d}":
            errors.append(f"нумерация: ожидалась CP-{i:03d}, найдена {r['id']}")
            break
    if set(axes) != set(ids):
        errors.append(f"axes.tsv: нет {sorted(set(ids)-set(axes))}, лишние {sorted(set(axes)-set(ids))}")

    for r in rows:
        i = r["id"]
        if r["group"] not in gmap:
            errors.append(f"{i}: неизвестная группа {r['group']}")
        if r["kind"] not in KINDS:
            errors.append(f"{i}: kind {r['kind']!r}")
        if r["origin"] not in ORIGINS:
            errors.append(f"{i}: origin {r['origin']!r}")
        if axes.get(i) not in AXES:
            errors.append(f"{i}: author_axis {axes.get(i)!r}")
        for f in ("claim", "status", "source"):
            if not r[f]:
                errors.append(f"{i}: пустое поле {f}")
        try:
            r["_levels"] = parse_levels(r["levels"])
        except ValueError as e:
            errors.append(f"{i}: {e}")
            r["_levels"] = []
        r["_cards"] = split_list(r["cards"])
        r["_checks"] = split_list(r["checks"])
        r["_oq"] = split_list(r["oq"])
        r["_dn"] = split_list(r["dn"])
        r["_also"] = split_list(r["also"], ";")
        for c in r["_cards"]:
            if c not in cards:
                errors.append(f"{i}: нет карточки {c}")
        for c in r["_checks"]:
            m = re.fullmatch(r"C-(\d+)", c)
            if m:
                if int(m.group(1)) not in c_ids:
                    errors.append(f"{i}: нет проверки {c}")
            elif re.fullmatch(r"WF-\d{3}", c):
                if c not in wf_ids:
                    errors.append(f"{i}: нет {c} в WOLFRAM_CHECKS.md")
            elif re.fullmatch(r"G60-\d{2}", c):
                if c not in g60_ids:
                    errors.append(f"{i}: нет {c} в verification_g60.py")
            elif "." in c:
                if resolve_file(c) is None:
                    errors.append(f"{i}: нет файла проверки {c}")
            else:
                errors.append(f"{i}: непонятная проверка {c!r}")
        for o in r["_oq"]:
            if o not in oq_anchors:
                errors.append(f"{i}: нет OQ {o}")
        for d in r["_dn"]:
            if d not in dns:
                errors.append(f"{i}: нет {d}")
        for s in [r["source"]] + r["_also"]:
            path, _ = split_src(s)
            if not (WORK / path).is_file():
                errors.append(f"{i}: нет файла {path}")

    # --- семейства карточек канона ---
    cand_cards = {k for k, c in cards.items() if CAND_STATUS_RE.search(c.get("status") or "")}
    _, fams = read_tsv(PKG / "canon_families.tsv", ["family", "title", "belongs_to", "cards", "note"])
    fam_cards = collections.defaultdict(list)
    for fm in fams:
        fm["_cards"] = split_list(fm["cards"])
        for c in fm["_cards"]:
            fam_cards[c].append(fm["family"])
            if c not in cards:
                errors.append(f"{fm['family']}: нет карточки {c}")
    dup = [c for c, v in fam_cards.items() if len(v) > 1]
    if dup:
        errors.append(f"карточки в нескольких семействах: {dup}")
    miss = sorted(cand_cards - set(fam_cards))
    extra = sorted(set(fam_cards) - cand_cards)
    if miss:
        errors.append(f"карточки со статусом кандидата вне семейств: {miss}")
    if extra:
        errors.append(f"в семействах карточки без статуса кандидата: {extra}")

    # --- покрытие файлов ---
    mentions = mention_files()
    _, excl = read_tsv(PKG / "excluded_files.tsv", ["path", "class", "reason"])
    excl_paths = {e["path"] for e in excl}
    covered = set()
    for r in rows:
        covered.add(split_src(r["source"])[0])
        for a in r["_also"]:
            covered.add(split_src(a)[0])
    for e in excl:
        if e["path"] not in mentions:
            errors.append(f"excluded_files: {e['path']} не содержит «кандидат» или не существует")
        if e["path"] in covered:
            warns.append(f"excluded_files: {e['path']} одновременно использован как источник")
    uncovered = sorted(mentions - covered - excl_paths)
    if uncovered:
        errors.append("файлы со словом «кандидат» вне реестра и исключений:\n  " + "\n  ".join(uncovered))

    # --- перекрёстные ссылки CP внутри текстов ---
    for r in rows:
        for m in re.findall(r"CP-\d{3}", r["claim"] + " " + r["status"]):
            if m not in ids:
                errors.append(f"{r['id']}: ссылка на несуществующую {m}")

    for nm in ("REGISTER_head.md", "REGISTER_tail.md"):
        for m in sorted(set(re.findall(r"CP-\d{3}", (PKG / nm).read_text(encoding="utf-8")))):
            if m not in ids:
                errors.append(f"{nm}: ссылка на несуществующую {m}")

    if errors:
        print("ОШИБКИ:")
        for e in errors:
            print(" -", e)
        print(f"\n{len(errors)} ошибок; производные не пересобраны.")
        return 1
    for w in warns:
        print("предупреждение:", w)

    # ------------------------------------------------------------------
    # Производные
    # ------------------------------------------------------------------
    tsv_lines = ["\t".join(CAND_COLS + ["author_axis"])]
    for r in rows:
        tsv_lines.append("\t".join([r[c] for c in CAND_COLS] + [axes[r["id"]]]))
    candidates_tsv = "\n".join(tsv_lines) + "\n"

    md = render_md(rows, groups, gmap, axes, cards, card_order, fams, fam_cards, oq_anchors, oq_blocks,
                   mentions, excl, covered)

    broken = []
    for m in re.finditer(r"\]\(([^)#]+)(?:#[^)]*)?\)", md):
        tgt = urllib.parse.unquote(m.group(1))
        if tgt.startswith(("http://", "https://")) or tgt.startswith("#"):
            continue
        if not (PKG / tgt).resolve().exists():
            broken.append(tgt)
    if broken:
        print("битые ссылки в REGISTER.md:", sorted(set(broken)))
        return 1

    out_tsv = PKG / "candidates.tsv"
    out_md = PKG / "REGISTER.md"
    if args.check:
        bad = []
        if not out_tsv.exists() or out_tsv.read_text(encoding="utf-8") != candidates_tsv:
            bad.append("candidates.tsv")
        if not out_md.exists() or out_md.read_text(encoding="utf-8") != md:
            bad.append("REGISTER.md")
        if bad:
            print("устарели производные:", ", ".join(bad), "- запустить без --check")
            return 1
        print(f"OK: {len(rows)} строк, {len(cand_cards)} карточек, {len(mentions)} файлов с «кандидат» "
              f"({len(covered & mentions)} в реестре, {len(excl_paths)} исключено), производные актуальны")
        return 0
    out_tsv.write_text(candidates_tsv, encoding="utf-8", newline="\n")
    out_md.write_text(md, encoding="utf-8", newline="\n")
    print(f"OK: {len(rows)} строк, {len(cand_cards)} карточек канона, {len(mentions)} файлов с «кандидат» "
          f"({len(covered & mentions)} в реестре, {len(excl_paths)} исключено); записаны candidates.tsv, REGISTER.md")
    return 0


# ----------------------------------------------------------------------
# Генерация Markdown
# ----------------------------------------------------------------------
def code_list(items):
    return ", ".join(f"`{x}`" for x in items)


def render_row(r, axes):
    lv = fmt_levels(r["_levels"])
    out = []
    out.append(f"#### {r['id']} · {r['ladder']} · уровни: {lv} · {KIND_RU[r['kind']]}")
    out.append("")
    out.append(r["claim"])
    out.append("")
    out.append(f"- **Происхождение:** {ORIGIN_RU[r['origin']]}. **Авторская ось:** {AXIS_RU[axes[r['id']]]}.")
    out.append(f"- **Статус в источнике:** {r['status']}.")
    refs = []
    if r["_cards"]:
        refs.append("карточки " + code_list(r["_cards"]))
    if r["_checks"]:
        refs.append("проверки " + code_list(r["_checks"]))
    if r["_oq"]:
        refs.append("OQ " + code_list(r["_oq"]))
    if r["_dn"]:
        refs.append("журнал " + code_list(r["_dn"]))
    if refs:
        out.append("- **Ссылается на:** " + "; ".join(refs) + ".")
    path, anc = split_src(r["source"])
    if anc.isdigit():
        src = f"[{path}]({rel_link(path)}), §{anc}"
    else:
        src = f"[{path}]({rel_link(path, anc)})" + (f" `#{anc}`" if anc else "")
    also = "; ".join(f"[{split_src(a)[0]}]({rel_link(*split_src(a))})" for a in r["_also"])
    out.append(f"- **Первичное место:** {src}" + (f". Также: {also}" if also else "") + ".")
    out.append("")
    return out


def render_md(rows, groups, gmap, axes, cards, card_order, fams, fam_cards, oq_anchors, oq_blocks,
              mentions, excl, covered):
    head = (PKG / "REGISTER_head.md").read_text(encoding="utf-8").rstrip("\n")
    tail = (PKG / "REGISTER_tail.md").read_text(encoding="utf-8").rstrip("\n")
    by_group = collections.defaultdict(list)
    for r in rows:
        by_group[r["group"]].append(r)
    cand_cards = {k for k in fam_cards}
    L = [head, ""]

    # ---- сводка ----
    L.append("## 1. Сводка")
    L.append("")
    L.append(f"Строк реестра (исследовательский слой): **{len(rows)}** в {len(groups)} группах. "
             f"Карточек канона со статусом кандидата: **{len(cand_cards)}** в {len(fams)} семействах. "
             f"Файлов `work/` со словом «кандидат»: {len(mentions)} "
             f"({len(covered & mentions)} использованы как источники строк, {len(excl)} исключены с причиной).")
    L.append("")
    L.append("Авторская ось (сколько строк в каждой группе): "
             + "; ".join(f"`{AXIS_SHORT[a]}` — {AXIS_RU[a]}" for a in AXES) + ".")
    L.append("")
    L.append("| Группа | Куда относится | Строк | " + " | ".join(AXIS_SHORT[a] for a in AXES) + " |")
    L.append("|---|---|---:|" + "---:|" * len(AXES))
    tot = collections.Counter()
    for g in groups:
        c = collections.Counter(axes[r["id"]] for r in by_group[g["group"]])
        tot.update(c)
        L.append(f"| [{g['group']}](#{g['group'].lower()}) {g['title']} | {g['belongs_to']} | {len(by_group[g['group']])} | "
                 + " | ".join(str(c[a]) if c[a] else "·" for a in AXES) + " |")
    L.append(f"| **Итого** | | **{len(rows)}** | " + " | ".join(f"**{tot[a]}**" for a in AXES) + " |")
    L.append("")
    waiting = [r for r in rows if axes[r["id"]] == "needs_author"]
    if waiting:
        L.append("Строки, которые источники прямо помечают как ждущие автора: "
                 + ", ".join(f"{r['id']}" for r in waiting)
                 + ". Остальные вопросы «за автором» — в разделе 7.")
        L.append("")

    # ---- карточки канона ----
    L.append("## 2. Карточки канона со статусом кандидата")
    L.append("")
    L.append("Это канонический слой: карточки лежат в `source/fts_cards.jsonl`, статус читается из поля `status`. "
             "Наличие карточки не означает авторского принятия [AGENTS: Standing rules 4]. "
             "Сколько строк реестра (исследовательский слой) ссылается на карточку, указано в последнем столбце.")
    L.append("")
    refs_by_card = collections.defaultdict(list)
    for r in rows:
        for c in r["_cards"]:
            refs_by_card[c].append(r["id"])
    for fm in fams:
        L.append(f"### {fm['family']} · {fm['title']}")
        L.append("")
        L.append(f"Относится к: {fm['belongs_to']}. {fm['note']}")
        L.append("")
        L.append("| Карточка | Тип | Статус | Зависит от | Строки реестра |")
        L.append("|---|---|---|---|---|")
        for c in fm["_cards"]:
            cd = cards[c]
            deps = ", ".join(cd.get("depends_on") or []) or "—"
            rr = ", ".join(refs_by_card.get(c, [])) or "—"
            L.append(f"| `{c}` | {cd.get('type')} | {cd.get('status')} | {deps} | {rr} |")
        L.append("")

    # ---- группы ----
    L.append("## 3. Предложения исследовательского слоя по группам")
    L.append("")
    for g in groups:
        L.append(f"### {g['group']}")
        L.append("")
        L.append(f"**{g['title']}**")
        L.append("")
        L.append(f"- Относится к: {g['belongs_to']}.")
        L.append(f"- Ссылается на: {g['refs_to']}.")
        L.append(f"- Примечание: {g['note']}")
        L.append("")
        for r in by_group[g["group"]]:
            L.extend(render_row(r, axes))

    # ---- индексы ----
    L.append("## 4. Куда относятся: указатель по уровням")
    L.append("")
    L.append("Строка попадает под каждый уровень из своего поля `levels` (диапазоны развёрнуты). "
             "Номер без приставки неоднозначен [notation.md]: лестница указана в поле `ladder` строки.")
    L.append("")
    by_level = collections.defaultdict(list)
    for r in rows:
        for x in r["_levels"]:
            by_level[x].append(r["id"])
    L.append("| Уровень | Строк | Строки |")
    L.append("|---|---:|---|")
    for lv in sorted(by_level):
        name = "−1" if lv == -1 else str(lv)
        L.append(f"| {name} | {len(by_level[lv])} | {', '.join(by_level[lv])} |")
    nolv = [r["id"] for r in rows if not r["_levels"]]
    L.append(f"| без номера | {len(nolv)} | {', '.join(nolv)} |")
    L.append("")
    lad = collections.defaultdict(list)
    for r in rows:
        lad[r["ladder"]].append(r["id"])
    L.append("По лестнице (`ladder`): " + "; ".join(f"**{k}** — {len(v)}" for k, v in sorted(lad.items(), key=lambda kv: -len(kv[1]))) + ".")
    L.append("")

    L.append("## 5. Куда ссылаются")
    L.append("")
    L.append("### 5.1. Карточки канона, на которые ссылаются строки реестра")
    L.append("")
    L.append("Показаны карточки, названные в полях `cards`. Порядок — как в `source/fts_cards.jsonl`; "
             "звёздочка — сама карточка имеет статус кандидата (раздел 2).")
    L.append("")
    L.append("| Карточка | Статус | Строк | Строки |")
    L.append("|---|---|---:|---|")
    for c in card_order:
        if c in refs_by_card:
            mark = "*" if c in cand_cards else ""
            L.append(f"| `{c}`{mark} | {cards[c].get('status')} | {len(refs_by_card[c])} | {', '.join(refs_by_card[c])} |")
    L.append("")

    L.append("### 5.2. Открытые вопросы (`OPEN_QUESTIONS.md`)")
    L.append("")
    L.append("«Курируемые» — OQ названы в поле `oq` строки. «По имени файла» — OQ сам упоминает первичный файл строки "
             "(механическая сверка по имени файла; для общих имён REVIEW.md и т. п. берутся две последние части пути).")
    L.append("")
    rows_by_oq = collections.defaultdict(list)
    for r in rows:
        for o in r["_oq"]:
            rows_by_oq[o].append(r["id"])

    def key_for(path):
        p = pathlib.PurePosixPath(path)
        if p.name in GENERIC_NAMES:
            return "/".join(p.parts[-2:])
        return p.name

    auto = collections.defaultdict(set)
    for r in rows:
        if pathlib.PurePosixPath(split_src(r["source"])[0]).name in NO_AUTO_NAMES:
            continue
        k = key_for(split_src(r["source"])[0])
        for b in oq_blocks:
            if b["anchors"] and k in b["text"]:
                for a in b["anchors"]:
                    if r["id"] not in rows_by_oq.get(a, []):
                        auto[a].add(r["id"])
    all_oq = [a for a in oq_anchors if a in rows_by_oq or a in auto]
    L.append("| OQ | Суть | Курируемые | По имени файла |")
    L.append("|---|---|---|---|")
    for a in all_oq:
        title = oq_anchors[a]
        title = title if len(title) <= 110 else title[:107] + "…"
        title = title.replace("|", "\\|")
        L.append(f"| `{a}` | {title} | {', '.join(rows_by_oq.get(a, [])) or '—'} | "
                 f"{', '.join(sorted(auto.get(a, []))) or '—'} |")
    L.append("")
    unref = len(oq_anchors) - len(all_oq)
    L.append(f"В `OPEN_QUESTIONS.md` {len(oq_anchors)} адресов; реестр связан с {len(all_oq)}; "
             f"{unref} не связаны ни с одной строкой.")
    L.append("")

    L.append("### 5.3. Проверки и свидетели")
    L.append("")
    by_check = collections.defaultdict(list)
    for r in rows:
        for c in r["_checks"]:
            by_check[c].append(r["id"])

    def check_key(c):
        m = re.fullmatch(r"([A-Z]+\d*)-(\d+)", c)
        return (0, m.group(1), int(m.group(2))) if m else (1, c, 0)

    L.append("| Проверка / свидетель | Строки |")
    L.append("|---|---|")
    for c in sorted(by_check, key=check_key):
        L.append(f"| `{c}` | {', '.join(by_check[c])} |")
    L.append("")
    L.append("`C-NN` — `verification*.py` (математические факты, не смысл уровней); `WF-NNN` — Wolfram, "
             "[audit/WOLFRAM_CHECKS.md](../audit/WOLFRAM_CHECKS.md); `G60-NN` — `verification_g60.py`; "
             "файлы `*.py` — свидетели вне общего маршрута. PASS ничего не повышает.")
    L.append("")

    L.append("### 5.4. Записи журнала диалога")
    L.append("")
    by_dn = collections.defaultdict(list)
    for r in rows:
        for d in r["_dn"]:
            by_dn[d].append(r["id"])
    L.append("| Запись | Строки |")
    L.append("|---|---|")
    for d in sorted(by_dn):
        L.append(f"| `{d}` | {', '.join(by_dn[d])} |")
    L.append("")

    L.append("### 5.5. Документы-источники")
    L.append("")
    by_src = collections.defaultdict(lambda: ([], []))
    for r in rows:
        by_src[split_src(r["source"])[0]][0].append(r["id"])
        for a in r["_also"]:
            by_src[split_src(a)[0]][1].append(r["id"])
    L.append("| Документ | Первичный для | Упомянут также в |")
    L.append("|---|---|---|")
    for p in sorted(by_src):
        pr, al = by_src[p]
        L.append(f"| [{p}]({rel_link(p)}) | {', '.join(pr) or '—'} | {', '.join(al) or '—'} |")
    L.append("")

    # ---- покрытие ----
    L.append("## 6. Покрытие и исключения")
    L.append("")
    L.append("`build_register.py` проверяет, что каждый файл `work/*.md` (без истории, выгрузок и сырых входов "
             "deep-research) со словом «кандидат» либо назван в строке реестра (первичное место или «также»), "
             "либо перечислен в `excluded_files.tsv` с причиной. Это покрытие на уровне файлов, не абзацев: "
             "отдельное предложение внутри большого документа реестр может не называть.")
    L.append("")
    L.append("Классы: `log` — журнал решений; `procedure` — планы, аудиты, запросы; `derived` — машинные производные; "
             "`status_note` — констатация статуса без нового предложения; `lit_protocol` / `lit_review` — «кандидат» значит "
             "найденная или отобранная работа, а не предложение ФТС.")
    L.append("")
    L.append("| Файл | Класс | Почему не строка реестра |")
    L.append("|---|---|---|")
    for e in sorted(excl, key=lambda e: (e["class"], e["path"])):
        L.append(f"| [{e['path']}]({rel_link(e['path'])}) | `{e['class']}` | {e['reason'].replace('|', chr(92) + '|')} |")
    L.append("")

    L.append(tail)
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    sys.exit(main())
