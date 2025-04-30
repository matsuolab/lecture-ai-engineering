import streamlit as st
import pandas as pd
import numpy as np
import time

# ============================================
# ページ設定 (Uncommented)
# ============================================
st.set_page_config(
    page_title="Streamlit デモ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# タイトルと説明
# ============================================
st.title("Streamlit 初心者向けデモ")
st.markdown("### Streamlitの主要なUI要素とレイアウト機能")
st.markdown("以下のタブをクリックして、様々な機能を確認してください。")

# ============================================
# サイドバー
# ============================================
st.sidebar.header("デモのガイド")
st.sidebar.info("各タブでStreamlitのさまざまな機能を確認できます。")

# ============================================
# タブでコンテンツを整理
# ============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "基本要素", "レイアウト", "データ表示", "グラフ表示", "インタラクティブ", "カスタマイズ"
])

# --- Tab 1: 基本的なUI要素 ---
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

# --- Tab 2: レイアウト ---
with tab2:
    st.header("レイアウト")

    # カラム
    st.subheader("カラムレイアウト")
    col1, col2 = st.columns(2)
    with col1:
        st.write("これは左カラムです")
        st.number_input("数値を入力", value=10, key="col_num_input") # Added key for uniqueness
    with col2:
        st.write("これは右カラムです")
        st.metric("メトリクス", "42", "2%")
    st.divider()

    # タブ (Nested Tabs Example)
    st.subheader("タブ (ネストされたタブ)")
    inner_tab1, inner_tab2 = st.tabs(["内部タブ A", "内部タブ B"])
    with inner_tab1:
        st.write("これは内部タブ A の内容です")
    with inner_tab2:
        st.write("これは内部タブ B の内容です")
    st.divider()

    # エクスパンダー
    st.subheader("エクスパンダー")
    with st.expander("詳細を表示"):
        st.write("これはエクスパンダー内の隠れたコンテンツです")
        st.code("print('Hello, Streamlit！')")

# --- Tab 3: データ表示 ---
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

# --- Tab 4: グラフ表示 ---
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

# --- Tab 5: インタラクティブ機能 ---
with tab5:
    st.header("インタラクティブ機能")

    # プログレスバー
    st.subheader("プログレスバー")
    if st.button("進捗をシミュレート"):
        progress_bar = st.progress(0) # Create progress bar inside button click
        for i in range(101):
            time.sleep(0.01)
            progress_bar.progress(i) # Update progress
        st.balloons()
        st.success("完了！")
    st.divider()

    # ファイルアップロード
    st.subheader("ファイルアップロード")
    uploaded_file = st.file_uploader("ファイルをアップロード", type=["csv", "txt"])
    if uploaded_file is not None:
        # ファイルのデータを表示
        bytes_data = uploaded_file.getvalue()
        st.write(f"ファイル名: {uploaded_file.name}")
        st.write(f"ファイルサイズ: {len(bytes_data)} bytes")

        # CSVの場合はデータフレームとして読み込む
        if uploaded_file.name.endswith('.csv'):
            try:
                df_uploaded = pd.read_csv(uploaded_file)
                st.write("CSVデータのプレビュー:")
                st.dataframe(df_uploaded.head())
            except Exception as e:
                st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        elif uploaded_file.name.endswith('.txt'):
             # テキストファイルの内容を表示（最初の数行）
             try:
                 string_data = bytes_data.decode("utf-8")
                 st.write("テキストファイルの内容（最初の5行）:")
                 st.text("\n".join(string_data.splitlines()[:5]))
             except Exception as e:
                 st.error(f"テキストファイルの読み込み中にエラーが発生しました: {e}")


# --- Tab 6: カスタマイズ ---
with tab6:
    st.header("スタイルのカスタマイズ")

    # カスタムCSS
    st.subheader("カスタムCSS")
    st.markdown("""
    <style>
    .big-font {
        font-size: 24px !important; /* Increased font size */
        font-weight: bold;
        color: #FF4B4B; /* Changed color */
        border: 1px solid #FF4B4B;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">これはカスタムCSSでスタイリングされたテキストです！</p>', unsafe_allow_html=True)
    st.markdown("`st.markdown`内で`<style>`タグを使用することで、CSSを適用できます。")


# ============================================
# デモの使用方法 (Original section kept at the end)
# ============================================
st.divider()
st.subheader("このデモの元々の使い方（参考）")
st.markdown("""
元々のコードは、コメントアウトされた部分を一つずつ解除して機能を試す形式でした。
この改良版では、主要な機能がタブに整理されています。
""")
st.code("""
# コメントアウトされた例:
# if st.button("クリックしてください"):
#     st.success("ボタンがクリックされました！")

# コメントを解除した例:
if st.button("クリックしてください"):
    st.success("ボタンがクリックされました！")
""")
