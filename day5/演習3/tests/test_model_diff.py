"""
モデル差分テスト用ファイル
過去のベースラインモデルと比較して性能劣化がないことを確認するテスト
"""
import os
import pytest
import pandas as pd
import pickle
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# テスト用データとモデルパスを定義
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Titanic.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
MODEL_PATH = os.path.join(MODEL_DIR, "titanic_model.pkl")
BASELINE_MODEL_PATH = os.path.join(MODEL_DIR, "titanic_model_baseline.pkl")


@pytest.fixture
def sample_data():
    """テスト用データセットを読み込む"""
    return pd.read_csv(DATA_PATH)


@pytest.fixture
def test_data():
    """テスト用のデータを準備"""
    df = pd.read_csv(DATA_PATH)
    X = df.drop("Survived", axis=1) if "Survived" in df.columns else df
    y = df["Survived"] if "Survived" in df.columns else None
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_test, y_test


def test_model_exists():
    """モデルファイルが存在するか確認"""
    assert os.path.exists(MODEL_PATH), "モデルファイルが存在しません"


def test_compare_with_baseline(test_data):
    """現在のモデルとベースラインモデルの精度を比較"""
    X_test, y_test = test_data
    
    # 現在のモデルの読み込み
    assert os.path.exists(MODEL_PATH), "モデルファイルが存在しません"
    with open(MODEL_PATH, "rb") as f:
        current_model = pickle.load(f)
    
    # 現在のモデルで予測
    current_pred = current_model.predict(X_test)
    current_accuracy = accuracy_score(y_test, current_pred)
    
    # ベースラインモデルの確認
    if os.path.exists(BASELINE_MODEL_PATH):
        # ベースラインモデルが存在する場合は比較
        with open(BASELINE_MODEL_PATH, "rb") as f:
            baseline_model = pickle.load(f)
        
        baseline_pred = baseline_model.predict(X_test)
        baseline_accuracy = accuracy_score(y_test, baseline_pred)
        
        # 精度比較
        assert current_accuracy >= baseline_accuracy * 0.95, f"モデルの精度が大幅に低下しています。現在: {current_accuracy}, ベースライン: {baseline_accuracy}"
        print(f"精度比較 - 現在: {current_accuracy:.4f}, ベースライン: {baseline_accuracy:.4f}")
    else:
        # ベースラインモデルが存在しない場合は現在のモデルをベースラインとして保存
        print(f"ベースラインモデルが存在しないため、現在のモデル（精度: {current_accuracy:.4f}）をベースラインとして保存します")
        with open(BASELINE_MODEL_PATH, "wb") as f:
            pickle.dump(current_model, f)


def test_prediction_consistency(test_data):
    """モデルの予測一貫性をテスト"""
    X_test, _ = test_data
    
    # モデルの読み込み
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    
    # 同じデータで2回予測
    pred1 = model.predict(X_test)
    pred2 = model.predict(X_test)
    
    # 予測結果の一貫性を確認
    assert np.array_equal(pred1, pred2), "モデルの予測に一貫性がありません"


if __name__ == "__main__":
    # pytest用のエントリポイント（直接実行の場合）
    import pytest
    pytest.main(["-xvs", __file__])
