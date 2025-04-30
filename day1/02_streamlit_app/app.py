# app.py
import streamlit as st
import ui
import llm
import database
import metrics
import data
import torch
from transformers import pipeline
from config import MODEL_NAME
from huggingface_hub import HfFolder

# --- ページ設定 ---
st.set_page_config(page_title="Gemma Dashboard", layout="wide")

st.markdown("""
<style>
/* グローバル設定 */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #f8fafc;
    transition: all 0.5s ease-in-out;
}

/* サイドバー */
section[data-testid="stSidebar"] {
    background: rgba(30, 41, 59, 0.8);
    backdrop-filter: blur(8px);
    border-right: 2px solid #334155;
}
section[data-testid="stSidebar"] .css-1d391kg {
    padding: 2rem 1rem;
}
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span {
    color: #cbd5e1;
}

/* ページタイトル */
h1, h2, h3, h4 {
    color: #38bdf8;
    font-weight: 700;
}

/* カードデザイン */
.card {
    background-color: #1e293b;
    padding: 1.5rem;
    border-radius: 1.5rem;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 2rem;
    transition: transform 0.3s;
}
.card:hover {
    transform: translateY(-5px);
}

/* チャット吹き出し */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
}
.user-message, .ai-message {
    max-width: 70%;
    padding: 1rem 1.5rem;
    border-radius: 1.5rem;
    font-size: 1rem;
    line-height: 1.5;
    word-wrap: break-word;
    transition: all 0.3s ease;
}
.user-message {
    background: linear-gradient(135deg, #3b82f6, #60a5fa);
    color: #ffffff;
    align-self: flex-start;
}
.ai-message {
    background: linear-gradient(135deg, #64748b, #94a3b8);
    color: #ffffff;
    align-self: flex-end;
}

/* フェードアニメーション */
.main {
    animation: fadeIn 0.8s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px);}
    to { opacity: 1; transform: translateY(0);}
}

/* レスポンシブ調整 */
@media (max-width: 768px) {
    .user-message, .ai-message {
        max-width: 90%;
        font-size: 0.95rem;
    }
}
</style>
""", unsafe_allow_html=True)



# --- 初期化 ---
metrics.initialize_nltk()
database.init_db()
data.ensure_initial_data()

# --- モデルロード ---
@st.cache_resource
def load_model():
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        st.toast(f"Using device: {device}")
        pipe = pipeline(
            "text-generation",
            model=MODEL_NAME,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device=device
        )
        st.success(f"✅ モデル '{MODEL_NAME}' 読み込み完了")
        return pipe
    except Exception as e:
        st.error(f"❌ モデル読み込み失敗: {e}")
        return None

pipe = llm.load_model()

# --- サイドバー ---
st.sidebar.title("📚 ナビゲーション")
if 'page' not in st.session_state:
    st.session_state.page = "チャット"

page = st.sidebar.radio(
    "ページ選択",
    ["チャット", "履歴閲覧", "サンプルデータ管理"],
    key="page_selector",
    index=["チャット", "履歴閲覧", "サンプルデータ管理"].index(st.session_state.page),
    on_change=lambda: setattr(st.session_state, 'page', st.session_state.page_selector)
)

st.sidebar.markdown("---")
st.sidebar.caption("🚀 開発者: [Your Name]")

# --- メインエリア ---
# --- Streamlit アプリケーション ---
st.title("💬✨ Gemma 2 Chatbot Dashboard")
st.write("あなた専用AIアシスタント - Gemmaモデルでチャットしよう！")
st.markdown("---")

if st.session_state.page == "チャット":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if pipe:
        ui.display_chat_page(pipe)
    else:
        st.error("チャット機能を利用できません。")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "履歴閲覧":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    ui.display_history_page()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "サンプルデータ管理":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    ui.display_data_page()
    st.markdown('</div>', unsafe_allow_html=True)
