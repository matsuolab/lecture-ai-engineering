import streamlit as st

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