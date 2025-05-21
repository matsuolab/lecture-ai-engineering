import time
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

def load_test_data():
    # テスト用 CSV のパスを適宜変更してください
    df = pd.read_csv('../演習1/data/titanic_test.csv')
    X = df.drop('Survived', axis=1)
    y = df['Survived']
    return X, y

def test_model_inference_accuracy():
    # 学習済みモデルのロード
    model = joblib.load('../演習1/models/titanic_model.pkl')
    X_test, y_test = load_test_data()
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    # 精度閾値はご自身の閾値に調整してください
    assert acc >= 0.75, f"Expected accuracy >= 0.75, got {acc:.3f}"

def test_model_inference_time():
    model = joblib.load('../演習1/models/titanic_model.pkl')
    X_test, _ = load_test_data()
    # 平均推論時間を測定（100回繰り返し）
    n_runs = 100
    start = time.time()
    for _ in range(n_runs):
        model.predict(X_test)
    avg_time = (time.time() - start) / n_runs
    # 推論時間の閾値（秒）は環境に合わせて調整
    assert avg_time < 0.1, f"Inference too slow: {avg_time:.3f}s per run"
