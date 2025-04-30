import streamlit as st
import pandas as pd
import numpy as np
import time

# ============================================
# ページ設定
# ============================================
# st.set_page_config(
#     page_title="Streamlit デモ",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# ============================================
# タイトルと説明
# ============================================
st.title("Streamlit 初心者向けデモ")

# ============================================
# 基本的なUI要素
# ============================================

# テキスト入力
st.subheader("テキスト入力")
name = st.text_input("あなたの名前", "ゲスト")
date = st.date_input("今日の日付")
f_date = f"{date.year}年{date.month}月{date.day}日"
st.write(f"こんにちは、{name}さん！今日は{f_date}です。")

# ボタン
st.subheader("雪ボタン")
if st.button("クリックしてください。雪が降ります。"):
    st.snow()

# スライダー
st.subheader("スライダー")
age = st.slider("年齢", 0, 100, 25)
st.write(f"あなたの年齢: {age}")

# セレクトボックス
st.subheader("セレクトボックス")
option = st.selectbox(
    "好きな料理の種類は?",
    ["和食", "洋食", "中華料理", "フランス料理", "イタリア料理", "韓国料理"]
)
st.write(f"あなたは{option}を選びました")

# ============================================
# レイアウト
# ============================================


# タブ
st.subheader("タブ")
tab1, tab2, tab3 = st.tabs(["メトリクス", "バーチャート", "ラインチャート"])
with tab1:
    st.subheader("メトリクス")
    col1, col2, col3 = st.columns(3)
    col1.metric("温度", "23°C", "1.5°C")
    col2.metric("湿度", "45%", "-5%")
    col3.metric("気圧", "1013hPa", "0.1hPa")
with tab2:
    st.subheader("バーチャート")
    chart_data = pd.DataFrame({
      'カテゴリ': ['A', 'B', 'C', 'D'],
      '値': [10, 25, 15, 30]
      }).set_index('カテゴリ')
    st.bar_chart(chart_data)
with tab3:
    st.subheader("ラインチャート")
    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C'])
    st.line_chart(chart_data)



# ============================================
# データ表示
# ============================================

# サンプルデータフレームを作成
df = pd.DataFrame({
    '名前': ['田中', '鈴木', '佐藤', '高橋', '伊藤'],
    '年齢': [25, 30, 22, 28, 33],
    '都市': ['東京', '大阪', '福岡', '札幌', '名古屋']
})

# テーブル表示
st.subheader("テーブル")
st.table(df)

# ============================================
# インタラクティブ機能
# ============================================
st.header("インタラクティブ機能")

#プログレスバー
st.subheader("プログレスバー")
progress = st.progress(0)
if st.button("進捗をシミュレート"):
    for i in range(101):
        time.sleep(0.01)
        progress.progress(i / 100)
    st.balloons()

#ファイルアップロード
st.subheader("ファイルアップロード")
uploaded_file = st.file_uploader("ファイルをアップロード", type=["csv", "txt"])
if uploaded_file is not None:
    # ファイルのデータを表示
    bytes_data = uploaded_file.getvalue()
    st.write(f"ファイルサイズ: {len(bytes_data)} bytes")
    
    # CSVの場合はデータフレームとして読み込む
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.write("CSVデータのプレビュー:")
        st.dataframe(df.head())
