# llm.py
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer # Changed import
import streamlit as st
import time
from config import MODEL_NAME
from huggingface_hub import login

# モデルとトークナイザーをキャッシュして再利用
@st.cache_resource
def load_model_and_tokenizer(): # Renamed function
    """LLMモデルとトークナイザーをロードする"""
    try:
        # アクセストークンを環境変数やsecretsから取得する場合
        # hf_token = st.secrets.get("huggingface", {}).get("token")
        # if hf_token:
        #     login(token=hf_token)
        # else:
        #     st.warning("Hugging Faceトークンが見つかりません。モデルのダウンロードに認証が必要な場合があります。")

        st.info(f"Loading model: {MODEL_NAME}") # Loading message
        # Load tokenizer and model using AutoClass
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype="auto", # Use auto dtype as per example
            device_map="auto"   # Use auto device mapping
        )
        st.success(f"モデル '{MODEL_NAME}' とトークナイザーの読み込みに成功しました。")
        return model, tokenizer # Return both
    except Exception as e:
        st.error(f"モデル '{MODEL_NAME}' の読み込みに失敗しました: {e}")
        st.error("GPUメモリ不足、モデル名の誤り、またはネットワーク接続を確認してください。")
        return None, None

def generate_response(model, tokenizer, user_question): # Updated arguments
    """LLMを使用して質問に対する回答を生成する"""
    if model is None or tokenizer is None:
        return "モデルまたはトークナイザーがロードされていないため、回答を生成できません。", 0

    try:
        start_time = time.time()

        # Prepare input using chat template
        messages = [
            {"role": "user", "content": user_question},
        ]
        # enable_thinking=True is default, explicitly setting for clarity if needed
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            # enable_thinking=True # Optional: Switches between thinking and non-thinking modes. Default is True.
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        # Generate response
        # Keep max_new_tokens reasonable for chat, 32768 is too large
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512, # Adjusted max_new_tokens
            # Parameters from Gemma example, adjust if needed for Qwen
            # do_sample=True,
            # temperature=0.7,
            # top_p=0.9
        )
        # Extract only the generated tokens, excluding the input prompt
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()

        # Decode the response, handling potential thinking content (though not explicitly used here yet)
        # Qwen3 uses 151668 for </think>
        try:
            think_token_id = 151668
            # Find the last occurrence of the think token ID
            index = len(output_ids) - output_ids[::-1].index(think_token_id)
        except ValueError:
            index = 0 # If </think> token is not found

        # Decode thinking content (optional, can be logged or ignored)
        thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
        # Decode the main content
        content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

        # If thinking content exists, print/log it (optional)
        if thinking_content:
            print(f"Thinking content: {thinking_content}") # Log thinking content

        assistant_response = content # Use the decoded content

        end_time = time.time()
        response_time = end_time - start_time
        print(f"Generated response in {response_time:.2f}s") # デバッグ用
        return assistant_response, response_time

    except Exception as e:
        st.error(f"回答生成中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return f"エラーが発生しました: {str(e)}", 0