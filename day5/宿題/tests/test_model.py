import os
import time

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder


def test_inference_time():
    model = joblib.load("models/titanic_model.pkl")

    df = pd.read_csv("data/Titanic.csv")
    df = df[["Pclass", "Sex", "Age", "Fare", "Survived"]].dropna()
    df["Sex"] = LabelEncoder().fit_transform(df["Sex"])
    df[["Pclass", "Sex", "Age", "Fare"]] = df[["Pclass", "Sex", "Age", "Fare"]].astype(float)

    X = df[["Pclass", "Sex", "Age", "Fare"]]

    start = time.time()
    _ = model.predict(X)
    elapsed = time.time() - start

    assert elapsed < 1.0, f"Inference took too long: {elapsed:.3f} seconds"


def test_accuracy_vs_baseline():
    df = pd.read_csv("data/Titanic.csv")
    df = df[["Pclass", "Sex", "Age", "Fare", "Survived"]].dropna()
    df["Sex"] = LabelEncoder().fit_transform(df["Sex"])
    df[["Pclass", "Sex", "Age", "Fare"]] = df[["Pclass", "Sex", "Age", "Fare"]].astype(float)

    X = df[["Pclass", "Sex", "Age", "Fare"]]
    y = df["Survived"]

    current_model = joblib.load("models/titanic_model.pkl")
    current_preds = current_model.predict(X)
    current_acc = accuracy_score(y, current_preds)

    baseline_model = joblib.load("models/baseline_model.pkl")
    baseline_preds = baseline_model.predict(X)
    baseline_acc = accuracy_score(y, baseline_preds)

    assert current_acc >= baseline_acc, f"Current model is worse than baseline ({current_acc:.3f} < {baseline_acc:.3f})"


def test_model_size():
    model_path = "models/titanic_model.pkl"
    model_size = os.path.getsize(model_path) / (1024 * 1024)  # MB

    size_limit = 10.0
    assert model_size < size_limit, f"Model size is too large: {model_size:.2f} MB"


# def test_model_version():
#     import mlflow
#     # モデルレジストリへの登録が前提のテスト。未設定のためコメントアウト推奨。
#     model_uri = "models:/titanic_model/1"
#     model_version = mlflow.registered_model.get_model_version(model_uri)
#     assert model_version == 1, f"Model version is not the latest: {model_version}"
