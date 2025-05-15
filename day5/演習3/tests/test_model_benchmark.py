# tests/test_model_benchmark.py
import pytest
import pickle
import os
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
import sys

# このファイル (…/tests/) のひとつ上のディレクトリをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sklearn.model_selection import train_test_split
from tests.test_model import MODEL_PATH, DATA_PATH
# MODEL_PATH, DATA_PATH は test_model.py からインポートしています

@pytest.fixture(scope="session")
def model():
    # 既存の pickle モデルをロード
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

@pytest.fixture(scope="session")
def X_test():
    # 既存のテストデータ読み込みロジックを流用
    df = pd.read_csv(DATA_PATH)
    X = df.drop("Survived", axis=1)
    y = df["Survived"].astype(int)
    # 固定シードで分割
    _, X_test, _, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_test

def test_inference_performance(benchmark, model, X_test):
    import time; time.sleep(0.1)
    # ベンチマーク実行
    result = benchmark(model.predict, X_test)
    # 返り値チェック
    assert result is not None
