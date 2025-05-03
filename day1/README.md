# day1 演習用ディレクトリ

このリポジトリは、StreamlitとFastAPIを使用したアプリケーションの開発および演習用のディレクトリです。

演習には、「Google Colab」を使うことを想定しています。

リポジトリ内の「day1_practice.ipynb」をGoogle Colabで開き、演習を行なってください。

- [Open with Colab](https://colab.research.google.com/github/matsuolab/lecture-ai-engineering/blob/master/day1/day1_practice.ipynb)

## 事前準備

演習を行うにあたり、下記の3つのアカウントを利用します。

持っていない方は事前に準備することをおすすめします。

[1] Huggingface

 1.1 https://huggingface.co/　の右上のSign Upより登録してください。

 1.2 https://huggingface.co/docs/hub/security-tokens 　を読み、アクセストークンの作り方を理解してください。

 1.3 演習ではgemmaを利用する予定です。ライセンス登録など必要な準備を済ませておいてください。

 https://huggingface.co/google/gemma-2-2b-jpn-it  「Access Gemma on Hugging Face」からライセンスへの同意をする。

[2] Github

 2.1 https://docs.github.com/ja/get-started/start-your-journey/creating-an-account-on-github の指示に従ってアカウントを作成してください。

[3] ngrok

 3.1 https://dashboard.ngrok.com/signup よりアカウントを作成してください。

 3.2 https://dashboard.ngrok.com/get-started/your-authtoken より認証済みトークンが取得できることを確認してください。

## ディレクトリ構成

以下の3つの主要なディレクトリに分かれています。

### 01_streamlit_UI
Streamlitの基本的なUI要素を学ぶためのデモアプリケーションが含まれています。

- **`app.py`**: Streamlitの基本的なUI要素やレイアウトを試すためのサンプルコード。
- **`requirements.txt`**: このアプリケーションを実行するために必要なPythonパッケージ。

### 02_streamlit_app
Streamlitを使用したLLM（大規模言語モデル）ベースのチャットボットアプリケーションが含まれています。

- **`app.py`**: アプリケーションのエントリーポイント。チャット機能、履歴閲覧、サンプルデータ管理のUIを提供します。
- **`ui.py`**: チャットページや履歴閲覧ページなど、アプリケーションのUIロジックを管理します。
- **`llm.py`**: LLMモデルのロードとテキスト生成を行うモジュール。
- **`database.py`**: SQLiteデータベースを使用してチャット履歴やフィードバックを保存・管理します。
- **`metrics.py`**: BLEUスコアやコサイン類似度など、回答の評価指標を計算するモジュール。
- **`data.py`**: サンプルデータの作成やデータベースの初期化を行うモジュール。
- **`config.py`**: アプリケーションの設定（モデル名やデータベースファイル名）を管理します。
- **`requirements.txt`**: このアプリケーションを実行するために必要なPythonパッケージ。

### 03_FastAPI
FastAPIを使用し、ローカルLLMをAPIサービス化する内容が含まれています。

- **`app.py`**: FastAPIを使用してLLMモデルを提供するAPIサーバー。モデルのロード、テキスト生成、ヘルスチェック機能を提供します。
- **`python-client.py`**: FastAPIで提供されるAPIを利用するPythonクライアントのサンプルコード。
- **`requirements.txt`**: このアプリケーションを実行するために必要なPythonパッケージ。

## セットアップと実行方法

### 1. 必要な依存関係のインストール
各ディレクトリに移動し、`requirements.txt` を使用して必要なパッケージをインストールしてください。

```bash
# 例: 01_streamlit_UI の依存関係をインストール
cd 01_streamlit_UI
pip install -r requirements.txt
```

### 2. アプリケーションの実行
#### Streamlitアプリケーション

01_streamlit_UI または 02_streamlit_app ディレクトリで以下を実行します。

```bash
streamlit run app.py
```

#### FastAPIアプリケーション

03_FastAPI ディレクトリで以下を実行します。

```bash
python app.py
```

### 3. APIクライアントの使用
03_FastAPI/python-client.py を実行して、FastAPIで提供されるAPIを利用できます。

```bash
python python-client.py
```

## 使用技術
- Streamlit: インタラクティブなWebアプリケーションを簡単に構築するためのフレームワーク。
- FastAPI: 高速なAPIを構築するためのPythonフレームワーク。
- Transformers: LLMモデルのロードとテキスト生成を行うライブラリ。
- SQLite: チャット履歴やフィードバックを保存するための軽量データベース。
- Pyngrok: ローカルサーバーをインターネットに公開するためのツール。

## 注意事項
- FastAPIアプリケーションで使用するモデルは、config.py に指定されたモデル名（例: google/gemma-2-2b-jpn-it）を使用します。モデルのサイズや必要なリソースに注意してください。
- Streamlitアプリケーションでは、フィードバック機能を使用してモデルの回答を評価できます。
