import os
import pytest
import pandas as pd
import numpy as np
import pickle
import time
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
OLD_MODEL_PATH = os.path.join(MODEL_DIR, "old_model.pkl")  # ← 追加

# ===== データ準備 =====


@pytest.fixture
def sample_data():
    df = pd.read_csv(DATA_PATH)
    return df


@pytest.fixture
def preprocessor():
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

    return ColumnTransformer(
        [
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )


@pytest.fixture
def train_model(sample_data, preprocessor):
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


# ===== テスト群 =====


def test_model_exists():
    if not os.path.exists(MODEL_PATH):
        pytest.skip("モデルファイルが存在しないためスキップします")
    assert os.path.exists(MODEL_PATH), "モデルファイルが存在しません"


def test_model_accuracy_threshold(train_model):
    model, X_test, y_test = train_model
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    assert acc >= 0.80, f"モデル精度が基準を下回っています: {acc:.4f}"


def test_model_latency_threshold(train_model):
    model, X_test, _ = train_model
    start = time.time()
    model.predict(X_test)
    elapsed = time.time() - start
    assert elapsed < 1.0, f"推論時間が長すぎます: {elapsed:.4f}秒"


def test_model_reproducibility(sample_data, preprocessor):
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

    assert np.array_equal(
        model1.predict(X_test), model2.predict(X_test)
    ), "モデルの予測結果に再現性がありません"

def test_model_regression_against_previous(train_model):
    """過去モデルと比較して性能が著しく劣化していないか検証"""
    model, X_test, y_test = train_model

    if not os.path.exists(OLD_MODEL_PATH):
        pytest.skip("前バージョンのモデルが存在しないためスキップ")

    with open(OLD_MODEL_PATH, "rb") as f:
        old_model = pickle.load(f)

    old_acc = accuracy_score(y_test, old_model.predict(X_test))
    new_acc = accuracy_score(y_test, model.predict(X_test))

    assert (
        new_acc >= old_acc - 0.02
    ), f"モデルの精度が劣化しています。新: {new_acc:.4f}, 旧: {old_acc:.4f}"

