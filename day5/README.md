# day5 演習用ディレクトリ

第3回「MLOps」に関する演習用のディレクトリです。

# 演習の目的

本演習コンテンツでは、技術的な用語や仕組み（例：高度な実験管理や複雑なパイプライン処理など）の詳細な理解を目的とするのではなく、モデルの管理やAIシステムを継続的に取り扱うための方法を実際に体験することを主眼としています。

この体験を通じて、AIを継続的に扱うための仕組みや考え方を学び、実践的なスキルへの理解を深めることを目的とします。

# 演習概要
主な演習の流れは以下のようになっています。

1. 機械学習モデルの実験管理とパイプライン
2. 整合性テスト
3. CI(継続的インテクレーション)

本演習では、GPUを使用しないため、実行環境として「Google Colab」を前提としません。ご自身のPC等でPythonの実行環境を用意していただき、演習を行なっていただいて問題ありません。

# 事前準備
GitHubを使用した演習となるため、GitHubの「fork」、「clone」、「pull request」などの操作を行います。  
GitHubをご自身の演習環境上で使用できるようにしておいてください。  

「fork」、「clone」したスクリプトに対してgitコマンドで構成管理を行います。  
また、講師の環境ではGitHub CLIを使用する場合があります。  
必須ではありませんが、GitHub CLIを使えるようにしておくとGitHubの操作が楽に行える場合があります。

- GitHub CLIについて  
[https://docs.github.com/ja/github-cli/github-cli/about-github-cli](https://docs.github.com/ja/github-cli/github-cli/about-github-cli)

## 環境を用意できない方向け
「Google Colab」上でも演習を行うことは可能です。
演習内でMLflowというソフトウェアを使いUIを表示する際に、Google Colab上ではngrokを使用することになります。

GitHubを「Google Colab」上で使用できるようにするのに加え、day1の演習で使用したngrokを使用してMLflowのUIを表示しましょう。

### 参考情報
- Google Colab上でGitHubを使う  
   [https://zenn.dev/smiyawaki0820/articles/e346ca8b522356](https://zenn.dev/smiyawaki0820/articles/e346ca8b522356) 
- Google Colab上でMLflow UIを使う  
   [https://fight-tsk.blogspot.com/2021/07/mlflow-ui-google-colaboratory.html](https://fight-tsk.blogspot.com/2021/07/mlflow-ui-google-colaboratory.html)

# 演習内容
演習は大きく3つのパートに分かれています。
- 演習1: 機械学習モデルの実験管理とパイプライン
- 演習2: 整合性テスト
- 演習3: CI(継続的インテクレーション)

演習1と演習2は、day5フォルダ直下の「演習1」と「演習2」フォルダを使用します。

演習3は、リポジトリ直下の「.github」フォルダと、day5フォルダ直下の「演習3」フォルダを使用します。

演習に必要なライブラリは、day5フォルダ直下の「requirements.txt」ファイルに記載しています。各自の演習環境にインストールしてください。

## 演習1: 機械学習モデルの実験管理とパイプライン

### ゴール
- scikit-learn + MLflow + kedro を使用して、学習 → 評価 → モデル保存までのパイプラインを構築。
- パイプラインを動かす。

### 演習ステップ
1. **データ準備**  
   - Titanic データを使用  
   - データの取得 → 学習用・評価用に分割

2. **学習スクリプトの実装**  
   - ランダムフォレストによる学習処理  
   - 評価処理（accuracy）を関数化して構成

3. **モデル保存**  
   - MLflow を用いて学習済みモデルをトラッキング・保存

4. **オプション**  
   - MLflow UI による可視化 
   - パラメータ変更や再実行による再現性の確認・テスト

5. **パイプライン化**  
   - kedro を使って処理を Node 化して組み立て

#### 演習1で使用する主なコマンド
```bash
cd 演習1

python main.py
mlflow ui

python pipeline.py
```

---

## 演習2: 整合性テスト

### ゴール
- データの整合性チェック
- モデルの動作テスト

### 演習ステップ
1. **データテスト**  
   - pytest + great_expectations を使用  
   - データの型・欠損・値範囲を検証

2. **フォーマットチェック**  
   - black, flake8, などで静的コードチェックを実施

#### 演習2で使用する主なコマンド
```bash
cd 演習2

python main.py
pytest main.py

black main.py
```

## 演習3: CI(継続的インテクレーション)

### ゴール
- Python コードの静的検査・ユニットテストを含む CI 構築

1. **CI ツール導入**  
   - GitHub Actions を使用  
   - `.github/workflows/test.yml` を作成

1. **CI 結果確認**  
   - プルリクエスト時に自動でチェックを実行 

#### 演習3で使用する主なコマンド
GitHub CLIを使用した場合のプルリクエストの流れ

```bash
git branch develop
git checkout develop
gh repo set-default
gh pr create
```

# 宿題の関連情報
## CIでのテストケースを追加する場合のアイディアサンプル

1. **モデルテスト**  
   - モデルの推論精度（再現性）や推論時間を検証

2. **差分テスト**  
   - 過去バージョンと比較して性能の劣化がないか確認  
   - 例: `accuracy ≥ baseline`
