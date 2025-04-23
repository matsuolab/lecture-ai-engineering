# app.py
# import streamlit as st
# import ui                   # UIモジュール
# import llm                  # LLMモジュール
# import database             # データベースモジュール
# import metrics              # 評価指標モジュール
# import data                 # データモジュール
# import torch
# from transformers import pipeline
# from config import MODEL_NAME
# from huggingface_hub import HfFolder

# # --- アプリケーション設定 ---
# st.set_page_config(page_title="Gemma Chatbot", layout="wide")

# # --- 初期化処理 ---
# # NLTKデータのダウンロード（初回起動時など）
# metrics.initialize_nltk()

# # データベースの初期化（テーブルが存在しない場合、作成）
# database.init_db()

# # データベースが空ならサンプルデータを投入
# data.ensure_initial_data()

# # LLMモデルのロード（キャッシュを利用）
# # モデルをキャッシュして再利用
# @st.cache_resource
# def load_model():
#     """LLMモデルをロードする"""
#     try:
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         st.info(f"Using device: {device}") # 使用デバイスを表示
#         pipe = pipeline(
#             "text-generation",
#             model=MODEL_NAME,
#             model_kwargs={"torch_dtype": torch.bfloat16},
#             device=device
#         )
#         st.success(f"モデル '{MODEL_NAME}' の読み込みに成功しました。")
#         return pipe
#     except Exception as e:
#         st.error(f"モデル '{MODEL_NAME}' の読み込みに失敗しました: {e}")
#         st.error("GPUメモリ不足の可能性があります。不要なプロセスを終了するか、より小さいモデルの使用を検討してください。")
#         return None
# pipe = llm.load_model()

# # --- Streamlit アプリケーション ---
# st.title("🤖 Gemma 2 Chatbot with Feedback")
# st.write("Gemmaモデルを使用したチャットボットです。回答に対してフィードバックを行えます。")
# st.markdown("---")

# # --- サイドバー ---
# st.sidebar.title("ナビゲーション")
# # セッション状態を使用して選択ページを保持
# if 'page' not in st.session_state:
#     st.session_state.page = "チャット" # デフォルトページ

# page = st.sidebar.radio(
#     "ページ選択",
#     ["チャット", "履歴閲覧", "サンプルデータ管理"],
#     key="page_selector",
#     index=["チャット", "履歴閲覧", "サンプルデータ管理"].index(st.session_state.page), # 現在のページを選択状態にする
#     on_change=lambda: setattr(st.session_state, 'page', st.session_state.page_selector) # 選択変更時に状態を更新
# )


# # --- メインコンテンツ ---
# if st.session_state.page == "チャット":
#     if pipe:
#         ui.display_chat_page(pipe)
#     else:
#         st.error("チャット機能を利用できません。モデルの読み込みに失敗しました。")
# elif st.session_state.page == "履歴閲覧":
#     ui.display_history_page()
# elif st.session_state.page == "サンプルデータ管理":
#     ui.display_data_page()

# # --- フッターなど（任意） ---
# st.sidebar.markdown("---")
# st.sidebar.info("開発者: [Your Name]")

import streamlit as st
import os
import sys
import subprocess
import time
import requests
from llm import load_model
from ui import display_chat_page, display_history_page, display_data_page
from config import MODEL_NAME, AVAILABLE_MODELS


# ngrokの設定
def start_ngrok(port=8501):
    try:
        ngrok_token = st.secrets.get("ngrok", {}).get("token", "")
        if not ngrok_token:
            st.error("ngrokトークンが .streamlit/secrets.toml に設定されていません。")
            return None
        subprocess.run(["./ngrok", "authtoken", ngrok_token], check=True)
        ngrok_process = subprocess.Popen(["./ngrok", "http", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        response = requests.get("http://localhost:4040/api/tunnels")
        public_url = response.json()["tunnels"][0]["public_url"]
        st.success(f"ngrok公開URL: {public_url}")
        return public_url
    except Exception as e:
        st.error(f"ngrokトンネルの開始に失敗しました: {e}")
        return None


def main():
    st.set_page_config(page_title="AIチャットアプリ", layout="wide")

    public_url = start_ngrok()
    if public_url:
        st.markdown(f"[公開URLでアプリにアクセス]({public_url})")

    if "developer_name" not in st.session_state:
        st.session_state.developer_name = ""
    developer_name = st.sidebar.text_input("開発者名を入力してください", value=st.session_state.developer_name,
                                           key="developer_name_input")
    st.session_state.developer_name = developer_name
    if developer_name.strip():
        st.sidebar.info(f"開発者: {developer_name}")
    else:
        st.sidebar.info("開発者: 未入力")

    st.sidebar.header("モデル設定")
    # セッション状態で選択されたモデルを管理
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = MODEL_NAME

    model_name = st.sidebar.selectbox(
        "モデルを選択",
        options=list(AVAILABLE_MODELS.keys()),
        format_func=lambda x: AVAILABLE_MODELS[x],
        index=list(AVAILABLE_MODELS.keys()).index(st.session_state.selected_model)
    )
    # 選択されたモデルを更新
    st.session_state.selected_model = model_name

    quantization = st.sidebar.selectbox(
        "量子化オプション",
        options=["none", "4bit", "8bit"],
        index=0  # 預設啟用 4-bit 量子化
    )

    with st.spinner(f"モデル '{model_name}' をロード中..."):
        pipe = load_model(model_name, quantization)
        if pipe is None:
            st.error("モデルのロードに失敗しました。設定を確認してください。")
            return

    page = st.sidebar.radio(
        "ページを選択",
        ["チャット", "履歴", "データ管理"],
        label_visibility="collapsed"
    )

    # モデルの表示名を取得
    model_display_name = AVAILABLE_MODELS[st.session_state.selected_model]

    if page == "チャット":
        display_chat_page(pipe, model_display_name)  # 傳遞 model_display_name
    elif page == "履歴":
        display_history_page()
    elif page == "データ管理":
        display_data_page()


if __name__ == "__main__":
    main()