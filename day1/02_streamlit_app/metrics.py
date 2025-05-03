# metrics.py
import streamlit as st
import nltk
from janome.tokenizer import Tokenizer
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# NLTKのヘルパー関数（エラー時フォールバック付き）
try:
    nltk.download('punkt', quiet=True)
    from nltk.translate.bleu_score import sentence_bleu as nltk_sentence_bleu
    from nltk.tokenize import word_tokenize as nltk_word_tokenize
    print("NLTK loaded successfully.") # デバッグ用
except Exception as e:
    st.warning(f"NLTKの初期化中にエラーが発生しました: {e}\n簡易的な代替関数を使用します。")
    def nltk_word_tokenize(text):
        return text.split()
    def nltk_sentence_bleu(references, candidate):
        # 簡易BLEUスコア（完全一致/部分一致）
        ref_words = set(references[0])
        cand_words = set(candidate)
        common_words = ref_words.intersection(cand_words)
        precision = len(common_words) / len(cand_words) if cand_words else 0
        recall = len(common_words) / len(ref_words) if ref_words else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return f1 # F1スコアを返す（簡易的な代替）

def initialize_nltk():
    """NLTKのデータダウンロードを試みる関数"""
    try:
        nltk.download('punkt', quiet=True)
        print("NLTK Punkt data checked/downloaded.") # デバッグ用
    except Exception as e:
        st.error(f"NLTKデータのダウンロードに失敗しました: {e}")

def calculate_metrics(answer, correct_answer):
    """回答と正解から評価指標を計算する"""
    word_count = 0
    bleu_score = 0.0
    similarity_score = 0.0
    relevance_score = 0.0

    if not answer: # 回答がない場合は計算しない
        return bleu_score, similarity_score, word_count, relevance_score

    # 単語数のカウント
    tokenizer = Tokenizer()
    tokens = list(tokenizer.tokenize(answer))  # ← list() でイテレータをリストに変換
    word_count = len(tokens)

    # 正解がある場合のみBLEUと類似度を計算
    if correct_answer:
        answer_lower = answer.lower()
        correct_answer_lower = correct_answer.lower()

        # BLEU スコアの計算
        try:
            reference = [nltk_word_tokenize(correct_answer_lower)]
            candidate = nltk_word_tokenize(answer_lower)
            # ゼロ除算エラーを防ぐ
            if candidate:
                bleu_score = nltk_sentence_bleu(reference, candidate, weights=(0.25, 0.25, 0.25, 0.25)) # 4-gram BLEU
            else:
                bleu_score = 0.0
        except Exception as e:
            # st.warning(f"BLEUスコア計算エラー: {e}")
            bleu_score = 0.0 # エラー時は0

        # コサイン類似度の計算
        try:
            vectorizer = TfidfVectorizer()
            # fit_transformはリストを期待するため、リストで渡す
            if answer_lower.strip() and correct_answer_lower.strip(): # 空文字列でないことを確認
                tfidf_matrix = vectorizer.fit_transform([answer_lower, correct_answer_lower])
                similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            else:
                similarity_score = 0.0
        except Exception as e:
            # st.warning(f"類似度スコア計算エラー: {e}")
            similarity_score = 0.0 # エラー時は0

        # 関連性スコア（キーワードの一致率などで簡易的に計算）
        try:
            answer_words = set(re.findall(r'\w+', answer_lower))
            correct_words = set(re.findall(r'\w+', correct_answer_lower))
            if len(correct_words) > 0:
                common_words = answer_words.intersection(correct_words)
                relevance_score = len(common_words) / len(correct_words)
            else:
                relevance_score = 0.0
        except Exception as e:
            # st.warning(f"関連性スコア計算エラー: {e}")
            relevance_score = 0.0 # エラー時は0

    return bleu_score, similarity_score, word_count, relevance_score

def get_metrics_descriptions():
    """評価指標の説明を返す"""
    return {
        "正確性スコア (is_correct)": "回答の正確さを3段階で評価: 1.0 (正確), 0.5 (部分的に正確), 0.0 (不正確)",
        "応答時間 (response_time)": "質問を投げてから回答を得るまでの時間（秒）。モデルの効率性を表す",
        "BLEU スコア (bleu_score)": "機械翻訳評価指標で、正解と回答のn-gramの一致度を測定 (0〜1の値、高いほど類似)",
        "類似度スコア (similarity_score)": "TF-IDFベクトルのコサイン類似度による、正解と回答の意味的な類似性 (0〜1の値)",
        "単語数 (word_count)": "回答に含まれる単語の数。情報量や詳細さの指標",
        "関連性スコア (relevance_score)": "正解と回答の共通単語の割合。トピックの関連性を表す (0〜1の値)",
        "効率性スコア (efficiency_score)": "正確性を応答時間で割った値。高速で正確な回答ほど高スコア"
    }