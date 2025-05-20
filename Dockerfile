# PythonベースのDockerイメージを使用
FROM python:3.11

# カレントディレクトリをそのまま作業ディレクトリにする
WORKDIR /workspace

# requirements.txt をコンテナにコピーしてインストール
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt



