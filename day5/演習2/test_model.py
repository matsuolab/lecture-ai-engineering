from joblib import load
from sklearn.metrics import accuracy_score
import pandas as pd

def test_model_accuracy():
    model = load("day5/演習2/models/model_for_ci.pkl")
    df = pd.read_csv("day5/演習2/data/Titanic_for_ci.csv")
    X_test = df.drop("Survived", axis=1)
    y_test = df["Survived"]

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    assert acc >= 0.8, f"Accuracy too low: {acc}"
