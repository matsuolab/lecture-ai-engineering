# # llm
# import os
# import torch
# import streamlit as st
# import time
# from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
# from config import MODEL_NAME, AVAILABLE_MODELS
# from huggingface_hub import login, whoami

# @st.cache_resource
# def load_model(model_name=MODEL_NAME, quantization="none"):
#     try:
#         hf_token = st.secrets["huggingface"]["token"]
#         login(hf_token)
#         try:
#             user_info = whoami(token=hf_token)
#             st.info(f"Hugging Faceにログインしました: {user_info['name']}")
#         except Exception as e:
#             st.error(f"Hugging Faceトークンの検証に失敗しました: {e}")
#             return None

#         if model_name not in AVAILABLE_MODELS:
#             st.error(f"無効なモデル識別子: {model_name}")
#             return None

#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         st.info(f"使用デバイス: {device}")

#         quantization_config = None
#         if quantization == "4bit" and device == "cuda":
#             try:
#                 from bitsandbytes import BitsAndBytesConfig
#                 quantization_config = BitsAndBytesConfig(
#                     load_in_4bit=True,
#                     bnb_4bit_compute_dtype=torch.bfloat16
#                 )
#                 st.info(f"'{model_name}' に4-bit量子化を適用します")
#             except ImportError:
#                 st.warning("bitsandbytesが利用できないため、量子化は無効です")
#                 quantization_config = None
#         elif quantization == "8bit" and device == "cuda":
#             try:
#                 from bitsandbytes import BitsAndBytesConfig
#                 quantization_config = BitsAndBytesConfig(
#                     load_in_8bit=True
#                 )
#                 st.info(f"'{model_name}' に8-bit量子化を適用します")
#             except ImportError:
#                 st.warning("bitsandbytesが利用できないため、量子化は無効です")
#                 quantization_config = None

#         tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
#         model = AutoModelForCausalLM.from_pretrained(
#             model_name,
#             torch_dtype=torch.bfloat16,
#             device_map="auto",
#             quantization_config=quantization_config,
#             token=hf_token
#         )

#         pipe = pipeline(
#             "text-generation",
#             model=model,
#             tokenizer=tokenizer,
#             device_map="auto"
#         )
#         st.success(f"モデル '{model_name}' のロードに成功しました")
#         return pipe
#     except Exception as e:
#         st.error(f"モデル '{model_name}' のロードに失敗しました: {e}")
#         return None

# def generate_response(pipe, user_question):
#     if pipe is None:
#         return "モデルがロードされていないため、回答を生成できません。", 0

#     try:
#         start_time = time.time()
#         messages = [{"role": "user", "content": user_question}]
#         outputs = pipe(
#             messages,
#             max_new_tokens=512,
#             do_sample=True,
#             temperature=0.7,
#             top_p=0.9,
#             return_full_text=False
#         )
#         assistant_response = outputs[0]["generated_text"][-1]["content"].strip() if outputs else "回答の抽出に失敗しました。"
#         end_time = time.time()
#         response_time = end_time - start_time
#         print(f"回答生成時間: {response_time:.2f}秒")
#         return assistant_response, response_time
#     except Exception as e:
#         st.error(f"回答生成中にエラーが発生しました: {e}")
#         return f"エラー: {str(e)}", 0


#         end_time = time.time()
#         response_time = end_time - start_time
#         print(f"Generated response in {response_time:.2f}s") # デバッグ用
#         return assistant_response, response_time

#     except Exception as e:
#         st.error(f"回答生成中にエラーが発生しました: {e}")
#         # エラーの詳細をログに出力
#         import traceback
#         traceback.print_exc()
#         return f"エラーが発生しました: {str(e)}", 0

import os
import torch
import streamlit as st
import time
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from config import MODEL_NAME, AVAILABLE_MODELS
from huggingface_hub import login, whoami

@st.cache_resource
def load_model(model_name=MODEL_NAME, quantization="none"):
    try:
        hf_token = st.secrets["huggingface"]["token"]
        login(hf_token)
        try:
            user_info = whoami(token=hf_token)
            st.info(f"Hugging Faceにログインしました: {user_info['name']}")
        except Exception as e:
            st.error(f"Hugging Faceトークンの検証に失敗しました: {e}")
            return None

        if model_name not in AVAILABLE_MODELS:
            st.error(f"無効なモデル識別子: {model_name}")
            return None

        device = "cuda" if torch.cuda.is_available() else "cpu"
        st.info(f"使用デバイス: {device}")

        quantization_config = None
        if quantization == "4bit" and device == "cuda":
            try:
                from bitsandbytes import BitsAndBytesConfig
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.bfloat16
                )
                st.info(f"'{model_name}' に4-bit量子化を適用します")
            except ImportError:
                st.warning("bitsandbytesが利用できないため、量子化は無効です")
                quantization_config = None
        elif quantization == "8bit" and device == "cuda":
            try:
                from bitsandbytes import BitsAndBytesConfig
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=True
                )
                st.info(f"'{model_name}' に8-bit量子化を適用します")
            except ImportError:
                st.warning("bitsandbytesが利用できないため、量子化は無効です")
                quantization_config = None

        tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            quantization_config=quantization_config,
            token=hf_token
        )

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device_map="auto"
        )
        st.success(f"モデル '{model_name}' のロードに成功しました")
        return pipe
    except Exception as e:
        st.error(f"モデル '{model_name}' のロードに失敗しました: {e}")
        return None

def generate_response(pipe, user_question):
    if pipe is None:
        return "モデルがロードされていないため、回答を生成できません。", 0

    try:
        start_time = time.time()
        messages = [{"role": "user", "content": user_question}]
        outputs = pipe(
            messages,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            return_full_text=False
        )
        assistant_response = outputs[0]["generated_text"][-1]["content"].strip() if outputs else "回答の抽出に失敗しました。"
        end_time = time.time()
        response_time = end_time - start_time
        print(f"回答生成時間: {response_time:.2f}秒")
        return assistant_response, response_time
    except Exception as e:
        st.error(f"回答生成中にエラーが発生しました: {e}")
        return f"エラー: {str(e)}", 0
