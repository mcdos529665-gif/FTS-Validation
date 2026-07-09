# -*- coding: utf-8 -*-
"""
Д10 РЕАЛЬНЫЙ ТЕСТ на RadioML 2016.10a (option Б). Может ДВИГАТЬ потолок SP_COMPLEX только
через авторское решение по К1–К5 при PASS — сам скрипт статус не трогает.

Вопрос: даёт ли НЕПРЕРЫВНАЯ фаза (полный I/Q) роль над тенью+битом (огибающая + знак),
которую capacity-matched модель НЕ может дёшево восстановить — на РЕАЛЬНОМ RF-сигнале?

Контраст (shadow_lemma / §3), сигнал = комплексная огибающая z(t)=I(t)+iQ(t), 128 отсчётов:
  TEST (непрерывная фаза): вход [I(t); Q(t)]                      → 256 признаков.
  NULL (тень + бит):       вход [|z(t)|; sign(Q(t))]             → 256 признаков (тот же счёт).
  Инфо у null НЕ полная (потерян непрерывный аргумент внутри полуплоскости) — это и проверяем:
  несёт ли выброшенная непрерывная фаза предиктивную роль сверх огибающей и бита.

Гейт-апробации §3 (письменно, ДО прогона):
  (1) непрерывная фаза в ТЕСТ-модели? ДА — полный I/Q (=|z|·(cosφ,sinφ)), φ доступна.
  (2) таргет восстановим из одного sign? НЕТ — класс PSK-порядка задаётся УГЛОМ созвездия
      (BPSK 2 точки, QPSK 4, 8PSK 8 на окружности); один бит полуплоскости порядок не задаёт.
  (3) нужна ли φ тоньше полуплоскости? ДА — различить 8PSK от QPSK требует разрешения угла
      << π (точки созвездия ближе полуплоскости).

Первичный контраст (РОТАЦИОННЫЙ): классификация {BPSK, QPSK, 8PSK} — const-modulus, огибающая
  |z| почти неинформативна → роль несёт фаза.
КОНТРОЛЬ специфичности (АМПЛИТУДНЫЙ): {PAM4, AM-DSB, AM-SSB} — различие в амплитуде; непрерывная
  фаза выигрывать НЕ должна (null с огибающей достаточно). §4 п.4.

КЛЮЧЕВОЙ дизайн (complex-NN литература [внешнее]: null догоняет при росте ёмкости): пред-
регистрируем СВИП по ёмкости hidden ∈ {8,16,64,256}. Предсказание shadow_lemma: на РОТАЦИИ
Δacc=test−null ПОЛОЖИТЕЛЕН при малой ёмкости и УБЫВАЕТ с ростом (null восстанавливает фазу,
когда ёмкости хватает). На КОНТРОЛЕ Δ≈0 на всех ёмкостях.

Метрика: accuracy, парный Wilcoxon по фолдам (RepeatedStratifiedKFold 5×4).
Запуск:  python -X utf8 run_radioml.py --pkl <путь к RML2016.10a_dict.pkl>
         python -X utf8 run_radioml.py --selftest   # синтетическая заглушка формата (НЕ результат)
"""
import argparse, json, os, pickle, sys, warnings
warnings.filterwarnings("ignore")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy.stats import wilcoxon
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import accuracy_score

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260709
ROT = ["BPSK", "QPSK", "8PSK"]                 # const-modulus: фаза несёт всё
CTRL = ["PAM4", "AM-DSB", "AM-SSB"]            # амплитуда несёт; контроль специфичности
SNR_MIN = 10                                   # высокий SNR (чистый сигнал); заморожено
CAP_PER_CLASS = 2000                           # потолок выборки на класс (CPU-бюджет); заморожено
HIDDEN_SWEEP = [8, 16, 64, 256]                # свип ёмкости; заморожено
MAXIT = 300


def load_pkl(path):
    with open(path, "rb") as f:
        d = pickle.load(f, encoding="latin1")
    mods = sorted({k[0] for k in d})
    snrs = sorted({k[1] for k in d})
    shp = next(iter(d.values())).shape
    print(f"загружено: {len(mods)} модуляций, SNR {min(snrs)}..{max(snrs)}, форма выборки {shp}")
    assert shp[1:] == (2, 128), f"ожидалась форма (,2,128), получено {shp}"
    return d, mods, snrs


def build_xy(d, classes, rng):
    """Собрать сырьё (n,2,128) и метки для набора классов, SNR>=SNR_MIN, с потолком на класс."""
    Xs, ys = [], []
    for ci, mod in enumerate(classes):
        chunks = [d[(mod, s)] for s in range(SNR_MIN, 19, 2) if (mod, s) in d]
        if not chunks:
            raise KeyError(f"нет данных для {mod} при SNR>={SNR_MIN}")
        arr = np.concatenate(chunks, axis=0)          # (m,2,128)
        if len(arr) > CAP_PER_CLASS:
            idx = rng.choice(len(arr), CAP_PER_CLASS, replace=False)
            arr = arr[idx]
        Xs.append(arr); ys.append(np.full(len(arr), ci))
    return np.concatenate(Xs), np.concatenate(ys)


def feats_test(X):                                # непрерывная фаза: сырой I/Q
    return X.reshape(len(X), -1)                  # [I(0..127), Q(0..127)]


def feats_null(X):                                # тень + бит: |z(t)|, sign(Q(t))
    I, Q = X[:, 0, :], X[:, 1, :]
    mag = np.sqrt(I ** 2 + Q ** 2)
    bit = np.sign(Q)
    return np.concatenate([mag, bit], axis=1)


def eval_rep(feat_fun, X, y, hidden):
    F = feat_fun(X)
    rkf = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=SEED)
    accs = []
    for tr, te in rkf.split(F, y):
        sc = StandardScaler().fit(F[tr])
        clf = MLPClassifier(hidden_layer_sizes=(hidden,), max_iter=MAXIT, random_state=SEED)
        clf.fit(sc.transform(F[tr]), y[tr])
        accs.append(accuracy_score(y[te], clf.predict(sc.transform(F[te]))))
    return np.array(accs)


def run_task(name, d, classes, rng):
    X, y = build_xy(d, classes, rng)
    print(f"\n[{name}] классы={classes}  n={len(y)}  (баланс {np.bincount(y)})")
    rows = {}
    for h in HIDDEN_SWEEP:
        at = eval_rep(feats_test, X, y, h)
        an = eval_rep(feats_null, X, y, h)
        dlt = at - an
        p = wilcoxon(dlt, alternative="greater")[1] if np.any(dlt != 0) else 1.0
        rows[h] = {"test": float(at.mean()), "null": float(an.mean()),
                   "median_delta": float(np.median(dlt)), "wilcoxon_p": float(p)}
        print(f"  hidden={h:>3}: TEST {at.mean():.4f} | NULL {an.mean():.4f} | "
              f"Δ {np.median(dlt):+.4f} | p={p:.5f}")
    return rows


def make_selftest_dict(rng):
    """Синтетическая заглушка ФОРМАТА RML (НЕ данные): проверить, что пайплайн исполняется."""
    d = {}
    order = {"BPSK": 2, "QPSK": 4, "8PSK": 8}
    for mod in ROT:
        for s in range(SNR_MIN, 19, 2):
            k = order[mod]
            sym = rng.integers(0, k, size=(600, 128))
            ph = 2 * np.pi * sym / k
            I = np.cos(ph) + 0.1 * rng.standard_normal((600, 128))
            Q = np.sin(ph) + 0.1 * rng.standard_normal((600, 128))
            d[(mod, s)] = np.stack([I, Q], axis=1).astype(np.float32)
    for mod, amp in zip(CTRL, [1.0, 2.0, 3.0]):
        for s in range(SNR_MIN, 19, 2):
            base = amp + 0.2 * rng.standard_normal((600, 128))
            I = base * np.cos(rng.uniform(0, 2*np.pi, (600, 128)))
            Q = base * np.sin(rng.uniform(0, 2*np.pi, (600, 128)))
            d[(mod, s)] = np.stack([I, Q], axis=1).astype(np.float32)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkl", help="путь к RML2016.10a_dict.pkl")
    ap.add_argument("--selftest", action="store_true", help="синтетическая проверка пайплайна")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED)

    if args.selftest:
        print("=== SELFTEST (синтетическая заглушка формата — НЕ результат) ===")
        d = make_selftest_dict(rng)
        mods = sorted({k[0] for k in d})
        print(f"заглушка: {len(mods)} модуляций")
    elif args.pkl:
        if not os.path.exists(args.pkl):
            print(f"НЕТ ФАЙЛА: {args.pkl}\nПоложи RML2016.10a_dict.pkl по этому пути и повтори.")
            sys.exit(2)
        d, mods, snrs = load_pkl(args.pkl)
        missing = [m for m in ROT + CTRL if m not in mods]
        if missing:
            print(f"ВНИМАНИЕ: в датасете нет классов {missing}; проверь имена модуляций: {mods}")
            sys.exit(3)
    else:
        print("укажи --pkl <путь> или --selftest"); sys.exit(1)

    print(f"\nRadioML Д10: TEST [I,Q] vs NULL [|z|,sign Q]; SNR>={SNR_MIN}; "
          f"cap/class={CAP_PER_CLASS}; свип hidden={HIDDEN_SWEEP}; seed={SEED}")
    print("=" * 70)
    rot = run_task("РОТАЦИЯ (PSK-порядок)", d, ROT, rng)
    ctl = run_task("КОНТРОЛЬ (амплитудные)", d, CTRL, rng)

    # Пред-зарегистрированный критерий (см. PREREGISTRATION.md)
    lo, hi = HIDDEN_SWEEP[0], HIDDEN_SWEEP[-1]
    rot_win_all = all(rot[h]["wilcoxon_p"] < 0.01 and rot[h]["median_delta"] > 0.03 for h in HIDDEN_SWEEP)
    rot_win_lo = rot[lo]["wilcoxon_p"] < 0.01 and rot[lo]["median_delta"] > 0.03
    caught_up = rot_win_lo and (rot[hi]["median_delta"] < 0.03 or rot[hi]["wilcoxon_p"] >= 0.01)
    # контроль ЧИСТ = test НЕ выигрывает значимо (null может выигрывать — это ожидаемо и норм)
    ctrl_clean = all(ctl[h]["median_delta"] < 0.03 or ctl[h]["wilcoxon_p"] > 0.05 for h in HIDDEN_SWEEP)
    if args.selftest:
        verdict = "SELFTEST выполнен (пайплайн исполняется); числа НЕ являются результатом"
    elif rot_win_all and ctrl_clean:
        verdict = ("PASS (кандидат на снятие потолка): непрерывная фаза бьёт тень+бит на ВСЕХ "
                   "ёмкостях — null НЕ догоняет (роль фазы нередуцируема); контроль чист")
    elif caught_up and ctrl_clean:
        verdict = ("OVERLAY-СОГЛАСНО (потолок СТОИТ): роль при малой ёмкости есть, но null ДОГОНЯЕТ "
                   "при росте ширины → фаза удобна, но не необходима (complex-NN паттерн)")
    elif rot_win_lo and ctrl_clean:
        verdict = "ЧАСТИЧНО: роль при малой ёмкости есть, поведение по свипу неоднозначно; потолок стоит"
    else:
        verdict = "FAIL/НЕ РАЗДЕЛИЛОСЬ: непрерывная фаза не дала честной роли над тенью+битом"
    print("\n" + "=" * 70)
    print("ВЕРДИКТ:", verdict)
    if not args.selftest:
        print("(статус SP_COMPLEX двигает ТОЛЬКО автор по К1–К5; скрипт статус не трогает)")

    out = {"rotational": rot, "control": ctl, "verdict": verdict,
           "config": {"ROT": ROT, "CTRL": CTRL, "SNR_MIN": SNR_MIN, "CAP_PER_CLASS": CAP_PER_CLASS,
                      "HIDDEN_SWEEP": HIDDEN_SWEEP, "MAXIT": MAXIT, "SEED": SEED,
                      "selftest": bool(args.selftest)}}
    fname = "selftest.json" if args.selftest else "results.json"
    with open(os.path.join(HERE, fname), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"{fname} сохранён")


if __name__ == "__main__":
    main()
