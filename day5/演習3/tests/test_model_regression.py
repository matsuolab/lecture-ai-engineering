# day5/演習3/tests/test_model_regression.py

import numpy as np
from sklearn.metrics import accuracy_score
from day5.演習3.model import load_model, predict, load_sample_data

def test_model_regression_check():
    # 現在と過去のモデルを読み込み
    current_model = load_model("models/current_model.pkl")
    previous_model = load_model("models/previous_model.pkl")
    X_test, y_test = load_sample_data()

    # 予測
    y_pred_current = predict(current_model, X_test)
    y_pred_previous = predict(previous_model, X_test)

    # 精度計算
    acc_current = accuracy_score(y_test, y_pred_current)
    acc_previous = accuracy_score(y_test, y_pred_previous)

    # 精度劣化がないか（1%以内の許容誤差）
    assert acc_current >= acc_previous - 0.01, (
        f"Model performance regressed: current={acc_current:.2f}, previous={acc_previous:.2f}"
    )
