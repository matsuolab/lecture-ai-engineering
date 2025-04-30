import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ダッシュボード", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .main {
        padding: 2rem;
    }
    .card {
        background-color: #1c1f26;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
        text-align: center;
    }
    .hero {
        text-align: center;
        margin-bottom: 3rem;
    }
    .hero h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .hero p {
        font-size: 1.2rem;
        color: #9ca3af;
    }
    </style>
""", unsafe_allow_html=True)

# サイドバー
st.sidebar.title("メニュー")
st.sidebar.markdown("新規追加")

st.markdown('<div class="hero"><h1>データ可視化ダッシュボード</h1><p>リアルタイムデータ</p></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card"><h2>1000+</h2><p>ユーザー数</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card"><h2>87%</h2><p>満足度</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card"><h2>150</h2><p>レポート数</p></div>', unsafe_allow_html=True)

# チャートセクション
st.markdown("## データチャート")
st.line_chart({
    'データ1': [1, 5, 2, 6, 9, 4],
    'データ2': [2, 2, 7, 8, 5, 7]
})
