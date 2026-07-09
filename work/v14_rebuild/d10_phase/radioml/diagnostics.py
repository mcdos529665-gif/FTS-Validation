# -*- coding: utf-8 -*-
"""
ДИАГНОСТИКА апарата RadioML-прогона (post-hoc; НЕ вердикт, НЕ новый тест).

Повод (ревизия 2026-07-09): в опубликованном прогоне (RESULTS.md, коммит bce947e) найден
конфаунд представления. TEST получал СЫРОЙ [I,Q] — гейт §3 runbook п.1 по букве нарушен
(«если тест-модель получает только сырые координаты — ты НЕ построил фазовое представление»):
фаза была ДОСТУПНА (нелинейно извлекаема), но не ПОДАНА. NULL при этом получал ГОТОВЫЕ
нелинейные инварианты [|z|, sign Q]. Проигрыш TEST объясним стоимостью извлечения признаков
при малой ёмкости, а не «вредностью фазы». Плюс сработавшая пред-зарегистрированная оговорка
(null неожиданно силён на PSK — возможен темпоральный след фазы в бит-последовательности)
осталась НЕпроверенной.

Четыре вопроса → варианты признаков (задача РОТАЦИЯ {BPSK,QPSK,8PSK}, SNR>=10, как в прогоне):
  A. Чем выигрывает null?      mag_only [|z|] (128), sign_only [sign Q] (128)
     (если mag_only ≈ null_shadow — победу несёт огибающая: pulse-shaping кодирует величину
      фазовых скачков в проседаниях |z| [внешнее] → предпосылка «|z| неинформативна» ложна)
  B. Темпоральный ли канал?    null_shuf — тот же null с ФИКСИРОВАННОЙ перестановкой времени
     (рушит временной порядок; если null_shuf << null_shadow — канал темпоральный)
  C. ЧИСТЫЙ контраст фазы:     polar_phi [|z|, φ] (256) vs null_shadow [|z|, sign Q] (256) —
     оба получают огибающую ДАРОМ; различие ТОЛЬКО «непрерывный угол vs бит» (аналог пилота)
  D. LO-инвариантная фаза:     polar_dphi [|z|, Δφ] (256), Δφ_t = arg(z_{t+1 mod 128}·conj z_t)
Бейслайны на том же протоколе: raw_iq (256), null_shadow (256).
polar_trig [|z|, cosφ, sinφ] (384) — ёмкостно НЕ честен, только направление.

Протокол диагностики (ослаблен ради скорости): hidden {16, 64}, RepeatedStratifiedKFold 5×2
(10 фолдов), seed/срезы как в прогоне. Числа ОРИЕНТИРОВОЧНЫЕ; контраст для-записи потребует
новой пред-регистрации.
"""
import json, os, pickle, sys, warnings
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
SNR_MIN = 10
CAP = 2000
HIDDENS = [16, 64]
MAXIT = 300


def build_rot():
    with open(os.path.join(HERE, "RML2016.10a_dict.pkl"), "rb") as f:
        d = pickle.load(f, encoding="latin1")
    rng = np.random.default_rng(SEED)
    Xs, ys = [], []
    for ci, mod in enumerate(ROT):
        arr = np.concatenate([d[(mod, s)] for s in range(SNR_MIN, 19, 2) if (mod, s) in d])
        if len(arr) > CAP:
            arr = arr[rng.choice(len(arr), CAP, replace=False)]
        Xs.append(arr); ys.append(np.full(len(arr), ci))
    return np.concatenate(Xs), np.concatenate(ys)


def variants(X):
    I, Q = X[:, 0, :], X[:, 1, :]
    z = I + 1j * Q
    mag = np.abs(z)
    bit = np.sign(Q)
    phi = np.arctan2(Q, I)
    dphi = np.angle(np.roll(z, -1, axis=1) * np.conj(z))     # круговой Δφ, 128 значений
    perm = np.random.default_rng(SEED).permutation(X.shape[2])  # одна фикс. перестановка
    return {
        "raw_iq      (256, как TEST прогона)": np.concatenate([I, Q], axis=1),
        "null_shadow (256, как NULL прогона)": np.concatenate([mag, bit], axis=1),
        "mag_only    (128)": mag,
        "sign_only   (128)": bit,
        "null_shuf   (256, время перемешано)": np.concatenate([mag[:, perm], bit[:, perm]], axis=1),
        "polar_phi   (256, |z|+непрерыв. угол)": np.concatenate([mag, phi], axis=1),
        "polar_dphi  (256, |z|+Δφ LO-инвар.)": np.concatenate([mag, dphi], axis=1),
        "polar_trig  (384, ёмкостно НЕчестен)": np.concatenate([mag, np.cos(phi), np.sin(phi)], axis=1),
    }


def eval_feats(F, y, hidden):
    rkf = RepeatedStratifiedKFold(n_splits=5, n_repeats=2, random_state=SEED)
    accs = []
    for tr, te in rkf.split(F, y):
        sc = StandardScaler().fit(F[tr])
        clf = MLPClassifier(hidden_layer_sizes=(hidden,), max_iter=MAXIT, random_state=SEED)
        clf.fit(sc.transform(F[tr]), y[tr])
        accs.append(accuracy_score(y[te], clf.predict(sc.transform(F[te]))))
    return np.array(accs)


def main():
    print("ДИАГНОСТИКА RadioML-апарата (post-hoc; НЕ вердикт). РОТАЦИЯ {BPSK,QPSK,8PSK}")
    print(f"hidden={HIDDENS}, 10 фолдов, SNR>={SNR_MIN}, cap={CAP}/класс, seed={SEED}")
    print("=" * 78)
    X, y = build_rot()
    V = variants(X)
    out = {}
    base = {}
    for h in HIDDENS:
        base[h] = eval_feats(V["null_shadow (256, как NULL прогона)"], y, h)
    for name, F in V.items():
        out[name] = {}
        for h in HIDDENS:
            if name.startswith("null_shadow"):
                a = base[h]
            else:
                a = eval_feats(F, y, h)
            d = a - base[h]
            p = wilcoxon(d, alternative="greater")[1] if np.any(d != 0) else 1.0
            out[name][h] = {"acc": float(a.mean()), "std": float(a.std()),
                            "delta_vs_null": float(np.median(d)), "p_gt_null": float(p)}
        row = " | ".join(f"h={h}: {out[name][h]['acc']:.4f} (Δnull {out[name][h]['delta_vs_null']:+.4f})"
                         for h in HIDDENS)
        print(f"{name:<42} {row}")
    with open(os.path.join(HERE, "diagnostics.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("\ndiagnostics.json сохранён (числа ориентировочные; Wilcoxon эксплораторный)")


if __name__ == "__main__":
    main()
