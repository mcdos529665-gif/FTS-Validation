# -*- coding: utf-8 -*-
"""
Д10-тест v2 на RadioML 2016.10a — корректный контраст после ревизии v1 (DECISIONS (9)).
Дизайн и критерий заморожены в PREREGISTRATION_v2.md (коммит ДО прогона). Статус SP_COMPLEX
двигает только автор по К1–К5; скрипт статусов не трогает.

TEST   [|z|; Δφ]        — тень + НЕПРЕРЫВНЫЕ фазовые приращения (LO-инвариантны)
NULL-A [|z|; sign Q]    — канонический тень+бит (shadow_lemma)
NULL-B [|z|; sign Δφ]   — дифференциальный бит (сильнейший null: та же структура, без непрерывности)
Абляция lo_mean (1 признак: средний Δφ) — против артефакта генерации (класс-коррелированный offset).

Запуск: python -X utf8 run_radioml_v2.py --pkl RML2016.10a_dict.pkl
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
ROT = ["BPSK", "QPSK", "8PSK"]
CTRL = ["PAM4", "AM-DSB", "AM-SSB"]
SNR_MIN = 10
CAP = 2000
HIDDENS = [8, 16, 64, 256]
MAXIT = 300


def load_pkl(path):
    with open(path, "rb") as f:
        d = pickle.load(f, encoding="latin1")
    mods = sorted({k[0] for k in d})
    shp = next(iter(d.values())).shape
    assert shp[1:] == (2, 128), f"ожидалась (,2,128), получено {shp}"
    print(f"загружено: {len(mods)} модуляций, форма {shp}")
    return d


def build_xy(d, classes):
    rng = np.random.default_rng(SEED)
    Xs, ys = [], []
    for ci, mod in enumerate(classes):
        arr = np.concatenate([d[(mod, s)] for s in range(SNR_MIN, 19, 2) if (mod, s) in d])
        if len(arr) > CAP:
            arr = arr[rng.choice(len(arr), CAP, replace=False)]
        Xs.append(arr); ys.append(np.full(len(arr), ci))
    return np.concatenate(Xs), np.concatenate(ys)


def parts(X):
    I, Q = X[:, 0, :], X[:, 1, :]
    z = I + 1j * Q
    mag = np.abs(z)
    dphi = np.angle(np.roll(z, -1, axis=1) * np.conj(z))
    return mag, np.sign(Q), dphi


def feats_test(X):
    mag, _, dphi = parts(X)
    return np.concatenate([mag, dphi], axis=1)


def feats_null_a(X):
    mag, sq, _ = parts(X)
    return np.concatenate([mag, sq], axis=1)


def feats_null_b(X):
    mag, _, dphi = parts(X)
    return np.concatenate([mag, np.sign(dphi)], axis=1)


def feats_lo_mean(X):
    _, _, dphi = parts(X)
    return dphi.mean(axis=1, keepdims=True)


def eval_feats(F, y, hidden):
    rkf = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=SEED)
    accs = []
    for tr, te in rkf.split(F, y):
        sc = StandardScaler().fit(F[tr])
        clf = MLPClassifier(hidden_layer_sizes=(hidden,), max_iter=MAXIT, random_state=SEED)
        clf.fit(sc.transform(F[tr]), y[tr])
        accs.append(accuracy_score(y[te], clf.predict(sc.transform(F[te]))))
    return np.array(accs)


def run_task(name, d, classes):
    X, y = build_xy(d, classes)
    print(f"\n[{name}] {classes}  n={len(y)}")
    out = {}
    for h in HIDDENS:
        at = eval_feats(feats_test(X), y, h)
        aa = eval_feats(feats_null_a(X), y, h)
        ab = eval_feats(feats_null_b(X), y, h)
        da, db = at - aa, at - ab
        pa = wilcoxon(da, alternative="greater")[1] if np.any(da != 0) else 1.0
        pb = wilcoxon(db, alternative="greater")[1] if np.any(db != 0) else 1.0
        out[h] = {"test": float(at.mean()), "nullA": float(aa.mean()), "nullB": float(ab.mean()),
                  "medA": float(np.median(da)), "pA": float(pa),
                  "medB": float(np.median(db)), "pB": float(pb)}
        print(f"  h={h:>3}: TEST {at.mean():.4f} | A {aa.mean():.4f} (Δ{np.median(da):+.4f} p={pa:.5f})"
              f" | B {ab.mean():.4f} (Δ{np.median(db):+.4f} p={pb:.5f})")
    return out, X, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkl", default=os.path.join(HERE, "RML2016.10a_dict.pkl"))
    args = ap.parse_args()
    d = load_pkl(args.pkl)
    print(f"Д10 v2: TEST [|z|,Δφ] vs NULL-A [|z|,sign Q] и NULL-B [|z|,sign Δφ]; "
          f"SNR>={SNR_MIN}; hidden={HIDDENS}; seed={SEED}")
    print("=" * 78)
    rot, Xr, yr = run_task("РОТАЦИЯ", d, ROT)
    ctl, _, _ = run_task("КОНТРОЛЬ", d, CTRL)

    lo = eval_feats(feats_lo_mean(Xr), yr, 16)
    lo_acc = float(lo.mean())
    print(f"\n[АБЛЯЦИЯ lo_mean (1 признак, h=16)] acc = {lo_acc:.4f} (поле 0.333; порог брака 0.40)")

    # Замороженный критерий (PREREGISTRATION_v2)
    win = lambda r, h: (r[h]["pA"] < 0.01 and r[h]["medA"] > 0.05 and
                        r[h]["pB"] < 0.01 and r[h]["medB"] > 0.05)
    rot_all = all(win(rot, h) for h in HIDDENS)
    rot_lo = win(rot, 8)
    hi = HIDDENS[-1]
    caught = rot_lo and not win(rot, hi)
    ctrl_clean = all((ctl[h]["medA"] < 0.03 or ctl[h]["pA"] > 0.05) and
                     (ctl[h]["medB"] < 0.03 or ctl[h]["pB"] > 0.05) for h in HIDDENS)
    lo_ok = lo_acc < 0.40

    if not lo_ok:
        verdict = "АРТЕФАКТ: lo_mean классифицирует — класс-коррелированный offset; вердикт не выносится"
    elif rot_all and ctrl_clean:
        verdict = ("PASS (кандидат на снятие потолка): непрерывные фазовые приращения бьют ОБА "
                   "null'а на всех ёмкостях; контроль чист; абляция чиста")
    elif caught and ctrl_clean:
        verdict = "OVERLAY-СОГЛАСНО: роль при малой ёмкости, но null догоняет к 256 — потолок стоит"
    elif rot_lo and ctrl_clean:
        verdict = "ЧАСТИЧНО: роль при малой ёмкости, свип неоднозначен; потолок стоит"
    else:
        verdict = "FAIL: непрерывность приращений не дала роли над битами / контроль грязен"

    print("\n" + "=" * 78)
    print("ВЕРДИКТ v2:", verdict)
    print("(потолок двигает только автор по К1–К5; при PASS исполнитель готовит черновик)")

    out = {"rotational": rot, "control": ctl, "lo_mean_acc": lo_acc, "verdict": verdict,
           "config": {"ROT": ROT, "CTRL": CTRL, "SNR_MIN": SNR_MIN, "CAP": CAP,
                      "HIDDENS": HIDDENS, "MAXIT": MAXIT, "SEED": SEED}}
    with open(os.path.join(HERE, "results_v2.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("results_v2.json сохранён")


if __name__ == "__main__":
    main()
