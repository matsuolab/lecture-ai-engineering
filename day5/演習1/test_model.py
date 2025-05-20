"""
演習1用のモデルテストと差分テストファイル
"""
import os
import pytest
import pandas as pd
import pickle
import numpy as np
import time
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# テスト用データとモデルパスを定義
DATA_PATH = os.path.join(os.path.dirname(__file__), "data/Titanic.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/titanic_model.pkl")
BASELINE_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/titanic_model_baseline.pkl")


@pytest.fixture
def sample_data():
    """テスト用データセットを読み込む"""
    data = pd.read_csv(DATA_PATH)
    # データの前処理
    data = data[["Pclass", "Sex", "Age", "Fare", "Survived"]].dropna()
    data["Sex"] = LabelEncoder().fit_transform(data["Sex"])  # 性別を数値に変換
    
    # 整数型の列を浮動小数点型に変換
    data["Pclass"] = data["Pclass"].astype(float)
    data["Sex"] = data["Sex"].astype(float)
    data["Age"] = data["Age"].astype(float)
    data["Fare"] = data["Fare"].astype(float)
    data["Survived"] = data["Survived"].astype(float)
    
    X = data[["Pclass", "Sex", "Age", "Fare"]]
    y = data["Survived"]
    
    return X, y


@pytest.fixture
def test_data(sample_data):
    """テスト用のデータを準備"""
    X, y = sample_data
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_test, y_test


def test_model_exists():
    """モデルファイルが存在するか確認"""
    assert os.path.exists(MODEL_PATH), "モデルファイルが存在しません"


def test_model_accuracy(test_data):
    """モデルの精度を検証"""
    X_test, y_test = test_data
    
    # モデルのロード
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    
    # 予測と精度計算
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Titanicデータセットでは0.75以上の精度が一般的に良いとされる
    assert accuracy >= 0.75, f"モデルの精度が低すぎます: {accuracy}"
    print(f"モデル精度: {accuracy:.4f}")


def test_model_inference_time(test_data):
    """モデルの推論時間を検証"""
    X_test, _ = test_data
    
    # モデルのロード
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    
    # 推論時間の計測
    start_time = time.time()
    model.predict(X_test)
    end_time = time.time()
    
    inference_time = end_time - start_time
    
    # 推論時間が1秒未満であることを確認
    assert inference_time < 1.0, f"推論時間が長すぎます: {inference_time}秒"
    print(f"推論時間: {inference_time:.4f}秒")


def test_model_reproducibility(sample_data):
    """モデルの再現性を検証"""
    X, y = sample_data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 同じパラメータで２つのモデルを作成
    model1 = RandomForestClassifier(n_estimators=100, random_state=42)
    model2 = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # 学習
    model1.fit(X_train, y_train)
    model2.fit(X_train, y_train)
    
    # 同じ予測結果になることを確認
    predictions1 = model1.predict(X_test)
    predictions2 = model2.predict(X_test)
    
    assert np.array_equal(predictions1, predictions2), "モデルの予測結果に再現性がありません"


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
        
        # 精度比較（5%の許容範囲内）
        assert current_accuracy >= baseline_accuracy * 0.95, f"モデルの精度が大幅に低下しています。現在: {current_accuracy}, ベースライン: {baseline_accuracy}"
        print(f"精度比較 - 現在: {current_accuracy:.4f}, ベースライン: {baseline_accuracy:.4f}")
    else:
        # ベースラインモデルが存在しない場合は現在のモデルをベースラインとして保存
        print(f"ベースラインモデルが存在しないため、現在のモデル（精度: {current_accuracy:.4f}）をベースラインとして保存します")
        os.makedirs(os.path.dirname(BASELINE_MODEL_PATH), exist_ok=True)
        with open(BASELINE_MODEL_PATH, "wb") as f:
            pickle.dump(current_model, f)


if __name__ == "__main__":
    # pytest用のエントリポイント（直接実行の場合）
    import pytest
    pytest.main(["-xvs", __file__])
