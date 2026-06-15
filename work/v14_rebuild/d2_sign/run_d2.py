# -*- coding: utf-8 -*-
"""
D2 sign-retrieval test — прогон по PREREGISTRATION.md. Детерминирован.
T1 forget |x| / T2 flat ¬A flag / T3 «Половина_А» (flag + |x|·context) / ORACLE signed x.
Запуск: python -X utf8 work/v14_rebuild/d2_sign/run_d2.py
Выход:  results.json + печать сводки и вердикта.
"""
import warnings, json, os
warnings.filterwarnings("ignore")
import numpy as np
from scipy.stats import wilcoxon
from sklearn.datasets import load_breast_cancer, fetch_openml
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260615
K_CTX = 6      # cap: context features per ambiguous feature in T3 interactions
P_LOST = 0.5   # fraction of rows with sign lost, per ambiguous feature


def get_datasets():
    out = []
    d = load_breast_cancer()
    out.append(("breast_cancer", np.asarray(d.data, float), np.asarray(d.target, int)))
    for name in ["ionosphere", "sonar", "diabetes"]:
        try:
            ds = fetch_openml(name, version=1, as_frame=True, parser="auto")
            X = ds.data.select_dtypes(include=[np.number]).to_numpy(float)
            keep = ~np.isnan(X).any(axis=0)
            X = X[:, keep]
            y = LabelEncoder().fit_transform(ds.target.astype(str))
            if X.shape[1] >= 4 and len(set(y)) == 2:
                out.append((name, X, y))
            else:
                print("skip", name, "- not binary/too few numeric cols")
        except Exception as e:
            print("skip", name, "-", repr(e)[:80])
    return out


def build_encodings(X, rng):
    n, d = X.shape
    Z = StandardScaler().fit_transform(X)              # signed
    amb = list(range(d // 2))                            # ambiguous features
    ctx = [j for j in range(d) if j not in amb]          # clean context
    lost = np.zeros((n, len(amb)), bool)
    for k in range(len(amb)):
        lost[:, k] = rng.random(n) < P_LOST
    obs = Z.copy()
    for k, j in enumerate(amb):
        obs[lost[:, k], j] = np.abs(Z[lost[:, k], j])    # lose sign -> |z|
    flag = lost.astype(float)
    ctx_used = ctx[:K_CTX]
    inter = []
    for j in amb:
        for c in ctx_used:
            inter.append((np.abs(obs[:, j]) * Z[:, c]).reshape(-1, 1))   # |x|·context
    T2 = np.hstack([obs, flag])
    T3 = np.hstack([obs, flag] + inter) if inter else T2
    return {"ORACLE": Z, "T1": obs, "T2": T2, "T3": T3}


def models():
    return {
        "logreg": lambda: LogisticRegression(max_iter=2000, C=1.0),
        "histgb": lambda: HistGradientBoostingClassifier(random_state=SEED),
    }


def run():
    data = get_datasets()
    rec = {}
    for i, (dname, X, y) in enumerate(data):
        enc = build_encodings(X, np.random.default_rng(SEED + i))
        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=SEED)
        splits = list(cv.split(enc["T2"], y))
        for mname, mk in models().items():
            for ename, M in enc.items():
                aucs = []
                for tr, te in splits:
                    Xt, Xe = M[tr], M[te]
                    if mname == "logreg":
                        sc = StandardScaler().fit(Xt)
                        Xt, Xe = sc.transform(Xt), sc.transform(Xe)
                    clf = mk().fit(Xt, y[tr])
                    aucs.append(roc_auc_score(y[te], clf.predict_proba(Xe)[:, 1]))
                rec[(dname, mname, ename)] = aucs

    names = [d for d, _, _ in data]
    per_ds = {}
    summary = {}
    for mname in models():
        cat = lambda e: np.concatenate([rec[(d, mname, e)] for d in names])
        t1, t2, t3, orc = cat("T1"), cat("T2"), cat("T3"), cat("ORACLE")
        diff = t3 - t2
        try:
            p = float(wilcoxon(t3, t2, alternative="greater").pvalue)
        except Exception:
            p = float("nan")
        summary[mname] = {
            "median_T1": float(np.median(t1)), "median_T2": float(np.median(t2)),
            "median_T3": float(np.median(t3)), "median_ORACLE": float(np.median(orc)),
            "median_T3_minus_T2": float(np.median(diff)),
            "winrate_T3_gt_T2": float(np.mean(diff > 0)),
            "p_T3_gt_T2_wilcoxon": p,
            "median_ORACLE_minus_T2": float(np.median(orc - t2)),
            "median_T2_minus_T1": float(np.median(t2 - t1)),
            "n_folds": int(len(diff)),
        }
        per_ds[mname] = {d: float(np.median(np.array(rec[(d, mname, "T3")]) -
                                            np.array(rec[(d, mname, "T2")]))) for d in names}
    return names, summary, per_ds


def verdict(summary):
    hg = summary["histgb"]; lg = summary["logreg"]
    hg_sig = hg["p_T3_gt_T2_wilcoxon"] < 0.05 and hg["median_T3_minus_T2"] > 0
    lg_sig = lg["p_T3_gt_T2_wilcoxon"] < 0.05 and lg["median_T3_minus_T2"] > 0
    room = max(hg["median_ORACLE_minus_T2"], lg["median_ORACLE_minus_T2"])
    if room < 0.01:
        return "PLATFORM WEAK (ORACLE≈T2: знак почти не предиктивен) — тест неинформативен"
    if hg_sig:
        return "CONFIRMED — T3>T2 значимо для HistGB (внешняя кодировочная роль есть)"
    if lg_sig:
        return "WEAK — T3>T2 только для LogReg (приём для слабых моделей, не глубокая роль)"
    return "NOT CONFIRMED — T3≈T2 (обе модели): внешней кодировочной роли НЕТ"


if __name__ == "__main__":
    names, summary, per_ds = run()
    v = verdict(summary)
    print("\n=== D2 sign-retrieval ===  datasets:", names, " SEED:", SEED)
    for m in summary:
        s = summary[m]
        print(f"\n[{m}] folds={s['n_folds']}")
        print(f"  AUC med: T1={s['median_T1']:.3f}  T2={s['median_T2']:.3f}  "
              f"T3={s['median_T3']:.3f}  ORACLE={s['median_ORACLE']:.3f}")
        print(f"  T3-T2 med={s['median_T3_minus_T2']:+.4f}  winrate={s['winrate_T3_gt_T2']:.2f}  "
              f"Wilcoxon p(T3>T2)={s['p_T3_gt_T2_wilcoxon']:.4f}")
        print(f"  platform: ORACLE-T2={s['median_ORACLE_minus_T2']:+.4f}  T2-T1={s['median_T2_minus_T1']:+.4f}")
        print(f"  per-dataset T3-T2: " + ", ".join(f"{d}={per_ds[m][d]:+.4f}" for d in names))
    print("\nВЕРДИКТ:", v)
    out = {"seed": SEED, "datasets": names, "summary": summary,
           "per_dataset_T3_minus_T2": per_ds, "verdict": v}
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\nresults.json written")
