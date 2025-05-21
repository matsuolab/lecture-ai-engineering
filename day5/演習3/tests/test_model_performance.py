import time
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
import os


def load_test_data():
    # テストデータの読み込み
    df = pd.read_csv(
        os.path.join(os.getcwd(), "day5", "演習1", "data", "titanic_test.csv")
    )
    X = df.drop("Survived", axis=1)
    y = df["Survived"]
    return X, y


def get_model():
    # モデルファイルのパスをカレントディレクトリ基準で指定
    model_path = os.path.join(
        os.getcwd(), "day5", "演習1", "models", "titanic_model.pkl"
    )
    assert os.path.exists(model_path), f"Model file not found at {model_path}"
    return joblib.load(model_path)


def test_model_inference_accuracy():
    model = get_model()
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    assert acc >= 0.75, f"Expected accuracy >= 0.75, got {acc:.3f}"


def test_model_inference_time():
    model = get_model()
    X_test, _ = load_test_data()
    n_runs = 100
    start = time.time()
    for _ in range(n_runs):
        model.predict(X_test)
    avg_time = (time.time() - start) / n_runs
    assert avg_time < 0.1, f"Inference too slow: {avg_time:.3f}s per run"
