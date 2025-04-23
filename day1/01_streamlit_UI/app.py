import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time
from datetime import datetime

# ============================================
# ページ設定
# ============================================
st.set_page_config(
    page_title="拡張 Streamlit デモ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# タイトルと説明
# ============================================
st.title("✨ 拡張版 Streamlit 初心者向けデモアプリ")
st.markdown("### このデモでは、**Streamlitの様々なコンポーネントと機能**を一気に体験できます。")

# ============================================
# サイドバー 
# ============================================
st.sidebar.title("🔧 オプション設定")
theme = st.sidebar.radio("テーマを選択", ["ライト", "ダーク"])
show_extra = st.sidebar._checkbox("拡張セクションを表示", value=True)

# ============================================
# 基本的なUI要素
# ============================================
st.header("🧱 基本的なUI要素")

name = st.text_input("あなたの名前", "ゲスト")
toggle = st.toggle("秘密のスイッチ")
birthbay = st.date_input("誕生日を選択")
color = st.color_picker("好きな色を選んでください", "#00f900")
st.write(f"こんにちは、**{name}**さん！")

if toggle:
    st.success("スイッチがONになっています！")

# ============================================
# レイアウト
# ============================================
st.header("🧩 レイアウトと構造")
col1, col2, col3 = st.columns(3)
col1.metric("温度", "24°C", "+2.1°C")
col2.metric("湿度", "47%", "-3%")
col3.metric("気圧", "1012hPa", "+1.2")

with st.expander("📚 詳細を見る"):
    st.write("ここには詳細情報や補足説明を記載できます。")
    st.code("print('こんにちは')", language="python")

# ============================================
# データ表示
# ============================================
st.header("📊 データ表示")

df = pd.DataFrame({
    '名前': ['田中', '鈴木', '佐藤', '高橋', '伊藤'],
    '年齢': [25, 30, 22, 28, 33],
    '都市': ['東京', '大阪', '福岡', '札幌', '名古屋']
})
st.dataframe(df)

# ============================================
# グラフ表示
# ============================================
st.header("📈 グラフ表示")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)
st.line_chart(chart_data)

# Matplotlib
st.subheader("Matplotlib グラフ")
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [10, 20, 5, 15])
ax.set_title("Matplotlib Plot")

# plotly
st.subheader("Plotly グラフ")
fig2 = px.bar(x=["A", "B", "C"], y=[10, 20, 15])
st.plotly_chart(fig2)

# ============================================
# メディア表示
# ============================================
st.header("🖼️ メディア表示")

st.image("https://picsum.photos/600/300", caption="ランダム画像", use_container_width=True)
st.audio("https://file-examples.com/storage/fe01b89d1b6125a768c1bb1/2017/11/file_example_MP3_700KB.mp3")
st.video("https://www.youtube.com/watch?v=DLzxrzFCyOs")

# ============================================
# インタラクティブ＆セッション管理
# ============================================
st.header("🤖 チャット風UIと進捗")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message("user"):
        st.markdown(msg)

if user_input := st.chat_input("質問を入力してください"):
    st.session_state.messages.append(user_input)
    st.chat_message("assistant").markdown("これは自動応答のサンプルです 🤖")

if st.button("進捗バーを開始"):
    with st.spinner("処理中..."):
        for i in range(100):
            time.sleep(0.01)
            st.progress(i + 1)
        st.success("完了しました！")

# ============================================
# ファイルアップロードと表示
# ============================================
st.header("📂 ファイルアップロード")

uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])
if uploaded_file is not None:
    df_uploaded = pd.read_csv(uploaded_file)
    st.dataframe(df_uploaded)

# ============================================
# 使い方ガイド
# ============================================
st.divider()
st.markdown("📝 このアプリの使い方：")
st.markdown("""
- サイドバーで表示項目を切り替えたりテーマを選択できます。
- 各セクションのコンポーネントを試して、どんな表示が可能か確認しましょう。
- チャットやプログレスバー、画像・動画・音声などもサポートしています。
""")