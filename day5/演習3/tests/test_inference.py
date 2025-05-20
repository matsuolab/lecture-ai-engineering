# day5/演習3/tests/test_inference.py

import time
import numpy as np
from sklearn.metrics import accuracy_score
from day5.演習3.model import load_model, predict, load_sample_data

def test_inference_time_and_accuracy():
    # モデルとテストデータの読み込み
    model = load_model("models/current_model.pkl")
    X_test, y_test = load_sample_data()

    # 推論時間の測定
    start = time.time()
    y_pred = predict(model, X_test)
    duration = time.time() - start

    # 時間が1秒未満であることを期待
    assert duration < 1.0, f"Inference too slow: {duration:.3f} sec"

    # 精度の確認（80%以上を期待）
    acc = accuracy_score(y_test, y_pred)
    assert acc >= 0.8, f"Low inference accuracy: {acc:.2f}"
