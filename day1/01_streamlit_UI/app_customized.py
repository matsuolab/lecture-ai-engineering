import streamlit as st
import pandas as pd
import numpy as np
import time

from mymodel import Cifar10Model

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
st.title("Streamlit customized version -- developer : create-alt --")
st.markdown("## 高性能なCifar-10分類モデルを開発しよう！")
st.markdown("以下のスライドやセレクトボックスを操作して分類モデルのパラメータを操作し、限られたepochでより高精度なモデルを開発しましょう。")
st.markdown("サーバーがGPUを使用できない設定の場合学習に極端に時間がかかる可能性があります。最初の実行時にはデータダウンロードのため特に時間がかかります。")

# ボタン押下で学習を開始する
st.subheader("ボタン")
if st.button("学習を開始する"):
    st.success("ボタンがクリックされました！")

# 学習率等のハイパーパラメータを調整
st.subheader("スライダー")
age = st.slider("年齢", 0, 100, 25)
st.write(f"あなたの年齢: {age}")

# 活性化関数や最適化手法を選択
st.subheader("セレクトボックス")
option = st.selectbox(
    "好きなプログラミング言語は?",
    ["Python", "JavaScript", "Java", "C++", "Go", "Rust"]
)
st.write(f"あなたは{option}を選びました")

# モデルを保存するか、新しいモデルを開発するかを選択する
st.subheader("カラムレイアウト")
col1, col2 = st.columns(2)
with col1:
    st.write("これは左カラムです")
    st.number_input("数値を入力", value=10)
with col2:
    st.write("これは右カラムです")
    st.metric("メトリクス", "42", "2%")

# 今回使用しているコードを表示
st.subheader("エクスパンダー")
with st.expander("詳細を表示"):
    st.write("これはエクスパンダー内の隠れたコンテンツです")
    st.code("print('Hello, Streamlit！')")

# lossの変動具合を描画
st.subheader("ラインチャート")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C'])
st.line_chart(chart_data)

# 学習進捗を表示出来たらする
# st.subheader("プログレスバー")
# progress = st.progress(0)
# if st.button("進捗をシミュレート"):
#     for i in range(101):
#         time.sleep(0.01)
#         progress.progress(i / 100)
#     st.balloons()
