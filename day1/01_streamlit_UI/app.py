import streamlit as st
import pandas as pd
import numpy as np
import time
import requests

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
st.markdown("### コメントを解除しながらStreamlitの機能を学びましょう")
st.markdown("このデモコードでは、コメントアウトされた部分を順番に解除しながらUIの変化を確認できます。")

# ============================================
# サイドバー 
# ============================================
st.sidebar.header("デモのガイド")
st.sidebar.info("コードのコメントを解除して、Streamlitのさまざまな機能を確認しましょう。")

# ============================================
# 基本的なUI要素
# ============================================
st.header("基本的なUI要素")

# テキスト入力
st.subheader("テキスト入力")
name = st.text_input("あなたの名前", "ゲスト")
st.write(f"こんにちは、{name}さん！")

# ボタン
# st.subheader("ボタン")
# if st.button("クリックしてください"):
#     st.success("ボタンがクリックされました！")

# チェックボックス
# st.subheader("チェックボックス")
# if st.checkbox("チェックを入れると追加コンテンツが表示されます"):
#     st.info("これは隠れたコンテンツです！")

# スライダー
# st.subheader("スライダー")
# age = st.slider("年齢", 0, 100, 25)
# st.write(f"あなたの年齢: {age}")

# セレクトボックス
# st.subheader("セレクトボックス")
# option = st.selectbox(
#     "好きなプログラミング言語は?",
#     ["Python", "JavaScript", "Java", "C++", "Go", "Rust"]
# )
# st.write(f"あなたは{option}を選びました")

# ============================================
# レイアウト
# ============================================
# st.header("レイアウト")

# カラム
# st.subheader("カラムレイアウト")
# col1, col2 = st.columns(2)
# with col1:
#     st.write("これは左カラムです")
#     st.number_input("数値を入力", value=10)
# with col2:
#     st.write("これは右カラムです")
#     st.metric("メトリクス", "42", "2%")

# タブ
# st.subheader("タブ")
# tab1, tab2 = st.tabs(["第1タブ", "第2タブ"])
# with tab1:
#     st.write("これは第1タブの内容です")
# with tab2:
#     st.write("これは第2タブの内容です")

# エクスパンダー
# st.subheader("エクスパンダー")
# with st.expander("詳細を表示"):
#     st.write("これはエクスパンダー内の隠れたコンテンツです")
#     st.code("print('Hello, Streamlit！')")

# ============================================
# データ表示
# ============================================
# st.header("データの表示")

# サンプルデータフレームを作成
# df = pd.DataFrame({
#     '名前': ['田中', '鈴木', '佐藤', '高橋', '伊藤'],
#     '年齢': [25, 30, 22, 28, 33],
#     '都市': ['東京', '大阪', '福岡', '札幌', '名古屋']
# })

# データフレーム表示
# st.subheader("データフレーム")
# st.dataframe(df, use_container_width=True)

# テーブル表示
# st.subheader("テーブル")
# st.table(df)

# メトリクス表示
st.subheader("明日の天気")

jma_url = "http://www.jma.go.jp/bosai/common/const/area.json"
jma_json = requests.get(jma_url).json()

regions = {region["name"] : region["children"]  for region in jma_json["centers"].values()}
col1, col2, col3 = st.columns(3)
option_region = col1.selectbox("地方", regions.keys(), index=2)

prefectures = {jma_json["offices"][prefecture]["name"] : prefecture for prefecture in regions[option_region]}
index = 5 if option_region=="関東甲信地方" else 0
option_prefecture = col2.selectbox("県", prefectures.keys(), index=index)

jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{prefectures[option_prefecture]}.json"
jma_json = requests.get(jma_url).json()
area = {area["area"]["name"] : i for i, area in enumerate(jma_json[0]["timeSeries"][0]["areas"])}
option_area = col3.selectbox("地域", area.keys())

weather = jma_json[0]["timeSeries"][0]["areas"][area[option_area]]["weathers"][1].split("　")[0]
weather_img = "☀️" if weather=="晴れ" else "☁️" if weather=="くもり" else "☔️" if weather=="雨"else weather

temp = jma_json[0]["timeSeries"][2]["areas"][area[option_area]]["temps"]
temp_tomorrow = temp[-1]
temp_diff = f"{int(temp_tomorrow) - int(temp[0])}°C" if len(temp)==4 else ""

pops = jma_json[0]["timeSeries"][1]["areas"][area[option_area]]["pops"]
pops_tomorrow = pops[-1]
pops_diff = int(pops_tomorrow) - int(pops[0])

col1, col2, col3 = st.columns(3)
col1.metric("天気", weather_img, "")
col2.metric("気温", f"{temp_tomorrow}°C", temp_diff)
col3.metric("降水確率", f"{pops_tomorrow}%", f"{pops_diff}%")

# col1, col2, col3 = st.columns(3)
# col1.metric("温度", "23°C", "1.5°C")
# col2.metric("湿度", "45%", "-5%")
# col3.metric("気圧", "1013hPa", "0.1hPa")

# ============================================
# グラフ表示
# ============================================
# st.header("グラフの表示")

# ラインチャート
# st.subheader("ラインチャート")
# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['A', 'B', 'C'])
# st.line_chart(chart_data)

# バーチャート
# st.subheader("バーチャート")
# chart_data = pd.DataFrame({
#     'カテゴリ': ['A', 'B', 'C', 'D'],
#     '値': [10, 25, 15, 30]
# }).set_index('カテゴリ')
# st.bar_chart(chart_data)

# ============================================
# インタラクティブ機能
# ============================================
# st.header("インタラクティブ機能")

# プログレスバー
# st.subheader("プログレスバー")
# progress = st.progress(0)
# if st.button("進捗をシミュレート"):
#     for i in range(101):
#         time.sleep(0.01)
#         progress.progress(i / 100)
#     st.balloons()

# ファイルアップロード
# st.subheader("ファイルアップロード")
# uploaded_file = st.file_uploader("ファイルをアップロード", type=["csv", "txt"])
# if uploaded_file is not None:
#     # ファイルのデータを表示
#     bytes_data = uploaded_file.getvalue()
#     st.write(f"ファイルサイズ: {len(bytes_data)} bytes")
#     
#     # CSVの場合はデータフレームとして読み込む
#     if uploaded_file.name.endswith('.csv'):
#         df = pd.read_csv(uploaded_file)
#         st.write("CSVデータのプレビュー:")
#         st.dataframe(df.head())

# ============================================
# カスタマイズ
# ============================================
# st.header("スタイルのカスタマイズ")

# カスタムCSS
# st.markdown("""
# <style>
# .big-font {
#     font-size:20px ！important;
#     font-weight: bold;
#     color: #0066cc;
# }
# </style>
# """, unsafe_allow_html=True)
# 
# st.markdown('<p class="big-font">これはカスタムCSSでスタイリングされたテキストです！</p>', unsafe_allow_html=True)

# ============================================
# デモの使用方法
# ============================================
st.divider()
st.subheader("このデモの使い方")
st.markdown("""
1. コードエディタでコメントアウトされた部分を見つけます（#で始まる行）
2. 確認したい機能のコメントを解除します（先頭の#を削除）
3. 変更を保存して、ブラウザで結果を確認します
4. 様々な組み合わせを試して、UIがどのように変化するか確認しましょう
""")

st.code("""
# コメントアウトされた例:
# if st.button("クリックしてください"):
#     st.success("ボタンがクリックされました！")

# コメントを解除した例:
if st.button("クリックしてください"):
    st.success("ボタンがクリックされました！")
""")