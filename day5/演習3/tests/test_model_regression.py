# day5/演習3/tests/test_model_regression.py

import os
import time
import pickle
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# ファイルパス定義
HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, "../data/Titanic.csv")
CURRENT_MODEL_PATH = os.path.join(HERE, "../models/titanic_model.pkl")
BASELINE_MODEL_PATH = os.path.join(HERE, "../models/titanic_model_baseline.pkl")


@pytest.fixture(scope="session")
def test_data():
    df = pd.read_csv(DATA_PATH)
    X = df.drop("Survived", axis=1)
    y = df["Survived"].astype(int)
    return train_test_split(X, y, test_size=0.2, random_state=42)


def eval_model(path, X_test, y_test):
    model = pickle.load(open(path, "rb"))
    # 精度
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    # 推論時間（1 回だけ）
    start = time.time()
    model.predict(X_test)
    t = time.time() - start
    return acc, t


def test_no_regression(test_data):
    X_train, X_test, y_train, y_test = test_data

    base_acc, base_t = eval_model(BASELINE_MODEL_PATH, X_test, y_test)
    cur_acc, cur_t = eval_model(CURRENT_MODEL_PATH, X_test, y_test)

    # 精度はベースライン比で 1% 以上落ちていないこと
    assert (
        cur_acc >= base_acc - 0.01
    ), f"Accuracy regression: current={cur_acc:.3f} < baseline={base_acc:.3f}"
    # 推論時間はベースライン比で 5% 以上遅くなっていないこと
    assert (
        cur_t <= base_t * 1.05
    ), f"Inference time regression: current={cur_t:.3f}s > baseline={base_t:.3f}s"
