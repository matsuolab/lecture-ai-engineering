import os
import pickle
import pytest
from sklearn.metrics import accuracy_score
import pandas as pd

CURRENT_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "../models/titanic_model.pkl"
)
REFERENCE_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "../models/old_model.pkl"
)
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Titanic.csv")


@pytest.fixture
def test_data():
    df = pd.read_csv(DATA_PATH)
    X = df.drop("Survived", axis=1)
    y = df["Survived"].astype(int)
    return X, y


def test_model_performance_regression(test_data):
    X, y = test_data

    if not os.path.exists(REFERENCE_MODEL_PATH):
        pytest.skip("過去モデルが存在しないためスキップします")

    with open(REFERENCE_MODEL_PATH, "rb") as f:
        reference_model = pickle.load(f)
    with open(CURRENT_MODEL_PATH, "rb") as f:
        current_model = pickle.load(f)

    acc_reference = accuracy_score(y, reference_model.predict(X))
    acc_current = accuracy_score(y, current_model.predict(X))

    assert (
        acc_current >= acc_reference
    ), f"新モデルの精度が過去モデルを下回っています（{acc_current:.2f} < {acc_reference:.2f}）"
