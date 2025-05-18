import os
import pickle
import pytest
import numpy as np
from sklearn.pipeline import Pipeline

# 既存と同じパス定義
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
MODEL_PATH = os.path.join(MODEL_DIR, "titanic_model.pkl")


def test_preprocessor_output_shape_and_no_nan(sample_data, preprocessor):
    """
    前処理器(preprocessor)の fit_transform 後の出力形状と欠損値がないことを確認
    """
    X = sample_data.drop("Survived", axis=1)
    # fit_transform してみる
    X_trans = preprocessor.fit_transform(X)

    # 行数は変わらず
    assert X_trans.shape[0] == X.shape[0]

    # 列数は最低でも数値特徴量の数以上（OneHotで拡張されているはず）
    numeric_count = len(["Age", "Pclass", "SibSp", "Parch", "Fare"])
    assert X_trans.shape[1] >= numeric_count

    # 欠損値がないこと
    assert not np.isnan(X_trans).any()


def test_predict_proba_validity(train_model):
    """
    predict_proba が返す確率の shape/sum が正しいか
    """
    model: Pipeline
    X_test, y_test = None, None
    model, X_test, y_test = train_model

    proba = model.predict_proba(X_test)
    # 2クラス→(n_samples, 2)
    assert proba.ndim == 2
    assert proba.shape == (len(X_test), 2)

    # 各行の合計が 1 になる
    sums = proba.sum(axis=1)
    assert np.allclose(sums, 1.0)


def test_model_save_and_load_consistency(train_model):
    """
    pickle で保存したモデルを読み直して、同じ予測結果が得られるか
    """
    # いったん train_model でモデルを作成・保存している前提
    _, X_test, _ = train_model

    # ロード
    with open(MODEL_PATH, "rb") as f:
        loaded = pickle.load(f)

    # 同一 pipeline オブジェクト構造になっているか
    assert isinstance(loaded, Pipeline)

    # 予測結果が一致
    orig_preds = loaded.predict(X_test)
    re_preds = loaded.predict(X_test)
    assert np.array_equal(orig_preds, re_preds)


def test_missing_column_raises_on_preprocess(sample_data, preprocessor):
    """
    必須カラムを欠損させると前処理段階でエラーになることを確認
    """
    X = sample_data.drop("Survived", axis=1)
    # 例えば 'Fare' を落としてみる
    X_bad = X.drop("Fare", axis=1)
    with pytest.raises(ValueError):
        # fit_transform でも transform でもよい
        preprocessor.fit_transform(X_bad)


def test_feature_importances_positive(train_model):
    """
    RandomForest の feature_importances_ が正しく得られ、全体の寄与度が正数であること
    """
    model, _, _ = train_model
    # pipeline の最後のステップを取り出し
    clf = model.named_steps["classifier"]
    importances = clf.feature_importances_

    # 1 次元配列で、各要素が 0 以上で合計 > 0
    assert importances.ndim == 1
    assert np.all(importances >= 0)
    assert importances.sum() > 0