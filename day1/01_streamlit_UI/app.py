import streamlit as st
import pandas as pd
import numpy as np
import time
from io import StringIO

# ============================================
# ページ設定
# ============================================
st.set_page_config(
    page_title="Streamlit デザインデモ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# タイトルと説明
# ============================================
st.title("Streamlit デザインデモ")
st.markdown("### Streamlit UI要素とレイアウトの確認")

# ============================================
# サイドバー
# ============================================
st.sidebar.header("ナビゲーション")
st.sidebar.info("各タブでStreamlitの機能を確認できます。")

# ============================================
# メインコンテンツ (タブで整理)
# ============================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "基本UI", "レイアウト", "データ表示", "グラフ", "インタラクティブ", "カスタマイズ"
])

with tab1:
    st.header("基本的なUI要素")

    # テキスト入力
    st.subheader("テキスト入力")
    name = st.text_input("あなたの名前", "ゲスト")
    st.write(f"こんにちは、{name}さん！")
    st.divider()

    # ボタン
    st.subheader("ボタン")
    if st.button("クリックしてください"):
        st.success("ボタンがクリックされました！")
    st.divider()

    # チェックボックス
    st.subheader("チェックボックス")
    if st.checkbox("チェックを入れると追加コンテンツが表示されます"):
        st.info("これは隠れたコンテンツです！")
    st.divider()

    # スライダー
    st.subheader("スライダー")
    age = st.slider("年齢", 0, 100, 25)
    st.write(f"あなたの年齢: {age}")
    st.divider()

    # セレクトボックス
    st.subheader("セレクトボックス")
    option = st.selectbox(
        "好きなプログラミング言語は?",
        ["Python", "JavaScript", "Java", "C++", "Go", "Rust"]
    )
    st.write(f"あなたは{option}を選びました")

with tab2:
    st.header("レイアウト")

    # カラム
    st.subheader("カラムレイアウト")
    col1, col2 = st.columns(2)
    with col1:
        st.write("これは左カラムです")
        st.number_input("数値を入力", value=10)
    with col2:
        st.write("これは右カラムです")
        st.metric("メトリクス", "42", "2%")
    st.divider()

    # タブ (ネストされたタブの例)
    st.subheader("タブ (ネスト)")
    inner_tab1, inner_tab2 = st.tabs(["第1タブ", "第2タブ"])
    with inner_tab1:
        st.write("これはネストされた第1タブの内容です")
    with inner_tab2:
        st.write("これはネストされた第2タブの内容です")
    st.divider()

    # エクスパンダー
    st.subheader("エクスパンダー")
    with st.expander("詳細を表示"):
        st.write("これはエクスパンダー内の隠れたコンテンツです")
        st.code("print('Hello, Streamlit！')")

with tab3:
    st.header("データの表示")

    # サンプルデータフレームを作成
    df = pd.DataFrame({
        '名前': ['田中', '鈴木', '佐藤', '高橋', '伊藤'],
        '年齢': [25, 30, 22, 28, 33],
        '都市': ['東京', '大阪', '福岡', '札幌', '名古屋']
    })

    # データフレーム表示
    st.subheader("データフレーム")
    st.dataframe(df, use_container_width=True)
    st.divider()

    # テーブル表示
    st.subheader("テーブル")
    st.table(df)
    st.divider()

    # メトリクス表示
    st.subheader("メトリクス")
    col1, col2, col3 = st.columns(3)
    col1.metric("温度", "23°C", "1.5°C")
    col2.metric("湿度", "45%", "-5%")
    col3.metric("気圧", "1013hPa", "0.1hPa")


with tab4:
    st.header("グラフの表示")

    # ラインチャート
    st.subheader("ラインチャート")
    chart_data_line = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C'])
    st.line_chart(chart_data_line)
    st.divider()

    # バーチャート
    st.subheader("バーチャート")
    chart_data_bar = pd.DataFrame({
        'カテゴリ': ['A', 'B', 'C', 'D'],
        '値': [10, 25, 15, 30]
    }).set_index('カテゴリ')
    st.bar_chart(chart_data_bar)


with tab5:
    st.header("インタラクティブ機能")

    # プログレスバー
    st.subheader("プログレスバー")
    progress_text = "進捗状況"
    my_bar = st.progress(0, text=progress_text)
    if st.button("進捗をシミュレート"):
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=f"{progress_text}: {percent_complete+1}%")
        st.balloons()
        my_bar.progress(0, text=progress_text)
    st.divider()


    # ファイルアップロード
    st.subheader("ファイルアップロード")
    uploaded_file = st.file_uploader("ファイルをアップロード", type=["csv", "txt"])
    if uploaded_file is not None:
        # ファイルのデータを表示
        bytes_data = uploaded_file.getvalue()
        st.write(f"ファイル名: {uploaded_file.name}, サイズ: {len(bytes_data)} bytes")

        # CSVの場合はデータフレームとして読み込む
        if uploaded_file.name.endswith('.csv'):
            try:
                df_uploaded = pd.read_csv(uploaded_file)
                st.write("CSVデータのプレビュー:")
                st.dataframe(df_uploaded.head())
            except Exception as e:
                st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        elif uploaded_file.name.endswith('.txt'):
             # テキストファイルの内容を表示 (最初の数行)
             stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
             st.write("テキストファイルの内容 (最初の5行):")
             st.text("".join(stringio.readlines(5)))


with tab6:
    st.header("スタイルのカスタマイズ")

    # カスタムCSS
    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
        color: #0066cc;
    }
    .highlight {
        background-color: yellow;
        padding: 5px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">これはカスタムCSSでスタイリングされたテキストです！</p>', unsafe_allow_html=True)
    st.markdown('<p class="highlight">これはハイライトされたテキストです。</p>', unsafe_allow_html=True)


# ============================================
# デモの使用方法
# ============================================
# フッター情報をサイドバーなどに移動するか、アプリの説明として最初に表示する方がデザイン的にすっきりするかもしれません。
# 一旦コメントアウトします。
# st.divider()
# st.subheader("このデモの使い方")
# st.markdown("""
# 1. コードエディタでコメントアウトされた部分を見つけます（#で始まる行）
# 2. 確認したい機能のコメントを解除します（先頭の#を削除）
# 3. 変更を保存して、ブラウザで結果を確認します
# 4. 様々な組み合わせを試して、UIがどのように変化するか確認しましょう
# """)
# 
# st.code("""
# # コメントアウトされた例:
# # if st.button("クリックしてください"):
# #     st.success("ボタンがクリックされました！")
# 
# # コメントを解除した例:
# if st.button("クリックしてください"):
#     st.success("ボタンがクリックされました！")
# """)