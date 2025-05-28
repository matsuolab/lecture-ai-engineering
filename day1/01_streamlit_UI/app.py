import streamlit as st
import pandas as pd
import numpy as np
import time

# ============================================
# ページ設定
# ============================================
st.set_page_config(
    page_title="Streamlit カスタムUIデモ",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': 'Enhanced UI demo with custom CSS'
    }
)

# ============================================
# カスタムCSS / テーマ
# ============================================
st.markdown("""
<style>
/* フォントと背景 */
body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background-color: #f5f7fa;
}

/* ヘッダースタイル */
.css-1v0mbdj {
    background-color: #0066cc !important;
    color: white !important;
    padding: 1rem 2rem;
    border-radius: 0 0 1rem 1rem;
}

/* .big-font を拡張 */
.big-font {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #0066cc !important;
    text-transform: uppercase;
    margin-bottom: 1em;
}

/* カード風コンテナ */
.card {
    background: white;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* サイドバーカスタム */
.stSidebar {
    background-color: #e1ecf7;
}

.stSidebar .sidebar-content {
    color: #003366;
}

/* ボタンカスタム */
.stButton > button {
    background-color: #0066cc;
    color: white;
    border-radius: 0.75rem;
    padding: 0.5rem 1.5rem;
    font-weight: bold;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #0052a3;
}

/* メトリクスカード */
.css-1hynsf2 {
    background-color: #ffffff;
    border-radius: 1rem;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ============================================
# ヘッダー
# ============================================
st.markdown('<h1 class="big-font">Streamlit カスタムUIデモ</h1>', unsafe_allow_html=True)
st.markdown('<p class="card">コメントを解除しながらStreamlitの機能を学びましょう。</p>', unsafe_allow_html=True)

# ============================================
# サイドバー 
# ============================================
st.sidebar.header("デモのガイド")
st.sidebar.info(
    "1. コメントを解除する\n"
    "2. UIの変化を確認する\n"
    "3. 自由にアレンジしよう!"
)

# ============================================
# 基本要素 in カード
# ============================================
st.markdown('<div class="card"><h2>基本的なUI要素</h2></div>', unsafe_allow_html=True)

# テキスト入力
st.markdown('<div class="card"><h3>テキスト入力</h3></div>', unsafe_allow_html=True)
name = st.text_input("あなたの名前", "ゲスト")
st.success(f"こんにちは、{name}さん！")

# ボタン
st.markdown('<div class="card"><h3>ボタン</h3></div>', unsafe_allow_html=True)
if st.button("クリックしてください"):
    st.balloons()
    st.success("ボタンがクリックされました！")

# チェックボックス
st.markdown('<div class="card"><h3>チェックボックス</h3></div>', unsafe_allow_html=True)
if st.checkbox("詳細を表示"):
    st.info("隠れたコンテンツがここに表示されます！")

# スライダー
st.markdown('<div class="card"><h3>スライダー</h3></div>', unsafe_allow_html=True)
age = st.slider("年齢", 0, 100, 25)
st.write(f"あなたの年齢: {age}")

# ============================================
# レイアウト: カラム & タブ
# ============================================
st.markdown('<div class="card"><h2>レイアウトサンプル</h2></div>', unsafe_allow_html=True)
col1, col2 = st.columns([2,1])
with col1:
    st.metric("温度", "23°C", "+1.5°C")
    st.metric("湿度", "45%", "-3%")
with col2:
    st.image("https://placekitten.com/200/200", caption="サンプル画像")

tab1, tab2 = st.tabs(["グラフ", "データ"])
with tab1:
    chart_data = pd.DataFrame(np.random.randn(20,3), columns=['A','B','C'])
    st.line_chart(chart_data)
with tab2:
    df = pd.DataFrame({
        '名前': ['田中','鈴木','佐藤'],
        '点数': [88, 92, 79]
    })
    st.table(df)

# ============================================
# プログレスバー
# ============================================
st.markdown('<div class="card"><h2>プログレスバー</h2></div>', unsafe_allow_html=True)
progress = st.progress(0)
if st.button("進捗をシミュレート"):
    for i in range(101):
        time.sleep(0.01)
        progress.progress(i)
    st.success("完了しました！🎉")

# ============================================
# フッター
# ============================================
st.divider()
st.markdown('<p style="text-align:center; color:#888;">© 2025 Streamlit カスタムUIデモ</p>', unsafe_allow_html=True)
