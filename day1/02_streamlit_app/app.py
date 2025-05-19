import streamlit as st

def display_chat_page(pipe):
    st.header("📝 バッチ推論チャット")
    st.write("改行区切りで複数のテキストを一括入力して、まとめて推論します。")

    # テキストエリアで複数入力
    batch_input = st.text_area("テキストを改行で区切って入力してください", height=300)

    # ボタン押したら推論
    if st.button("まとめて推論する"):
        if batch_input.strip():
            # 改行でリストに分割
            text_list = [line.strip() for line in batch_input.strip().splitlines() if line.strip()]

            if not text_list:
                st.warning("空白行だけです。ちゃんとテキストを入力してください！")
                return

            st.success(f"📝 入力テキスト数：{len(text_list)}件")

            with st.spinner("推論中..."):
                try:
                    # バッチ推論
                    results = pipe(text_list, max_length=100)
                except Exception as e:
                    st.error(f"推論中にエラーが発生しました: {e}")
                    return

            # 出力を一覧表示
            for idx, (inp, outp) in enumerate(zip(text_list, results)):
                with st.expander(f"【{idx+1}件目】入力内容を見る", expanded=False):
                    st.markdown(f"**入力:** {inp}")
                    st.markdown(f"**出力:** {outp['generated_text']}")
        else:
            st.warning("最低1件は入力してください。")
