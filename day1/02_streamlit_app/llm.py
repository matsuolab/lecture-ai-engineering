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
            # model_kwargs={"torch_dtype": torch.bfloat16},
            # Qwen models might benefit from trust_remote_code=True depending on implementation
            # trust_remote_code=True, 
            device=device
        )
        st.success(f"モデル '{MODEL_NAME}' の読み込みに成功しました。")
        return pipe
    except Exception as e:
        st.error(f"モデル '{MODEL_NAME}' の読み込みに失敗しました: {e}")
        st.error("GPUメモリ不足の可能性があります。不要なプロセスを終了するか、より小さいモデルの使用を検討してください。")
        return None

def generate_response(pipe, user_question):
    """LLMを使用して質問に対する回答を生成する"""
    if pipe is None:
        return "モデルがロードされていないため、回答を生成できません。", 0

    try:
        start_time = time.time()
        messages = [
            # Define the chat messages for the model
            # Note: Qwen models might expect a specific chat template structure.
            # The pipeline usually handles this, but manual formatting might be needed if issues arise.
            {"role": "user", "content": user_question},
        ]
        # Generate response using the pipeline
        # Consider adding return_full_text=False if you only want the generated part,
        # but the default (True) is often easier to parse robustly.
        outputs = pipe(messages, max_new_tokens=512, do_sample=True, temperature=0.7, top_p=0.9) # return_full_text=True is often default

        # --- Response Parsing Logic ---
        assistant_response = ""
        if outputs and isinstance(outputs, list) and outputs[0].get("generated_text"):
            generated_output = outputs[0]["generated_text"]

            if isinstance(generated_output, list):
                # Case 1: Output is a list of message dictionaries (e.g., chat format)
                # Find the last message from the assistant
                for msg in reversed(generated_output):
                    if msg.get("role") == "assistant":
                        assistant_response = msg.get("content", "").strip()
                        break
            elif isinstance(generated_output, str):
                # Case 2: Output is a single string containing the conversation
                full_text = generated_output
                # Try to find the text *after* the last user message in the input
                last_user_message_content = messages[-1]['content']
                # Find the *last* occurrence of the user message content in the full text
                last_occurrence_index = full_text.rfind(last_user_message_content)

                if last_occurrence_index != -1:
                    # Extract text after the last user message
                    response_start_index = last_occurrence_index + len(last_user_message_content)
                    possible_response = full_text[response_start_index:].strip()

                    # Basic cleanup: remove potential special tokens if needed (adjust based on model)
                    # Example: Qwen might use <|im_end|> or similar tokens.
                    # This is a basic example; more robust parsing might be needed.
                    # possible_response = possible_response.replace("<|im_end|>", "").strip()
                    # possible_response = possible_response.split("<|im_start|>")[0].strip() # Example

                    assistant_response = possible_response
                else:
                    # Fallback if the user message isn't found (e.g., if return_full_text=False was used unexpectedly)
                    # Or if the output format is completely different.
                    assistant_response = full_text # Use the full text as a fallback, might contain prompt

        # --- Fallback/Error Handling ---
        if not assistant_response:
             # Log the full output for debugging if parsing failed
             print(f"Warning: Could not extract assistant response. Full output: {outputs}")
             assistant_response = "回答の抽出に失敗しました。モデルの出力形式を確認してください。"

        end_time = time.time()
        response_time = end_time - start_time
        print(f"Generated response in {response_time:.2f}s") # デバッグ用
        return assistant_response, response_time

    except Exception as e:
        st.error(f"回答生成中にエラーが発生しました: {e}")
        # エラーの詳細をログに出力
        import traceback
        traceback.print_exc()
        return f"エラーが発生しました: {str(e)}", 0
