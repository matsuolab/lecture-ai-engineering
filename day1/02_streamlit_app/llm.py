# llm.py
import os
import torch
from transformers import pipeline
import streamlit as st
import time
from config import MODEL_NAME
from huggingface_hub import login

# モデルをキャッシュして再利用
@st.cache_resource
def load_model():
    """LLMモデルをロードする"""
    try:

        # アクセストークンを保存
        hf_token = st.secrets["huggingface"]["token"]
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        st.info(f"Using device: {device}") # 使用デバイスを表示
        pipe = pipeline(
            "text-generation",
            model=MODEL_NAME,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device=device
        )
        st.success(f"モデル '{MODEL_NAME}' の読み込みに成功しました。")
        return pipe
    except Exception as e:
        st.error(f"モデル '{MODEL_NAME}' の読み込みに失敗しました: {e}")
        st.error("GPUメモリ不足の可能性があります。不要なプロセスを終了するか、より小さいモデルの使用を検討してください。")
        return None

def generate_response(pipe, user_question, history=None):
    if pipe is None:
        return "モデルがロードされていないため、回答を生成できません。", 0

    try:
        import transformers
        start_time = time.time()

        is_chat_template = hasattr(pipe.tokenizer, "chat_template") and pipe.tokenizer.chat_template

        if is_chat_template:
            # Chatテンプレ対応モデル（Gemma, Llama2-chat）
            messages = []
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": user_question})

            outputs = pipe(
                messages,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )

            assistant_response = outputs[0]["generated_text"].strip()

        else:
            # Chatテンプレ非対応モデル（Calm-1b, Rinna）
            # → 履歴を渡さず、単発質問のみ
            prompt = user_question

            outputs = pipe(
                prompt,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )

            assistant_response = outputs[0]["generated_text"].strip()

            # プロンプト部分を除去（Calmは出力にプロンプトを含めがち）
            if prompt in assistant_response:
                assistant_response = assistant_response.replace(prompt, "").strip()

        end_time = time.time()
        response_time = end_time - start_time
        print(f"Generated response in {response_time:.2f}s")
        return assistant_response, response_time

    except Exception as e:
        st.error(f"回答生成中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return f"エラーが発生しました: {str(e)}", 0