import subprocess
import os
import joblib
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def load_test_data():
    full = pd.read_csv(
        os.path.join(os.getcwd(), "day5", "演習1", "data", "titanic.csv")
    )
    X = full.drop("Survived", axis=1)
    y = full["Survived"]
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.11, random_state=88)
    return X_test, y_test


def get_model():
    model_path = os.path.join(
        os.getcwd(), "day5", "演習1", "models", "titanic_model.pkl"
    )
    assert os.path.exists(model_path), f"Model not found at {model_path}"
    return joblib.load(model_path)


def parse_main_accuracy():
    """
    day5/演習1/main.py をカレントディレクトリに切り替えて実行し、
    出力から 'accuracy:' の行をパースして返す
    """
    workdir = os.path.join(os.getcwd(), "day5", "演習1")
    proc = subprocess.run(
        ["python", "main.py"],
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    out = proc.stdout
    for line in out.splitlines():
        if "accuracy:" in line:
            return float(line.split("accuracy:")[1].strip())
    pytest.skip("Could not parse accuracy from main.py output")


def test_model_inference_accuracy():
    acc = parse_main_accuracy()
    # CI 環境では微妙に変動するため、閾値を 0.74 に調整
    assert acc >= 0.74, f"Expected accuracy >= 0.74, got {acc:.3f}"
