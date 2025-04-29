# ui.py
import streamlit as st
import pandas as pd
from datetime import datetime

from database import (
    save_to_db, get_chat_history, get_db_count, clear_db
)
from llm import generate_response
from data import create_sample_evaluation_data
from metrics import get_metrics_descriptions

# ---------- チャットページ ----------
def chat_ui(pipe):
    st.header("🤖 Gemma 2 Chatbot with Feedback")

    if pipe is None:
        st.error("モデルの読み込みに失敗しました。")
        return

    # セッションステート: 会話履歴
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 既存のメッセージを表示
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    # 新規入力
    user_input = st.chat_input("ここに質問を入力…")
    if user_input:
        # ユーザーメッセージ追加
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # モデル応答
        with st.spinner("Gemma が回答を生成中…"):
            answer, rt = generate_response(pipe, user_input)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
        st.info(f"応答時間: {rt:.2f}秒", icon="⏱️")

        # フィードバック
        with st.expander("★ フィードバックを送る", expanded=True):
            feedback = st.radio(
                "回答の評価",
                ["正確", "部分的に正確", "不正確"],
                horizontal=True
            )
            correction = st.text_area("より正確な回答（任意）", height=80)
            comment = st.text_area("コメント（任意）", height=80)
            if st.button("送信する"):
                is_correct = {"正確":1.0, "部分的に正確":0.5, "不正確":0.0}[feedback]
                combined = feedback
                if comment:
                    combined += f": {comment}"
                save_to_db(
                    user_input, answer, combined,
                    correction, is_correct, rt
                )
                st.success("フィードバックを保存しました！", icon="✅")

# ---------- 履歴ページ ----------
def history_ui():
    st.header("📜 チャット履歴と分析")
    df = get_chat_history()
    if df.empty:
        st.info("まだ履歴がありません。")
        return

    # --- timestamp を datetime 型に変換 ---
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # フィルタ：日付レンジ＋テキスト検索
    min_date = df["timestamp"].min().date()
    max_date = df["timestamp"].max().date()
    col1, col2 = st.columns([1, 2])
    with col1:
        date_range = st.date_input(
            "日付で絞り込み",
            value=(min_date, max_date)
        )
    with col2:
        keyword = st.text_input("質問 or フィードバックで検索")

    mask = (
        (df["timestamp"].dt.date >= date_range[0]) &
        (df["timestamp"].dt.date <= date_range[1])
    )
    if keyword:
        mask &= df.apply(
            lambda r: keyword in str(r["question"]) or keyword in str(r["feedback"]),
            axis=1
        )
    filtered = df[mask]

    st.write(f"該当件数: {len(filtered)} 件")
    for _, row in filtered.iterrows():
        with st.expander(f"{row['timestamp']} ｜ Q: {row['question'][:30]}…"):
            st.markdown(f"**回答:** {row['answer']}")
            st.markdown(f"**評価:** {row['feedback']}")
            if row["correct_answer"]:
                st.markdown(f"**修正案:** {row['correct_answer']}")
            cols = st.columns(3)
            cols[0].metric("正確度", f"{row['is_correct']:.1f}")
            cols[1].metric("応答時間", f"{row['response_time']:.2f}s")
            cols[2].metric("単語数", f"{row['word_count']}")

# ---------- データ管理ページ ----------
def data_ui():
    st.header("⚙️ サンプルデータ管理")
    count = get_db_count()
    st.write(f"現在のレコード数: **{count}** 件")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("サンプルデータを追加"):
            create_sample_evaluation_data()
            st.toast("サンプルデータを追加しました。")
    with c2:
        if st.button("データベースをクリア"):
            if st.confirm("本当に全ての履歴を消去してもよろしいですか？"):
                clear_db()
                st.toast("データベースをクリアしました。")

    st.markdown("---")
    st.subheader("各種評価指標の説明")
    for metric, desc in get_metrics_descriptions().items():
        with st.expander(metric):
            st.write(desc)
