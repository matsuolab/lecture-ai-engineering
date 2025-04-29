import streamlit as st

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