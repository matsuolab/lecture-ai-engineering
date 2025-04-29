import streamlit as st
import random
import time
import pandas as pd
import altair as alt

# ============================================
# ページ設定
# ============================================
st.set_page_config(
    page_title="おみくじアプリ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# タイトルと説明
# ============================================
st.title("🎋 おみくじアプリ")
st.markdown("名前を入力して、おみくじを引いてみましょう🎲")

# ============================================
# サイドバー 
# ============================================
st.sidebar.header("おみくじガイド")
st.sidebar.info("名前を入力し、『おみくじを引く』ボタンをクリックしてください。 過去の結果を詳細な時間軸で確認できます。")

# ============================================
# セッションステート初期化
# ============================================
if 'history' not in st.session_state:
    st.session_state.history = []  # 過去の結果を保存（time, result）

# ============================================
# おみくじ機能
# ============================================
name = st.text_input("あなたの名前", "ゲスト")
st.write(f"こんにちは、{name}さん🎋")

st.subheader("おみくじを引く")
if st.button("おみくじを引く！"):
    with st.spinner("運勢を占っています..."):
        time.sleep(1.5)
    fortunes = ["大吉", "中吉", "小吉", "凶", "大凶"]
    probabilities = [0.2, 0.3, 0.3, 0.15, 0.05]
    result = random.choices(fortunes, probabilities)[0]
    timestamp = pd.Timestamp.now()
    st.session_state.history.append({'time': timestamp, 'result': result})
    st.success(f"{result}が出ました！🎉")
    st.balloons()

# ============================================
# 結果の推移グラフ (詳細時間軸 vs 運勢カテゴリ)
# ============================================
st.subheader("おみくじ結果の推移")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    # Altairでプロット: x軸に年月日時分秒を表示
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('time:T', title='時間', axis=alt.Axis(format='%Y-%m-%d %H:%M:%S')),
        y=alt.Y('result:N', title='運勢', sort=["大吉", "中吉", "小吉", "凶", "大凶"]),
        tooltip=[alt.Tooltip('time:T', title='日時', format='%Y-%m-%d %H:%M:%S'), 'result:N']
    ).properties(width=800, height=400)
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("まだおみくじを引いていません。")

# おみくじ詳細のエクスパンダー
with st.expander("おみくじの説明を表示"):    
    st.write(
        "- **大吉**: 全てが順調に進むでしょう。\n"
        "- **中吉**: 良いことも悪いこともほどほどです。\n"
        "- **小吉**: 小さな幸運がありますが、慎重に。\n"
        "- **凶**: 用心深く過ごしましょう。\n"
        "- **大凶**: 大きな試練があるかもしれません。"
    )

# カスタムCSS
st.markdown("""
<style>
.big-font {
    font-size:24px !important;
    font-weight: bold;
    color: #d6336c;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="big-font">おみくじを楽しんでください！</p>', unsafe_allow_html=True)
