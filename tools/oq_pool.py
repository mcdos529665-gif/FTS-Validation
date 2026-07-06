# -*- coding: utf-8 -*-
"""
oq_pool.py — анализатор OPEN_QUESTIONS: пулы пересекающихся вопросов.

Парсит work/OPEN_QUESTIONS.md, извлекает из каждого ОТКРЫТОГО пункта признаки
(C-NN, ID карточек, уровни У-n, основания О/правила Д, ключевые термины),
строит граф «пункт—пункт» по общим признакам и печатает связные компоненты
(пулы) — кандидаты на совместное рассмотрение вместо хронологического порядка.

Дисциплина: каждое ребро показывает СВИДЕТЕЛЬСТВО (общие признаки).
Перегруженный символ χ признаком НЕ является (χ_E ≠ χ-носитель ≠ Q(χ) —
лексическая склейка запрещена); учитывается только явный 'χ_E'.
Токен 'C-60' — политика (одно решение), исключён из парных рёбер и
отчитывается отдельным списком.

Запуск:  python -X utf8 tools/oq_pool.py [--thresh N] [--write]
  --thresh N     порог веса ребра (по умолчанию 3)
  --write        сохранить отчёт (иначе только stdout)
  --hubs         вместо пулов: ранжированные хабы (признак → пункты)
  --cross        вместо пулов: мосты между курируемыми пулами (OQ_TRIAGE)
  --intersects   и хабы, и мосты → work/OQ_INTERSECTS.md (с --write)
  (пулы → work/OQ_POOLS.md; пересечения → work/OQ_INTERSECTS.md)

Веса признаков: C-NN=3, ID карточки=3, уровень=2, О/Д=2, термин=1.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OQ = ROOT / "work" / "OPEN_QUESTIONS.md"

W_C, W_ID, W_LVL, W_OD, W_KW = 3, 3, 2, 2, 1

ID_STOP = {"PASS", "FAIL", "TBD", "MANIFEST", "RESULTS", "PREREGISTRATION",
           "II", "III", "NB", "OOD"}

# (имя, regex по lower-тексту). Слова с риском подстрочной склейки — с \b.
KEYWORDS = [
    ("χ_E", r"χ_e"),
    ("Фурье", r"фурье"), ("ЦПТ", r"цпт"), ("Леви", r"леви"),
    ("Blackwell", r"blackwell"), ("HoTT", r"hott"), ("FTSConv", r"ftsconv"),
    ("пентада", r"пентад"), ("колонка", r"колонк"),
    ("узел", r"\bузел|\bузл"), ("окно", r"\bокн[оаеу]"),
    ("граница", r"границ"), ("единичная", r"единичн"), ("нулевая", r"нулев"),
    ("фаза", r"\bфаз"), ("ветвь", r"\bветв"),
    ("ratio/отношения", r"ratio|отношени"), ("арность", r"арност"),
    ("тотализация", r"тотализ"), ("анти-мода", r"анти-?мод"),
    ("κ", r"κ|каппа"), ("C(E)", r"c\(e\)"), ("d_Δ", r"d_δ|d_delta"),
    ("M′-Audit", r"m′|m’"), ("MNAR/пропуски", r"mnar|пропущен|missing"),
    ("шифр", r"шифр"), ("тор", r"\bтор\b|\bтора\b|\bторе\b"), ("сфера", r"сфер"),
    ("Эджворт", r"эджворт"), ("кумулянт", r"кумулянт"),
    ("кейсы-разведения", r"разведен|кейс"),
    ("знак", r"\bзнак"), ("минус", r"\bминус"),
    ("зеркало", r"зеркал"), ("отражение", r"отражен"),
    ("порядок", r"\bпорядок|\bпорядк"), ("Compare", r"compare|сравнен"),
    ("Agg/агрегация", r"\bagg|агрегац"), ("миры", r"\bмиры|\bмиров\b|мир-мы"),
    ("θ", r"θ|тета"), ("пред-регистрация", r"пред-?регистр"),
    ("provenance", r"provenance|провенанс"), ("абляция", r"абляц"),
    ("словарь Д", r"словар"), ("атомарность", r"атомарн"),
    ("полюс", r"полюс"), ("идемпотент", r"идемпотент"),
    ("корни единицы", r"корн[а-я]* един|z/3|z/6|z/8"),
    ("веса w_i", r"\bw_i|веса? w"), ("чётность", r"чётн|четн"),
    ("проекция π", r"проекц|полушаг"), ("двухсписочная", r"двухсписочн"),
    ("отсутствие", r"отсутств"), ("красная команда", r"красн[а-я]{0,2} команд"),
    ("формулы верхних", r"формул[а-я]* (?:13|верхн)"),
    ("оверлей", r"оверле|overlay"),
]
POLICY = [("C-60+ (политика проб)", r"c-60")]


def parse_items(text):
    items, section, cur = [], "(верх файла)", None
    for lineno, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^## (.+)$", line)
        if m:
            section, cur = m.group(1).strip(), None
            continue
        m = re.match(r"^- \[([ x~])\] (.*)$", line)
        if m:
            cur = {"line": lineno, "section": section,
                   "status": m.group(1), "text": m.group(2)}
            items.append(cur)
            continue
        if cur is not None and re.match(r"^ {2,}\S", line):
            cur["text"] += " " + line.strip()
        else:
            cur = None
    return items


def features(text):
    low = text.lower()
    f = {"C": set(), "ID": set(), "LVL": set(), "OD": set(),
         "KW": set(), "POL": set()}
    for m in re.finditer(r"C-(\d{1,2})(?:\s*(?:…|\.\.|–|—)\s*C-(\d{1,2}))?", text):
        a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
        f["C"].update(range(a, b + 1))
    for m in re.finditer(r"\b[A-Z][A-Z0-9_]{2,}\b", text):
        s = m.group(0)
        if s not in ID_STOP and not re.fullmatch(r"C-?\d+", s):
            f["ID"].add(s)
    for m in re.finditer(r"У\(?(-?\d{1,2})\)?", text):
        f["LVL"].add(int(m.group(1)))
    for m in re.finditer(r"\bU_?(\d{1,2})\b", text):
        f["LVL"].add(int(m.group(1)))
    for m in re.finditer(r"У(\d{1,2})\s*[–—]\s*У?(\d{1,2})", text):
        f["LVL"].update(range(int(m.group(1)), int(m.group(2)) + 1))
    for m in re.finditer(r"\b(1?\d)\s*(?:…|\.\.|–|—|→)\s*(1?\d)\b", text):
        a, b = int(m.group(1)), int(m.group(2))
        if 0 <= a < b <= 17 and b - a <= 9:
            f["LVL"].update(range(a, b + 1))
    for m in re.finditer(r"[ОO]_?(\d{1,2})\b", text):
        f["OD"].add("О" + m.group(1))
    for m in re.finditer(r"Д(\d{1,2})\b", text):
        f["OD"].add("Д" + m.group(1))
    for name, rx in KEYWORDS:
        if re.search(rx, low):
            f["KW"].add(name)
    for name, rx in POLICY:
        if re.search(rx, low):
            f["POL"].add(name)
    return f


def pair_weight(fa, fb):
    shared = {
        "C": fa["C"] & fb["C"], "ID": fa["ID"] & fb["ID"],
        "LVL": fa["LVL"] & fb["LVL"], "OD": fa["OD"] & fb["OD"],
        "KW": fa["KW"] & fb["KW"],
    }
    w = (W_C * len(shared["C"]) + W_ID * len(shared["ID"]) +
         W_LVL * len(shared["LVL"]) + W_OD * len(shared["OD"]) +
         W_KW * len(shared["KW"]))
    return w, shared


FEAT_W = {"C": W_C, "ID": W_ID, "LVL": W_LVL, "OD": W_OD, "KW": W_KW}

# Признаки, слишком общие для смыслового хаба (пополняется по факту прогона).
# 'C-60' — политика проб (закрыта, П1), не структурная связь.
HUB_STOP = {"C-60"}


def load_open_items():
    text = io.open(OQ, encoding="utf-8").read()
    items = parse_items(text)
    open_items = [it for it in items if it["status"] in " ~"]
    closed = len(items) - len(open_items)
    for i, it in enumerate(open_items):
        it["id"] = i + 1
        am = re.search(r"\{#(oq-[a-z0-9-]+)\}", it["text"])
        it["anchor"] = am.group(1) if am else "oq-?"
        it["text"] = re.sub(r"\s*\{#oq-[a-z0-9-]+\}", "", it["text"]).strip()
        it["f"] = features(it["text"])
    return open_items, closed


def _label(kind, v):
    if kind == "C":
        return f"C-{v}"
    if kind == "LVL":
        return f"У{v}"
    return str(v)


def _fmt_shared(shared):
    parts = []
    if shared["C"]:
        parts.append("C-" + ",".join(str(x) for x in sorted(shared["C"])))
    if shared["ID"]:
        parts.append(",".join(sorted(shared["ID"])))
    if shared["LVL"]:
        parts.append("У" + ",".join(str(x) for x in sorted(shared["LVL"])))
    if shared["OD"]:
        parts.append(",".join(sorted(shared["OD"])))
    if shared["KW"]:
        parts.append(",".join(sorted(shared["KW"])))
    return "; ".join(parts) or "—"


def hubs_report(open_items, top=24):
    inv = {}
    for it in open_items:
        for kind in ("C", "ID", "LVL", "OD", "KW"):
            for v in it["f"][kind]:
                inv.setdefault((kind, v), []).append(it)
    rows = []
    for (kind, v), its in inv.items():
        lab = _label(kind, v)
        if len(its) < 2 or lab in HUB_STOP:
            continue
        score = FEAT_W[kind] * len(its)
        rows.append((score, FEAT_W[kind], len(its), kind, lab, its))
    rows.sort(key=lambda r: (-r[0], -r[1], -r[2], r[4]))
    out = ["## Хабы (признак → пункты) — ранг = вес признака × охват", ""]
    for score, w, cov, kind, lab, its in rows[:top]:
        anchors = " ".join(f"`{it['anchor']}`"
                           for it in sorted(its, key=lambda x: x["line"]))
        out.append(f"- **{lab}** ({kind}, вес {w}×охват {cov}={score}) — {anchors}")
    out.append("")
    return "\n".join(out)


def parse_pools(path):
    """slug → set(Пx | 'Парк') из курируемого OQ_TRIAGE.md.

    Членство = якоря в СТРОКЕ-определении пула (заголовок `**Пx**` + непрерывные
    следующие строки, пока в них есть якоря). Первая строка без якоря = началась
    проза → захват прекращается (иначе упоминание чужого якоря в описании ложно
    приписывает членство; так же ловится утечка за `**Парк`). Членство может быть
    множественным (пункт-мост честно попадает в два пула)."""
    pools, cur, active = {}, None, False
    for line in io.open(path, encoding="utf-8"):
        h = re.match(r"^\*\*(П\d+)\b", line)
        if h:
            cur, active = h.group(1), True
        elif line.startswith("**Парк"):
            cur, active = "Парк", True
        elif re.match(r"^##\s", line):
            cur, active = None, False
        if cur and active:
            anchors = re.findall(r"oq-[a-z0-9-]+", line)
            if anchors:
                for s in anchors:
                    pools.setdefault(s, set()).add(cur)
            elif not h:
                active = False  # прошли список членов — дальше описание
    return pools


def cross_report(open_items, pools, thresh=2):
    n = len(open_items)
    bridges = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = open_items[i], open_items[j]
            pa = pools.get(a["anchor"], set())
            pb = pools.get(b["anchor"], set())
            if not pa or not pb or (pa & pb):
                continue  # нет разметки, либо общий пул — не мост
            w, shared = pair_weight(a["f"], b["f"])
            if w >= thresh:
                bridges.append((w, a, b, pa, pb, shared))
    bridges.sort(key=lambda x: (-x[0], x[1]["anchor"]))
    out = [f"## Мосты между пулами (порог {thresh}; пары из РАЗНЫХ пулов)", ""]
    if not bridges:
        out.append("(мостов не найдено)")
    for w, a, b, pa, pb, shared in bridges:
        out.append(f"- `{a['anchor']}` ({'/'.join(sorted(pa))}) ↔ "
                   f"`{b['anchor']}` ({'/'.join(sorted(pb))}) — вес {w}: {_fmt_shared(shared)}")
    out.append("")
    return "\n".join(out)


def intersects_report(open_items, show_hubs, show_cross):
    out = ["# OQ-INTERSECTS — точки пересечения открытых вопросов (машинный слой)", ""]
    out.append(f"Источник: work/OPEN_QUESTIONS.md · открытых {len(open_items)} · "
               f"генератор `tools/oq_pool.py --intersects`.")
    out.append("Хаб = признак, общий для ≥2 пунктов (ранг = вес признака × охват). "
               "Мост = ребро между пунктами из РАЗНЫХ курируемых пулов (OQ_TRIAGE).")
    out.append("Гардрейлы: χ-склейка запрещена; C-60 (политика) вне хабов/рёбер; "
               "**similarity ≠ зависимость** — типизацию «гейт/закрывает» ставит курируемый "
               "слой событий (шаг 3 плана), не эта машина.")
    out.append("Курируемый слой (события E1…E5, канонные предки, ТОП-5) — "
               "`work/OQ_TRIAGE.md` §«Точки пересечения». Этот файл машинный — регенерируем.")
    out.append("")
    if show_hubs:
        out.append(hubs_report(open_items))
    if show_cross:
        out.append(cross_report(open_items, parse_pools(ROOT / "work" / "OQ_TRIAGE.md")))
    return "\n".join(out)


def main():
    thresh = 3
    write = "--write" in sys.argv
    if "--thresh" in sys.argv:
        thresh = int(sys.argv[sys.argv.index("--thresh") + 1])

    open_items, closed = load_open_items()

    show_hubs = "--hubs" in sys.argv or "--intersects" in sys.argv
    show_cross = "--cross" in sys.argv or "--intersects" in sys.argv
    if show_hubs or show_cross:
        report = intersects_report(open_items, show_hubs, show_cross)
        print(report)
        if write:
            dest = ROOT / "work" / "OQ_INTERSECTS.md"
            io.open(dest, "w", encoding="utf-8", newline="\n").write(report + "\n")
            print(f"\n[written] {dest}")
        return

    n = len(open_items)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            w, shared = pair_weight(open_items[i]["f"], open_items[j]["f"])
            if w >= thresh:
                edges.append((i, j, w, shared))
                parent[find(i)] = find(j)

    pools = {}
    for i in range(n):
        pools.setdefault(find(i), []).append(i)
    ordered = sorted(pools.values(), key=len, reverse=True)

    out = []
    out.append(f"# OQ-POOLS — пулы пересекающихся открытых вопросов")
    out.append(f"")
    out.append(f"Источник: work/OPEN_QUESTIONS.md · открытых {n} (закрытых пропущено {closed})"
               f" · порог ребра {thresh} · генератор tools/oq_pool.py")
    out.append(f"Ребро = общие признаки (C-NN·ID·уровень·О/Д·термин); свидетельства ниже.")
    out.append(f"Идентификатор пункта — стабильный якорь `{{#oq-...}}` (из OPEN_QUESTIONS.md); "
               f"#NN — позиционный, дрейфует при закрытии/добавлении. Ссылайся якорем.")
    out.append("")

    def snip(t, k=96):
        return (t[:k] + "…") if len(t) > k else t

    pool_no = 0
    for comp in ordered:
        if len(comp) == 1:
            continue
        pool_no += 1
        members = [open_items[i] for i in comp]
        # связующие признаки пула: встречаются у >=2 членов
        agg = {}
        for kind, wt in (("C", W_C), ("ID", W_ID), ("LVL", W_LVL),
                         ("OD", W_OD), ("KW", W_KW)):
            cnt = {}
            for it in members:
                for v in it["f"][kind]:
                    cnt[v] = cnt.get(v, 0) + 1
            for v, c in cnt.items():
                if c >= 2:
                    label = f"C-{v}" if kind == "C" else (f"У{v}" if kind == "LVL" else str(v))
                    agg[label] = (wt, c)
        glue = ", ".join(f"{k}×{c}" for k, (wt, c) in
                         sorted(agg.items(), key=lambda x: (-x[1][0], -x[1][1], x[0]))[:12])
        out.append(f"## Пул {pool_no} ({len(comp)} п.) — связки: {glue or '—'}")
        for it in sorted(members, key=lambda x: x["line"]):
            out.append(f"- #{it['id']:02d} `{it['anchor']}` (стр.{it['line']}) {snip(it['text'])}")
        out.append("")

    orphans = [open_items[i] for comp in ordered if len(comp) == 1 for i in comp]
    if orphans:
        out.append(f"## Одиночки ({len(orphans)})")
        for it in sorted(orphans, key=lambda x: x["line"]):
            out.append(f"- #{it['id']:02d} `{it['anchor']}` (стр.{it['line']}) {snip(it['text'])}")
        out.append("")

    pol = [it for it in open_items if it["f"]["POL"]]
    if pol:
        out.append("## Политика C-60+ (одно решение, сквозь пулы)")
        for it in sorted(pol, key=lambda x: x["line"]):
            out.append(f"- #{it['id']:02d} `{it['anchor']}` (стр.{it['line']}) {snip(it['text'], 80)}")
        out.append("")

    report = "\n".join(out)
    print(report)
    if write:
        dest = ROOT / "work" / "OQ_POOLS.md"
        io.open(dest, "w", encoding="utf-8", newline="\n").write(report + "\n")
        print(f"\n[written] {dest}")


if __name__ == "__main__":
    main()
