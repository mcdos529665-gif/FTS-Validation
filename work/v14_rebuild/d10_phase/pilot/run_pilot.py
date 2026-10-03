# -*- coding: utf-8 -*-
"""
Д10-ПИЛОТ (валидация методики; НЕ двигает потолок SP_COMPLEX — синтетика, runbook §4 п.1).

Цель пилота — методологическая, две галочки:
  (1) усиленный гейт §3 даёт НЕПУСТОЙ тест (фаза реально в тест-модели, таргет требует
      непрерывной θ, не восстановим из одного бита);
  (2) методика ЛОВИТ роль фазы, когда она заведомо есть (контраст спроектирован иметь её).
Если даже здесь test не бьёт null — это сильный (хотя и не двигающий потолок) сигнал против
самого подхода; исход любого знака оформляется честно.

Минимальный контраст (изолирует ровно «непрерывная фаза vs бит», ср. shadow_lemma):
  k вращений θ_i ~ U[0,2π); композиция Θ = (Σ θ_i) mod 2π.
    TEST (непрерывная фаза):  [cos θ_i, sin θ_i]          (2k признаков)
    NULL (тень + бит):        [cos θ_i, sign(sin θ_i)]    (2k признаков, ТОТ ЖЕ счёт)
  Отличие ТОЛЬКО во второй координате: непрерывный sin θ_i  vs  его знак sign(sin θ_i).
  Информация РАВНА: null восстанавливает sin = sign·√(1−cos²) → полный θ_i. Но чтобы
  СЛОЖИТЬ углы (композиция), null должен сперва восстановить непрерывный sin нелинейно;
  при равной МАЛОЙ ёмкости это дороже, чем когда sin подан напрямую (test).

Гейт-апробации §3 (письменно, ДО прогона):
  (1) непрерывная фаза в ТЕСТ-модели? ДА — пара (cos θ_i, sin θ_i).
  (2) таргет восстановим из одного sign(sin)? НЕТ — сектор суммы k=3 непрерывных углов.
  (3) нужна ли θ тоньше полуплоскости? ДА — M секторов, π·2/M радиан.

РОТАЦИОННЫЙ таргет:  sector(Θ, M) ∈ {0..M-1}  (требует точной композиции непрерывных фаз).
КОНТРОЛЬ специфичности: target = (Σ_i cos θ_i > median) — зависит ТОЛЬКО от cos θ_i,
  который у обеих моделей ИДЕНТИЧЕН; отличие sin/sign нерелевантно → преимущества быть НЕ должно.

Модель: MLPClassifier(HIDDEN) — одинаковая для обеих; малой ёмкости, чтобы представление
  имело значение. Метрика: accuracy; парный Wilcoxon по фолдам (RepeatedStratifiedKFold).
"""
import warnings, json, os, sys
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
K = 3            # число складываемых вращений
M = 8            # секторов результирующей фазы
N = 6000         # объём выборки
HIDDEN = (16,)   # фиксированная малая ёмкость, ОДИНАКОВАЯ для test и null
MAXIT = 500


def gen_angles(n, k, seed):
    rng = np.random.RandomState(seed)
    return rng.uniform(0.0, 2.0 * np.pi, size=(n, k))


def feats_test(theta):                       # непрерывная фаза: (cos, sin)
    cols = []
    for i in range(theta.shape[1]):
        cols.append(np.cos(theta[:, i]))
        cols.append(np.sin(theta[:, i]))
    return np.column_stack(cols)


def feats_null(theta):                       # тень + бит: (cos, sign(sin))
    cols = []
    for i in range(theta.shape[1]):
        cols.append(np.cos(theta[:, i]))
        cols.append(np.sign(np.sin(theta[:, i])))
    return np.column_stack(cols)


def target_rotational(theta, m):             # сектор композиции Σθ mod 2π
    big = np.mod(theta.sum(axis=1), 2.0 * np.pi)
    return np.minimum((big / (2.0 * np.pi) * m).astype(int), m - 1)


def target_control(theta):                   # линеен по cos θ_i (обе модели их видят одинаково)
    s = np.cos(theta).sum(axis=1)
    return (s > np.median(s)).astype(int)


def eval_rep(feat_fun, theta, y):
    X = feat_fun(theta)
    rkf = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=SEED)
    accs = []
    for tr, te in rkf.split(X, y):
        sc = StandardScaler().fit(X[tr])            # скейлер на train, transform обоих (без утечки)
        clf = MLPClassifier(hidden_layer_sizes=HIDDEN, max_iter=MAXIT, random_state=SEED)
        clf.fit(sc.transform(X[tr]), y[tr])
        accs.append(accuracy_score(y[te], clf.predict(sc.transform(X[te]))))
    return np.array(accs)


def run():
    print("Д10-ПИЛОТ: непрерывная фаза (cos,sin) vs тень+бит (cos,sign sin)")
    print(f"K={K} вращений, M={M} секторов, N={N}, hidden={HIDDEN}, maxit={MAXIT}, seed={SEED}")
    print("=" * 66)

    theta = gen_angles(N, K, SEED)
    out = {}

    for name, ytgt in [("rotational", target_rotational(theta, M)),
                       ("control", target_control(theta))]:
        a_test = eval_rep(feats_test, theta, ytgt)
        a_null = eval_rep(feats_null, theta, ytgt)
        d = a_test - a_null
        stat, p = wilcoxon(d, alternative="greater") if np.any(d != 0) else (0.0, 1.0)
        out[name] = {
            "test_mean": float(a_test.mean()), "test_std": float(a_test.std()),
            "null_mean": float(a_null.mean()), "null_std": float(a_null.std()),
            "median_delta": float(np.median(d)), "mean_delta": float(d.mean()),
            "wilcoxon_p_test_gt_null": float(p),
            "test_acc": a_test.tolist(), "null_acc": a_null.tolist(),
        }
        print(f"\n[{name}]")
        print(f"  TEST (cos,sin)      acc = {a_test.mean():.4f} ± {a_test.std():.4f}")
        print(f"  NULL (cos,sign sin) acc = {a_null.mean():.4f} ± {a_null.std():.4f}")
        print(f"  Δ (test − null): медиана {np.median(d):+.4f}, среднее {d.mean():+.4f}")
        print(f"  Wilcoxon (test > null): p = {p:.6f}")

    # Пред-зарегистрированный критерий (см. PREREGISTRATION.md)
    rot, ctrl = out["rotational"], out["control"]
    rot_win = (rot["wilcoxon_p_test_gt_null"] < 0.01) and (rot["median_delta"] > 0.05)
    ctrl_clean = (abs(ctrl["median_delta"]) < 0.02) or (ctrl["wilcoxon_p_test_gt_null"] > 0.05)
    if rot_win and ctrl_clean:
        verdict = "МЕТОДИКА РАБОТАЕТ: непрерывная фаза даёт роль на композиции, не на контроле"
    elif rot_win and not ctrl_clean:
        verdict = "ЧАСТИЧНО: test бьёт на ротации, но контроль грязный (не специфично для фазы)"
    else:
        verdict = "НЕ РАЗДЕЛИЛОСЬ: даже спроектированный phase-таргет не дал роли при равной ёмкости"

    print("\n" + "=" * 66)
    print("ВЕРДИКТ ПИЛОТА:", verdict)
    print("(пилот синтетический — потолок SP_COMPLEX НЕ двигает; §4 п.1)")

    out["summary"] = {
        "verdict": verdict, "rot_win": bool(rot_win), "ctrl_clean": bool(ctrl_clean),
        "config": {"K": K, "M": M, "N": N, "hidden": list(HIDDEN), "maxit": MAXIT, "seed": SEED},
    }
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("results.json сохранён")
    return verdict


if __name__ == "__main__":
    run()
