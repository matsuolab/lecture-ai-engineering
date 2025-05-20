import streamlit as st
import pandas as pd
import numpy as np
import time

from mymodel import trainer

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
st.markdown("以下のスライドやセレクトボックスを操作して分類モデルのパラメータを操作し、限られたepoch(10epoch)でより高精度なモデルを開発しましょう。")
st.markdown("サーバーがGPUを使用できない設定の場合学習に極端に時間がかかる可能性があります。最初の実行時にはデータダウンロードのため特に時間がかかります。")

st.subheader("最適化手法設定")
opt = st.selectbox(
    "今回使用する最適化手法を選択してください",
    ["Adam", "AdamW", "Adadelta", "RMSprop", "Adagrad", "SGD"]
)

# 学習率等のハイパーパラメータを調整
st.subheader("初期学習率の設定")
lr = st.slider("学習率(仕様上 x100で表記 例：1->0.01)", 1, 100, 1) / 100

# 活性化関数や最適化手法を選択
st.subheader("活性化関数設定")
activation = st.selectbox(
    "今回使用する活性化関数を選択してください",
    ["ReLU", "LeakyReLU", "Sigmoid", "GLU"]
)

negative_slope = 0.01
if activation == "LeakyReLU":
    negative_slope = st.slider("係数設定(仕様上 x100で表記 例：1->0.01)", 1, 100, 1) / 100

# ボタン押下で学習を開始する
if st.button("学習を開始する"):
    trainer_cifar10model = trainer(activation=activation, negative_slope=negative_slope, optimizer=opt, lr=lr)
    accuracy, loss, accuracy_valid = trainer_cifar10model.train_model(num_epochs=5)
    
    # lossの変動具合を描画
    # st.subheader("ラインチャート")
    # chart_data = pd.DataFrame(
    #     np.array(accuracy, accuracy_valid),
    #     columns=['train_accuracy', 'valid_accuracy'])
    # st.line_chart(chart_data)
    st.write("accuracy : ", accuracy_valid)

# # モデルを保存するか、新しいモデルを開発するかを選択する
# st.subheader("出力モデルの保存有無を選択")
# col1, col2 = st.columns(2)
# with col1:
#     st.write("このモデルを保存します")
#     if st.button("保存"):
#         # モデル保存
#         pass
# with col2:
#     st.write("モデルをリセットして作り直す")
#     if st.button("リロード"):
#         # メモリ開放とサイトのリロード
#         pass

# 今回使用しているコードを表示
# st.subheader("エクスパンダー")
# with st.expander("詳細を表示"):
#     st.write("これはエクスパンダー内の隠れたコンテンツです")
#     st.code("print('Hello, Streamlit！')")


# 学習進捗を表示出来たらする
# st.subheader("プログレスバー")
# progress = st.progress(0)
# if st.button("進捗をシミュレート"):
#     for i in range(101):
#         time.sleep(0.01)
#         progress.progress(i / 100)
#     st.balloons()