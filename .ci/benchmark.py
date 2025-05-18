import json
import time
from pathlib import Path
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

# 設定
MODEL_PATH = Path("day5/演習3/model.pkl")
TEST_DATA_PATH = Path("day5/演習3/data/Titanic.csv")
OUTPUT = Path("current_metrics.json")
REPEATS = 100

# 1) データロード
df = pd.read_csv(TEST_DATA_PATH)
X = df.drop("label", axis=1)
y = df["label"]

# 2) モデルロード
model = joblib.load(MODEL_PATH)

# 3) 精度計算
preds = model.predict(X)
acc = accuracy_score(y, preds)

# 4) レイテンシ計測
#    ダミー入力を REPEATS 回、
#    時間計測して平均 ms を算出
samples = X.sample(n=10, random_state=0)
t0 = time.perf_counter()
for _ in range(REPEATS):
    _ = model.predict(samples)
t1 = time.perf_counter()
avg_latency_ms = (t1 - t0) / REPEATS * 1000

# 5) 結果を出力
metrics = {
    "accuracy": acc,
    "latency_ms": avg_latency_ms
}
with open(OUTPUT, "w") as f:
    json.dump(metrics, f, indent=2)
print("Current metrics:", metrics)