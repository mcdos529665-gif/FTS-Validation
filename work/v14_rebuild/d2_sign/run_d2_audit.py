# -*- coding: utf-8 -*-
"""Непредрегистрированная аудиторская реанализация D2.

Исправляет методологический дефект исходного run_d2.py: исходная
стандартизация выполнялась на всём датасете до CV. Здесь импутация,
масштабирование, потеря знака и взаимодействия T3 строятся из train-fold.
Исходные PREREGISTRATION.md/results.json/RESULTS.md не меняются.
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
from sklearn.datasets import fetch_openml, load_breast_cancer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler


HERE = Path(__file__).resolve().parent
SEED = 20260615
N_SPLITS = 5
N_REPEATS = 4
P_LOST = 0.5
K_CTX = 6
OPENML = {"ionosphere": 59, "sonar": 40, "diabetes": 37}


def array_sha256(*arrays: np.ndarray) -> str:
    digest = hashlib.sha256()
    for array in arrays:
        contiguous = np.ascontiguousarray(array)
        digest.update(str(contiguous.shape).encode("ascii"))
        digest.update(str(contiguous.dtype).encode("ascii"))
        digest.update(contiguous.tobytes())
    return digest.hexdigest()


def get_datasets(cache: str):
    output = []
    builtin = load_breast_cancer()
    X_builtin = np.asarray(builtin.data, float)
    y_builtin = np.asarray(builtin.target, int)
    output.append((
        "breast_cancer",
        X_builtin,
        y_builtin,
        {
            "name": "breast_cancer",
            "source": "sklearn_builtin_load_breast_cancer",
            "data_id": None,
            "version": sklearn.__version__,
            "n_rows": int(X_builtin.shape[0]),
            "n_columns": int(X_builtin.shape[1]),
            "materialized_sha256": array_sha256(X_builtin, y_builtin),
        },
    ))
    for name, data_id in OPENML.items():
        dataset = fetch_openml(data_id=data_id, as_frame=True, parser="auto", data_home=cache)
        numeric = dataset.data.select_dtypes(include=[np.number])
        X = numeric.to_numpy(float)
        y = LabelEncoder().fit_transform(dataset.target.astype(str))
        details = dataset.details
        metadata = {
            "name": name,
            "source": "OpenML",
            "data_id": int(details["id"]),
            "version": int(details["version"]),
            "openml_name": details["name"],
            "md5_checksum": details.get("md5_checksum"),
            "n_rows": int(X.shape[0]),
            "n_columns": int(X.shape[1]),
            "materialized_sha256": array_sha256(X, y),
        }
        if metadata["data_id"] != data_id or metadata["version"] != 1:
            raise RuntimeError(f"OpenML identity drift for {name}: {metadata}")
        if X.shape[1] < 4 or len(np.unique(y)) != 2:
            raise RuntimeError(f"Invalid D2 dataset {name}: shape={X.shape}, classes={np.unique(y)}")
        output.append((name, X, y, metadata))
    return output


def deterministic_loss_mask(n_rows: int, n_ambiguous: int, seed: int):
    rng = np.random.default_rng(seed)
    return rng.random((n_rows, n_ambiguous)) < P_LOST


def fold_encodings(X_train_raw, X_test_raw, lost_train, lost_test):
    imputer = SimpleImputer(strategy="median")
    X_train_imputed = imputer.fit_transform(X_train_raw)
    X_test_imputed = imputer.transform(X_test_raw)

    raw_scaler = StandardScaler().fit(X_train_imputed)
    Z_train = raw_scaler.transform(X_train_imputed)
    Z_test = raw_scaler.transform(X_test_imputed)
    dimension = Z_train.shape[1]
    ambiguous = list(range(dimension // 2))
    context = list(range(dimension // 2, dimension))
    context_used = context[:K_CTX]

    obs_train, obs_test = Z_train.copy(), Z_test.copy()
    for index, feature in enumerate(ambiguous):
        obs_train[lost_train[:, index], feature] = np.abs(Z_train[lost_train[:, index], feature])
        obs_test[lost_test[:, index], feature] = np.abs(Z_test[lost_test[:, index], feature])

    flag_train, flag_test = lost_train.astype(float), lost_test.astype(float)
    interactions_train, interactions_test = [], []
    for feature in ambiguous:
        for context_feature in context_used:
            interactions_train.append((np.abs(obs_train[:, feature]) * Z_train[:, context_feature]).reshape(-1, 1))
            interactions_test.append((np.abs(obs_test[:, feature]) * Z_test[:, context_feature]).reshape(-1, 1))

    T2_train = np.hstack([obs_train, flag_train])
    T2_test = np.hstack([obs_test, flag_test])
    if interactions_train:
        T3_train = np.hstack([obs_train, flag_train] + interactions_train)
        T3_test = np.hstack([obs_test, flag_test] + interactions_test)
    else:
        T3_train, T3_test = T2_train, T2_test
    return {
        "ORACLE": (Z_train, Z_test),
        "T1": (obs_train, obs_test),
        "T2": (T2_train, T2_test),
        "T3": (T3_train, T3_test),
    }


def corrected_cv_summary(differences: np.ndarray):
    differences = np.asarray(differences, dtype=float)
    mean = float(np.mean(differences))
    variance = float(np.var(differences, ddof=1))
    correction = 1.0 / len(differences) + 1.0 / (N_SPLITS - 1)
    standard_error = float(np.sqrt(correction * variance))
    statistic = mean / standard_error if standard_error else (float("inf") if mean > 0 else 0.0)
    p_greater = float(stats.t.sf(statistic, df=len(differences) - 1)) if standard_error else (0.0 if mean > 0 else 1.0)
    critical = float(stats.t.ppf(0.975, df=len(differences) - 1))
    return {
        "mean": mean,
        "median": float(np.median(differences)),
        "sd": float(np.std(differences, ddof=1)),
        "corrected_se": standard_error,
        "ci95": [mean - critical * standard_error, mean + critical * standard_error],
        "t_corrected": float(statistic),
        "p_greater_corrected": p_greater,
        "wins": int(np.sum(differences > 0)),
        "n_folds": int(len(differences)),
    }


def holm(p_values: dict[str, float]):
    ordered = sorted(p_values, key=p_values.get)
    result, running = {}, 0.0
    for rank, key in enumerate(ordered):
        running = max(running, min(1.0, (len(ordered) - rank) * p_values[key]))
        result[key] = running
    return result


def dataset_panel_summary(per_dataset):
    names = list(per_dataset)
    effects = np.array([per_dataset[name]["mean"] for name in names], dtype=float)
    nonzero = np.abs(effects) > 1e-12
    effective = effects[nonzero]
    wins = int(np.sum(effective > 0))
    p_value = float(stats.binomtest(wins, len(effective), 0.5, alternative="greater").pvalue) if len(effective) else 1.0
    mean = float(np.mean(effects))
    se = float(stats.sem(effects))
    critical = float(stats.t.ppf(0.975, len(effects) - 1))
    return {
        "effects_by_dataset": dict(zip(names, map(float, effects))),
        "mean": mean,
        "median": float(np.median(effects)),
        "ci95_t_across_datasets": [mean - critical * se, mean + critical * se],
        "wins": wins,
        "ties": int(np.sum(~nonzero)),
        "n_independent_datasets": int(len(effects)),
        "sign_test_p_greater": p_value,
    }


def run():
    cache = os.environ.get("FTS_OPENML_CACHE", str(Path(tempfile.gettempdir()) / "fts_openml_audit"))
    datasets = get_datasets(cache)
    raw = {}
    metadata = []
    for index, (name, X, y, details) in enumerate(datasets):
        metadata.append(details)
        n_ambiguous = X.shape[1] // 2
        lost = deterministic_loss_mask(len(X), n_ambiguous, SEED + index)
        cv = RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=SEED)
        raw[name] = {model: {tier: [] for tier in ("T1", "T2", "T3", "ORACLE")} for model in ("logreg", "histgb")}
        for train, test in cv.split(X, y):
            encodings = fold_encodings(X[train], X[test], lost[train], lost[test])
            for model in raw[name]:
                for tier, (X_train, X_test) in encodings.items():
                    if model == "logreg":
                        feature_scaler = StandardScaler().fit(X_train)
                        X_train_model = feature_scaler.transform(X_train)
                        X_test_model = feature_scaler.transform(X_test)
                        classifier = LogisticRegression(max_iter=2000, C=1.0)
                    else:
                        X_train_model, X_test_model = X_train, X_test
                        classifier = HistGradientBoostingClassifier(random_state=SEED)
                    classifier.fit(X_train_model, y[train])
                    raw[name][model][tier].append(float(roc_auc_score(y[test], classifier.predict_proba(X_test_model)[:, 1])))

    models = {}
    for model in ("histgb", "logreg"):
        per_dataset, p_values = {}, {}
        for name, *_rest in datasets:
            t1 = np.asarray(raw[name][model]["T1"])
            t2 = np.asarray(raw[name][model]["T2"])
            t3 = np.asarray(raw[name][model]["T3"])
            oracle = np.asarray(raw[name][model]["ORACLE"])
            row = corrected_cv_summary(t3 - t2)
            row["mean_auc"] = {"T1": float(t1.mean()), "T2": float(t2.mean()), "T3": float(t3.mean()), "ORACLE": float(oracle.mean())}
            row["mean_T2_minus_T1"] = float(np.mean(t2 - t1))
            row["mean_ORACLE_minus_T2"] = float(np.mean(oracle - t2))
            per_dataset[name] = row
            p_values[name] = row["p_greater_corrected"]
        adjusted = holm(p_values)
        for name in per_dataset:
            per_dataset[name]["p_greater_holm_4"] = adjusted[name]
        models[model] = {"per_dataset": per_dataset, "panel": dataset_panel_summary(per_dataset)}

    output = {
        "analysis_kind": "post_hoc_audit_reanalysis_not_preregistered",
        "method_change": "all imputation, scaling and interaction construction fitted inside train-fold",
        "seed": SEED,
        "cv": {"splits": N_SPLITS, "repeats": N_REPEATS, "folds_per_dataset": N_SPLITS * N_REPEATS},
        "datasets": metadata,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "models": models,
        "raw_fold_auc": raw,
        "audit_verdict": "D2 strong claim not confirmed; HistGB is primary and no independent-dataset inference supports T3>T2.",
    }
    (HERE / "audit_results.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_report(output)
    return output


def interval(values):
    return f"[{values[0]:+.4f}; {values[1]:+.4f}]"


def write_report(output):
    lines = [
        "# AUDIT REANALYSIS — D2 sign-retrieval",
        "",
        "**Статус:** post-hoc аудиторская реанализация, не была предзарегистрирована. "
        "Исторические `PREREGISTRATION.md`, `results.json` и `RESULTS.md` сохранены без изменений.",
        "",
        "## Найдено → зависимости → вывод → что не закрыто",
        "",
        "**Найдено.** В исходном `run_d2.py` первый `StandardScaler().fit_transform(X)` "
        "использовал весь датасет до разбиения CV. Это P1-методологический дефект: параметры test-fold "
        "попадали в построение ORACLE/T1/T2/T3. Кроме того, 80 repeated-CV фолдов были объединены "
        "как независимые наблюдения для Wilcoxon.",
        "",
        "**Зависимости.** В исправленном прогоне импутация, исходное масштабирование, потеря знака и "
        "взаимодействия T3 строятся после split с fit только на train-fold. Внутри датасета показана "
        "corrected repeated-CV неопределённость, четыре p-value скорректированы Holm. Между датасетами "
        "используется один mean ΔAUC на датасет и точный sign test. Индексы неоднозначных и контекстных "
        "признаков фиксированы правилом до fit; T3 всё же имеет больше признаков и параметров, чем T2.",
        "",
    ]
    for model, block in output["models"].items():
        label = "HistGB — первичный" if model == "histgb" else "LogReg — вторичный"
        lines += [f"### {label}", "", "| Датасет | mean ΔAUC T3−T2 | corrected 95% CI | p one-sided | Holm p | ORACLE−T2 | T2−T1 |", "|---|---:|---:|---:|---:|---:|---:|"]
        for name, row in block["per_dataset"].items():
            lines.append(
                f"| {name} | {row['mean']:+.4f} | {interval(row['ci95'])} | {row['p_greater_corrected']:.4f} | "
                f"{row['p_greater_holm_4']:.4f} | {row['mean_ORACLE_minus_T2']:+.4f} | {row['mean_T2_minus_T1']:+.4f} |"
            )
        panel = block["panel"]
        lines += [
            "",
            f"Панель: wins={panel['wins']}/{panel['n_independent_datasets']} (ties={panel['ties']}), "
            f"exact sign p={panel['sign_test_p_greater']:.4f}; mean={panel['mean']:+.4f}, "
            f"median={panel['median']:+.4f}, 95% t-CI={interval(panel['ci95_t_across_datasets'])}.",
            "",
        ]
    primary = output["models"]["histgb"]["panel"]
    lines += [
        "**Вывод.** Сильное утверждение D2 не подтверждено. Первичная гибкая модель не даёт "
        f"междатасетного свидетельства T3>T2: wins={primary['wins']}/4, exact sign "
        f"p={primary['sign_test_p_greater']:.4f}. Любой эффект LogReg остаётся вторичным инженерным "
        "эффектом ограниченной модели и не повышает ФТС-статус.",
        "",
        "**Что не закрыто.** Эксперимент проверяет только кодировочную роль, не внутреннюю семантику "
        "У8/У9. Вычислительная ёмкость T2/T3 не уравнена. При четырёх независимых датасетах exact "
        "sign test не может достичь α=0.05 даже при 4/4 победах; новая сильная попытка требует новой "
        "предрегистрации, capacity-matched null и большей панели.",
        "",
        "## Данные",
        "",
        "| Имя | Источник | Data ID | Version | Rows×columns | MD5/SHA256 |",
        "|---|---|---:|---|---:|---|",
    ]
    for item in output["datasets"]:
        checksum = item.get("md5_checksum") or item["materialized_sha256"]
        lines.append(
            f"| {item['name']} | {item['source']} | {item.get('data_id') or '—'} | {item['version']} | "
            f"{item['n_rows']}×{item['n_columns']} | `{checksum}` |"
        )
    lines += ["", "Полные fold-level AUC, materialized SHA256 и версии среды сохранены в `audit_results.json`.", ""]
    (HERE / "AUDIT_REANALYSIS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    result = run()
    print(result["audit_verdict"])
