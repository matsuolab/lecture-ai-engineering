import time
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
import pytest
import os

# 検証したいモデルのファイルパス 
MODEL_PATH = 'day5/演習3/models/current_titanic_model.pkl'
# テストデータのファイルパス 
TEST_DATA_PATH = 'day5/演習3/data/processed/test.csv'

# 目標とする精度 (もしあれば設定してください。例: 0.8 は 80%)
ACCURACY_THRESHOLD = 0.8

# 目標とする推論時間 (秒単位。例: 0.1 は 0.1秒以内)
INFERENCE_TIME_THRESHOLD = 0.1

@pytest.fixture
def model():
    """テスト前にモデルを読み込むフィクスチャ"""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        pytest.fail(f"エラー：モデルファイルが見つかりません: {MODEL_PATH}")

@pytest.fixture
def test_data():
    """テスト前にテストデータを読み込むフィクスチャ"""
    if os.path.exists(TEST_DATA_PATH):
        df = pd.read_csv(TEST_DATA_PATH)
        # 特徴量のカラム名と正解ラベルのカラム名をあなたのデータに合わせてください
        X_test = df.drop('Survived', axis=1, errors='ignore')  # 'Survived' が正解ラベルと仮定
        y_test = df['Survived'] if 'Survived' in df.columns else None
        return X_test, y_test
    else:
        pytest.fail(f"エラー：テストデータファイルが見つかりません: {TEST_DATA_PATH}")

def test_model_accuracy(model, test_data):
    """モデルの精度を検証するテスト"""
    X_test, y_test = test_data
    if y_test is not None:
        try:
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"\nモデルの精度: {accuracy:.4f}")
            if ACCURACY_THRESHOLD is not None:
                assert accuracy > ACCURACY_THRESHOLD, f"精度が目標値 ({ACCURACY_THRESHOLD:.2f}) を下回っています: {accuracy:.4f}"
        except Exception as e:
            pytest.fail(f"精度検証中にエラーが発生しました: {e}")
    else:
        pytest.skip("テストデータに正解ラベルが含まれていません。精度の検証をスキップします。")

def test_model_inference_time(model, test_data):
    """モデルの推論時間を検証するテスト"""
    X_test, _ = test_data
    if X_test is not None and not X_test.empty:
        try:
            start_time = time.time()
            model.predict(X_test[:1])  # 最初の1件で推論時間を計測 (データ量が多い場合は調整)
            end_time = time.time()
            inference_time = end_time - start_time
            print(f"モデルの推論時間 (最初の1件): {inference_time:.6f} 秒")
            if INFERENCE_TIME_THRESHOLD is not None:
                assert inference_time < INFERENCE_TIME_THRESHOLD, f"推論時間が目標値 ({INFERENCE_TIME_THRESHOLD:.6f} 秒) を超えています: {inference_time:.6f} 秒"
        except Exception as e:
            pytest.fail(f"推論時間検証中にエラーが発生しました: {e}")
    else:
        pytest.skip("テストデータが空のため、推論時間の検証をスキップします。")