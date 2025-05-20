import json, numpy as np, hashlib

def hash_array(arr):
    return hashlib.sha256(arr.tobytes()).hexdigest()

BASE = json.load(open("tests/baseline.json"))

def test_output_regression(model, sample_df):
    pred = model.predict(sample_df.drop(columns=["label"]).iloc[:100])
    assert hash_array(pred) == BASE["pred_hash"], "Model output changed unexpectedly"
