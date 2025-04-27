import streamlit as st
import pandas as pd
import time

# -------------------------------------------------
# ページ設定
# -------------------------------------------------
st.set_page_config(
    page_title="Git 使い方講座 - 初心者向け",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# タイトル & 説明
# -------------------------------------------------
st.title("🐙 Git 使い方講座 (初心者向け)")
st.markdown(
    """
### このページでは、Git の **超基本操作** をシンプルに学びます  
- **コマンドはすべてコピペ可能**  
- 手元のターミナルで実際に動かしながら確認してみましょう  
- わからなくなったら右サイドバーからトピックを切り替えてください
"""
)

st.divider()

# -------------------------------------------------
# サイドバー：ナビゲーション
# -------------------------------------------------
st.sidebar.header("📚 学習ナビ")
topic = st.sidebar.radio(
    "トピックを選択してください",
    (
        "① Git を準備しよう",
        "② ローカル作業の基本",
        "③ ブランチを使おう",
        "④ リモートへ Push",
        "⑤ 困ったときの対処法",
    ),
)

# -------------------------------------------------
# トピック ①：Git を準備しよう
# -------------------------------------------------
if topic.startswith("①"):
    st.header("① Git を準備しよう")
    st.markdown(
        """
#### 1. Git のインストール確認
ターミナルで以下を実行し、バージョンが表示されれば OK です。
"""
    )
    st.code("git --version")

    st.markdown(
        """
#### 2. ユーザー情報を設定  
コミットに「誰が」「どのメールで」作業したかを残します。
"""
    )
    st.code(
        """
git config --global user.name  "YOUR_NAME"
git config --global user.email "YOUR_EMAIL@example.com"
"""
    )

    st.markdown(
        """
#### 3. 設定内容を確認
"""
    )
    st.code("git config --list --global")

# -------------------------------------------------
# トピック ②：ローカル作業の基本
# -------------------------------------------------
elif topic.startswith("②"):
    st.header("② ローカル作業の基本")
    st.markdown("#### 1. 新しいリポジトリを作成")
    st.code(
        """
mkdir my_project
cd my_project
git init      # .git フォルダが作成される
"""
    )

    st.markdown("#### 2. 変更を確認 & ステージング")
    st.code(
        """
git status              # 変更点を確認
git add <ファイル名>     # 変更をステージへ
git add .               # まとめて追加
"""
    )

    st.markdown("#### 3. コミットを作成")
    st.code('git commit -m "最初のコミット"')

    st.info("💡 **Tip**: `git add` → `git commit` の 2 段階で履歴に残すイメージです。")

# -------------------------------------------------
# トピック ③：ブランチを使おう
# -------------------------------------------------
elif topic.startswith("③"):
    st.header("③ ブランチを使おう")
    st.markdown("#### 1. ブランチを作成して切り替え")
    st.code(
        """
git branch feature-xyz       # ブランチ作成
git switch feature-xyz       # あるいは: git checkout feature-xyz
"""
    )

    st.markdown("#### 2. 変更をコミットして main に統合")
    st.code(
        """
# (feature-xyz 上で編集 → add → commit)
git switch main
git merge feature-xyz
"""
    )
    st.success("マージ完了！ 🎉")

# -------------------------------------------------
# トピック ④：リモートへ Push
# -------------------------------------------------
elif topic.startswith("④"):
    st.header("④ リモートへ Push")
    st.markdown("#### 1. GitHub で空のリポジトリを作成し、URL をコピー")
    st.markdown(
        "> 例: `https://github.com/YOUR_NAME/my_project.git` を想定します。"
    )

    st.markdown("#### 2. リモートを登録して Push")
    st.code(
        """
git remote add origin https://github.com/YOUR_NAME/my_project.git
git branch -M main           # main ブランチを既定に
git push -u origin main      # 初回のみ -u を付けると追跡設定される
"""
    )

    # プログレスバーで Push を疑似体験
    st.subheader("Push のイメージ")
    prog = st.progress(0, text="Push 中...")
    for i in range(101):
        time.sleep(0.01)
        prog.progress(i, text=f"Push 中... {i}%")
    st.balloons()

# -------------------------------------------------
# トピック ⑤：困ったときの対処法
# -------------------------------------------------
elif topic.startswith("⑤"):
    st.header("⑤ 困ったときの対処法")
    st.markdown("#### 1. 直前の add を取り消す")
    st.code("git restore --staged <ファイル名>")

    st.markdown("#### 2. 直前の commit メッセージを修正")
    st.code('git commit --amend -m "修正後のメッセージ"')

    st.markdown("#### 3. うっかりファイルを消したとき")
    st.code("git restore <ファイル名>")

    st.warning("⚠️ **注意**: `git reset --hard` は履歴を巻き戻す強力なコマンド。使う前に必ず `git log` で確認！")

# -------------------------------------------------
# よく使うコマンド早見表
# -------------------------------------------------
st.divider()
st.subheader("📌 よく使う Git コマンド早見表")

cmd_df = pd.DataFrame(
    {
        "コマンド": [
            "git init",
            "git status",
            "git add <file>",
            "git commit -m 'msg'",
            "git branch <name>",
            "git switch <name>",
            "git merge <name>",
            "git clone <url>",
            "git pull",
            "git push",
        ],
        "説明": [
            "リポジトリを初期化",
            "変更点を確認",
            "ファイルをステージへ",
            "ステージ → 履歴へ",
            "新しいブランチを作成",
            "ブランチを切り替え",
            "ブランチを統合",
            "リポジトリを複製",
            "リモートの変更を取得",
            "ローカル変更を送信",
        ],
    }
)
st.dataframe(cmd_df, use_container_width=True)

# -------------------------------------------------
# フッター
# -------------------------------------------------
st.markdown(
    """
---
##### 🚀 これで準備完了！  
ローカルで実際にコマンドを打ってみて、Git のワークフローを体感しましょう。
"""
)
