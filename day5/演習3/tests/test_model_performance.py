import time
import os
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def load_test_data():
    full = pd.read_csv(
        os.path.join(os.getcwd(), "day5", "演習1", "data", "Titanic.csv")
    )
    X = full.drop("Survived", axis=1)
    y = full["Survived"]
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.11, random_state=88)
    return X_test, y_test


def get_model():
    model_path = os.path.join(
        os.getcwd(), "day5", "演習1", "models", "titanic_model.pkl"
    )
    assert os.path.exists(model_path), f"Model file not found at {model_path}"
    return joblib.load(model_path)


def preprocess_X(model, X):
    # モデルの feature_names_in_ から必要な列のみ抽出
    feat = list(model.feature_names_in_)
    X_sel = X[feat]
    X_num = X_sel.select_dtypes(include="number")
    return X_num.values


def test_model_inference_accuracy():
    model = get_model()
    X_test, y_test = load_test_data()
    X_input = preprocess_X(model, X_test)
    y_pred = model.predict(X_input)
    acc = accuracy_score(y_test, y_pred)
    assert acc >= 0.75, f"Expected accuracy >= 0.75, got {acc:.3f}"


def test_model_inference_time():
    model = get_model()
    X_test, _ = load_test_data()
    X_input = preprocess_X(model, X_test)
    n_runs = 100
    start = time.time()
    for _ in range(n_runs):
        model.predict(X_input)
    avg_time = (time.time() - start) / n_runs
    assert avg_time < 0.1, f"Inference too slow: {avg_time:.3f}s per run"
