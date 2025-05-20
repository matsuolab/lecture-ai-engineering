import os
import time

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder


def load_data():
    """前処理込みで特徴量とラベルを返す"""
    df = pd.read_csv("./data/Titanic.csv")
    df = df[["Pclass", "Sex", "Age", "Fare", "Survived"]].dropna()
    df["Sex"] = LabelEncoder().fit_transform(df["Sex"])
    df[["Pclass", "Sex", "Age", "Fare"]] = df[["Pclass", "Sex", "Age", "Fare"]].astype(float)
    X = df[["Pclass", "Sex", "Age", "Fare"]]
    y = df["Survived"]
    return X, y


def test_inference_time():
    model = joblib.load("./models/titanic_model.pkl")
    X, _ = load_data()

    start = time.time()
    _ = model.predict(X)
    elapsed = time.time() - start

    assert elapsed < 1.0, f"Inference took too long: {elapsed:.3f} seconds"


def test_accuracy_vs_baseline():
    X, y = load_data()

    current_model = joblib.load("./models/titanic_model.pkl")
    baseline_model = joblib.load("./models/baseline_model.pkl")

    current_acc = accuracy_score(y, current_model.predict(X))
    baseline_acc = accuracy_score(y, baseline_model.predict(X))

    assert current_acc >= baseline_acc, f"Current model is worse than baseline ({current_acc:.3f} < {baseline_acc:.3f})"


def test_model_size():
    path = "./models/titanic_model.pkl"
    size_mb = os.path.getsize(path) / (1024 * 1024)

    assert size_mb < 10.0, f"Model file too large: {size_mb:.2f} MB"
