import streamlit as st
import pandas as pd
import numpy as np
import time

# ページ設定
st.set_page_config(
    page_title="Streamlit デモ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# サイドバーでページ選択
page = st.sidebar.selectbox(
    "体験したい機能を選んでください",
    ["基本UI", "レイアウト", "グラフ表示", "ファイルアップロード"]
)

# メインコンテンツ切り替え
if page == "基本UI":
    st.title("基本的なUI要素")
    
    name = st.text_input("あなたの名前", "ゲスト")
    st.write(f"こんにちは、{name}さん！")

    if st.button("クリックしてください"):
        st.success("ボタンがクリックされました！")

    if st.checkbox("チェックを入れると追加コンテンツが表示されます"):
        st.info("これは隠れたコンテンツです！")

    age = st.slider("年齢", 0, 100, 25)
    st.write(f"あなたの年齢: {age}")

    option = st.selectbox("好きな言語は？", ["Python", "JavaScript", "C++"])
    st.write(f"あなたは {option} を選びました")

elif page == "レイアウト":
    st.title("レイアウトのデモ")

    col1, col2 = st.columns(2)
    with col1:
        st.write("これは左カラムです")
        st.number_input("数値を入力", value=10)
    with col2:
        st.write("これは右カラムです")
        st.metric("メトリクス", "42", "2%")

    tab1, tab2 = st.tabs(["第1タブ", "第2タブ"])
    with tab1:
        st.write("これは第1タブの内容です")
    with tab2:
        st.write("これは第2タブの内容です")

elif page == "グラフ表示":
    st.title("グラフの表示")

    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
    st.line_chart(chart_data)

    bar_data = pd.DataFrame({
        'カテゴリ': ['A', 'B', 'C', 'D'],
        '値': [10, 25, 15, 30]
    }).set_index('カテゴリ')
    st.bar_chart(bar_data)

elif page == "ファイルアップロード":
    st.title("ファイルアップロード")

    uploaded_file = st.file_uploader("CSVまたはTXTファイルをアップロード", type=["csv", "txt"])
    if uploaded_file is not None:
        st.write(f"ファイルサイズ: {len(uploaded_file.getvalue())} bytes")

        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            st.write("CSVデータのプレビュー:")
            st.dataframe(df)

