import os
import time
import pickle
import pytest
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# パス定義
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Titanic.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
MODEL_PATH = os.path.join(MODEL_DIR, "titanic_model.pkl")


@pytest.fixture
def sample_data():
    """テスト用データセットを読み込む"""
    if not os.path.exists(DATA_PATH):
        from sklearn.datasets import fetch_openml

        titanic = fetch_openml("titanic", version=1, as_frame=True)
        df = titanic.data
        df["Survived"] = titanic.target

        df = df[
            ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked", "Survived"]
        ]

        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df.to_csv(DATA_PATH, index=False)

    return pd.read_csv(DATA_PATH)


@pytest.fixture
def preprocessor():
    """前処理パイプラインを定義"""
    numeric_features = ["Age", "Pclass", "SibSp", "Parch", "Fare"]
    categorical_features = ["Sex", "Embarked"]

    numeric_transformer = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        [
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    return preprocessor


@pytest.fixture
def train_model(sample_data, preprocessor):
    """モデルの学習とテストデータの準備"""
    X = sample_data.drop("Survived", axis=1)
    y = sample_data["Survived"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
        ]
    )

    model.fit(X_train, y_train)

    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    return model, X_test, y_test


def test_model_exists():
    """モデルファイルが存在するか確認"""
    if not os.path.exists(MODEL_PATH):
        pytest.skip("モデルファイルが存在しないためスキップします")
    assert os.path.exists(MODEL_PATH), "モデルファイルが存在しません"


def test_model_accuracy(train_model):
    """モデルの精度を検証"""
    model, X_test, y_test = train_model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    assert accuracy >= 0.75, f"モデルの精度が低すぎます: {accuracy}"


def test_model_inference_time(train_model):
    """モデルの推論時間を検証"""
    model, X_test, _ = train_model
    start_time = time.time()
    model.predict(X_test)
    end_time = time.time()
    inference_time = end_time - start_time
    assert inference_time < 1.0, f"推論時間が長すぎます: {inference_time:.3f}秒"


def test_model_reproducibility(sample_data, preprocessor):
    """モデルの再現性を検証"""
    X = sample_data.drop("Survived", axis=1)
    y = sample_data["Survived"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model1 = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
        ]
    )
    model2 = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
        ]
    )

    model1.fit(X_train, y_train)
    model2.fit(X_train, y_train)

    predictions1 = model1.predict(X_test)
    predictions2 = model2.predict(X_test)

    assert np.array_equal(predictions1, predictions2), "モデルの予測結果に再現性がありません"


def test_inference_time_and_accuracy():
    """推論時間と精度の統合テスト"""
    # モデルとテストデータの読み込み
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    df = pd.read_csv(DATA_PATH)
    X_test = df.drop("Survived", axis=1)
    y_test = df["Survived"].astype(int)

    # 推論時間の測定
    start = time.time()
    y_pred = model.predict(X_test)
    duration = time.time() - start

    assert duration < 1.0, f"Inference too slow: {duration:.3f} sec"

    # 精度の確認（80%以上を期待）
    acc = accuracy_score(y_test, y_pred)
    assert acc >= 0.8, f"Low inference accuracy: {acc:.2f}"
