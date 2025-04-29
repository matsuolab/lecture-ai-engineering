# app.py
import streamlit as st
import torch
from transformers import pipeline

import database
import data
import metrics
from config import MODEL_NAME
import ui

# --- アプリケーション全体設定 ---
st.set_page_config(page_title="Gemma Chatbot", layout="wide")
metrics.initialize_nltk()
database.init_db()
data.ensure_initial_data()

@st.cache_resource(show_spinner=False)
def load_pipeline():
    device = 0 if torch.cuda.is_available() else -1
    return pipeline(
        "text-generation",
        model=MODEL_NAME,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device=device
    )

pipe = load_pipeline()

# --- 上部タブ ナビゲーション ---
tab_chat, tab_history, tab_data = st.tabs(
    ["💬 チャット", "📜 履歴", "⚙️ データ管理"]
)

with tab_chat:
    ui.chat_ui(pipe)

with tab_history:
    ui.history_ui()

with tab_data:
    ui.data_ui()
