import os
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import random
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import LabelEncoder
from mlflow.models.signature import infer_signature

from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import OneHotEncoder



# データ準備
def prepare_data(test_size=0.2, random_state=42):
    # Titanicデータセットの読み込み
    path = "data/Titanic.csv"
    data = pd.read_csv(path)

    # 必要な特徴量の選択と前処理
    data = data[["Pclass", "Sex", "Age", "Fare", "Survived"]].dropna()
    data["Sex"] = LabelEncoder().fit_transform(data["Sex"])  # 性別を数値に変換

    # 整数型の列を浮動小数点型に変換
    data["Pclass"] = data["Pclass"].astype(float)
    data["Sex"] = data["Sex"].astype(float)
    data["Age"] = data["Age"].astype(float)
    data["Fare"] = data["Fare"].astype(float)
    data["Survived"] = data["Survived"].astype(float)

    X = data[["Pclass", "Sex", "Age", "Fare"]]
    y = data["Survived"]

    # データ分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


# 学習と評価
"""def train_and_evaluate(
    X_train, X_test, y_train, y_test, n_estimators=100, max_depth=None, random_state=42
):
    model = RandomForestClassifier(
        n_estimators=n_estimators, max_depth=max_depth, random_state=random_state
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return model, accuracy"""

def train_and_evaluate(
    X_train, X_test, y_train, y_test, n_estimators=100, max_depth=None, random_state=42
):
    # 前処理用の数値／カテゴリ特徴量リスト取得
    numeric_features = X_train.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X_train.select_dtypes(exclude=[np.number]).columns.tolist()

    # 前処理パイプライン
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])
    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

    # モデル＆パイプライン作成
    base_clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", base_clf)
    ])

    # ハイパーパラメータチューニング（簡易的にn_estimatorsとmax_depthを周辺探索）
    param_grid = {
        "classifier__n_estimators": [n_estimators, n_estimators * 2],
        "classifier__max_depth": [max_depth, 5, 10]
    }
    grid = GridSearchCV(
        pipeline, param_grid, cv=5, scoring="accuracy", n_jobs=-1
    )
    grid.fit(X_train, y_train)
    best_model = grid.best_estimator_

    # 評価
    preds = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    # （必要ならF1なども出力ログに残せます）
    # f1 = f1_score(y_test, preds, average='binary')
    # print(classification_report(y_test, preds))

    return best_model, accuracy


# モデル保存
def log_model(model, accuracy, params):
    with mlflow.start_run():
        # パラメータをログ
        for param_name, param_value in params.items():
            mlflow.log_param(param_name, param_value)

        # メトリクスをログ
        mlflow.log_metric("accuracy", accuracy)

        # モデルのシグネチャを推論
        signature = infer_signature(X_train, model.predict(X_train))

        # モデルを保存
        mlflow.sklearn.log_model(
            model,
            "model",
            signature=signature,
            input_example=X_test.iloc[:5],  # 入力例を指定
        )
        # accurecyとparmsは改行して表示
        print(f"モデルのログ記録値 \naccuracy: {accuracy}\nparams: {params}")


# メイン処理
if __name__ == "__main__":
    # ランダム要素の設定
    test_size = round(
        random.uniform(0.1, 0.3), 2
    )  # 10%〜30%の範囲でテストサイズをランダム化
    data_random_state = random.randint(1, 100)
    model_random_state = random.randint(1, 100)
    n_estimators = random.randint(50, 200)
    max_depth = random.choice([None, 3, 5, 10, 15])

    # パラメータ辞書の作成
    params = {
        "test_size": test_size,
        "data_random_state": data_random_state,
        "model_random_state": model_random_state,
        "n_estimators": n_estimators,
        "max_depth": "None" if max_depth is None else max_depth,
    }

    # データ準備
    X_train, X_test, y_train, y_test = prepare_data(
        test_size=test_size, random_state=data_random_state
    )

    # 学習と評価
    model, accuracy = train_and_evaluate(
        X_train,
        X_test,
        y_train,
        y_test,
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=model_random_state,
    )

    # モデル保存
    log_model(model, accuracy, params)

    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, f"titanic_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"モデルを {model_path} に保存しました")
