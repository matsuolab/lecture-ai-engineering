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
    print("NLTK loaded successfully.")  # デバッグ用
except Exception as e:
    st.warning(f"NLTKの初期化中にエラーが発生しました: {e}\n簡易的な代替関数を使用します。")
    def nltk_word_tokenize(text):
        return text.split()
    def nltk_sentence_bleu(references, candidate, weights=(0.25,0.25,0.25,0.25)):
        # 簡易BLEUスコア（完全一致/部分一致）
        ref_words = set(references[0])
        cand_words = set(candidate)
        common_words = ref_words.intersection(cand_words)
        precision = len(common_words) / len(cand_words) if cand_words else 0
        recall = len(common_words) / len(ref_words) if ref_words else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return f1


def initialize_nltk():
    """NLTKのデータダウンロードを試みる関数"""
    try:
        nltk.download('punkt', quiet=True)
        print("NLTK Punkt data checked/downloaded.")
    except Exception as e:
        st.error(f"NLTKデータのダウンロードに失敗しました: {e}")


def calculate_metrics(answer, correct_answer):
    """回答と正解から評価指標を計算し、1～4グラムの一致率も返す"""
    word_count = 0
    bleu_score = 0.0
    similarity_score = 0.0
    relevance_score = 0.0
    ngram_scores = {f"{n}-gram_score": 0.0 for n in range(1,5)}

    if not answer:
        return bleu_score, similarity_score, word_count, relevance_score, ngram_scores

    # 単語数のカウント
    tokenizer = Tokenizer()
    tokens = list(tokenizer.tokenize(answer))
    word_count = len(tokens)

    if correct_answer:
        answer_lower = answer.lower()
        correct_lower = correct_answer.lower()

        # BLEU スコア
        try:
            reference = [nltk_word_tokenize(correct_lower)]
            candidate = nltk_word_tokenize(answer_lower)
            bleu_score = nltk_sentence_bleu(reference, candidate)
        except Exception:
            bleu_score = 0.0

        # コサイン類似度
        try:
            vectorizer = TfidfVectorizer()
            if answer_lower.strip() and correct_lower.strip():
                tfidf = vectorizer.fit_transform([answer_lower, correct_lower])
                similarity_score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        except Exception:
            similarity_score = 0.0

        # 関連性スコア
        try:
            aw = set(re.findall(r'\w+', answer_lower))
            cw = set(re.findall(r'\w+', correct_lower))
            if cw:
                relevance_score = len(aw & cw) / len(cw)
        except Exception:
            relevance_score = 0.0

        # n-gram一致率の計算
        try:
            # 単語トークンを取得
            ref_tokens = nltk_word_tokenize(correct_lower)
            cand_tokens = nltk_word_tokenize(answer_lower)
            for n in range(1,5):
                # n-gramリスト作成
                ref_ngrams = [tuple(ref_tokens[i:i+n]) for i in range(len(ref_tokens)-n+1)]
                cand_ngrams = [tuple(cand_tokens[i:i+n]) for i in range(len(cand_tokens)-n+1)]
                if cand_ngrams and ref_ngrams:
                    common = set(ref_ngrams) & set(cand_ngrams)
                    ngram_scores[f"{n}-gram_score"] = len(common) / len(ref_ngrams)
        except Exception:
            pass

    return bleu_score, similarity_score, word_count, relevance_score, ngram_scores


def get_metrics_descriptions():
    """評価指標の説明を返す"""
    return {
        "正確性スコア (is_correct)": "回答の正確さを3段階で評価: 1.0 (正確), 0.5 (部分的に正確), 0.0 (不正確)",
        "応答時間 (response_time)": "質問を投げてから回答を得るまでの時間（秒）。モデルの効率性を表す",
        "BLEU スコア (bleu_score)": "機械翻訳評価指標で、正解と回答のn-gramの一致度を測定 (0〜1の値、高いほど類似)",
        "類似度スコア (similarity_score)": "TF-IDFベクトルのコサイン類似度による、正解と回答の意味的な類似性 (0〜1の値)",
        "単語数 (word_count)": "回答に含まれる単語の数。情報量や詳細さの指標",
        "関連性スコア (relevance_score)": "正解と回答の共通単語の割合。トピックの関連性を表す (0〜1の値)",
        "1-gram_score": "正解文と回答文の1-gram一致率。正解中の単語がどれだけ回答に含まれるか (0〜1)",
        "2-gram_score": "正解文と回答文の2-gram一致率。連続2単語の一致率 (0〜1)",
        "3-gram_score": "正解文と回答文の3-gram一致率。連続3単語の一致率 (0〜1)",
        "4-gram_score": "正解文と回答文の4-gram一致率。連続4単語の一致率 (0〜1)",
        "効率性スコア (efficiency_score)": "正確性を応答時間で割った値。高速で正確な回答ほど高スコア"
    }