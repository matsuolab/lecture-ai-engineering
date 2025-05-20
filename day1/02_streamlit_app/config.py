# # config.py
# DB_FILE = "chat_feedback.db"
# MODEL_NAME = "google/gemma-2-2b-jpn-it"

# データベースファイルのパス
DB_FILE = "chat_history.db"

# デフォルトモデル
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"

# 利用可能なモデルリスト
AVAILABLE_MODELS = {
    # "mistralai/Mixtral-8x7B-Instruct-v0.1": "Mixtral-8x7B (高効率)",
    # LLaMA-3-8Bの権限がある場合、コメントを解除して追加
    # "meta-llama/Llama-3-8B": "LLaMA-3-8B (高精度)"
    "google/gemma-7b": "Gemma-7B (汎用)",
    "mistralai/Mistral-7B-Instruct-v0.3": "Mistral-7B (高効率)",
    "Qwen/Qwen2-7B-Instruct": "Qwen2-7B (多言語)"   
}
