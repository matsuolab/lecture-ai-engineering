# モデルテストと差分テストの実装

このディレクトリには演習1、演習2、演習3向けに以下のテストが追加されています：

1. **モデルテスト**
   - 推論精度の検証（`test_model_accuracy`）
   - 推論時間の測定（`test_model_inference_time`）
   - 予測の再現性と一貫性確認（`test_model_reproducibility`, `test_prediction_consistency`）

2. **差分テスト**
   - 過去のベースラインモデルとの性能比較（`test_compare_with_baseline`）
   - 初回実行時には現在のモデルがベースラインとして保存されます

## テスト実行方法

### 演習1のテスト実行
```bash
cd 演習1
pytest test_model.py -v
```

### 演習2のテスト実行
```bash
cd 演習2
pytest test_model.py -v
```

### 演習3のテスト実行
```bash
cd 演習3
# データテスト
pytest tests/test_data.py -v
# モデルテスト
pytest tests/test_model.py -v
# 差分テスト
pytest tests/test_model_diff.py -v
```

### CIでの全テスト実行
リポジトリにpull requestを作成すると、GitHub Actionsによって全てのテストが自動的に実行されます。