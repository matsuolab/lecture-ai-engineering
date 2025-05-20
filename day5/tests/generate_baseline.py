import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.resolve()))
import json
import hashlib
import pandas as pd
import importlib
from sklearn.metrics import accuracy_score

# 1) モデルのロード
Model = importlib.import_module("src.model").Model
model = Model.load("artifacts/model.joblib")

# 2) 入力データ読み込み
df = pd.read_csv("artifacts/sample.csv")
X = df.drop(columns=["label"])
y_true = df["label"].values

# 3) 予測と精度計算
y_pred = model.predict(X)
acc = float(accuracy_score(y_true, y_pred))

# 4) ハッシュ生成（予測結果100件分のみ。test_regression と一致させるなら同じスライスで）
pred_slice = y_pred[:100]
pred_hash = hashlib.sha256(pred_slice.tobytes()).hexdigest()

# 5) JSON にまとめて保存
baseline = {
    "accuracy": acc,
    "pred_hash": pred_hash
}
with open("tests/baseline.json", "w") as fp:
    json.dump(baseline, fp, indent=2)

print("Generated tests/baseline.json:", baseline)
