import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ============================================
# ページ設定
# ============================================
st.set_page_config(
    page_title="シンプルTODOリスト",
    page_icon="✅",
    layout="centered",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    /* 全体設定 */
    .main {
        background-color: #F8F9FA;
        padding: 20px;
    }
    
    /* ヘッダー */
    .app-header {
        color: #0C63E7;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* カード */
    .task-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #0C63E7;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .completed-task {
        background-color: #F1F5F9;
        border-left: 5px solid #10B981;
    }
    
    .high-priority {
        border-left: 5px solid #EF4444;
    }
    
    .medium-priority {
        border-left: 5px solid #F59E0B;
    }
    
    .low-priority {
        border-left: 5px solid #3B82F6;
    }
    
    /* セクションヘッダー */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1F2937;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 0.5rem;
    }
    
    /* フッター */
    .footer {
        text-align: center;
        color: #6B7280;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
    }
    
    /* データ可視化セクション */
    .metrics-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# セッション状態の初期化
# ============================================
if 'tasks' not in st.session_state:
    # デフォルトのタスクを用意
    default_tasks = [
        {"title": "牛乳を買う", "description": "スーパーで低脂肪牛乳1リットルを購入", "due_date": "2025-04-24", "priority": "中", "completed": False},
        {"title": "Streamlitの勉強", "description": "Streamlitの基本機能を理解する", "due_date": "2025-04-25", "priority": "高", "completed": False},
        {"title": "レポート提出", "description": "マーケティング分析レポートを完成させる", "due_date": "2025-04-30", "priority": "高", "completed": False},
        {"title": "部屋の掃除", "description": "リビングと寝室の掃除", "due_date": "2025-04-27", "priority": "低", "completed": True},
    ]
    st.session_state.tasks = default_tasks

if 'task_filter' not in st.session_state:
    st.session_state.task_filter = "すべて"

# ============================================
# サイドバー
# ============================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2387/2387635.png", width=100)
    st.markdown("### TODOリストアプリ")
    st.markdown("---")
    
    # フィルター設定
    st.markdown("### 📋 タスク表示設定")
    filter_options = ["すべて", "未完了", "完了", "優先度: 高", "優先度: 中", "優先度: 低"]
    selected_filter = st.selectbox("フィルター", filter_options)
    st.session_state.task_filter = selected_filter
    
    # 並び替え設定
    st.markdown("### 🔄 並び替え設定")
    sort_options = ["追加日時", "期限", "優先度"]
    sort_by = st.selectbox("並び替え", sort_options)
    
    st.markdown("---")
    
    # 統計情報
    st.markdown("### 📊 タスク統計")
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for task in st.session_state.tasks if task["completed"])
    pending_tasks = total_tasks - completed_tasks
    
    st.markdown(f"**合計タスク数:** {total_tasks}")
    st.markdown(f"**完了タスク:** {completed_tasks}")
    st.markdown(f"**未完了タスク:** {pending_tasks}")
    
    if total_tasks > 0:
        progress = completed_tasks / total_tasks
        st.progress(progress)
        st.markdown(f"**進捗状況:** {progress:.0%}")
    
    st.markdown("---")
    st.markdown("### 🎨 表示設定")
    show_descriptions = st.checkbox("詳細を表示", value=True)
    dark_mode = st.checkbox("ダークモード", value=False)

# ============================================
# メインコンテンツ
# ============================================
st.markdown('<h1 class="app-header">✅ TODOリスト</h1>', unsafe_allow_html=True)

# タスク追加フォーム
st.markdown('<div class="section-header">新しいタスク</div>', unsafe_allow_html=True)

with st.form(key="add_task_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        task_title = st.text_input("タスク名", placeholder="タスクの名前を入力してください")
    
    with col2:
        task_priority = st.selectbox("優先度", ["高", "中", "低"])
    
    task_description = st.text_area("詳細", placeholder="タスクの詳細を入力（任意）", height=100)
    
    col3, col4 = st.columns(2)
    
    with col3:
        task_due_date = st.date_input("期限", datetime.now())
    
    with col4:
        # スペース調整用
        st.write("")
        st.write("")
        submit_button = st.form_submit_button(label="タスクを追加", use_container_width=True)

if submit_button and task_title:
    # 新しいタスクを追加
    new_task = {
        "title": task_title,
        "description": task_description,
        "due_date": task_due_date.strftime("%Y-%m-%d"),
        "priority": task_priority,
        "completed": False
    }
    st.session_state.tasks.append(new_task)
    st.success(f"タスク「{task_title}」を追加しました！")
    st.experimental_rerun()

# タスクリストの表示
st.markdown('<div class="section-header">タスク一覧</div>', unsafe_allow_html=True)

# フィルタリング
filtered_tasks = st.session_state.tasks
if st.session_state.task_filter == "未完了":
    filtered_tasks = [task for task in st.session_state.tasks if not task["completed"]]
elif st.session_state.task_filter == "完了":
    filtered_tasks = [task for task in st.session_state.tasks if task["completed"]]
elif st.session_state.task_filter.startswith("優先度:"):
    priority = st.session_state.task_filter.split(": ")[1]
    filtered_tasks = [task for task in st.session_state.tasks if task["priority"] == priority]

# 並び替え
if sort_by == "期限":
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x["due_date"])
elif sort_by == "優先度":
    priority_order = {"高": 0, "中": 1, "低": 2}
    filtered_tasks = sorted(filtered_tasks, key=lambda x: priority_order[x["priority"]])

# タスクがない場合
if not filtered_tasks:
    st.info("タスクがありません。新しいタスクを追加してください。")

# タスクの表示
for i, task in enumerate(filtered_tasks):
    priority_class = f"{task['priority'].lower()}-priority"
    completed_class = "completed-task" if task["completed"] else ""
    
    st.markdown(f'<div class="task-card {priority_class} {completed_class}">', unsafe_allow_html=True)
    
    # タスクのヘッダー部分
    col1, col2, col3 = st.columns([5, 2, 1])
    
    with col1:
        # チェックボックスでタスクの完了状態を切り替え
        is_complete = st.checkbox(
            task["title"],
            value=task["completed"],
            key=f"task_{i}"
        )
        if is_complete != task["completed"]:
            st.session_state.tasks[st.session_state.tasks.index(task)]["completed"] = is_complete
            st.experimental_rerun()
    
    with col2:
        st.write(f"期限: {task['due_date']}")
    
    with col3:
        # 優先度によって色を変える
        priority_colors = {"高": "🔴", "中": "🟠", "低": "🔵"}
        st.write(f"{priority_colors[task['priority']]} {task['priority']}")
    
    # 詳細部分
    if show_descriptions and task["description"]:
        st.markdown(f"<p style='margin-left: 24px; color: #6B7280;'>{task['description']}</p>", unsafe_allow_html=True)
    
    # タスク操作ボタン
    col4, col5 = st.columns([6, 1])
    
    with col5:
        if st.button("削除", key=f"delete_{i}"):
            st.session_state.tasks.remove(task)
            st.success("タスクを削除しました")
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# データ可視化
# ============================================
st.markdown('<div class="section-header">📊 タスク分析</div>', unsafe_allow_html=True)

st.markdown('<div class="metrics-container">', unsafe_allow_html=True)

# 優先度別のタスク数
priority_counts = {"高": 0, "中": 0, "低": 0}
for task in st.session_state.tasks:
    priority_counts[task["priority"]] += 1

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("優先度別タスク")
    # 円グラフデータ
    priorities = list(priority_counts.keys())
    counts = list(priority_counts.values())
    
    # Plotlyを使う場合
    try:
        import plotly.express as px
        fig = px.pie(values=counts, names=priorities, hole=0.4,
                    color_discrete_map={"高": "#EF4444", "中": "#F59E0B", "低": "#3B82F6"})
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    except:
        # Plotlyがない場合はmatplotlibを使う
        st.bar_chart(priority_counts)

with chart_col2:
    st.subheader("完了・未完了の割合")
    completion_status = {"完了": 0, "未完了": 0}
    for task in st.session_state.tasks:
        if task["completed"]:
            completion_status["完了"] += 1
        else:
            completion_status["未完了"] += 1
    
    # Plotlyを使う場合
    try:
        fig = px.pie(values=list(completion_status.values()), 
                    names=list(completion_status.keys()), hole=0.4,
                    color_discrete_map={"完了": "#10B981", "未完了": "#6B7280"})
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    except:
        # Plotlyがない場合
        st.bar_chart(completion_status)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# フッター
# ============================================
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("シンプルTODOリスト アプリ | Streamlit で作成")
st.markdown("© 2025 - 全ての権利を放棄します🙃")
st.markdown('</div>', unsafe_allow_html=True)