# llm.py
import streamlit as st
import os
import time
import torch
import streamlit as st
from transformers import pipeline
from huggingface_hub import login
from config import MODEL_NAME

# ── ここに「必ず中学生にもわかるように例えを入れて解説する」システムプロンプトを定義
SYSTEM_PROMPT = (
    "【システム】これから中学生にもわかるように、"
    "例えを交えて丁寧に説明してください。\n"
)
@st.cache_resource
def load_model():
    """
    LLMモデルをロードし、パイプラインをキャッシュする。
    Hugging Face トークンのログイン処理もここで実施。
    """
    # HF トークンを取得してログイン（.streamlit/secrets.toml に設定しておくこと）
    hf_token = os.environ["HUGGINGFACE_TOKEN"]
    login(token=hf_token)

    # デバイス設定
    device = "cuda" if torch.cuda.is_available() else "cpu"
    st.info(f"Using device: {device}")

    # テキスト生成パイプラインを構築
    pipe = pipeline(
        # ここでモデルの種類を指定するが、まだ未定
        "text-generation",
        model=MODEL_NAME,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device=device,)
    st.success(f"モデル '{MODEL_NAME}' の読み込みに成功しました。")
    return pipe

pipe = load_model()

def generate_response(
    user_question: str,
    max_new_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9
) -> tuple[str, float]:
    """
    ユーザーの質問にシステムプロンプトを先行付与し、
    モデルから回答を取得する。

    Returns:
      (回答文字列, 応答時間[s])
    """
    # 1) システムプロンプト + ユーザークエリ を結合
    prompt = SYSTEM_PROMPT + user_question

    # 2) モデル呼び出し＆時間計測
    start_time = time.time()
    outputs = pipe(
        prompt,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        top_p=top_p
    )
    elapsed = time.time() - start_time

    # 3) 出力からシステムプロンプト部分を削って回答部分だけ抽出
    full_text = outputs[0]["generated_text"]
    answer = full_text[len(SYSTEM_PROMPT):].strip()

    return answer, elapsed