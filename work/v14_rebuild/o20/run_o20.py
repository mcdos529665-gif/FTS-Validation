# -*- coding: utf-8 -*-
"""
O_20 mini-project — прогон по протоколу PREREGISTRATION.md.
Три уровня кодирования отсутствия: T1 (impute&forget), T2 (flat flag ¬A),
T3 (per-column typed 0_A). Первичный контраст T3>T2. Детерминировано.
Запуск: python -X utf8 work/v14_rebuild/o20/run_o20.py
Выход:  work/v14_rebuild/o20/results.json  (+ печать сводки и вердикта)
"""
import warnings, json, os
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from sklearn.datasets import fetch_openml
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260613
PANEL = ["colic", "hepatitis", "vote", "cylinder-bands"]


def load(name):
    ds = fetch_openml(name, version=1, as_frame=True, parser="auto")
    X = ds.data.copy()
    y = LabelEncoder().fit_transform(ds.target.astype(str))
    return X, y


def split_cols(X):
    cat = [c for c in X.columns if str(X[c].dtype) in ("category", "object", "bool")]
    num = [c for c in X.columns if c not in cat]
    return num, cat


def base_matrix(Xtr, Xte, num, cat):
    """Импутированная база (одинаковая во всех T). Всё фитится на train."""
    blocks_tr, blocks_te = [], []
    if num:
        imp = SimpleImputer(strategy="median")
        blocks_tr.append(imp.fit_transform(Xtr[num]))
        blocks_te.append(imp.transform(Xte[num]))
    if cat:
        imp = SimpleImputer(strategy="most_frequent")
        a_tr = imp.fit_transform(Xtr[cat].astype(object))
        a_te = imp.transform(Xte[cat].astype(object))
        oh = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        blocks_tr.append(oh.fit_transform(a_tr))
        blocks_te.append(oh.transform(a_te))
    Xtr_b = np.hstack(blocks_tr) if blocks_tr else np.empty((len(Xtr), 0))
    Xte_b = np.hstack(blocks_te) if blocks_te else np.empty((len(Xte), 0))
    return Xtr_b, Xte_b


def indicators(Xtr, Xte, tier):
    """Блок индикаторов отсутствия из СЫРОЙ маски. T1: нет; T2: флаг; T3: по колонке."""
    Mtr, Mte = Xtr.isna(), Xte.isna()
    if tier == "T1":
        z = np.empty((len(Xtr), 0)), np.empty((len(Xte), 0))
        return z
    if tier == "T2":
        return (Mtr.any(axis=1).to_numpy().reshape(-1, 1).astype(float),
                Mte.any(axis=1).to_numpy().reshape(-1, 1).astype(float))
    # T3: только колонки, пропущенные в train (непостоянные на train)
    cols = [c for c in Xtr.columns if Mtr[c].any()]
    return (Mtr[cols].to_numpy().astype(float), Mte[cols].to_numpy().astype(float))


def fit_eval(Xtr_raw, Xte_raw, ytr, yte, num, cat, tier, model):
    Xtr_b, Xte_b = base_matrix(Xtr_raw, Xte_raw, num, cat)
    Itr, Ite = indicators(Xtr_raw, Xte_raw, tier)
    Xtr = np.hstack([Xtr_b, Itr]); Xte = np.hstack([Xte_b, Ite])
    if model == "logistic":
        sc = StandardScaler().fit(Xtr)
        Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)
        clf = LogisticRegression(penalty="l2", C=1.0, max_iter=2000, solver="lbfgs")
    else:  # secondary robustness
        clf = HistGradientBoostingClassifier(random_state=SEED)
    clf.fit(Xtr, ytr)
    p = clf.predict_proba(Xte)[:, 1]
    return roc_auc_score(yte, p)


def run(model="logistic"):
    rkf = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=SEED)
    per_ds = {}
    for name in PANEL:
        X, y = load(name)
        num, cat = split_cols(X)
        fold = {"T1": [], "T2": [], "T3": []}
        for tr, te in rkf.split(X, y):
            Xtr, Xte = X.iloc[tr], X.iloc[te]
            ytr, yte = y[tr], y[te]
            for tier in ("T1", "T2", "T3"):
                fold[tier].append(fit_eval(Xtr, Xte, ytr, yte, num, cat, tier, model))
        per_ds[name] = {t: np.array(v) for t, v in fold.items()}
    return per_ds


def summarize(per_ds, label):
    print(f"\n===== {label} =====")
    d32_all, d21_all = [], []
    wins32 = 0
    rows = []
    for name, f in per_ds.items():
        a1, a2, a3 = f["T1"].mean(), f["T2"].mean(), f["T3"].mean()
        d32 = f["T3"] - f["T2"]; d21 = f["T2"] - f["T1"]
        d32_all += list(d32); d21_all += list(d21)
        win = a3 > a2
        wins32 += int(win)
        rows.append((name, a1, a2, a3, d32.mean(), d21.mean(), win))
        print(f"{name:14s} T1={a1:.4f} T2={a2:.4f} T3={a3:.4f} "
              f"ΔT3-T2={d32.mean():+.4f} ΔT2-T1={d21.mean():+.4f} {'T3>T2' if win else 'T3<=T2'}")
    d32_all = np.array(d32_all)
    # Wilcoxon по 80 парам (T3 vs T2)
    try:
        w_stat, w_p = wilcoxon(d32_all, alternative="greater")
    except ValueError:
        w_stat, w_p = float("nan"), float("nan")
    med = float(np.median(d32_all)); mean = float(d32_all.mean())
    print(f"--- pooled ΔT3-T2: mean={mean:+.4f} median={med:+.4f} "
          f"Wilcoxon(greater) p={w_p:.4g}; datasets T3>T2: {wins32}/4")
    return dict(rows=[(r[0], *[float(x) for x in r[1:6]], bool(r[6])) for r in rows],
                pooled_mean=mean, pooled_median=med, wilcoxon_p=float(w_p),
                wins32=wins32, n_pairs=int(len(d32_all)))


def verdict(prim):
    maj = prim["wins32"] >= 3
    sig = (prim["wilcoxon_p"] < 0.05)
    supported = maj and sig
    practical = abs(prim["pooled_median"]) >= 0.005
    print("\n========== ВЕРДИКТ (по зафиксированному правилу) ==========")
    print(f"T3>T2 на {prim['wins32']}/4 датасетах (нужно ≥3): {maj}")
    print(f"pooled Wilcoxon p={prim['wilcoxon_p']:.4g} (нужно <0.05): {sig}")
    if supported and practical:
        v = "O_20 ПОДТВЕРЖДЁН на этом тесте (T3>T2, эффект практически значим)"
    elif supported and not practical:
        v = "O_20 формально подтверждён, но эффект практически НИЧТОЖЕН (median ΔAUC<0.005)"
    else:
        v = "O_20 НЕ ПОДТВЕРЖДЁН на этом тесте (типизация не бьёт плоский флаг)"
    print(v)
    return dict(majority=maj, significant=sig, practical=practical,
                supported=bool(supported), verdict=v)


if __name__ == "__main__":
    prim = summarize(run("logistic"), "PRIMARY: logistic regression")
    sec = summarize(run("histgb"), "SECONDARY (robustness): HistGradientBoosting")
    vrd = verdict(prim)
    out = dict(seed=SEED, panel=PANEL, primary=prim, secondary=sec, verdict=vrd)
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"\nsaved: {os.path.join(HERE, 'results.json')}")
