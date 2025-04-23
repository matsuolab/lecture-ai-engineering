# database.py
import sqlite3
import pandas as pd
from datetime import datetime
import streamlit as st
from config import DB_FILE
from metrics import calculate_metrics  # metricsを計算するために必要

# --- スキーマ定義 ---
TABLE_NAME = "chat_history"
SCHEMA = f'''
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    question TEXT,
    answer TEXT,
    feedback TEXT,
    correct_answer TEXT,
    is_correct REAL,
    response_time REAL,
    bleu_score REAL,
    similarity_score REAL,
    word_count INTEGER,
    relevance_score REAL,
    gram1_score REAL,
    gram2_score REAL,
    gram3_score REAL,
    gram4_score REAL
)
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
        raise e

# --- データ操作関数 ---
def save_to_db(question, answer, feedback, correct_answer, is_correct, response_time):
    """チャット履歴と評価指標をデータベースに保存する"""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # メトリクスを計算
        bleu_score, similarity_score, word_count, relevance_score, ngram_scores = calculate_metrics(
            answer, correct_answer
        )
        one_gram = ngram_scores.get("1-gram_score", 0.0)
        two_gram = ngram_scores.get("2-gram_score", 0.0)
        three_gram = ngram_scores.get("3-gram_score", 0.0)
        four_gram = ngram_scores.get("4-gram_score", 0.0)

        c.execute(f'''
        INSERT INTO {TABLE_NAME} (
            timestamp, question, answer, feedback, correct_answer, is_correct,
            response_time, bleu_score, similarity_score, word_count, relevance_score,
            gram1_score, gram2_score, gram3_score, gram4_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp, question, answer, feedback, correct_answer, is_correct,
            response_time, bleu_score, similarity_score, word_count, relevance_score,
            one_gram, two_gram, three_gram, four_gram
        ))
        conn.commit()
        print("Data saved to DB successfully.")
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
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC", conn)
        if 'is_correct' in df.columns:
            df['is_correct'] = pd.to_numeric(df['is_correct'], errors='coerce')
        return df
    except sqlite3.Error as e:
        st.error(f"履歴の取得中にエラーが発生しました: {e}")
        return pd.DataFrame()
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
        return False

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()
        st.success("データベースが正常にクリアされました。")
        st.session_state.confirm_clear = False
        return True
    except sqlite3.Error as e:
        st.error(f"データベースのクリア中にエラーが発生しました: {e}")
        st.session_state.confirm_clear = False
        return False
    finally:
        if conn:
            conn.close()
