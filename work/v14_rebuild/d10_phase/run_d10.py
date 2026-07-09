# -*- coding: utf-8 -*-
"""
Д10-тест: фаза как представление (непрерывное вращение U(1) vs дискретное зеркало Z/2).
Синтетическая волновая интерференция.

Два набора задач:
1. РОТАЦИОННЫЕ (композиция вращений):
   - Интерференция: z = r1·e^{iθ1} + r2·e^{iθ2}; целевая f ∝ |z| sin(arg(z) − θ_ref)
   - Спектр: |z| в зависимости от фазового сдвига Δθ
   - Угловая скорость: darg(z)/dt

2. КОНТРОЛЬНЫЕ (гауссовы облака, без вращения):
   - Линейная функция от двух координат
   - Гауссовский процесс (локально гладкая функция)

Архитектура:
- Тестовая (полярная): вход [real, imag] (2 фичи) → LogisticRegression
- Null (декартова + тень): вход [|z|, real, sign(imag)] (3 фичи) → LogisticRegression

Ёмкость: null имеет 4 параметра, test — 3. При равных попытках test должна проигрывать,
если вращение не даёт роли.

Метрика: ROC-AUC, Wilcoxon signed-rank по фолдам.
Критерий PASS: test > null на РОТАЦИОННЫХ (p < 0.01, ΔAUC > +0.03) И null ≈ test
на КОНТРОЛЬНЫХ (p > 0.05).
"""

import warnings, json, os, sys
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260709

# Ротационные задачи (композиция вращений)
ROTATIONAL_TASKS = [
    "interference_sine",      # z = r1·e^{iθ1} + r2·e^{iθ2}; y ~ sin(arg(z))
    "interference_cosine",    # z = r1·e^{iθ1} + r2·e^{iθ2}; y ~ cos(arg(z))
    "phase_shift_effect",     # y зависит от Δθ = θ1 − θ2 нелинейно
    "rotating_vector",        # вращающийся вектор; y ~ sin(θ + t)
]

# Контрольные задачи (без вращения)
CONTROL_TASKS = [
    "gaussian_linear",        # гауссово облако; y ~ a·x1 + b·x2
    "gaussian_smooth",        # гауссово облако; y ~ exp(−||x||²)
]

def generate_rotational_interference_sine(n=1000, seed=None):
    """z = r1·e^{iθ1} + r2·e^{iθ2}; y = 1 если sin(arg(z)) > 0, иначе 0."""
    rng = np.random.RandomState(seed)
    r1 = rng.uniform(0.5, 2, n)
    r2 = rng.uniform(0.5, 2, n)
    th1 = rng.uniform(0, 2*np.pi, n)
    th2 = rng.uniform(0, 2*np.pi, n)

    z = r1 * np.exp(1j * th1) + r2 * np.exp(1j * th2)
    real = z.real
    imag = z.imag
    y = (np.sin(np.arctan2(imag, real)) > 0).astype(int)

    X = np.column_stack([real, imag])
    return X, y

def generate_rotational_interference_cosine(n=1000, seed=None):
    """z = r1·e^{iθ1} + r2·e^{iθ2}; y = 1 если cos(arg(z)) > 0, иначе 0."""
    rng = np.random.RandomState(seed)
    r1 = rng.uniform(0.5, 2, n)
    r2 = rng.uniform(0.5, 2, n)
    th1 = rng.uniform(0, 2*np.pi, n)
    th2 = rng.uniform(0, 2*np.pi, n)

    z = r1 * np.exp(1j * th1) + r2 * np.exp(1j * th2)
    real = z.real
    imag = z.imag
    arg_z = np.arctan2(imag, real)
    y = (np.cos(arg_z) > 0).astype(int)

    X = np.column_stack([real, imag])
    return X, y

def generate_rotational_phase_shift(n=1000, seed=None):
    """y зависит нелинейно от Δθ = θ1 − θ2."""
    rng = np.random.RandomState(seed)
    r1 = rng.uniform(0.8, 1.5, n)
    r2 = rng.uniform(0.8, 1.5, n)
    th1 = rng.uniform(0, 2*np.pi, n)
    delta_th = rng.uniform(-np.pi, np.pi, n)  # фазовый сдвиг
    th2 = th1 + delta_th

    z = r1 * np.exp(1j * th1) + r2 * np.exp(1j * th2)
    real = z.real
    imag = z.imag

    # y = 1 если |z| и cos(delta_th) согласованы в специфичном смысле
    agreement = (np.abs(z) > 1.0) & (np.cos(delta_th) > 0.2)
    y = agreement.astype(int)

    X = np.column_stack([real, imag])
    return X, y

def generate_rotational_rotating_vector(n=1000, seed=None):
    """Вращающийся вектор: y ~ sin(θ + t), где t — параметр."""
    rng = np.random.RandomState(seed)
    t = rng.uniform(0, 2*np.pi, n)  # "время"
    r = rng.uniform(0.5, 2, n)
    theta = rng.uniform(0, 2*np.pi, n)

    z = r * np.exp(1j * (theta + t))
    real = z.real
    imag = z.imag
    y = (np.sin(theta + t) > 0).astype(int)

    X = np.column_stack([real, imag])
    return X, y

def generate_control_gaussian_linear(n=1000, seed=None):
    """Гауссово облако; y ~ a·x1 + b·x2."""
    rng = np.random.RandomState(seed)
    x1 = rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)
    y = (0.5 * x1 + 0.5 * x2 > 0).astype(int)
    y = (y + rng.normal(0, 0.3, n) > 0.5).astype(int)  # небольшой шум

    X = np.column_stack([x1, x2])
    return X, y

def generate_control_gaussian_smooth(n=1000, seed=None):
    """Гауссово облако; y ~ exp(−||x||²)."""
    rng = np.random.RandomState(seed)
    x1 = rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)
    norm_sq = x1**2 + x2**2
    y = (np.exp(-norm_sq) > np.median(np.exp(-norm_sq))).astype(int)

    X = np.column_stack([x1, x2])
    return X, y

def load_task(task_name, seed):
    """Загрузить синтетическую задачу."""
    generators = {
        "interference_sine": generate_rotational_interference_sine,
        "interference_cosine": generate_rotational_interference_cosine,
        "phase_shift_effect": generate_rotational_phase_shift,
        "rotating_vector": generate_rotational_rotating_vector,
        "gaussian_linear": generate_control_gaussian_linear,
        "gaussian_smooth": generate_control_gaussian_smooth,
    }
    X, y = generators[task_name](n=1000, seed=seed)
    return X, y

def fit_eval_polar(Xtr, Xte, ytr, yte):
    """Полярная модель: вход [real, imag]."""
    Xtr_scaled = StandardScaler().fit_transform(Xtr)
    Xte_scaled = StandardScaler().fit_transform(Xte)
    clf = LogisticRegression(penalty='l2', C=1.0, max_iter=2000, solver='lbfgs',
                             random_state=SEED)
    clf.fit(Xtr_scaled, ytr)
    p = clf.predict_proba(Xte_scaled)[:, 1]
    auc = roc_auc_score(yte, p)
    return auc

def fit_eval_null(Xtr, Xte, ytr, yte):
    """Null-модель: вход [|z|, Re(z), sign(Im(z))]."""
    # Xtr, Xte уже содержат [real, imag]
    abs_z_tr = np.linalg.norm(Xtr, axis=1)
    real_tr = Xtr[:, 0]
    sign_im_tr = np.sign(Xtr[:, 1])

    abs_z_te = np.linalg.norm(Xte, axis=1)
    real_te = Xte[:, 0]
    sign_im_te = np.sign(Xte[:, 1])

    Xtr_null = np.column_stack([abs_z_tr, real_tr, sign_im_tr])
    Xte_null = np.column_stack([abs_z_te, real_te, sign_im_te])

    Xtr_scaled = StandardScaler().fit_transform(Xtr_null)
    Xte_scaled = StandardScaler().fit_transform(Xte_null)

    clf = LogisticRegression(penalty='l2', C=1.0, max_iter=2000, solver='lbfgs',
                             random_state=SEED)
    clf.fit(Xtr_scaled, ytr)
    p = clf.predict_proba(Xte_scaled)[:, 1]
    auc = roc_auc_score(yte, p)
    return auc

def run():
    """Прогон всех задач."""
    print("Д10-тест: фаза vs декартова + тень (sign(Im))")
    print("="*60)

    results = {}

    # Все задачи
    all_tasks = ROTATIONAL_TASKS + CONTROL_TASKS

    rkf = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=SEED)

    for task in all_tasks:
        print(f"\n[{task}]")
        X, y = load_task(task, seed=SEED)

        fold_polar = []
        fold_null = []

        fold_id = 0
        for tr_idx, te_idx in rkf.split(X, y):
            Xtr, Xte = X[tr_idx], X[te_idx]
            ytr, yte = y[tr_idx], y[te_idx]

            auc_polar = fit_eval_polar(Xtr, Xte, ytr, yte)
            auc_null = fit_eval_null(Xtr, Xte, ytr, yte)

            fold_polar.append(auc_polar)
            fold_null.append(auc_null)

            fold_id += 1

        results[task] = {
            "polar": np.array(fold_polar),
            "null": np.array(fold_null),
        }

        mean_polar = np.mean(fold_polar)
        mean_null = np.mean(fold_null)
        delta_auc = mean_polar - mean_null

        print(f"  Polar (test) AUC: {mean_polar:.4f} ± {np.std(fold_polar):.4f}")
        print(f"  Null           : {mean_null:.4f} ± {np.std(fold_null):.4f}")
        print(f"  Δ AUC (test − null): {delta_auc:+.4f}")

    # Статистика
    print("\n" + "="*60)
    print("СТАТИСТИЧЕСКИЙ АНАЛИЗ")
    print("="*60)

    # Разделяем ротационные и контрольные
    rotational_deltas = []
    control_deltas = []

    for task in ROTATIONAL_TASKS:
        polar = results[task]["polar"]
        null = results[task]["null"]
        deltas = polar - null
        rotational_deltas.extend(deltas)

    for task in CONTROL_TASKS:
        polar = results[task]["polar"]
        null = results[task]["null"]
        deltas = polar - null
        control_deltas.extend(deltas)

    rotational_deltas = np.array(rotational_deltas)
    control_deltas = np.array(control_deltas)

    print(f"\nРОТАЦИОННЫЕ задачи ({len(ROTATIONAL_TASKS)} × 20 фолдов = {len(rotational_deltas)} пар):")
    print(f"  Медиана Δ AUC: {np.median(rotational_deltas):+.4f}")
    print(f"  Среднее:       {np.mean(rotational_deltas):+.4f} ± {np.std(rotational_deltas):.4f}")

    # Wilcoxon для ротационных
    if len(rotational_deltas) > 1:
        stat, pval = wilcoxon(rotational_deltas, alternative='greater')
        print(f"  Wilcoxon (test > null): statistic={stat:.1f}, p={pval:.6f}")
    else:
        print("  (недостаточно данных для Wilcoxon)")

    print(f"\nКОНТРОЛЬНЫЕ задачи ({len(CONTROL_TASKS)} × 20 фолдов = {len(control_deltas)} пар):")
    print(f"  Медиана Δ AUC: {np.median(control_deltas):+.4f}")
    print(f"  Среднее:       {np.mean(control_deltas):+.4f} ± {np.std(control_deltas):.4f}")

    if len(control_deltas) > 1:
        stat_ctrl, pval_ctrl = wilcoxon(control_deltas, alternative='greater')
        print(f"  Wilcoxon (test > null): statistic={stat_ctrl:.1f}, p={pval_ctrl:.6f}")
    else:
        print("  (недостаточно данных для Wilcoxon)")

    # Критерий PASS/FAIL
    print("\n" + "="*60)
    print("ВЕРДИКТ")
    print("="*60)

    med_rot = np.median(rotational_deltas)
    stat_rot, pval_rot = wilcoxon(rotational_deltas, alternative='greater') if len(rotational_deltas) > 1 else (0, 1)
    med_ctrl = np.median(control_deltas)
    stat_ctrl, pval_ctrl = wilcoxon(control_deltas, alternative='greater') if len(control_deltas) > 1 else (0, 1)

    # Проверка критериев
    rot_pass = (pval_rot < 0.01) and (med_rot > 0.03)
    ctrl_clean = pval_ctrl > 0.05  # На контрольных нет значимого эффекта

    print(f"\nКритерий PASS для H1:")
    print(f"  [1] test > null на РОТАЦИОННЫХ (p < 0.01): {pval_rot < 0.01} (p={pval_rot:.6f})")
    print(f"  [2] Δ AUC > +0.03 на РОТАЦИОННЫХ: {med_rot > 0.03} (медиана={med_rot:+.4f})")
    print(f"  [3] Контроль чист (p > 0.05 на гауссовых): {ctrl_clean} (p={pval_ctrl:.6f})")

    if rot_pass and ctrl_clean:
        verdict = "PASS (H1 подтверждена: фаза даёт роль на вращениях, не на гауссовых)"
    elif rot_pass and not ctrl_clean:
        verdict = "UNCLEAR (H1 частично; контроль не чист — не специфично для вращений)"
    else:
        verdict = "FAIL (H0: нет значимого преимущества test над null на ротационных)"

    print(f"\n{verdict}")

    # Сохранить результаты
    results_export = {}
    for task in all_tasks:
        results_export[task] = {
            "polar": results[task]["polar"].tolist(),
            "null": results[task]["null"].tolist(),
            "delta": (results[task]["polar"] - results[task]["null"]).tolist(),
        }

    results_export["summary"] = {
        "rotational": {
            "count": len(rotational_deltas),
            "median_delta": float(med_rot),
            "mean_delta": float(np.mean(rotational_deltas)),
            "std_delta": float(np.std(rotational_deltas)),
            "wilcoxon_p": float(pval_rot),
        },
        "control": {
            "count": len(control_deltas),
            "median_delta": float(med_ctrl),
            "mean_delta": float(np.mean(control_deltas)),
            "std_delta": float(np.std(control_deltas)),
            "wilcoxon_p": float(pval_ctrl),
        },
        "verdict": verdict,
    }

    json_path = os.path.join(HERE, "results.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results_export, f, indent=2, ensure_ascii=False)

    print(f"\nРезультаты сохранены: {json_path}")

    return verdict, results_export

if __name__ == "__main__":
    verdict, results = run()
    sys.exit(0)
