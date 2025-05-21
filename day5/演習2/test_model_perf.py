import os
import pytest
from main import DataLoader, ModelTester

def test_model_accuracy_against_old_model():
    # 現在のモデルを評価
    data = DataLoader.load_titanic_data()
    X, y = DataLoader.preprocess_titanic_data(data)
    model = ModelTester.load_model("models/titanic_model.pkl")
    metrics = ModelTester.evaluate_model(model, X, y)
    current_accuracy = metrics["accuracy"]

    # ベースラインのモデルを評価（例: old_model.pkl）
    old_model_path = "models/old_model.pkl"
    if not os.path.exists(old_model_path):
        pytest.skip("old_model.pkl が存在しません。スキップします。")

    old_model = ModelTester.load_model(old_model_path)
    old_metrics = ModelTester.evaluate_model(old_model, X, y)
    old_accuracy = old_metrics["accuracy"]

    assert current_accuracy >= old_accuracy, f"現モデルが旧モデルより劣化しています。({current_accuracy:.4f} < {old_accuracy:.4f})"
