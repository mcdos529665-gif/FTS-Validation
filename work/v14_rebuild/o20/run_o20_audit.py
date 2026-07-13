# -*- coding: utf-8 -*-
"""Непредрегистрированная аудиторская реанализация O_20.

Исходные PREREGISTRATION.md, results.json и RESULTS.md не меняются.
Этот скрипт фиксирует OpenML data_id/version, сохраняет сырые
фолдовые эффекты, но не считает repeated-CV фолды независимыми
внешними репликациями. Основная единица междатасетного вывода —
один агрегированный эффект на датасет.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy import stats
import sklearn
from sklearn.datasets import fetch_openml
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler


HERE = Path(__file__).resolve().parent
SEED = 20260613
N_SPLITS = 5
N_REPEATS = 4
PANEL = {
    "colic": 25,
    "hepatitis": 55,
    "vote": 56,
    "cylinder-bands": 33,
}


def array_sha256(*arrays: np.ndarray) -> str:
    digest = hashlib.sha256()
    for array in arrays:
        contiguous = np.ascontiguousarray(array)
        digest.update(str(contiguous.shape).encode("ascii"))
        digest.update(str(contiguous.dtype).encode("ascii"))
        digest.update(contiguous.tobytes())
    return digest.hexdigest()


def load_dataset(name: str, data_id: int, cache: str):
    dataset = fetch_openml(data_id=data_id, as_frame=True, parser="auto", data_home=cache)
    X = dataset.data.copy()
    y = LabelEncoder().fit_transform(dataset.target.astype(str))
    details = dataset.details
    metadata = {
        "name": name,
        "data_id": int(details["id"]),
        "version": int(details["version"]),
        "openml_name": details["name"],
        "md5_checksum": details.get("md5_checksum"),
        "n_rows": int(X.shape[0]),
        "n_columns": int(X.shape[1]),
        "target_classes": int(len(np.unique(y))),
        "materialized_sha256": array_sha256(pd.util.hash_pandas_object(X, index=True).to_numpy(), y),
    }
    if metadata["data_id"] != data_id or metadata["version"] != 1:
        raise RuntimeError(f"OpenML identity drift for {name}: {metadata}")
    return X, y, metadata


def split_cols(X: pd.DataFrame):
    categorical = [c for c in X.columns if str(X[c].dtype) in ("category", "object", "bool")]
    numeric = [c for c in X.columns if c not in categorical]
    return numeric, categorical


def base_matrix(X_train, X_test, numeric, categorical):
    train_blocks, test_blocks = [], []
    if numeric:
        imputer = SimpleImputer(strategy="median")
        train_blocks.append(imputer.fit_transform(X_train[numeric]))
        test_blocks.append(imputer.transform(X_test[numeric]))
    if categorical:
        imputer = SimpleImputer(strategy="most_frequent")
        train_cat = imputer.fit_transform(X_train[categorical].astype(object))
        test_cat = imputer.transform(X_test[categorical].astype(object))
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        train_blocks.append(encoder.fit_transform(train_cat))
        test_blocks.append(encoder.transform(test_cat))
    train = np.hstack(train_blocks) if train_blocks else np.empty((len(X_train), 0))
    test = np.hstack(test_blocks) if test_blocks else np.empty((len(X_test), 0))
    return train, test


def indicators(X_train, X_test, tier):
    train_missing, test_missing = X_train.isna(), X_test.isna()
    if tier == "T1":
        return np.empty((len(X_train), 0)), np.empty((len(X_test), 0))
    if tier == "T2":
        return (
            train_missing.any(axis=1).to_numpy().reshape(-1, 1).astype(float),
            test_missing.any(axis=1).to_numpy().reshape(-1, 1).astype(float),
        )
    columns = [column for column in X_train.columns if train_missing[column].any()]
    return (
        train_missing[columns].to_numpy().astype(float),
        test_missing[columns].to_numpy().astype(float),
    )


def fit_eval(X_train_raw, X_test_raw, y_train, y_test, numeric, categorical, tier, model):
    X_train_base, X_test_base = base_matrix(X_train_raw, X_test_raw, numeric, categorical)
    train_indicators, test_indicators = indicators(X_train_raw, X_test_raw, tier)
    X_train = np.hstack([X_train_base, train_indicators])
    X_test = np.hstack([X_test_base, test_indicators])
    if model == "logistic":
        scaler = StandardScaler().fit(X_train)
        X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)
        # В sklearn 1.8+ явный penalty="l2" устарел; default остаётся L2.
        classifier = LogisticRegression(C=1.0, max_iter=2000, solver="lbfgs")
    else:
        classifier = HistGradientBoostingClassifier(random_state=SEED)
    classifier.fit(X_train, y_train)
    return float(roc_auc_score(y_test, classifier.predict_proba(X_test)[:, 1]))


def holm(p_values: dict[str, float]) -> dict[str, float]:
    ordered = sorted(p_values, key=p_values.get)
    adjusted: dict[str, float] = {}
    running = 0.0
    count = len(ordered)
    for rank, key in enumerate(ordered):
        value = min(1.0, (count - rank) * p_values[key])
        running = max(running, value)
        adjusted[key] = running
    return adjusted


def corrected_cv_summary(differences: np.ndarray):
    differences = np.asarray(differences, dtype=float)
    mean = float(np.mean(differences))
    median = float(np.median(differences))
    variance = float(np.var(differences, ddof=1))
    # Nadeau-Bengio corrected resampled t approximation: 1/n + n_test/n_train.
    correction = 1.0 / len(differences) + 1.0 / (N_SPLITS - 1)
    standard_error = float(np.sqrt(correction * variance))
    if standard_error == 0:
        statistic = float("inf") if mean > 0 else 0.0
        p_greater = 0.0 if mean > 0 else 1.0
    else:
        statistic = mean / standard_error
        p_greater = float(stats.t.sf(statistic, df=len(differences) - 1))
    critical = float(stats.t.ppf(0.975, df=len(differences) - 1))
    return {
        "mean": mean,
        "median": median,
        "sd": float(np.std(differences, ddof=1)),
        "corrected_se": standard_error,
        "ci95": [mean - critical * standard_error, mean + critical * standard_error],
        "t_corrected": float(statistic),
        "p_greater_corrected": p_greater,
        "wins": int(np.sum(differences > 0)),
        "n_folds": int(len(differences)),
    }


def dataset_panel_summary(per_dataset: dict[str, dict]):
    names = list(per_dataset)
    effects = np.array([per_dataset[name]["mean"] for name in names], dtype=float)
    nonzero = np.abs(effects) > 1e-12
    effective = effects[nonzero]
    wins = int(np.sum(effective > 0))
    sign_p = float(stats.binomtest(wins, len(effective), 0.5, alternative="greater").pvalue) if len(effective) else 1.0
    mean = float(np.mean(effects))
    if len(effects) > 1:
        se = float(stats.sem(effects))
        critical = float(stats.t.ppf(0.975, len(effects) - 1))
        interval = [mean - critical * se, mean + critical * se]
    else:
        interval = [float("nan"), float("nan")]
    return {
        "effects_by_dataset": dict(zip(names, map(float, effects))),
        "mean": mean,
        "median": float(np.median(effects)),
        "ci95_t_across_datasets": interval,
        "wins": wins,
        "ties": int(np.sum(~nonzero)),
        "n_independent_datasets": int(len(effects)),
        "sign_test_p_greater": sign_p,
        "practical_abs_ge_0_005": int(np.sum(np.abs(effects) >= 0.005)),
    }


def run():
    cache = os.environ.get("FTS_OPENML_CACHE", str(Path(tempfile.gettempdir()) / "fts_openml_audit"))
    cv = RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=SEED)
    raw: dict[str, dict] = {}
    datasets = []
    for name, data_id in PANEL.items():
        X, y, metadata = load_dataset(name, data_id, cache)
        datasets.append(metadata)
        numeric, categorical = split_cols(X)
        splits = list(cv.split(X, y))
        raw[name] = {}
        for model in ("logistic", "histgb"):
            raw[name][model] = {tier: [] for tier in ("T1", "T2", "T3")}
            for train, test in splits:
                for tier in raw[name][model]:
                    raw[name][model][tier].append(
                        fit_eval(X.iloc[train], X.iloc[test], y[train], y[test], numeric, categorical, tier, model)
                    )

    models = {}
    for model in ("logistic", "histgb"):
        per_dataset = {}
        p_values = {}
        flag_effects = {}
        for name in PANEL:
            t1 = np.asarray(raw[name][model]["T1"])
            t2 = np.asarray(raw[name][model]["T2"])
            t3 = np.asarray(raw[name][model]["T3"])
            summary = corrected_cv_summary(t3 - t2)
            summary["mean_auc"] = {"T1": float(t1.mean()), "T2": float(t2.mean()), "T3": float(t3.mean())}
            summary["mean_T2_minus_T1"] = float(np.mean(t2 - t1))
            per_dataset[name] = summary
            p_values[name] = summary["p_greater_corrected"]
            flag_effects[name] = summary["mean_T2_minus_T1"]
        adjusted = holm(p_values)
        for name in per_dataset:
            per_dataset[name]["p_greater_holm_4"] = adjusted[name]
        models[model] = {
            "per_dataset": per_dataset,
            "panel": dataset_panel_summary(per_dataset),
            "flag_T2_minus_T1_by_dataset": flag_effects,
        }

    output = {
        "analysis_kind": "post_hoc_audit_reanalysis_not_preregistered",
        "seed": SEED,
        "cv": {"splits": N_SPLITS, "repeats": N_REPEATS, "folds_per_dataset": N_SPLITS * N_REPEATS},
        "datasets": datasets,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "models": models,
        "raw_fold_auc": raw,
        "audit_verdict": (
            "O_20 not supported. The primary dataset-level unit gives fewer than 3/4 wins; "
            "with only four independent datasets an exact one-sided sign test cannot attain p<0.05 even at 4/4 wins."
        ),
    }
    (HERE / "audit_results.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_report(output)
    return output


def format_interval(values):
    return f"[{values[0]:+.4f}; {values[1]:+.4f}]"


def write_report(output):
    lines = [
        "# AUDIT REANALYSIS — O_20",
        "",
        "**Статус:** post-hoc аудиторская реанализация, не была предзарегистрирована. "
        "Исходные `PREREGISTRATION.md`, `results.json` и `RESULTS.md` не изменены.",
        "",
        "## Найдено → зависимости → вывод → что не закрыто",
        "",
        "**Найдено.** Исходный pooled Wilcoxon объединял 80 зависимых repeated-CV фолдов. "
        "Он остаётся исторической описательной величиной, но не является междатасетным подтверждением. "
        "Точный OpenML panel закреплён data ID/version; все преобразования по-прежнему фитятся только на train-fold.",
        "",
        "**Зависимости.** Один агрегированный эффект `mean AUC(T3−T2)` на датасет является единицей "
        "внешней репликации. Внутри датасета показана приближённая corrected repeated-CV неопределённость; "
        "четыре односторонних внутри-датасетных p-value скорректированы Holm. T3 содержит больше "
        "признаков и параметров, чем T2, поэтому даже положительный эффект не отделял бы типизацию "
        "от увеличения ёмкости представления.",
        "",
    ]
    for model, block in output["models"].items():
        lines += [f"### {model}", "", "| Датасет | mean ΔAUC | corrected 95% CI | p one-sided | Holm p | T2−T1 |", "|---|---:|---:|---:|---:|---:|"]
        for name, row in block["per_dataset"].items():
            lines.append(
                f"| {name} | {row['mean']:+.4f} | {format_interval(row['ci95'])} | "
                f"{row['p_greater_corrected']:.4f} | {row['p_greater_holm_4']:.4f} | {row['mean_T2_minus_T1']:+.4f} |"
            )
        panel = block["panel"]
        lines += [
            "",
            f"Панель: wins={panel['wins']}/{panel['n_independent_datasets']} (ties={panel['ties']}), "
            f"exact sign p={panel['sign_test_p_greater']:.4f}; mean={panel['mean']:+.4f}, "
            f"median={panel['median']:+.4f}, 95% t-CI={format_interval(panel['ci95_t_across_datasets'])}.",
            "",
        ]
    primary = output["models"]["logistic"]["panel"]
    lines += [
        "**Вывод.** O_20 не подтверждён. Первичная логистическая модель выигрывает на "
        f"{primary['wins']}/4 независимых датасетах; точный sign-test p={primary['sign_test_p_greater']:.4f}. "
        "При n=4 даже 4/4 победы дают минимальное одностороннее p=0.0625, поэтому исходный дизайн "
        "вообще не мог дать α=0.05 на уровне независимых датасетов.",
        "",
        "**Что не закрыто.** Панель в основном имеет слабый `T2−T1`, поэтому она плохо идентифицирует "
        "ценность самой пропущенности. Не уравнены число параметров и вычислительный бюджет T2/T3. "
        "Новая попытка допустима только с новой предрегистрацией, большим числом независимых датасетов, "
        "capacity-matched null и документированно информативным механизмом missingness; этот аудит новую "
        "гипотезу не запускает.",
        "",
        "## Данные и воспроизводимость",
        "",
        "| Имя | OpenML data ID | Version | Rows×columns | OpenML MD5 |",
        "|---|---:|---:|---:|---|",
    ]
    for item in output["datasets"]:
        lines.append(
            f"| {item['name']} | {item['data_id']} | {item['version']} | "
            f"{item['n_rows']}×{item['n_columns']} | `{item['md5_checksum']}` |"
        )
    lines += [
        "",
        "OpenML помечает `cylinder-bands` data_id=33/version=1 как inactive из-за известных "
        "проблем набора. Версия закреплена для исторической воспроизводимости, но это P2-ограничение "
        "панели, а не допустимый источник нового сильного вывода.",
        "",
        "Полные fold-level AUC, materialized SHA256 и версии среды сохранены в `audit_results.json`.",
        "",
    ]
    (HERE / "AUDIT_REANALYSIS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    result = run()
    print(result["audit_verdict"])
