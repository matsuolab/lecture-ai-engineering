# app.py
import streamlit as st
import ui                   # UIモジュール
import llm                  # LLMモジュール
import database             # データベースモジュール
import metrics              # 評価指標モジュール
import data                 # データモジュール
import torch
from transformers import pipeline
from config import MODEL_NAME
from huggingface_hub import HfFolder

# --- アプリケーション設定 ---
st.set_page_config(page_title="🤖 Gemma Chatbot", layout="wide", page_icon="🤖")

# --- 初期化処理 ---
metrics.initialize_nltk()
database.init_db()
data.ensure_initial_data()

# --- モデルロード（キャッシュ利用） ---
@st.cache_resource
def load_model():
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        with st.spinner(f"デバイス {device} でモデルをロード中..."):
            pipe = pipeline(
                "text-generation",
                model=MODEL_NAME,
                model_kwargs={"torch_dtype": torch.bfloat16},
                device=device
            )
        st.success(f"✅ モデル '{MODEL_NAME}' の読み込みに成功しました。")
        return pipe
    except Exception as e:
        st.error(f"❌ モデル '{MODEL_NAME}' の読み込みに失敗しました: {e}")
        st.info("💡 不要なプロセスを閉じるか、小さいモデルに切り替えてください。")
        return None

pipe = llm.load_model()

# --- ヘッダー ---
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🤖 Gemma 2 Chatbot with Feedback</h1>
    <p style='text-align: center;'>Gemmaモデルで動くスマートなチャットボット体験へようこそ！</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# --- サイドバー ---
with st.sidebar:
    st.title("📚 ナビゲーション")
    st.markdown("---")

    if 'page' not in st.session_state:
        st.session_state.page = "チャット"  # デフォルトページ

    page = st.radio(
        "📄 ページ選択",
        ["チャット", "履歴閲覧", "サンプルデータ管理"],
        key="page_selector",
        index=["チャット", "履歴閲覧", "サンプルデータ管理"].index(st.session_state.page),
        on_change=lambda: setattr(st.session_state, 'page', st.session_state.page_selector)
    )

    st.markdown("---")
    st.caption("🛠️ 開発者: Your Name")

# --- メインコンテンツ ---
if st.session_state.page == "チャット":
    if pipe:
        ui.display_chat_page(pipe)
    else:
        st.error("⚠️ モデルロードに失敗したため、チャット機能が利用できません。")
elif st.session_state.page == "履歴閲覧":
    ui.display_history_page()
elif st.session_state.page == "サンプルデータ管理":
    ui.display_data_page()

# --- フッター（任意） ---
st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
