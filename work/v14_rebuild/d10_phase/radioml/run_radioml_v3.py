# -*- coding: utf-8 -*-
"""
Д10-тест v3 на RadioML 2016.10a — CFO-нормализованный контраст (чистый остаток после v2-АРТЕФАКТА).
Дизайн и критерий заморожены в PREREGISTRATION_v3.md (коммит ДО прогона). Статус SP_COMPLEX
двигает только автор по К1–К5; скрипт статусов не трогает.

CFO-нормализация: z'_t = z_t * exp(-i*m̂*t), m̂ = mean_t(Δφ_t) — артефакт lo_mean вычтен из
ОБЕИХ сторон симметрично; контраст изолирует повременную непрерывную фазу.

TEST   [|z'|; Δφ']         — нормализованная тень + непрерывные приращения фазы
NULL-A [|z'|; sign(Q')]    — канонический тень+бит (shadow_lemma)
NULL-B [|z'|; sign(Δφ')]   — дифференциальный бит (сильнейший null)
SCALARS                    — 10 скалярных признаков из Δφ' (при hidden=64)
m̂'-абляция                — 1 признак: mean(Δφ') ПОСЛЕ дероутации (ожидание ≈ 0, должна быть мертва)

Запуск: python -X utf8 run_radioml_v3.py [--pkl RML2016.10a_dict.pkl]
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
        Xs.append(arr)
        ys.append(np.full(len(arr), ci))
    return np.concatenate(Xs), np.concatenate(ys)


def cfo_normalize(X):
    """
    CFO-нормализация по runbook_v3 §3.
    Вход X: (N, 2, 128) — канал 0 = I, канал 1 = Q.
    Выход z_prime: (N, 128) комплексный.
    m_hat: (N,) — оценка несущей по примеру.
    dphi_prime_mean: (N,) — mean(Δφ') для assert.
    """
    I, Q = X[:, 0, :], X[:, 1, :]
    z = I + 1j * Q                                                 # (N, 128)

    # Δφ_t = angle(z_{t+1 mod 128} · conj(z_t))
    dphi = np.angle(np.roll(z, -1, axis=1) * np.conj(z))          # (N, 128)
    m_hat = dphi.mean(axis=1)                                      # (N,)   скаляр на пример

    # Дероутация: z'_t = z_t * exp(-i * m̂ * t)
    t = np.arange(128, dtype=float)                                # (128,)
    phase_correction = np.exp(-1j * m_hat[:, None] * t[None, :])  # (N, 128) broadcast
    z_prime = z * phase_correction                                 # (N, 128)

    # Пересчёт Δφ' для assert нормализации
    dphi_prime = np.angle(np.roll(z_prime, -1, axis=1) * np.conj(z_prime))  # (N, 128)
    dphi_prime_mean = dphi_prime.mean(axis=1)                                 # (N,)

    return z_prime, m_hat, dphi_prime, dphi_prime_mean


def check_normalization(dphi_prime_mean, label=""):
    """
    Машинная проверка нормализации по runbook_v3 §3.
    Возвращает (max_abs, status): 'ok' / 'warn' / 'fail'
    """
    max_abs = float(np.max(np.abs(dphi_prime_mean)))
    if max_abs < 1e-6:
        status = "ok"
    elif max_abs < 1e-3:
        status = "warn"
    else:
        status = "fail"
    print(f"  нормализация{' [' + label + ']' if label else ''}: max|mean Δφ'| = {max_abs:.3e} → {status}")
    return max_abs, status


def feats_test(z_prime, dphi_prime):
    """TEST: [|z'_t| (128); Δφ'_t (128)] — тень + непрерывные приращения фазы."""
    mag = np.abs(z_prime)                          # (N, 128)
    return np.concatenate([mag, dphi_prime], axis=1)   # (N, 256)


def feats_null_a(z_prime):
    """NULL-A: [|z'_t| (128); sign(Q'_t) (128)] — канонический тень+бит."""
    mag = np.abs(z_prime)
    Q_prime = z_prime.imag
    return np.concatenate([mag, np.sign(Q_prime)], axis=1)


def feats_null_b(z_prime, dphi_prime):
    """NULL-B: [|z'_t| (128); sign(Δφ'_t) (128)] — дифференциальный бит."""
    mag = np.abs(z_prime)
    return np.concatenate([mag, np.sign(dphi_prime)], axis=1)


def feats_scalars(dphi_prime):
    """
    SCALARS: 10 признаков из Δφ'.
    [std(Δφ'), mean(|Δφ'|), histogram(Δφ', bins=8, range=(-π,π], density=True)]
    """
    N = dphi_prime.shape[0]
    std_dphi = dphi_prime.std(axis=1, keepdims=True)                    # (N, 1)
    mean_abs = np.abs(dphi_prime).mean(axis=1, keepdims=True)           # (N, 1)
    # Гистограмма по каждому примеру отдельно
    bins = 8
    hist_arr = np.zeros((N, bins))
    edges = np.linspace(-np.pi, np.pi, bins + 1)
    for i in range(N):
        h, _ = np.histogram(dphi_prime[i], bins=edges, density=True)
        hist_arr[i] = h * (edges[1] - edges[0])                         # нормализация → сумма ≈ 1
    return np.concatenate([std_dphi, mean_abs, hist_arr], axis=1)       # (N, 10)


def feats_mhat_prime(dphi_prime_mean):
    """m̂'-абляция: 1 признак = mean(Δφ') ПОСЛЕ дероутации (должна быть ≈ 0)."""
    return dphi_prime_mean[:, None]                                      # (N, 1)


def eval_feats(F, y, hidden):
    rkf = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=SEED)
    accs = []
    for tr, te in rkf.split(F, y):
        sc = StandardScaler().fit(F[tr])
        clf = MLPClassifier(hidden_layer_sizes=(hidden,), max_iter=MAXIT, random_state=SEED)
        clf.fit(sc.transform(F[tr]), y[tr])
        accs.append(accuracy_score(y[te], clf.predict(sc.transform(F[te]))))
    return np.array(accs)


def run_task(name, d, classes, verbose=True):
    """
    Прогон РОТАЦИИ или КОНТРОЛЯ по всем ёмкостям.
    Возвращает словарь результатов, X (raw), y, z_prime, dphi_prime, dphi_prime_mean.
    """
    X, y = build_xy(d, classes)
    z_prime, m_hat, dphi_prime, dphi_prime_mean = cfo_normalize(X)

    if verbose:
        print(f"\n[{name}] {classes}  n={len(y)}")
    max_abs, norm_status = check_normalization(dphi_prime_mean, name)

    out = {"norm_max": max_abs, "norm_status": norm_status}

    if norm_status == "fail":
        print(f"  СТОП: нормализация не сошлась (>{1e-3:.0e}) — АРТЕФАКТ, вердикт не выносится")
        return out, X, y, z_prime, dphi_prime, dphi_prime_mean

    Ft = feats_test(z_prime, dphi_prime)
    Fa = feats_null_a(z_prime)
    Fb = feats_null_b(z_prime, dphi_prime)

    for h in HIDDENS:
        at = eval_feats(Ft, y, h)
        aa = eval_feats(Fa, y, h)
        ab = eval_feats(Fb, y, h)
        da, db = at - aa, at - ab
        pa = wilcoxon(da, alternative="greater")[1] if np.any(da != 0) else 1.0
        pb = wilcoxon(db, alternative="greater")[1] if np.any(db != 0) else 1.0
        out[h] = {
            "test":  float(at.mean()),
            "nullA": float(aa.mean()),
            "nullB": float(ab.mean()),
            "medA":  float(np.median(da)),
            "pA":    float(pa),
            "medB":  float(np.median(db)),
            "pB":    float(pb),
        }
        if verbose:
            print(
                f"  h={h:>3}: TEST {at.mean():.4f} | "
                f"A {aa.mean():.4f} (Δ{np.median(da):+.4f} p={pa:.5f}) | "
                f"B {ab.mean():.4f} (Δ{np.median(db):+.4f} p={pb:.5f})"
            )

    return out, X, y, z_prime, dphi_prime, dphi_prime_mean


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkl", default=os.path.join(HERE, "RML2016.10a_dict.pkl"))
    args = ap.parse_args()

    d = load_pkl(args.pkl)
    print(
        f"Д10 v3: TEST [|z'|,Δφ'] vs NULL-A [|z'|,sign Q'] и NULL-B [|z'|,sign Δφ']; "
        f"CFO-нормализация; SNR>={SNR_MIN}; hidden={HIDDENS}; seed={SEED}"
    )
    print("=" * 78)

    rot, Xr, yr, zr_prime, dphi_r, dphi_r_mean = run_task("РОТАЦИЯ", d, ROT)
    ctl, Xc, yc, zc_prime, dphi_c, dphi_c_mean = run_task("КОНТРОЛЬ", d, CTRL)

    # SCALARS-абляция (hidden=64, только РОТАЦИЯ)
    print("\n[SCALARS-абляция (10 признаков, h=64)]")
    Fs = feats_scalars(dphi_r)
    Ft64 = feats_test(zr_prime, dphi_r)
    scalars_accs = eval_feats(Fs, yr, 64)
    test64_accs = eval_feats(Ft64, yr, 64)
    scalars_acc = float(scalars_accs.mean())
    test64_acc = float(test64_accs.mean())
    delta_scalars = test64_accs - scalars_accs
    p_scalars = wilcoxon(delta_scalars, alternative="greater")[1] if np.any(delta_scalars != 0) else 1.0
    med_scalars = float(np.median(delta_scalars))
    print(f"  SCALARS acc={scalars_acc:.4f} | TEST(64) acc={test64_acc:.4f} "
          f"| Δ={med_scalars:+.4f} p={p_scalars:.5f}")

    # m̂'-абляция (hidden=16, только РОТАЦИЯ)
    print("\n[m̂'-абляция (1 признак: mean Δφ' ≈ 0, h=16)]")
    Fm = feats_mhat_prime(dphi_r_mean)
    mhat_accs = eval_feats(Fm, yr, 16)
    mhat_acc = float(mhat_accs.mean())
    print(f"  m̂'-абляция acc={mhat_acc:.4f} (поле 0.333; порог СТОП: 0.40)")

    # ============================================================
    # Замороженный критерий (PREREGISTRATION_v3.md §4 runbook_v3)
    # ============================================================
    norm_ok = (rot.get("norm_status", "fail") != "fail" and
               ctl.get("norm_status", "fail") != "fail")
    mhat_dead = mhat_acc < 0.40

    def win(r, h):
        """Победа на ёмкости h: p<0.01 И медиана Δ>+0.05, против ОБОИХ null'ов."""
        if h not in r:
            return False
        return (r[h]["pA"] < 0.01 and r[h]["medA"] > 0.05 and
                r[h]["pB"] < 0.01 and r[h]["medB"] > 0.05)

    rot_all_h = all(win(rot, h) for h in HIDDENS if h in rot)
    rot_h8 = win(rot, 8)

    # OVERLAY: победа при h=8, но хотя бы один null догоняет к 256
    # «догоняет» := медиана Δ < +0.05 или p ≥ 0.01 для хотя бы одного null
    def null_catches(r, h):
        if h not in r:
            return True
        a_catches = (r[h]["medA"] < 0.05 or r[h]["pA"] >= 0.01)
        b_catches = (r[h]["medB"] < 0.05 or r[h]["pB"] >= 0.01)
        return a_catches or b_catches

    overlay = rot_h8 and null_catches(rot, 256)

    ctrl_clean = all(
        (ctl[h]["medA"] < 0.03 or ctl[h]["pA"] > 0.05) and
        (ctl[h]["medB"] < 0.03 or ctl[h]["pB"] > 0.05)
        for h in HIDDENS if h in ctl
    )

    # SCALARS: TEST(64) − SCALARS >= +0.05 И p<0.01
    scalars_gap = med_scalars >= 0.05 and p_scalars < 0.01

    print("\n" + "=" * 78)
    print("ЗАМОРОЖЕННЫЙ КРИТЕРИЙ §4 runbook_v3:")
    print(f"  norm_ok={norm_ok}  mhat_dead={mhat_dead}  rot_all_h={rot_all_h}  "
          f"rot_h8={rot_h8}  overlay={overlay}  ctrl_clean={ctrl_clean}  scalars_gap={scalars_gap}")

    if not norm_ok:
        verdict = "АРТЕФАКТ: нормализация не сошлась — вердикт не выносится"
    elif not mhat_dead:
        verdict = "АРТЕФАКТ: m̂'-абляция классифицирует — новый скалярный артефакт, вердикт не выносится"
    elif rot_all_h and ctrl_clean and scalars_gap:
        verdict = ("PASS-Т (темпоральная роль): победа над ОБОИМИ null'ами на всех h; "
                   "TEST(64)−SCALARS≥+0.05; контроль чист; m̂'-абляция мертва")
    elif rot_all_h and ctrl_clean and not scalars_gap:
        verdict = ("PASS-С (скалярная роль): победа над ОБОИМИ null'ами на всех h, "
                   "контроль чист, НО TEST(64)−SCALARS<+0.05 — роль исчерпывается скалярными статистиками")
    elif overlay and ctrl_clean:
        verdict = "OVERLAY-СОГЛАСНО: роль при h=8, но хотя бы один null догоняет к h=256 — потолок стоит"
    elif not rot_h8:
        verdict = "FAIL: нет победы над обоими null'ами при h=8"
    elif not ctrl_clean:
        verdict = "FAIL: контроль грязен (TEST выигрывает там, где не должен)"
    else:
        verdict = "FAIL: условия критерия не выполнены"

    print("ВЕРДИКТ v3:", verdict)
    print("(потолок SP_COMPLEX двигает только автор по К1–К5)")

    out = {
        "rotational":   rot,
        "control":      ctl,
        "scalars_h64":  {"acc": scalars_acc, "test64_acc": test64_acc,
                         "med_delta": med_scalars, "p": float(p_scalars)},
        "mhat_prime_h16": {"acc": mhat_acc},
        "verdict":      verdict,
        "config": {
            "ROT": ROT, "CTRL": CTRL, "SNR_MIN": SNR_MIN, "CAP": CAP,
            "HIDDENS": HIDDENS, "MAXIT": MAXIT, "SEED": SEED,
            "note": "CFO-нормализация: z'=z*exp(-i*m̂*t), m̂=mean(Δφ); все признаки из z'",
        },
    }
    out_path = os.path.join(HERE, "results_v3.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"results_v3.json сохранён → {out_path}")


if __name__ == "__main__":
    main()
