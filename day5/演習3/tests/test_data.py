import os
import pytest
import pandas as pd
import numpy as np
import great_expectations as gx
from sklearn.datasets import fetch_openml
import warnings
from 演習2.main import DataLoader, ModelTester
from sklearn.model_selection import train_test_split

# 警告を抑制
warnings.filterwarnings("ignore")

# テスト用データパスを定義
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Titanic.csv")


@pytest.fixture
def sample_data():
    """Titanicテスト用データセットを読み込む"""
    return pd.read_csv(DATA_PATH)


def test_data_exists(sample_data):
    """データが存在することを確認"""
    assert not sample_data.empty, "データセットが空です"
    assert len(sample_data) > 0, "データセットにレコードがありません"


def test_data_columns(sample_data):
    """必要なカラムが存在することを確認"""
    expected_columns = [
        "Pclass",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Fare",
        "Embarked",
        "Survived",
    ]
    for col in expected_columns:
        assert (
            col in sample_data.columns
        ), f"カラム '{col}' がデータセットに存在しません"


def test_data_types(sample_data):
    """データ型の検証"""
    # 数値型カラム
    numeric_columns = ["Pclass", "Age", "SibSp", "Parch", "Fare"]
    for col in numeric_columns:
        assert pd.api.types.is_numeric_dtype(
            sample_data[col].dropna()
        ), f"カラム '{col}' が数値型ではありません"

    # カテゴリカルカラム
    categorical_columns = ["Sex", "Embarked"]
    for col in categorical_columns:
        assert (
            sample_data[col].dtype == "object"
        ), f"カラム '{col}' がカテゴリカル型ではありません"

    # 目的変数
    survived_vals = sample_data["Survived"].dropna().unique()
    assert set(survived_vals).issubset({"0", "1"}) or set(survived_vals).issubset(
        {0, 1}
    ), "Survivedカラムには0, 1のみ含まれるべきです"


def test_missing_values_acceptable(sample_data):
    """欠損値の許容範囲を確認"""
    # 完全に欠損するのではなく、許容範囲内の欠損を確認
    for col in sample_data.columns:
        missing_rate = sample_data[col].isna().mean()
        assert (
            missing_rate < 0.8
        ), f"カラム '{col}' の欠損率が80%を超えています: {missing_rate:.2%}"


def test_value_ranges(sample_data):
    """値の範囲を検証"""
    context = gx.get_context()
    data_source = context.data_sources.add_pandas("pandas")
    data_asset = data_source.add_dataframe_asset(name="pd dataframe asset")

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        "batch definition"
    )
    batch = batch_definition.get_batch(batch_parameters={"dataframe": sample_data})

    results = []

    # 必須カラムの存在確認
    required_columns = [
        "Pclass",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Fare",
        "Embarked",
    ]
    missing_columns = [
        col for col in required_columns if col not in sample_data.columns
    ]
    if missing_columns:
        print(f"警告: 以下のカラムがありません: {missing_columns}")
        return False, [{"success": False, "missing_columns": missing_columns}]

    expectations = [
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="Pclass", value_set=[1, 2, 3]
        ),
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="Sex", value_set=["male", "female"]
        ),
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="Age", min_value=0, max_value=100
        ),
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="Fare", min_value=0, max_value=600
        ),
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="Embarked", value_set=["C", "Q", "S", ""]
        ),
    ]

    for expectation in expectations:
        result = batch.validate(expectation)
        results.append(result)
        is_successful = all(result.success for result in results)
    assert is_successful, "データの値範囲が期待通りではありません"


def train_model():
    """演習2のモデルとテストデータを返すfixture"""
    data = DataLoader.load_titanic_data()
    X, y = DataLoader.preprocess_titanic_data(data)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = ModelTester.train_model(X_train, y_train)
    return model, X_test, y_test


def test_feature_count(train_model):
    """前処理後の特徴量数とモデルが学習時に認識した特徴量数が一致するか確認"""
    model, X_test, _ = train_model

    # 前処理後の特徴量数（transform後のshape）
    preprocessed_features = model.named_steps["preprocessor"].transform(X_test)
    n_features_transformed = preprocessed_features.shape[1]

    # モデルが学習時に記録している特徴量数
    n_features_model = model.named_steps["classifier"].n_features_in_

    assert (
        n_features_transformed == n_features_model
    ), f"前処理後の特徴量数 ({n_features_transformed}) とモデルが期待する特徴量数 ({n_features_model}) が一致しません"


def test_model_invalid_input(train_model):
    """不正な形式の入力に対して適切なエラーが出ることを確認"""
    model, _, _ = train_model

    # 数値ではなく文字列を含む入力を意図的に与える
    invalid_input = pd.DataFrame(
        [["invalid", None, "bad", "input", "data", "xxx", "???"]],
        columns=["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"],
    )

    with pytest.raises(Exception) as exc_info:
        model.predict(invalid_input)

    # エラー内容を確認する場合（オプション）
    error_msg = str(exc_info.value)
    print("予想されるエラーメッセージ:", error_msg)

    # エラーメッセージを一部確認しておくと堅牢性アップ
    assert (
        "could not convert" in error_msg or "input" in error_msg.lower()
    ), f"期待される形式のエラーメッセージではありません: {error_msg}"
