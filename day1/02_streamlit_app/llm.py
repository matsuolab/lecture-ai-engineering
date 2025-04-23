# llm.py
import os
import time
import torch
import streamlit as st
from transformers import pipeline
from huggingface_hub import login

# -------------------------------------------------------------------
# 1. Hugging Face アクセストークンのログイン
# -------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def _hf_login():
    """Hugging Face のアクセストークンで一度だけログインする"""
    try:
        hf_token = st.secrets["huggingface"]["token"]
        login(token=hf_token, add_to_git_credential=True)
    except Exception as e:
        st.warning(f"Hugging Face へのログインに失敗しました: {e}")

# -------------------------------------------------------------------
# 2. モデルのロード
# -------------------------------------------------------------------
@st.cache_resource(show_spinner="モデルをロード中です…")
def load_model(model_name: str):
    """model_name を指定して text-generation パイプをロード"""
    _hf_login()                          # ← 一度だけ実行
    device = "cuda" if torch.cuda.is_available() else "cpu"
    st.info(f"Using device: {device}")

    try:
        pipe = pipeline(
            "text-generation",
            model=model_name,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device=device,
        )
        st.success(f"モデル '{model_name}' を読み込みました。")
        return pipe
    except Exception as e:
        st.error(f"モデル '{model_name}' の読み込みに失敗: {e}")
        return None

# -------------------------------------------------------------------
# 3. 文章生成
# -------------------------------------------------------------------
def generate_response(pipe, user_question: str):
    """与えられた pipe で回答を生成し、(text, 秒) を返す"""
    if pipe is None:
        return "モデルがロードされていないため、回答を生成できません。", 0.0

    try:
        start = time.time()
        messages = [{"role": "user", "content": user_question}]
        outputs  = pipe(messages, max_new_tokens=512,
                        do_sample=True, temperature=0.7, top_p=0.9)

        # --- Gemma / Llama-3 で共通的に“最後の assistant 出力”を抽出 ---
        assistant_response = ""
        if outputs and isinstance(outputs, list):
            gen = outputs[0].get("generated_text")
            if isinstance(gen, list) and gen and gen[-1].get("role") == "assistant":
                assistant_response = gen[-1].get("content", "").strip()
            elif isinstance(gen, str):
                assistant_response = gen.strip()

        if not assistant_response:
            assistant_response = "回答の抽出に失敗しました。"

        return assistant_response, (time.time() - start)

    except Exception as e:
        st.error(f"回答生成中にエラー: {e}")
        return f"エラーが発生しました: {e}", 0.0
