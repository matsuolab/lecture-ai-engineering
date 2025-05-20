import time, json, pathlib, importlib

import pytest
import pandas as pd

# 例：src.model に Model クラスがある想定
@pytest.fixture(scope="session")
def model():
    mdl = importlib.import_module("src.model").Model.load("artifacts/model.joblib")
    return mdl

@pytest.fixture(scope="session")
def sample_df():
    return pd.read_csv("artifacts/sample.csv")
