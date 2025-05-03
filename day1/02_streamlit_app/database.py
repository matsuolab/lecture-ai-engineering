# database.py
import sqlite3
import pandas as pd
from datetime import datetime
import streamlit as st
from config import DB_FILE
from metrics import calculate_metrics # metricsを計算するために必要

# --- スキーマ定義 ---
TABLE_NAME = "chat_history"
SCHEMA = f'''
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 timestamp TEXT,
 question TEXT,
 answer TEXT,
 feedback TEXT,
 correct_answer TEXT,
 is_correct REAL,      -- INTEGERからREALに変更 (0.5を許容するため)
 response_time REAL,
 bleu_score REAL,
 similarity_score REAL,
 word_count INTEGER,
 relevance_score REAL)
'''

# --- データベース初期化 ---
def init_db():
    """データベースとテーブルを初期化する"""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(SCHEMA)
        conn.commit()
        conn.close()
        print(f"Database '{DB_FILE}' initialized successfully.")
    except Exception as e:
        st.error(f"データベースの初期化に失敗しました: {e}")
        raise e # エラーを再発生させてアプリの起動を止めるか、適切に処理する

# --- データ操作関数 ---
def save_to_db(question, answer, feedback, correct_answer, is_correct, response_time):
    """チャット履歴と評価指標をデータベースに保存する"""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 追加の評価指標を計算
        bleu_score, similarity_score, word_count, relevance_score = calculate_metrics(
            answer, correct_answer
        )

        c.execute(f'''
        INSERT INTO {TABLE_NAME} (timestamp, question, answer, feedback, correct_answer, is_correct,
                                 response_time, bleu_score, similarity_score, word_count, relevance_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, question, answer, feedback, correct_answer, is_correct,
             response_time, bleu_score, similarity_score, word_count, relevance_score))
        conn.commit()
        print("Data saved to DB successfully.") # デバッグ用
    except sqlite3.Error as e:
        st.error(f"データベースへの保存中にエラーが発生しました: {e}")
    finally:
        if conn:
            conn.close()

def get_chat_history():
    """データベースから全てのチャット履歴を取得する"""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        # is_correctがREAL型なので、それに応じて読み込む
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC", conn)
        # is_correct カラムのデータ型を確認し、必要なら変換
        if 'is_correct' in df.columns:
             df['is_correct'] = pd.to_numeric(df['is_correct'], errors='coerce') # 数値に変換、失敗したらNaN
        return df
    except sqlite3.Error as e:
        st.error(f"履歴の取得中にエラーが発生しました: {e}")
        return pd.DataFrame() # 空のDataFrameを返す
    finally:
        if conn:
            conn.close()

def get_db_count():
    """データベース内のレコード数を取得する"""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        count = c.fetchone()[0]
        return count
    except sqlite3.Error as e:
        st.error(f"レコード数の取得中にエラーが発生しました: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def clear_db():
    """データベースの全レコードを削除する"""
    conn = None
    confirmed = st.session_state.get("confirm_clear", False)

    if not confirmed:
        st.warning("本当にすべてのデータを削除しますか？もう一度「データベースをクリア」ボタンを押すと削除が実行されます。")
        st.session_state.confirm_clear = True
        return False # 削除は実行されなかった

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()
        st.success("データベースが正常にクリアされました。")
        st.session_state.confirm_clear = False # 確認状態をリセット
        return True # 削除成功
    except sqlite3.Error as e:
        st.error(f"データベースのクリア中にエラーが発生しました: {e}")
        st.session_state.confirm_clear = False # エラー時もリセット
        return False # 削除失敗
    finally:
        if conn:
            conn.close()