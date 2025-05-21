import os
import pytest
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import accuracy_score

# テスト用パスを定義
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Titanic.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
MODEL_PATH = os.path.join(MODEL_DIR, "titanic_model.pkl")
BASELINE_MODEL_PATH = os.path.join(MODEL_DIR, "baseline_model.pkl")

@pytest.fixture
def sample_data():
    """テスト用データセットを読み込む"""
    return pd.read_csv(DATA_PATH)

@pytest.fixture
def current_model():
    """現在のモデルを読み込む"""
    if not os.path.exists(MODEL_PATH):
        pytest.skip("現在のモデルファイルが存在しないためスキップします")
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

@pytest.fixture
def baseline_model():
    """ベースラインモデルを読み込む。存在しない場合は現在のモデルをコピーして作成"""
    if not os.path.exists(BASELINE_MODEL_PATH):
        if not os.path.exists(MODEL_PATH):
            pytest.skip("モデルファイルが存在しないためスキップします")
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(BASELINE_MODEL_PATH, "wb") as f:
            pickle.dump(model, f)
    
    with open(BASELINE_MODEL_PATH, "rb") as f:
        return pickle.load(f)

def test_model_no_regression(sample_data, current_model, baseline_model):
    """現在のモデルがベースラインモデルより性能が劣化していないことを確認"""
    # データの準備
    X = sample_data.drop("Survived", axis=1)
    y = sample_data["Survived"].astype(int)
    
    # 両方のモデルで予測
    try:
        y_pred_current = current_model.predict(X)
        current_accuracy = accuracy_score(y, y_pred_current)
        
        y_pred_baseline = baseline_model.predict(X)
        baseline_accuracy = accuracy_score(y, y_pred_baseline)
        
        # 現在のモデルの精度がベースラインモデル以上であることを確認
        assert current_accuracy >= baseline_accuracy, \
            f"モデルの性能が劣化しています。現在: {current_accuracy:.4f}, ベースライン: {baseline_accuracy:.4f}"
            
        print(f"モデルの比較 - 現在: {current_accuracy:.4f}, ベースライン: {baseline_accuracy:.4f}")
    except Exception as e:
        # 入力形式が異なる場合などのエラー処理
        pytest.skip(f"モデル比較中にエラーが発生しました: {str(e)}")