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

# データの読み込みや前処理を行うクラス
class DataLoader:
    """データロードを行うクラス"""

    @staticmethod
    def load_titanic_data(path=None):
        """
        Titanicデータセットを読み込む静的メソッド
        引数:
            path: 読み込みたいCSVファイルのパス（省略可能）
        戻り値:
            pandas.DataFrame
        """
        if path:
            # 指定されたパスがあれば、それを使って読み込む
            return pd.read_csv(path)
        else:
            # パスが指定されていない場合、既定のローカルファイルを使用
            local_path = "data/Titanic.csv"
            if os.path.exists(local_path):
                return pd.read_csv(local_path)

    @staticmethod
    def preprocess_titanic_data(data):
        """
        Titanicデータを前処理する静的メソッド
        引数:
            data: 読み込んだDataFrame
        戻り値:
            X: 説明変数のDataFrame
            y: 目的変数（生存したか）のSeries（存在しない場合はNone）
        """
        # 元のデータを壊さないようにコピーを作る
        data = data.copy()

        # 不要な列（乗客ID、名前、チケット番号、キャビン）を削除対象に
        columns_to_drop = []
        for col in ["PassengerId", "Name", "Ticket", "Cabin"]:
            if col in data.columns:
                columns_to_drop.append(col)

        # 実際に存在する不要列だけ削除する
        if columns_to_drop:
            data.drop(columns_to_drop, axis=1, inplace=True)

        # 'Survived'（生存フラグ）があれば、それを目的変数yとして分離
        if "Survived" in data.columns:
            y = data["Survived"]
            X = data.drop("Survived", axis=1)
            return X, y
        else:
            # 予測時など、目的変数がない場合はyをNoneにして返す
            return data, None
        
class DataValidator:
    """データバリデーションを行うクラス"""

    @staticmethod
    def validate_titanic_data(data):
        """Titanicデータセットの検証を行う静的メソッド"""

        # データがDataFrame型であるかを確認
        if not isinstance(data, pd.DataFrame):
            return False, ["データはpd.DataFrameである必要があります"]

        # Great Expectationsを使ったバリデーション処理
        try:
            # コンテキストを取得（プロジェクト設定などを管理）
            context = gx.get_context()

            # Pandas用データソースを追加
            data_source = context.data_sources.add_pandas("pandas")

            # データ資産（データフレーム）を定義
            data_asset = data_source.add_dataframe_asset(name="pd dataframe asset")

            # 全体データを使ったバッチ定義を作成
            batch_definition = data_asset.add_batch_definition_whole_dataframe(
                "batch definition"
            )

            # 検証対象のバッチ（1回の検証対象データ）を取得
            batch = batch_definition.get_batch(batch_parameters={"dataframe": data})

            # 検証結果を格納するリスト
            results = []

            # 必須カラムを定義
            required_columns = [
                "Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked",
            ]

            # データ内に存在しないカラムを抽出
            missing_columns = [
                col for col in required_columns if col not in data.columns
            ]

            # 必須カラムが不足していたら失敗として返す
            if missing_columns:
                print(f"警告: 以下のカラムがありません: {missing_columns}")
                return False, [{"success": False, "missing_columns": missing_columns}]

            # 期待される条件（expectation）を定義
            expectations = [
                # Pclass は 1, 2, 3 のいずれか
                gx.expectations.ExpectColumnDistinctValuesToBeInSet(
                    column="Pclass", value_set=[1, 2, 3]
                ),
                # Sex は male または female
                gx.expectations.ExpectColumnDistinctValuesToBeInSet(
                    column="Sex", value_set=["male", "female"]
                ),
                # Age は 0〜100 の範囲
                gx.expectations.ExpectColumnValuesToBeBetween(
                    column="Age", min_value=0, max_value=100
                ),
                # Fare（運賃）は 0〜600 の範囲
                gx.expectations.ExpectColumnValuesToBeBetween(
                    column="Fare", min_value=0, max_value=600
                ),
                # Embarked（乗船地）は C, Q, S または空欄
                gx.expectations.ExpectColumnDistinctValuesToBeInSet(
                    column="Embarked", value_set=["C", "Q", "S", ""]
                ),
            ]

            # 各expectationをバッチに対して実行して結果を記録
            for expectation in expectations:
                result = batch.validate(expectation)
                results.append(result)

            # 全てのバリデーションが成功しているか確認
            is_successful = all(result.success for result in results)

            # 成否と結果一覧を返す
            return is_successful, results

        except Exception as e:
            # 予期せぬエラーが発生した場合の処理
            print(f"Great Expectations検証エラー: {e}")
            return False, [{"success": False, "error": str(e)}]
        

class ModelTester:
    """モデルテストを行うクラス"""

    @staticmethod
    def create_preprocessing_pipeline():
        """前処理パイプラインを作成する静的メソッド"""
        
        # 数値特徴量を定義
        numeric_features = ["Age", "Fare", "SibSp", "Parch"]
        
        # 数値特徴量の前処理：欠損値補完（中央値）→標準化
        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        # カテゴリ特徴量を定義
        categorical_features = ["Pclass", "Sex", "Embarked"]

        # カテゴリ特徴量の前処理：欠損補完（最頻値）→ワンホットエンコーディング
        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        # 数値とカテゴリの処理をまとめたカラム変換パイプライン
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features),
            ],
            remainder="drop",  # 指定していない列は削除
        )

        return preprocessor

    @staticmethod
    def train_model(X_train, y_train, model_params=None):
        """モデルを学習する静的メソッド"""

        # パラメータが指定されていなければデフォルト値を使う
        if model_params is None:
            model_params = {"n_estimators": 100, "random_state": 42}

        # 前処理パイプラインを作成
        preprocessor = ModelTester.create_preprocessing_pipeline()

        # モデル全体：前処理 + ランダムフォレスト
        model = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", RandomForestClassifier(**model_params)),
            ]
        )
        
        print("モデルの学習を開始します...")

        # 学習を実行
        model.fit(X_train, y_train)
        return model

    @staticmethod
    def evaluate_model(model, X_test, y_test):
        """モデルを評価する静的メソッド"""

        # 推論開始時刻
        start_time = time.time()

        # 予測
        y_pred = model.predict(X_test)

        # 推論にかかった時間を計測
        inference_time = time.time() - start_time

        # 正解率を計算
        accuracy = accuracy_score(y_test, y_pred)

        return {"accuracy": accuracy, "inference_time": inference_time}

        @staticmethod
    def save_model(model, path="models/titanic_model.pkl"):
        """学習済みモデルを保存する静的メソッド"""

        # 保存先ディレクトリを作成（なければ作る）
        model_dir = "models"
        os.makedirs(model_dir, exist_ok=True)

        # 保存パスを構成
        model_path = os.path.join(model_dir, f"titanic_model.pkl")

        # モデルを pickle で保存
        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        return path

    @staticmethod
    def load_model(path="models/titanic_model.pkl"):
        """保存されたモデルを読み込む静的メソッド"""

        with open(path, "rb") as f:
            model = pickle.load(f)

        return model

    @staticmethod
    def compare_with_baseline(current_metrics, baseline_threshold=0.75):
        """
        現在のモデルの精度がベースライン以上かを判定する静的メソッド
        """
        return current_metrics["accuracy"] >= baseline_threshold


# pytestで実行可能な関数（関数名が test_ で始まることが条件）
def test_data_validation():
    """データバリデーションのテスト"""

    # Titanicデータを読み込む（ローカル or パス指定）
    data = DataLoader.load_titanic_data()

    # 読み込んだデータを前処理して、説明変数Xと目的変数yに分割
    X, y = DataLoader.preprocess_titanic_data(data)

    # -------------------------------
    # 【正常データ】のバリデーション
    # -------------------------------
    # 正常なデータに対してバリデーションを実行
    success, results = DataValidator.validate_titanic_data(X)

    # バリデーションが成功していることを期待（成功しないとAssertionError）
    assert success, "データバリデーションに失敗しました"

    # -------------------------------
    # 【異常データ】のバリデーション
    # -------------------------------
    # データをコピーして意図的に異常な値を注入（Pclassに存在しない値 5）
    bad_data = X.copy()
    bad_data.loc[0, "Pclass"] = 5

    # 異常なデータを検証
    success, results = DataValidator.validate_titanic_data(bad_data)

    # バリデーションが失敗していることを期待（成功してしまったらエラー）
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
    assert (
        metrics["inference_time"] < 1.0
    ), f"推論時間が長すぎます: {metrics['inference_time']}秒"


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
