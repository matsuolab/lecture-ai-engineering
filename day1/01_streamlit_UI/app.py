import streamlit as st
import pandas as pd
import numpy as np
import time


st.set_page_config(
    page_title="Streamlit",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f4f4f4; /* 全体の背景色 */
    }
    [data-testid="stHeader"] {
        background-color: #e0f2f7; /* ヘッダーの背景色 */
        padding: 1rem;
        border-bottom: 1px solid #b0bec5;
    }
    [data-testid="stSidebar"] {
        background-color: #eceff1; /* サイドバーの背景色 */
    }
    .st-expander {
        border: 1px solid #b0bec5;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .st-expander-content {
        padding-left: 20px;
    }
    .metric-container {
        padding: 15px;
        border-radius: 5px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("✨ Streamlit デモ ✨")
st.divider()


with st.sidebar:
    st.header("ナビゲーション")
    st.info("各機能のデモは、以下のリンクからアクセスできます。コードのコメントを解除して、様々な機能を試してみましょう。")
    st.markdown("[基本的なUI要素](#基本的なui要素)")
    st.markdown("[レイアウト](#レイアウト)")
    st.markdown("[データの表示](#データの表示)")
    st.markdown("[グラフの表示](#グラフの表示)")
    st.markdown("[インタラクティブ機能](#インタラクティブ機能)")
    st.markdown("[スタイルのカスタマイズ](#スタイルのカスタマイズ)")
    st.markdown("[デモの使い方](#このデモの使い方)")
    st.markdown("---")
    st.subheader("Streamlit 情報")
    st.info("[Streamlit 公式ドキュメント](https://docs.streamlit.io/)")
    st.info("[Streamlit Community](https://discuss.streamlit.io/)")


st.header("基本的なUI要素")
st.subheader("テキスト入力")
name = st.text_input("あなたの名前", "ゲスト")
st.info(f"入力された名前: **{name}**")

st.subheader("ボタン")
if st.button("🚀 クリックしてアクションを実行"):
    st.success("ボタンがクリックされました！")
    st.balloons() 

st.subheader("チェックボックス")
if st.checkbox("🎁 特別コンテンツを表示"):
    st.info("🎉 チェックを入れてくれてありがとう！特別な情報をお届けします。")
    st.markdown("このコンテンツはチェックボックスがオンの時のみ表示されます。")

st.subheader("スライダー")
age = st.slider("年齢を選択", 0, 100, 25)
st.info(f"選択された年齢: **{age}** 歳")

st.subheader("セレクトボックス")
option = st.selectbox(
    "📚 好きなプログラミング言語を選んでください",
    ["Python", "JavaScript", "Java", "C++", "Go", "Rust"]
)
st.info(f"選択された言語: **{option}**")
st.divider()

st.header("レイアウト")

st.subheader("カラムレイアウト")
col1, col2 = st.columns(2)
with col1:
    st.info("左側のカラムです。数値を入力してください。")
    number = st.number_input("数値を入力", value=10)
    st.write(f"入力された数値: {number}")
with col2:
    st.info("右側のカラムです。重要な指標を表示します。")
    st.metric(label="今日の訪問者数", value="1,250", delta="150")

st.subheader("タブ")
tab1, tab2 = st.tabs(["📊 データ", "⚙️ 設定"])
with tab1:
    st.info("データに関する情報を表示します。")
    st.write("ここでは、データフレームやグラフなどを表示できます。")
with tab2:
    st.info("アプリケーションの設定を行います。")
    st.slider("調整パラメータ", 0, 100, 50)

st.subheader("エクスパンダー")
with st.expander("詳細な説明を読む"):

    st.code("print('Hello, Streamlit!')", language="python")
st.divider()


st.header("データの表示")

df = pd.DataFrame({
    '名前': ['田中', '鈴木', '佐藤', '高橋', '伊藤'],
    '年齢': [25, 30, 22, 28, 33],
    '都市': ['東京', '大阪', '福岡', '札幌', '名古屋']
})

st.subheader("データフレーム")
st.info("Pandas DataFrame をインタラクティブに表示します。")
st.dataframe(df, use_container_width=True)

st.subheader("テーブル")
st.info("DataFrame を静的なテーブルとして表示します。")
st.table(df)


st.header("グラフの表示")

st.subheader("ラインチャート")
st.info("時系列データや連続データの変化を視覚的に表現します。")
chart_data_line = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C'])
st.line_chart(chart_data_line)

st.subheader("バーチャート")
st.info("カテゴリごとの値の大きさを比較するのに適しています。")
chart_data_bar = pd.DataFrame({
    'カテゴリ': ['A', 'B', 'C', 'D'],
    '値': [10, 25, 15, 30]
}).set_index('カテゴリ')
st.bar_chart(chart_data_bar)
st.divider()


st.header("インタラクティブ機能")

st.subheader("プログレスバー")
st.info("処理の進行状況を視覚的に示します。")
progress_bar = st.progress(0)
if st.button("⏳ 進捗を開始"):
    for i in range(101):
        time.sleep(0.01)
        progress_bar.progress(i)
    st.success("完了！")
    st.balloons()

st.subheader("ファイルアップロード")
st.info("CSVやテキストファイルをアップロードして、データを読み込むことができます。")
uploaded_file = st.file_uploader("ファイルをアップロード", type=["csv", "txt"])
if uploaded_file is not None:
    st.success("ファイルのアップロードに成功しました！")
    bytes_data = uploaded_file.getvalue()
    st.write(f"ファイルサイズ: {len(bytes_data)} バイト")

    if uploaded_file.name.endswith('.csv'):
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            st.subheader("アップロードされたCSVデータのプレビュー:")
            st.dataframe(df_uploaded.head())
        except Exception as e:
            st.error(f"CSVファイルの読み込みに失敗しました: {e}")
    else:
        string_data = bytes_data.decode("utf-8")
        st.subheader("アップロードされたテキストデータ:")
        st.text_area("テキスト内容", string_data, height=200)
st.divider()

st.header("スタイルのカスタマイズ")
st.info("カスタムCSSを適用して、アプリケーションの見た目を変更できます。")

st.markdown("""
<style>
.highlight-text {
    font-size: 20px !important;
    font-weight: bold;
    color: #2e7d32; /* 緑色 */
    background-color: #f1f8e9; /* 薄い緑色 */
    padding: 5px;
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="highlight-text">✨ これはカスタムCSSで強調されたテキストです！ ✨</p>', unsafe_allow_html=True)
st.divider()
