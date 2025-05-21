import pytest
import time
import os
import pandas as pd
from models.main import DataLoader, ModelTester  # パスはリポジトリ構成に合わせて変更


def test_model_inference_accuracy():
    """モデルの推論精度をテスト"""
    # モデル読み込み
    model = ModelTester.load_model("models/titanic_model.pkl")

    # テストデータの読み込みと前処理
    data = DataLoader.load_titanic_data("data/Titanic.csv")
    X, y = DataLoader.preprocess_titanic_data(data)

    # 精度評価
    y_pred = model.predict(X)
    accuracy = (y_pred == y).mean()

    # 閾値に基づくテスト
    assert accuracy >= 0.75, f"Accuracy too low: {accuracy:.4f}"


def test_model_inference_time():
    """モデルの推論時間をテスト"""
    model = ModelTester.load_model("models/titanic_model.pkl")
    data = DataLoader.load_titanic_data("data/Titanic.csv")
    X, _ = DataLoader.preprocess_titanic_data(data)

    start = time.time()
    _ = model.predict(X)
    elapsed = time.time() - start

    assert elapsed < 1.0, f"Inference took too long: {elapsed:.4f} sec"

