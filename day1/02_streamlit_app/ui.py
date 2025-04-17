import streamlit as st
import pandas as pd
import time
from database import save_to_db, get_chat_history, get_db_count, clear_db
from llm import generate_response
from data import create_sample_evaluation_data
from metrics import get_metrics_descriptions

# --- サイドバーとページタイトルの設定 ---
def setup_page():
    """アプリケーションの基本設定とナビゲーションを行う"""
    st.set_page_config(page_title="AI回答評価システム", layout="wide")
    
    with st.sidebar:
        st.title("AI回答評価システム")
        page = st.radio(
            "ナビゲーション",
            ["チャット", "履歴と分析", "データ管理"],
            format_func=lambda x: {
                "チャット": "💬 チャット",
                "履歴と分析": "📊 履歴と分析",
                "データ管理": "🗄️ データ管理"
            }[x]
        )
        
        # サイドバーに使い方ガイド
        with st.expander("📘 使い方ガイド"):
            st.markdown("""
            ### 基本的な使い方
            1. **チャット**: 質問を入力し、AIからの回答を評価します
            2. **履歴と分析**: 過去の質問と回答の履歴を確認し、傾向を分析します
            3. **データ管理**: サンプルデータの追加や削除を行います
            """)
    
    return page

# --- チャットページのUI ---
def display_chat_page(pipe):
    """チャットページのUIを表示する"""
    st.title("💬 チャット")
    
    # 状態管理の初期化
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""
    if "current_answer" not in st.session_state:
        st.session_state.current_answer = ""
    if "response_time" not in st.session_state:
        st.session_state.response_time = 0.0
    if "feedback_given" not in st.session_state:
        st.session_state.feedback_given = False
    
    # チャット履歴の表示
    if st.session_state.chat_history:
        with st.container():
            for i, chat in enumerate(st.session_state.chat_history):
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.image("https://via.placeholder.com/40", width=40, caption="You")
                with col2:
                    st.markdown(f"**質問**:\n{chat['question']}")
                
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.image("https://via.placeholder.com/40", width=40, caption="AI")
                with col2:
                    st.markdown(f"**回答**:\n{chat['answer']}")
                    st.caption(f"応答時間: {chat['response_time']:.2f}秒 | 評価: {chat['feedback']}" if 'feedback' in chat else "")
                
                st.markdown("---")
    
    # 質問入力エリア
    with st.container():
        st.write("### 新しい質問")
        user_question = st.text_area(
            "質問を入力してください",
            key="question_input",
            height=100,
            value=st.session_state.current_question,
            placeholder="ここに質問を入力してください..."
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            submit_button = st.button("送信", key="submit_question", use_container_width=True)
        with col2:
            # 空白スペース（レイアウト用）
            st.write("")
    
    # 質問が送信された場合
    if submit_button and user_question:
        st.session_state.current_question = user_question
        st.session_state.current_answer = ""
        st.session_state.feedback_given = False
        
        with st.status("AIが回答を生成中...") as status:
            start_time = time.time()
            answer, response_time = generate_response(pipe, user_question)
            status.update(label="回答が生成されました！", state="complete")
            st.session_state.current_answer = answer
            st.session_state.response_time = response_time
            
            # すぐに回答を表示
            st.subheader("AI回答:")
            st.markdown(st.session_state.current_answer)
            st.info(f"応答時間: {st.session_state.response_time:.2f}秒")
            
            # フィードバックフォームを表示
            feedback_container = st.container()
            with feedback_container:
                display_feedback_form()
            
            # ページをスクロールして回答が見えるようにする（Streamlitの制約内で可能な限り）
            st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
        
    # 既に回答があり、まだフィードバックがない場合
    elif st.session_state.current_question and st.session_state.current_answer and not st.session_state.feedback_given:
        st.subheader("AI回答:")
        st.markdown(st.session_state.current_answer)
        st.info(f"応答時間: {st.session_state.response_time:.2f}秒")
        
        # フィードバックフォームを表示
        display_feedback_form()
    
    # フィードバック済みで新しい質問がまだ入力されていない場合
    elif st.session_state.feedback_given:
        st.success("フィードバックありがとうございます。新しい質問を入力できます。")
        # 新しい質問を促す（ボタンは不要）

def display_feedback_form():
    """改善されたフィードバック入力フォームを表示する"""
    with st.form("feedback_form", clear_on_submit=False):
        st.subheader("回答の評価")
        
        # フィードバックオプションをラジオボタンで表示
        feedback = st.radio(
            "回答の評価を選択してください",
            ["👍 正確", "👌 部分的に正確", "👎 不正確"],
            horizontal=True,
            key="feedback_radio"
        )
        
        # 選択されたフィードバックの値をマッピング
        feedback_value = {
            "👍 正確": "正確",
            "👌 部分的に正確": "部分的に正確",
            "👎 不正確": "不正確"
        }[feedback]
        
        # 追加のフィードバック項目
        correct_answer = st.text_area(
            "より正確な回答（任意）",
            key="correct_answer_input",
            height=100,
            placeholder="AIの回答が不完全または不正確な場合、正確な回答を入力してください..."
        )
        
        feedback_comment = st.text_area(
            "コメント（任意）",
            key="feedback_comment_input",
            height=100,
            placeholder="回答に関する追加のコメントがあれば入力してください..."
        )
        
        # 送信ボタン
        submitted = st.form_submit_button(
            "フィードバックを送信",
            use_container_width=True
        )
        
        if submitted:
            # フィードバックをデータベースに保存
            is_correct = 1.0 if feedback_value == "正確" else (0.5 if feedback_value == "部分的に正確" else 0.0)
            combined_feedback = feedback_value
            if feedback_comment:
                combined_feedback += f": {feedback_comment}"
            
            save_to_db(
                st.session_state.current_question,
                st.session_state.current_answer,
                combined_feedback,
                correct_answer,
                is_correct,
                st.session_state.response_time
            )
            
            # セッション状態を更新
            st.session_state.feedback_given = True
            
            # チャット履歴に追加
            st.session_state.chat_history.append({
                "question": st.session_state.current_question,
                "answer": st.session_state.current_answer,
                "feedback": combined_feedback,
                "response_time": st.session_state.response_time
            })
            
            # 次の質問のために状態をリセット
            st.session_state.current_question = ""
            st.session_state.current_answer = ""
            st.session_state.response_time = 0.0
            
            st.success("フィードバックが保存されました！新しい質問を入力できます。")
            st.rerun()


# --- 履歴閲覧ページのUI ---
def display_history_page():
    """履歴閲覧ページのUIを表示する"""
    st.title("📊 履歴と分析")
    
    history_df = get_chat_history()
    
    if history_df.empty:
        st.info("まだチャット履歴がありません。チャットページで質問を行い、フィードバックを提供してください。")
        return
    
    # タブでセクションを分ける
    tab1, tab2 = st.tabs(["履歴閲覧", "評価指標分析"])
    
    with tab1:
        display_history_list(history_df)
    
    with tab2:
        display_metrics_analysis(history_df)


def display_history_list(history_df):
    """履歴リストを表示する"""
    # 検索機能と絞り込み
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("キーワードで検索", placeholder="質問や回答に含まれるキーワードを入力...")
    with col2:
        filter_options = {
            "すべて表示": None,
            "正確なもののみ": 1.0,
            "部分的に正確なもののみ": 0.5,
            "不正確なもののみ": 0.0
        }
        display_option = st.selectbox(
            "評価でフィルタ",
            options=list(filter_options.keys())
        )
    
    # フィルタリング処理
    filter_value = filter_options[display_option]
    if filter_value is not None:
        # is_correctがNaNの場合を考慮
        filtered_df = history_df[history_df["is_correct"].notna() & (history_df["is_correct"] == filter_value)]
    else:
        filtered_df = history_df
    
    # 検索処理
    if search_term:
        mask = (
            filtered_df["question"].str.contains(search_term, case=False, na=False) |
            filtered_df["answer"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if filtered_df.empty:
        st.info("選択した条件に一致する履歴はありません。")
        return
    
    # ソート機能
    sort_options = {
        "日付 (新しい順)": ("timestamp", False),
        "日付 (古い順)": ("timestamp", True),
        "正確性 (高い順)": ("is_correct", False),
        "正確性 (低い順)": ("is_correct", True),
        "応答時間 (速い順)": ("response_time", True),
        "応答時間 (遅い順)": ("response_time", False)
    }
    
    sort_option = st.selectbox(
        "並び替え",
        options=list(sort_options.keys()),
        index=0
    )
    
    sort_column, ascending = sort_options[sort_option]
    filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)
    
    # ページネーション
    items_per_page = st.select_slider(
        "1ページあたりの表示件数",
        options=[5, 10, 20, 50],
        value=10
    )
    
    total_items = len(filtered_df)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        current_page = st.number_input(
            'ページ',
            min_value=1,
            max_value=max(1, total_pages),
            value=1,
            step=1
        )
    
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    paginated_df = filtered_df.iloc[start_idx:end_idx]
    
    # 履歴リストの表示
    st.markdown(f"### 履歴一覧 ({start_idx+1}-{end_idx}/{total_items}件)")
    
    for i, row in paginated_df.iterrows():
        # 正確性に基づいて色付けされたカード表示
        accuracy_color = {
            1.0: "rgba(0, 180, 0, 0.1)",  # 緑 (正確)
            0.5: "rgba(255, 165, 0, 0.1)",  # オレンジ (部分的に正確)
            0.0: "rgba(255, 0, 0, 0.1)"   # 赤 (不正確)
        }.get(row['is_correct'], "rgba(200, 200, 200, 0.1)")  # デフォルト
        
        # 日付をフォーマット
        formatted_date = pd.to_datetime(row['timestamp']).strftime('%Y/%m/%d %H:%M')
        
        with st.container():
            st.markdown(
                f"""
                <div style="padding: 10px; border-radius: 5px; background-color: {accuracy_color}; margin-bottom: 10px;">
                    <small>{formatted_date}</small>
                    <h4 style="margin: 0;">Q: {row['question'][:100]}{"..." if len(row['question']) > 100 else ""}</h4>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            with st.expander("詳細を表示"):
                st.markdown(f"**質問:**\n{row['question']}")
                st.markdown(f"**回答:**\n{row['answer']}")
                st.markdown(f"**フィードバック:**\n{row['feedback']}")
                if row['correct_answer']:
                    st.markdown(f"**正確な回答:**\n{row['correct_answer']}")
                
                # 評価指標をカードとして表示
                cols = st.columns(3)
                
                # 正確性を視覚的に表示
                accuracy_value = row['is_correct']
                accuracy_label = "正確" if accuracy_value == 1.0 else ("部分的に正確" if accuracy_value == 0.5 else "不正確")
                accuracy_emoji = "✅" if accuracy_value == 1.0 else ("⚠️" if accuracy_value == 0.5 else "❌")
                
                cols[0].metric(f"{accuracy_emoji} 正確性", accuracy_label)
                cols[1].metric("⏱️ 応答時間", f"{row['response_time']:.2f}秒")
                cols[2].metric("📝 単語数", f"{row['word_count']}")
                
                # 他の評価指標
                metrics_container = st.container()
                with metrics_container:
                    cols = st.columns(3)
                    if pd.notna(row.get('bleu_score')):
                        cols[0].metric("BLEU", f"{row['bleu_score']:.4f}")
                    if pd.notna(row.get('similarity_score')):
                        cols[1].metric("類似度", f"{row['similarity_score']:.4f}")
                    if pd.notna(row.get('relevance_score')):
                        cols[2].metric("関連性", f"{row['relevance_score']:.4f}")


def display_metrics_analysis(history_df):
    """評価指標の分析結果を表示する"""
    # 解析対象期間の選択
    if 'timestamp' in history_df.columns:
        history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
        min_date = history_df['timestamp'].min().date()
        max_date = history_df['timestamp'].max().date()
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("開始日", min_date)
        with col2:
            end_date = st.date_input("終了日", max_date)
        
        # 日付でフィルタリング
        date_filtered_df = history_df[
            (history_df['timestamp'].dt.date >= start_date) &
            (history_df['timestamp'].dt.date <= end_date)
        ]
    else:
        date_filtered_df = history_df
    
    # is_correct が NaN のレコードを除外して分析
    analysis_df = date_filtered_df.dropna(subset=['is_correct'])
    if analysis_df.empty:
        st.warning("選択された期間に分析可能な評価データがありません。")
        return
    
    # 集計結果の概要
    total_questions = len(analysis_df)
    accurate_count = sum(analysis_df['is_correct'] == 1.0)
    partially_count = sum(analysis_df['is_correct'] == 0.5)
    inaccurate_count = sum(analysis_df['is_correct'] == 0.0)
    
    # 4列で表示する良さそうな指標
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("総質問数", total_questions)
    col2.metric("正確な回答", f"{accurate_count} ({accurate_count/total_questions:.1%})")
    col3.metric("部分的に正確", f"{partially_count} ({partially_count/total_questions:.1%})")
    col4.metric("不正確な回答", f"{inaccurate_count} ({inaccurate_count/total_questions:.1%})")
    
    # 正確性ラベルの作成
    accuracy_labels = {1.0: '正確', 0.5: '部分的に正確', 0.0: '不正確'}
    analysis_df['正確性'] = analysis_df['is_correct'].map(accuracy_labels)
    
    # グラフ表示を2列に分ける
    col1, col2 = st.columns(2)
    
    # 正確性の分布（円グラフ）
    with col1:
        st.write("##### 正確性の分布")
        accuracy_counts = analysis_df['正確性'].value_counts()
        if not accuracy_counts.empty:
            st.bar_chart(accuracy_counts)
        else:
            st.info("正確性データがありません。")
    
    # 時系列での正確性の推移
    with col2:
        st.write("##### 日別の正確性推移")
        if 'timestamp' in analysis_df.columns:
            # 日付ごとの正確性の平均を計算
            analysis_df['date'] = analysis_df['timestamp'].dt.date
            daily_accuracy = analysis_df.groupby('date')['is_correct'].mean()
            
            if not daily_accuracy.empty:
                st.line_chart(daily_accuracy)
            else:
                st.info("日別の正確性データがありません。")
        else:
            st.info("タイムスタンプデータがありません。")
    
    # 応答時間と他の指標の関係
    st.write("##### 応答時間とその他の指標の関係")
    metric_options = ["bleu_score", "similarity_score", "relevance_score", "word_count"]
    # 利用可能な指標のみ選択肢に含める
    valid_metric_options = [m for m in metric_options if m in analysis_df.columns and analysis_df[m].notna().any()]
    
    if valid_metric_options:
        col1, col2 = st.columns([1, 3])
        with col1:
            metric_option = st.selectbox(
                "比較する評価指標",
                valid_metric_options,
                key="metric_select"
            )
        
        chart_data = analysis_df[['response_time', metric_option, '正確性']].dropna()  # NaNを除外
        if not chart_data.empty:
            st.scatter_chart(
                chart_data,
                x='response_time',
                y=metric_option,
                color='正確性',
            )
        else:
            st.info(f"選択された指標 ({metric_option}) と応答時間の有効なデータがありません。")
    else:
        st.info("応答時間と比較できる指標データがありません。")
    
    # 全体の評価指標の統計とカスタム効率性スコア
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("##### 評価指標の統計")
        stats_cols = ['response_time', 'bleu_score', 'similarity_score', 'word_count', 'relevance_score']
        valid_stats_cols = [c for c in stats_cols if c in analysis_df.columns and analysis_df[c].notna().any()]
        if valid_stats_cols:
            metrics_stats = analysis_df[valid_stats_cols].describe()
            st.dataframe(metrics_stats)
        else:
            st.info("統計情報を計算できる評価指標データがありません。")
    
    with col2:
        st.write("##### 正確性レベル別の平均スコア")
        if valid_stats_cols and '正確性' in analysis_df.columns:
            try:
                accuracy_groups = analysis_df.groupby('正確性')[valid_stats_cols].mean()
                st.dataframe(accuracy_groups)
            except Exception as e:
                st.warning(f"正確性別スコアの集計中にエラーが発生しました: {e}")
        else:
            st.info("正確性レベル別の平均スコアを計算できるデータがありません。")
    
    # カスタム評価指標：効率性スコア
    st.write("##### 効率性スコア (正確性 / (応答時間 + 0.1))")
    if 'response_time' in analysis_df.columns and analysis_df['response_time'].notna().any():
        # ゼロ除算を避けるために0.1を追加
        analysis_df['efficiency_score'] = analysis_df['is_correct'] / (analysis_df['response_time'].fillna(0) + 0.1)
        
        # 効率性の高い上位10件を抽出
        top_efficiency = analysis_df.sort_values('efficiency_score', ascending=False).head(10)
        
        if not top_efficiency.empty:
            # 効率性スコアをグラフ表示
            efficiency_data = top_efficiency[['question', 'efficiency_score']].set_index('question')
            st.bar_chart(efficiency_data)
            
            # 表形式でも表示
            st.write("効率性スコアトップ10の質問:")
            st.dataframe(
                top_efficiency[['question', 'is_correct', 'response_time', 'efficiency_score']],
                hide_index=True
            )
        else:
            st.info("効率性スコアデータがありません。")
    else:
        st.info("効率性スコアを計算するための応答時間データがありません。")


# --- サンプルデータ管理ページのUI ---
def display_data_page():
    """サンプルデータ管理ページのUIを表示する"""
    st.title("🗄️ データ管理")
    
    # データの統計情報を表示
    count = get_db_count()
    
    # ステータスカードでデータベース情報を表示
    col1, col2, col3 = st.columns(3)
    col1.metric("現在のレコード数", count)
    
    # データ管理アクション
    st.subheader("データ操作")
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.write("##### サンプルデータの追加")
            st.write("テスト・分析用のサンプルデータを追加します。")
            sample_count = st.number_input("追加するサンプル数", min_value=1, max_value=100, value=10, step=1)
            if st.button("サンプルデータを追加", key="create_samples", use_container_width=True):
                with st.spinner(f"{sample_count}件のサンプルデータを生成中..."):
                    create_sample_evaluation_data(count=sample_count)
                    st.success(f"{sample_count}件のサンプルデータが追加されました！")
                    st.rerun()
    
    with col2:
        with st.container():
            st.write("##### データベースのクリア")
            st.write("⚠️ この操作は元に戻せません。すべてのデータが削除されます。")
            confirm_clear = st.text_input("確認のため「DELETE」と入力してください", key="confirm_clear")
            clear_disabled = confirm_clear != "DELETE"
            
            if st.button("データベースをクリア", disabled=clear_disabled, key="clear_db_button", use_container_width=True):
                with st.spinner("データベースをクリア中..."):
                    if clear_db():
                        st.success("データベースが正常にクリアされました。")
                        st.rerun()
    
    # 評価指標に関する解説
    st.subheader("評価指標の説明")
    metrics_info = get_metrics_descriptions()
    
    # 2列のグリッドで指標を表示
    col1, col2 = st.columns(2)
    metrics_list = list(metrics_info.items())
    
    for i, (metric, description) in enumerate(metrics_list):
        if i % 2 == 0:
            with col1:
                with st.expander(f"{metric}"):
                    st.markdown(description)
        else:
            with col2:
                with st.expander(f"{metric}"):
                    st.markdown(description)

# --- メイン関数 ---
def main():
    # ページ設定とナビゲーション
    page = setup_page()
    
    # パイプラインの初期化（実際の実装に合わせて変更）
    # これはダミーのパイプライン参照
    pipe = None  
    
    # 選択されたページを表示
    if page == "チャット":
        display_chat_page(pipe)
    elif page == "履歴と分析":
        display_history_page()
    elif page == "データ管理":
        display_data_page()

if __name__ == "__main__":
    main()