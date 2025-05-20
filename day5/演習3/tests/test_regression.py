import json
import os
import pickle
import time

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score

# パス定義
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA_PATH = os.path.join(ROOT, "data", "Titanic.csv")
BASELINE_DIR = os.path.join(ROOT, "baseline")
BASELINE_MODEL_PATH = os.path.join(BASELINE_DIR, "titanic_model_baseline.pkl")
BASELINE_METRICS_PATH = os.path.join(BASELINE_DIR, "metrics.json")
CANDIDATE_MODEL_PATH = os.path.join(ROOT, "models", "titanic_model.pkl")

# 許容マージン
ACCURACY_TOLERANCE = 0.02      # 2% だけ劣化を許す
SPEED_TOLERANCE    = 0.10      # 10% だけ遅くなるのを許す

@pytest.fixture(scope="module")
def titanic_df():
    return pd.read_csv(DATA_PATH)

def _predict(model, X):
    start = time.time()
    y_pred = model.predict(X)
    duration = time.time() - start
    return y_pred, duration

def test_regression_performance(titanic_df):
    # --- ベースライン読込 ---
    with open(BASELINE_MODEL_PATH, "rb") as f:
        baseline_model = pickle.load(f)
    with open(BASELINE_METRICS_PATH) as f:
        baseline_metrics = json.load(f)

    # --- 今回の(=候補)モデル読込 ---
    assert os.path.exists(CANDIDATE_MODEL_PATH), "学習済みモデルがありません"
    with open(CANDIDATE_MODEL_PATH, "rb") as f:
        candidate_model = pickle.load(f)

    X = titanic_df.drop("Survived", axis=1)
    y = titanic_df["Survived"].astype(int)

    # 精度 & 推論時間を計測
    y_pred_base, time_base = _predict(baseline_model, X)
    y_pred_cand, time_cand = _predict(candidate_model, X)

    acc_base = accuracy_score(y, y_pred_base)
    acc_cand = accuracy_score(y, y_pred_cand)

    # --- アサーション ---
    assert acc_cand + ACCURACY_TOLERANCE >= acc_base, (
        f"精度が劣化しています: baseline={acc_base:.3f}, new={acc_cand:.3f}"
    )
    assert time_cand <= time_base * (1 + SPEED_TOLERANCE), (
        f"推論が遅くなっています: baseline={time_base:.3f}s → new={time_cand:.3f}s"
    )
