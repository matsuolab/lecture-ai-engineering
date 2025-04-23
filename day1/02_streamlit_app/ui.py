# ui.py
import streamlit as st
import pandas as pd
import time
from database import save_to_db, get_chat_history, get_db_count, clear_db
from llm import generate_response
from data import create_sample_evaluation_data
from metrics import get_metrics_descriptions


# --- チャットページのUI ---
def display_chat_page(pipe):
    """チャットページのUIを表示する"""
    st.subheader("質問を入力してください")
    user_question = st.text_area(
        "質問",
        key="question_input",
        height=100,
        value=st.session_state.get("current_question", ""),
    )
    submit_button = st.button("質問を送信")

    # セッション状態の初期化（安全のため）
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""
    if "current_answer" not in st.session_state:
        st.session_state.current_answer = ""
    if "response_time" not in st.session_state:
        st.session_state.response_time = 0.0
    if "feedback_given" not in st.session_state:
        st.session_state.feedback_given = False

    # 質問が送信された場合
    if submit_button and user_question:
        st.session_state.current_question = user_question
        st.session_state.current_answer = ""  # 回答をリセット
        st.session_state.feedback_given = False  # フィードバック状態もリセット

        with st.spinner("モデルが回答を生成中..."):
            answer, response_time = generate_response(pipe, user_question)
            st.session_state.current_answer = answer
            st.session_state.response_time = response_time
            # ここでrerunすると回答とフィードバックが一度に表示される
            st.rerun()

    # 回答が表示されるべきか判断 (質問があり、回答が生成済みで、まだフィードバックされていない)
    if st.session_state.current_question and st.session_state.current_answer:
        st.subheader("回答:")
        st.markdown(st.session_state.current_answer)  # Markdownで表示
        st.info(f"応答時間: {st.session_state.response_time:.2f}秒")

        # フィードバックフォームを表示 (まだフィードバックされていない場合)
        if not st.session_state.feedback_given:
            display_feedback_form()
        else:
            # フィードバック送信済みの場合、次の質問を促すか、リセットする
            if st.button("次の質問へ"):
                # 状態をリセット
                st.session_state.current_question = ""
                st.session_state.current_answer = ""
                st.session_state.response_time = 0.0
                st.session_state.feedback_given = False
                st.rerun()  # 画面をクリア


def display_feedback_form():
    """フィードバック入力フォームを表示する"""
    with st.form("feedback_form"):
        st.subheader("フィードバック")
        feedback_options = ["正確 ☺️", "部分的に正確 😐", "不正確 😭"]
        # label_visibility='collapsed' でラベルを隠す
        feedback = st.radio(
            "回答の評価",
            feedback_options,
            key="feedback_radio",
            label_visibility="collapsed",
            horizontal=True,
        )
        correct_answer = st.text_area(
            "より正確な回答（任意）", key="correct_answer_input", height=100
        )
        feedback_comment = st.text_area(
            "コメント（任意）", key="feedback_comment_input", height=100
        )
        submitted = st.form_submit_button("フィードバックを送信")
        if submitted:
            # フィードバックをデータベースに保存
            is_correct = (
                1.0
                if feedback == "正確 ☺️"
                else (0.5 if feedback == "部分的に正確 😐" else 0.0)
            )
            # コメントがない場合でも '正確' などの評価はfeedbackに含まれるようにする
            combined_feedback = f"{feedback}"
            if feedback_comment:
                combined_feedback += f": {feedback_comment}"

            save_to_db(
                st.session_state.current_question,
                st.session_state.current_answer,
                combined_feedback,
                correct_answer,
                is_correct,
                st.session_state.response_time,
            )
            st.session_state.feedback_given = True
            st.success("フィードバックが保存されました！")
            st.write(response_comment(is_correct))
            # フォーム送信後に状態をリセットしない方が、ユーザーは結果を確認しやすいかも
            # 必要ならここでリセットして st.rerun()
            st.rerun()  # フィードバックフォームを消すために再実行

def response_comment(score):
    match score:
        case 1.0:
            return "お役に立てて嬉しいです!!"
        case 0.5:
            return "ご協力ありがとうございます!!!"
        case 0.0:
            return "お役に立てず申し訳ありません．．．\n今後とも精進します．"
        case _:
            return "何か至らない点がありましたか？"


# --- 履歴閲覧ページのUI ---
def display_history_page():
    """履歴閲覧ページのUIを表示する"""
    st.subheader("チャット履歴と評価指標")
    history_df = get_chat_history()

    if history_df.empty:
        st.info("まだチャット履歴がありません。")
        return

    # タブでセクションを分ける
    tab1, tab2 = st.tabs(["履歴閲覧", "評価指標分析"])

    with tab1:
        display_history_list(history_df)

    with tab2:
        display_metrics_analysis(history_df)


def display_history_list(history_df):
    """履歴リストを表示する"""
    st.write("#### 履歴リスト")
    # 表示オプション
    filter_options = {
        "すべて表示": None,
        "正確なもののみ": 1.0,
        "部分的に正確なもののみ": 0.5,
        "不正確なもののみ": 0.0,
    }
    display_option = st.radio(
        "表示フィルタ",
        options=filter_options.keys(),
        horizontal=True,
        label_visibility="collapsed",  # ラベル非表示
    )

    filter_value = filter_options[display_option]
    if filter_value is not None:
        # is_correctがNaNの場合を考慮
        filtered_df = history_df[
            history_df["is_correct"].notna()
            & (history_df["is_correct"] == filter_value)
        ]
    else:
        filtered_df = history_df

    if filtered_df.empty:
        st.info("選択した条件に一致する履歴はありません。")
        return

    # ページネーション
    items_per_page = 5
    total_items = len(filtered_df)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    current_page = st.number_input(
        "ページ", min_value=1, max_value=total_pages, value=1, step=1
    )

    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paginated_df = filtered_df.iloc[start_idx:end_idx]

    for i, row in paginated_df.iterrows():
        with st.expander(
            f"{row['timestamp']} - Q: {row['question'][:50] if row['question'] else 'N/A'}..."
        ):
            st.markdown(f"**Q:** {row['question']}")
            st.markdown(f"**A:** {row['answer']}")
            st.markdown(f"**Feedback:** {row['feedback']}")
            if row["correct_answer"]:
                st.markdown(f"**Correct A:** {row['correct_answer']}")

            # 評価指標の表示
            st.markdown("---")
            cols = st.columns(3)
            cols[0].metric("正確性スコア", f"{row['is_correct']:.1f}")
            cols[1].metric("応答時間(秒)", f"{row['response_time']:.2f}")
            cols[2].metric("単語数", f"{row['word_count']}")

            cols = st.columns(3)
            # NaNの場合はハイフン表示
            cols[0].metric(
                "BLEU",
                f"{row['bleu_score']:.4f}" if pd.notna(row["bleu_score"]) else "-",
            )
            cols[1].metric(
                "類似度",
                f"{row['similarity_score']:.4f}"
                if pd.notna(row["similarity_score"])
                else "-",
            )
            cols[2].metric(
                "関連性",
                f"{row['relevance_score']:.4f}"
                if pd.notna(row["relevance_score"])
                else "-",
            )

    st.caption(
        f"{total_items} 件中 {start_idx + 1} - {min(end_idx, total_items)} 件を表示"
    )


def display_metrics_analysis(history_df):
    """評価指標の分析結果を表示する"""
    st.write("#### 評価指標の分析")

    # is_correct が NaN のレコードを除外して分析
    analysis_df = history_df.dropna(subset=["is_correct"])
    if analysis_df.empty:
        st.warning("分析可能な評価データがありません。")
        return

    accuracy_labels = {1.0: "正確", 0.5: "部分的に正確", 0.0: "不正確"}
    analysis_df["正確性"] = analysis_df["is_correct"].map(accuracy_labels)

    # 正確性の分布
    st.write("##### 正確性の分布")
    accuracy_counts = analysis_df["正確性"].value_counts()
    if not accuracy_counts.empty:
        st.bar_chart(accuracy_counts)
    else:
        st.info("正確性データがありません。")

    # 応答時間と他の指標の関係
    st.write("##### 応答時間とその他の指標の関係")
    metric_options = ["bleu_score", "similarity_score", "relevance_score", "word_count"]
    # 利用可能な指標のみ選択肢に含める
    valid_metric_options = [
        m
        for m in metric_options
        if m in analysis_df.columns and analysis_df[m].notna().any()
    ]

    if valid_metric_options:
        metric_option = st.selectbox(
            "比較する評価指標を選択", valid_metric_options, key="metric_select"
        )

        chart_data = analysis_df[
            ["response_time", metric_option, "正確性"]
        ].dropna()  # NaNを除外
        if not chart_data.empty:
            st.scatter_chart(
                chart_data,
                x="response_time",
                y=metric_option,
                color="正確性",
            )
        else:
            st.info(
                f"選択された指標 ({metric_option}) と応答時間の有効なデータがありません。"
            )

    else:
        st.info("応答時間と比較できる指標データがありません。")

    # 全体の評価指標の統計
    st.write("##### 評価指標の統計")
    stats_cols = [
        "response_time",
        "bleu_score",
        "similarity_score",
        "word_count",
        "relevance_score",
    ]
    valid_stats_cols = [
        c
        for c in stats_cols
        if c in analysis_df.columns and analysis_df[c].notna().any()
    ]
    if valid_stats_cols:
        metrics_stats = analysis_df[valid_stats_cols].describe()
        st.dataframe(metrics_stats)
    else:
        st.info("統計情報を計算できる評価指標データがありません。")

    # 正確性レベル別の平均スコア
    st.write("##### 正確性レベル別の平均スコア")
    if valid_stats_cols and "正確性" in analysis_df.columns:
        try:
            accuracy_groups = analysis_df.groupby("正確性")[valid_stats_cols].mean()
            st.dataframe(accuracy_groups)
        except Exception as e:
            st.warning(f"正確性別スコアの集計中にエラーが発生しました: {e}")
    else:
        st.info("正確性レベル別の平均スコアを計算できるデータがありません。")

    # カスタム評価指標：効率性スコア
    st.write("##### 効率性スコア (正確性 / (応答時間 + 0.1))")
    if (
        "response_time" in analysis_df.columns
        and analysis_df["response_time"].notna().any()
    ):
        # ゼロ除算を避けるために0.1を追加
        analysis_df["efficiency_score"] = analysis_df["is_correct"] / (
            analysis_df["response_time"].fillna(0) + 0.1
        )
        # IDカラムが存在するか確認
        if "id" in analysis_df.columns:
            # 上位10件を表示
            top_efficiency = analysis_df.sort_values(
                "efficiency_score", ascending=False
            ).head(10)
            # id をインデックスにする前に存在確認
            if not top_efficiency.empty:
                st.bar_chart(top_efficiency.set_index("id")["efficiency_score"])
            else:
                st.info("効率性スコアデータがありません。")
        else:
            # IDがない場合は単純にスコアを表示
            st.bar_chart(
                analysis_df.sort_values("efficiency_score", ascending=False).head(10)[
                    "efficiency_score"
                ]
            )

    else:
        st.info("効率性スコアを計算するための応答時間データがありません。")


# --- サンプルデータ管理ページのUI ---
def display_data_page():
    """サンプルデータ管理ページのUIを表示する"""
    st.subheader("サンプル評価データの管理")
    count = get_db_count()
    st.write(f"現在のデータベースには {count} 件のレコードがあります。")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("サンプルデータを追加", key="create_samples"):
            create_sample_evaluation_data()
            st.rerun()  # 件数表示を更新

    with col2:
        # 確認ステップ付きのクリアボタン
        if st.button("データベースをクリア", key="clear_db_button"):
            if clear_db():  # clear_db内で確認と実行を行う
                st.rerun()  # クリア後に件数表示を更新

    # 評価指標に関する解説
    st.subheader("評価指標の説明")
    metrics_info = get_metrics_descriptions()
    for metric, description in metrics_info.items():
        with st.expander(f"{metric}"):
            st.write(description)

