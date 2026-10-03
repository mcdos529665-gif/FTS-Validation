# -*- coding: utf-8 -*-
"""Проба: какие реальные датасеты с НАСТОЯЩЕЙ пропущенностью доступны.
Это осмотр данных (loads / доля пропусков / число колонок с пропуском / бинарность
таргета), НЕ вычисление результата. Нужен, чтобы зафиксировать панель ДО предрегистрации.
"""
import warnings, sys
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml

# кандидаты с известной нативной пропущенностью и бинарным таргетом
CANDIDATES = ["colic", "hepatitis", "vote", "credit-approval", "cylinder-bands",
              "dresses-sales", "primary-tumor", "echocardiogram", "heart-c", "labor"]

def profile(name):
    try:
        ds = fetch_openml(name, version=1, as_frame=True, parser="auto")
    except Exception as e:
        return (name, f"FAIL load: {str(e)[:60]}")
    X, y = ds.data, ds.target
    n, p = X.shape
    miss_cells = X.isna().sum().sum()
    miss_frac = miss_cells / (n * p) if n * p else 0
    cols_with_miss = int((X.isna().sum() > 0).sum())
    rows_with_miss = int((X.isna().sum(axis=1) > 0).sum())
    nclass = y.nunique(dropna=True)
    # доля пропусков, размазанных по >=2 колонкам — нужно, чтобы типизация отличалась от флага
    return (name, dict(n=n, p=p, miss_frac=round(float(miss_frac), 3),
                       cols_with_miss=cols_with_miss, rows_with_miss=rows_with_miss,
                       n_classes=int(nclass), target=ds.target_names if hasattr(ds, "target_names") else "?"))

if __name__ == "__main__":
    for nm in CANDIDATES:
        name, prof = profile(nm)
        print(name, "::", prof)
