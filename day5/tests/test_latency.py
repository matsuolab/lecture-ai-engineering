import time

MAX_MS = 50  # 許容閾値

def test_latency(model, sample_df):
    start = time.perf_counter()
    model.predict(sample_df.drop(columns=["label"]))
    elapsed = (time.perf_counter() - start) * 1000
    assert elapsed < MAX_MS, f"Inference {elapsed:.1f} ms exceeds {MAX_MS} ms"
