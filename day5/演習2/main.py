import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pickle
import time
import great_expectations as gx


class DataLoader:
    """データロードを行うクラス"""

    @staticmethod
    def load_titanic_data(path=None):
        """Titanicデータセットを読み込む"""
        if path:
            return pd.read_csv(path)
        else:
            # ローカルのファイル
            script_dir = os.path.dirname(os.path.abspath(__file__))
            absolute_local_path = os.path.join(script_dir, "data", "Titanic.csv")
            if os.path.exists(absolute_local_path):
                return pd.read_csv(absolute_local_path)

    @staticmethod
    def preprocess_titanic_data(data):
        """Titanicデータを前処理する"""
        # 必要な特徴量を選択
        data = data.copy()

        # 不要な列を削除
        columns_to_drop = []
        for col in ["PassengerId", "Name", "Ticket", "Cabin"]:
            if col in data.columns:
                columns_to_drop.append(col)

        if columns_to_drop:
            data.drop(columns_to_drop, axis=1, inplace=True)

        # 目的変数とその他を分離
        if "Survived" in data.columns:
            y = data["Survived"]
            X = data.drop("Survived", axis=1)
            return X, y
        else:
            return data, None


class DataValidator:
    """データバリデーションを行うクラス"""

    @staticmethod
    def validate_titanic_data(data):
        """Titanicデータセットの検証"""
        # DataFrameに変換
        if not isinstance(data, pd.DataFrame):
            return False, ["データはpd.DataFrameである必要があります"]

        # Great Expectationsを使用したバリデーション
        try:
            context = gx.get_context()
            data_source = context.data_sources.add_pandas("pandas")
            data_asset = data_source.add_dataframe_asset(name="pd dataframe asset")

            batch_definition = data_asset.add_batch_definition_whole_dataframe(
                "batch definition"
            )
            batch = batch_definition.get_batch(batch_parameters={"dataframe": data})

            results = []

            # 必須カラムの存在確認
            required_columns = [
                "Pclass",
                "Sex",
                "Age",
                "SibSp",
                "Parch",
                "Fare",
                "Embarked",
            ]
            missing_columns = [
                col for col in required_columns if col not in data.columns
            ]
            if missing_columns:
                print(f"警告: 以下のカラムがありません: {missing_columns}")
                return False, [{"success": False, "missing_columns": missing_columns}]

            expectations = [
                gx.expectations.ExpectColumnDistinctValuesToBeInSet(
                    column="Pclass", value_set=[1, 2, 3]
                ),
                gx.expectations.ExpectColumnDistinctValuesToBeInSet(
                    column="Sex", value_set=["male", "female"]
                ),
                gx.expectations.ExpectColumnValuesToBeBetween(
                    column="Age", min_value=0, max_value=100
                ),
                gx.expectations.ExpectColumnValuesToBeBetween(
                    column="Fare", min_value=0, max_value=600
                ),
                gx.expectations.ExpectColumnDistinctValuesToBeInSet(
                    column="Embarked", value_set=["C", "Q", "S", ""]
                ),
            ]

            for expectation in expectations:
                result = batch.validate(expectation)
                results.append(result)

            # すべての検証が成功したかチェック
            is_successful = all(result.success for result in results)
            return is_successful, results

        except Exception as e:
            print(f"Great Expectations検証エラー: {e}")
            return False, [{"success": False, "error": str(e)}]


class ModelTester:
    """モデルテストを行うクラス"""

    @staticmethod
    def create_preprocessing_pipeline():
        """前処理パイプラインを作成"""
        numeric_features = ["Age", "Fare", "SibSp", "Parch"]
        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_features = ["Pclass", "Sex", "Embarked"]
        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features),
            ],
            remainder="drop",  # 指定されていない列は削除
        )
        return preprocessor

    @staticmethod
    def train_model(X_train, y_train, model_params=None):
        """モデルを学習する"""
        if model_params is None:
            model_params = {"n_estimators": 100, "random_state": 42}

        # 前処理パイプラインを作成
        preprocessor = ModelTester.create_preprocessing_pipeline()

        # モデル作成
        model = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", RandomForestClassifier(**model_params)),
            ]
        )

        # 学習
        model.fit(X_train, y_train)
        return model

    @staticmethod
    def evaluate_model(model, X_test, y_test):
        """モデルを評価する"""
        start_time = time.time()
        y_pred = model.predict(X_test)
        inference_time = time.time() - start_time

        accuracy = accuracy_score(y_test, y_pred)
        return {"accuracy": accuracy, "inference_time": inference_time}

    @staticmethod
    def save_model(model, path="models/titanic_model.pkl"):
        model_dir = "models"
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, f"titanic_model.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        return path

    @staticmethod
    def load_model(path="models/titanic_model.pkl"):
        """モデルを読み込む"""
        with open(path, "rb") as f:
            model = pickle.load(f)
        return model

    @staticmethod
    def compare_with_baseline(current_metrics, baseline_threshold=0.75):
        """ベースラインと比較する"""
        return current_metrics["accuracy"] >= baseline_threshold


# テスト関数（pytestで実行可能）
def test_data_validation():
    """データバリデーションのテスト"""
    # データロード
    data = DataLoader.load_titanic_data()
    X, y = DataLoader.preprocess_titanic_data(data)

    # 正常なデータのチェック
    success, results = DataValidator.validate_titanic_data(X)
    assert success, "データバリデーションに失敗しました"

    # 異常データのチェック
    bad_data = X.copy()
    bad_data.loc[0, "Pclass"] = 5  # 明らかに範囲外の値
    success, results = DataValidator.validate_titanic_data(bad_data)
    assert not success, "異常データをチェックできませんでした"


def test_model_performance():
    """モデル性能のテスト"""
    # データ準備
    data = DataLoader.load_titanic_data()
    X, y = DataLoader.preprocess_titanic_data(data)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # モデル学習
    model = ModelTester.train_model(X_train, y_train)

    # 評価
    metrics = ModelTester.evaluate_model(model, X_test, y_test)

    # ベースラインとの比較
    assert ModelTester.compare_with_baseline(
        metrics, 0.75
    ), f"モデル性能がベースラインを下回っています: {metrics['accuracy']}"

    # 推論時間の確認
    assert metrics["inference_time"] < 1.0, f"推論時間が長すぎます: {metrics['inference_time']}秒"


if __name__ == "__main__":
    # データロード
    data = DataLoader.load_titanic_data()
    X, y = DataLoader.preprocess_titanic_data(data)

    # データバリデーション
    success, results = DataValidator.validate_titanic_data(X)
    print(f"データ検証結果: {'成功' if success else '失敗'}")
    for result in results:
        # "success": falseの場合はエラーメッセージを表示
        if not result["success"]:
            print(f"異常タイプ: {result['expectation_config']['type']}, 結果: {result}")
    if not success:
        print("データ検証に失敗しました。処理を終了します。")
        exit(1)

    # モデルのトレーニングと評価
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # パラメータ設定
    model_params = {"n_estimators": 100, "random_state": 42}

    # モデルトレーニング
    model = ModelTester.train_model(X_train, y_train, model_params)
    metrics = ModelTester.evaluate_model(model, X_test, y_test)

    print(f"精度: {metrics['accuracy']:.4f}")
    print(f"推論時間: {metrics['inference_time']:.4f}秒")

    # モデル保存
    model_path = ModelTester.save_model(model)

    # ベースラインとの比較
    baseline_ok = ModelTester.compare_with_baseline(metrics)
    print(f"ベースライン比較: {'合格' if baseline_ok else '不合格'}")

import os  # os.path.exists を使うために必要
import pandas as pd  # DataLoader, preprocess_titanic_data が pandas を使うため
from sklearn.model_selection import train_test_split  # train_test_split を使うため

# (main.pyの他の必要なimport文 ... DataLoader, ModelTesterなど)
# この関数がmain.py内にある前提で、DataLoaderやModelTesterは既にインポートされているとします。
# もしこの関数を別ファイルにする場合は、必要なクラスのimport文を追加してください。


def test_inference_speed_and_accuracy():
    """学習済みモデルの推論時間と精度をチェックする関数"""
    print("\n--- 学習済みモデルの推論時間と精度のテスト開始 ---")

    # --- 合格基準の設定 ---
    # これらの値は必要に応じて調整してください
    TARGET_ACCURACY = 0.80  # 例: 精度の目標値 (80%以上で合格)
    TARGET_INFERENCE_TIME_SECONDS = 0.05  # 例: 推論時間の目標値 (0.05秒以内で合格)
    # ---------------------

    # 1. データロードと前処理
    try:
        data_full = DataLoader.load_titanic_data()
        if data_full is None:
            print("エラー: データファイル (data/Titanic.csv想定) のロードに失敗しました。")
            print("スクリプトと同じ階層に 'data' フォルダがあり、その中に 'Titanic.csv' があるか確認してください。")
            print("--- 推論時間と精度のテスト中止 ---")
            return
    except Exception as e:
        print(f"データロード中に予期せぬエラーが発生しました: {e}")
        print("--- 推論時間と精度のテスト中止 ---")
        return

    X_full, y_full = DataLoader.preprocess_titanic_data(data_full)

    if y_full is None:
        print("エラー: データに目的変数 'Survived' が見つかりません。精度評価ができません。")
        print("--- 推論時間と精度のテスト中止 ---")
        return

    _, X_test, _, y_test = train_test_split(
        X_full, y_full, test_size=0.2, random_state=42
    )

    # 2. モデルのロード
    model_path = "models/titanic_model.pkl"
    if not os.path.exists(model_path):
        print(f"エラー: 学習済みモデルファイルが見つかりません: {model_path}")
        print(f"メイン処理 (if __name__ == '__main__': ブロック) を実行して、モデルを学習・保存してください。")
        print("--- 推論時間と精度のテスト中止 ---")
        return

    try:
        model = ModelTester.load_model(path=model_path)
        print(f"モデルをロードしました: {model_path}")
    except FileNotFoundError:
        print(f"エラー: モデルファイル '{model_path}' のロードに失敗しました。ファイルが存在しません。")
        print("--- 推論時間と精度のテスト中止 ---")
        return
    except Exception as e:
        print(f"モデルのロード中に予期せぬエラーが発生しました: {e}")
        print("--- 推論時間と精度のテスト中止 ---")
        return

    # 3. モデル評価 (推論時間と精度)
    print(f"ロードされたモデルを使用して、テストデータで評価を行います...")
    metrics = ModelTester.evaluate_model(model, X_test, y_test)
    actual_accuracy = metrics["accuracy"]
    actual_inference_time = metrics["inference_time"]

    # 4. 結果の表示と合否判定
    print(f"\n評価結果:")
    print(f"  実際の精度: {actual_accuracy:.4f} (目標: {TARGET_ACCURACY:.4f} 以上)")
    print(
        f"  実際の推論時間: {actual_inference_time:.4f}秒 (目標: {TARGET_INFERENCE_TIME_SECONDS:.4f}秒 以下)"
    )

    print("\n合否判定:")
    # 精度の判定
    if actual_accuracy >= TARGET_ACCURACY:
        print(f"  ◎ 精度: 合格！ ({actual_accuracy:.4f} >= {TARGET_ACCURACY:.4f})")
    else:
        print(f"  × 精度: 不合格… ({actual_accuracy:.4f} < {TARGET_ACCURACY:.4f})")

    # 推論時間の判定
    if actual_inference_time <= TARGET_INFERENCE_TIME_SECONDS:
        print(
            f"  ◎ 推論時間: 合格！ ({actual_inference_time:.4f}秒 <= {TARGET_INFERENCE_TIME_SECONDS:.4f}秒)"
        )
    else:
        print(
            f"  × 推論時間: 不合格… ({actual_inference_time:.4f}秒 > {TARGET_INFERENCE_TIME_SECONDS:.4f}秒)"
        )

    baseline_threshold = 0.75
    baseline_ok = ModelTester.compare_with_baseline(
        metrics, baseline_threshold=baseline_threshold
    )
    print(f"  ベースライン比較 (閾値 {baseline_threshold}): {'合格' if baseline_ok else '不合格'}")

    print("\n--- 学習済みモデルの推論時間と精度のテスト終了 ---")
