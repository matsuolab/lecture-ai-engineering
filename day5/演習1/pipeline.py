from kedro.io import MemoryDataset, KedroDataCatalog
from kedro.pipeline import Pipeline, node
from kedro.runner import SequentialRunner
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import os
import random
import logging

# ロガーの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# データ準備
def prepare_data():
    try:
        # Titanicデータセットの読み込み
        path = "data/Titanic.csv"
        if not os.path.exists(path):
            raise FileNotFoundError(f"データファイルが見つかりません: {path}")

        data = pd.read_csv(path)
        logger.info(f"データを読み込みました。行数: {len(data)}")

        # 必要な特徴量の選択と前処理
        data = data[["Pclass", "Sex", "Age", "Fare", "Survived"]].dropna()
        logger.info(f"欠損値削除後の行数: {len(data)}")

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
            X, y, test_size=0.2, random_state=42
        )
        logger.info(
            f"トレーニングデータ: {X_train.shape}, テストデータ: {X_test.shape}"
        )
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logger.error(f"データ準備中にエラーが発生しました: {str(e)}")
        raise


# 学習と評価
def train_and_evaluate(X_train, X_test, y_train, y_test):
    try:
        # ハイパーパラメータの設定
        params = {
            "n_estimators": random.randint(50, 200),
            "max_depth": random.choice([None, 3, 5, 10, 15]),
            "min_samples_split": 2,
            "random_state": 42,
        }

        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        logger.info(f"モデルの精度: {accuracy:.4f}")
        return model, accuracy, params
    except Exception as e:
        logger.error(f"モデル学習中にエラーが発生しました: {str(e)}")
        raise


# モデル保存
def log_model(model, accuracy, params, X_train, X_test):
    try:
        # 実験名の設定
        mlflow.set_experiment("titanic-survival-prediction")

        with mlflow.start_run():
            # メトリクスのロギング
            mlflow.log_metric("accuracy", accuracy)

            # ハイパーパラメータのロギング
            mlflow.log_params(params)

            # 重要な特徴量のロギング
            feature_importances = model.feature_importances_
            for i, feature in enumerate(X_train.columns):
                mlflow.log_metric(
                    f"feature_importance_{feature}", feature_importances[i]
                )

            # モデルのシグネチャを推論
            signature = infer_signature(X_train, model.predict(X_train))

            # モデルを保存
            mlflow.sklearn.log_model(
                model,
                "model",
                signature=signature,
                input_example=X_test.iloc[:5],  # 入力例を指定
            )

            # アーティファクトの場所を取得してログに出力
            run_id = mlflow.active_run().info.run_id
            logger.info(f"モデルを記録しました。Run ID: {run_id}")
            logger.info(f"精度: {accuracy:.4f}")
    except Exception as e:
        logger.error(f"MLflowでのモデル記録中にエラーが発生しました: {str(e)}")
        raise


# Kedro パイプラインの定義
def create_pipeline():
    return Pipeline(
        [
            node(
                prepare_data,
                inputs=None,
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="prepare_data",
            ),
            node(
                train_and_evaluate,
                inputs=["X_train", "X_test", "y_train", "y_test"],
                outputs=["model", "accuracy", "params"],
                name="train_and_evaluate",
            ),
            node(
                log_model,
                inputs=["model", "accuracy", "params", "X_train", "X_test"],
                outputs=None,
                name="log_model",
            ),
        ]
    )


if __name__ == "__main__":
    try:
        # パイプラインの作成
        pipeline = create_pipeline()

        # データカタログの作成
        catalog = KedroDataCatalog(
            {
                "X_train": MemoryDataset(),
                "X_test": MemoryDataset(),
                "y_train": MemoryDataset(),
                "y_test": MemoryDataset(),
                "model": MemoryDataset(),
                "accuracy": MemoryDataset(),
                "params": MemoryDataset(),
            }
        )

        # Kedro ランナーの作成
        runner = SequentialRunner()

        # パイプラインの実行
        logger.info("パイプラインの実行を開始します。")
        runner.run(pipeline, catalog)
        logger.info("パイプラインの実行が完了しました。")
    except Exception as e:
        logger.error(f"パイプラインの実行中にエラーが発生しました: {str(e)}")
