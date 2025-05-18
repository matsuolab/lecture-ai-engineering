import json
import sys

THRESH_ACC_DROP = float(sys.argv[3])  # 例: 0.01  (1% 精度低下まで許容)
THRESH_LAT_UP = float(sys.argv[4])    # 例: 1.2   (レイテンシは20% 増加まで許容)

baseline_f, current_f = sys.argv[1], sys.argv[2]
with open(baseline_f) as f:
    base = json.load(f)
with open(current_f) as f:
    cur = json.load(f)

ok = True
# 精度チェック
if cur["accuracy"] + THRESH_ACC_DROP < base["accuracy"]:
    print(f"ERROR: accuracy dropped from {base['accuracy']} to {cur['accuracy']}")
    ok = False
else:
    print(f"OK: accuracy {cur['accuracy']} >= {base['accuracy'] - THRESH_ACC_DROP}")

# レイテンシチェック
if cur["latency_ms"] > base["latency_ms"] * THRESH_LAT_UP:
    print(f"ERROR: latency increased from {base['latency_ms']} to {cur['latency_ms']}")
    ok = False
else:
    print(f"OK: latency {cur['latency_ms']} <= {base['latency_ms']} * {THRESH_LAT_UP}")

sys.exit(0 if ok else 1)