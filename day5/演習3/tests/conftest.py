# day5/演習3/tests/conftest.py
import os
import pickle
import pytest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# テスト用データとモデルを置くディレクトリ
DATA_PATH  = os.path.join(os.path.dirname(__file__), "../data/Titanic.csv")
MODEL_DIR  = os.path.join(os.path.dirname(__file__), "../models")
MODEL_PATH = os.path.join(MODEL_DIR, "titanic_model.pkl")


@pytest.fixture
def sample_data():
    """Titanic の CSV を読み込んで DataFrame を返す"""
    if not os.path.exists(DATA_PATH):
        from sklearn.datasets import fetch_openml
        titanic = fetch_openml("titanic", version=1, as_frame=True)
        df = titanic.data
        df["Survived"] = titanic.target.astype(int)
        df = df[
            ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked", "Survived"]
        ]
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)


@pytest.fixture
def preprocessor():
    """前処理器 ColumnTransformer を返す"""
    num_feats = ["Age", "Pclass", "SibSp", "Parch", "Fare"]
    cat_feats = ["Sex", "Embarked"]

    num_tr = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
    ])
    cat_tr = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot",  OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([
        ("num", num_tr, num_feats),
        ("cat", cat_tr, cat_feats),
    ])


@pytest.fixture
def train_model(sample_data, preprocessor):
    """
    学習済みモデル Pipeline と
    テスト用の (X_test, y_test) を返す
    """
    df = sample_data
    X = df.drop("Survived", axis=1)
    y = df["Survived"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
    ])
    model.fit(X_train, y_train)

    # モデルをディスクに保存
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    return model, X_test, y_test