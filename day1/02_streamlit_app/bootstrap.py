# .streamlit/secrets.toml ファイルを作成
import os
import toml

# 設定ファイル用ディレクトリを作る
os.makedirs('.streamlit', exist_ok=True)

# 環境変数からトークンを取得して辞書にまとめる
secrets = {
    "huggingface": {
        "token": os.environ.get("HUGGINGFACE_TOKEN", "")
    }
}

# .streamlit/secrets.toml に書き出し
with open('.streamlit/secrets.toml', 'w') as f:
    toml.dump(secrets, f)
