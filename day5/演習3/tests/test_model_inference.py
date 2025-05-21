import os
import time
from day5.演習2.main import DataLoader, ModelTester

# モデルファイルパスの明示的な指定
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
MODEL_PATH = os.path.join(MODEL_DIR, "titanic_model.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Titanic.csv")


def test_model_inference_accuracy():
    """モデルの推論精度が0.75以上であることを検証"""
    model = ModelTester.load_model(MODEL_PATH)
    data = DataLoader.load_titanic_data(DATA_PATH)
    X, y = DataLoader.preprocess_titanic_data(data)
    y_pred = model.predict(X)
    accuracy = (y_pred == y).mean()
    assert accuracy >= 0.75, f"Accuracy too low: {accuracy:.4f}"


def test_model_inference_time():
    """モデルの推論が1秒以内に完了することを検証"""
    model = ModelTester.load_model(MODEL_PATH)
    data = DataLoader.load_titanic_data(DATA_PATH)
    X, y = DataLoader.preprocess_titanic_data(data)
    start = time.time()
    _ = model.predict(X)
    elapsed = time.time() - start
    assert elapsed < 1.0, f"Inference took too long: {elapsed:.4f} sec"
