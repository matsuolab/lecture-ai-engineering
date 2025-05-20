import os
import pickle
import random

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from mlflow.models.signature import infer_signature
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


# データ準備関数
def prepare_data(test_size=0.2, random_state=42):
    path = "data/Titanic.csv"
    data = pd.read_csv(path)

    data = data[["Pclass", "Sex", "Age", "Fare", "Survived"]].dropna()
    data["Sex"] = LabelEncoder().fit_transform(data["Sex"])

    data["Pclass"] = data["Pclass"].astype(float)
    data["Sex"] = data["Sex"].astype(float)
    data["Age"] = data["Age"].astype(float)
    data["Fare"] = data["Fare"].astype(float)
    data["Survived"] = data["Survived"].astype(float)

    X = data[["Pclass", "Sex", "Age", "Fare"]]
    y = data["Survived"]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)


# ランダムフォレスト学習
def train_and_evaluate(X_train, X_test, y_train, y_test, n_estimators=100, max_depth=None, random_state=42):
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    return model, accuracy


# ベースラインモデル作成
def create_baseline_model(X_train, y_train):
    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(X_train, y_train)
    return baseline


# MLflowでモデル記録
def log_model(model, accuracy, params, X_train, X_test):
    with mlflow.start_run():
        for k, v in params.items():
            mlflow.log_param(k, v)
        mlflow.log_metric("accuracy", accuracy)
        signature = infer_signature(X_train, model.predict(X_train))
        mlflow.sklearn.log_model(model, "model", signature=signature, input_example=X_test.iloc[:5])
        print(f"モデルのログ記録値 \naccuracy: {accuracy}\nparams: {params}")


# メイン処理
if __name__ == "__main__":
    # ランダムなハイパーパラメータ
    test_size = round(random.uniform(0.1, 0.3), 2)
    data_random_state = random.randint(1, 100)
    model_random_state = random.randint(1, 100)
    n_estimators = random.randint(50, 200)
    max_depth = random.choice([None, 3, 5, 10, 15])

    params = {
        "test_size": test_size,
        "data_random_state": data_random_state,
        "model_random_state": model_random_state,
        "n_estimators": n_estimators,
        "max_depth": "None" if max_depth is None else max_depth,
    }

    # データ準備
    X_train, X_test, y_train, y_test = prepare_data(test_size=test_size, random_state=data_random_state)

    # ランダムフォレスト学習
    model, accuracy = train_and_evaluate(X_train, X_test, y_train, y_test,
                                         n_estimators=n_estimators,
                                         max_depth=max_depth,
                                         random_state=model_random_state)

    # モデル記録（MLflow）
    log_model(model, accuracy, params, X_train, X_test)

    # モデル保存
    os.makedirs("models", exist_ok=True)
    with open("models/titanic_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("✅ titanic_model.pkl を保存しました")

    # ベースラインモデル保存（なければ作成）
    baseline_path = "models/baseline_model.pkl"
    if not os.path.exists(baseline_path):
        baseline_model = create_baseline_model(X_train, y_train)
        with open(baseline_path, "wb") as f:
            pickle.dump(baseline_model, f)
        print("✅ baseline_model.pkl を新規作成しました")
    else:
        print("ℹ️ baseline_model.pkl は既に存在します（再生成なし）")
