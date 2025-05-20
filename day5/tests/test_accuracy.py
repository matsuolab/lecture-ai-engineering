import numpy as np
from sklearn.metrics import accuracy_score

# 過去バージョンの期待値を JSON に保存しておく
with open("tests/baseline.json") as fp:
    BASE = json.load(fp)

def test_accuracy(model, sample_df):
    y_true = sample_df["label"].values
    y_pred = model.predict(sample_df.drop(columns=["label"]))
    acc = accuracy_score(y_true, y_pred)
    assert acc >= BASE["accuracy"], f"Accuracy dropped: {acc:.3f} < {BASE['accuracy']:.3f}"
