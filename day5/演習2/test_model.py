from joblib import load
from sklearn.metrics import accuracy_score
import pandas as pd

def test_model_accuracy():
    model = load("day5/演習2/models/model_for_ci.pkl")
    X_test = pd.read_csv("data/Titanic.csv").drop("Survived", axis=1)
    y_test = pd.read_csv("data/Titanic.csv")["Survived"]

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    assert acc >= 0.8, f"Accuracy too low: {acc}"
