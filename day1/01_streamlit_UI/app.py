import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# ============================================
# ページ設定とテーマ
# ============================================
st.set_page_config(
    page_title="AIマネーアドバイザー",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSSでデザインを改善
st.markdown("""
<style>
    /* 全体のフォントとカラー */
    .main {
        background-color: #f8f9fa;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* ヘッダーのスタイル */
    h1, h2, h3 {
        color: #2E7D32;
    }
    
    /* サイドバーのスタイル */
    .css-1d391kg {
        background-color: #f1f3f4;
    }
    
    /* カードスタイル */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* ボタンのスタイル */
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 8px 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* サブヘッダーのスタイル */
    .subheader {
        font-weight: 600;
        color: #333;
        margin-top: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #2E7D32;
        padding-left: 10px;
    }
    
    /* セクション区切り */
    .section-divider {
        border-top: 1px solid #e0e0e0;
        margin: 30px 0;
    }
    
    /* メトリクス装飾 */
    .metric-card {
        background: linear-gradient(to right, #2E7D32, #81C784);
        color: white;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* ナビゲーションアクティブ状態 */
    .nav-active {
        background-color: #e8f5e9;
        border-left: 4px solid #2E7D32;
        padding-left: 10px;
    }
    
    /* プロフィットメトリクス - 利益 */
    .profit-up {
        color: #2E7D32;
        font-weight: bold;
    }
    
    /* プロフィットメトリクス - 損失 */
    .profit-down {
        color: #C62828;
        font-weight: bold;
    }
    
    /* ヘッダーロゴスタイル */
    .logo-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .logo-text {
        font-size: 28px;
        font-weight: bold;
        margin-left: 10px;
        color: #2E7D32;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# タイトルとイントロセクション
# ============================================
st.markdown("""
<div class='logo-header'>
    <span style='font-size: 40px;'>💰</span>
    <span class='logo-text'>AIマネーアドバイザー</span>
</div>
""", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'><h3>AIがあなたの資産運用をスマートにサポート</h3></div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.info("💡 AI技術を駆使して、あなたの投資ポートフォリオを分析し最適な資産配分を提案します。サイドバーからさまざまな機能をお試しください。")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# サイドバーナビゲーション
# ============================================
with st.sidebar:
    st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <span style='font-size: 32px;'>💰</span>
        <span style='font-size: 20px; font-weight: bold; margin-left: 10px; color: #2E7D32;'>AIマネーアドバイザー</span>
    </div>
    """, unsafe_allow_html=True)
    
    nav_selection = st.radio(
        "メニュー",
        ["🏠 ダッシュボード", "📊 ポートフォリオ分析", "📈 市場動向", "🤖 AIアドバイス", "⚙️ 設定"]
    )
    
    st.markdown("---")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    user_name = "山田太郎"
    plan_type = "プレミアムプラン"
    st.markdown(f"""
    <div style='text-align: center;'>
        <div style='background-color: #e8f5e9; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto;'>
            <span style='font-size: 30px;'>👤</span>
        </div>
        <div style='font-weight: bold;'>{user_name}様</div>
        <div style='font-size: 12px; color: #666;'>{plan_type}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 市場状況ウィジェット
    st.markdown("### 市場状況")
    market_status = {
        "日経平均": {"value": "36,428.67", "change": "+1.2%", "color": "#2E7D32"},
        "TOPIX": {"value": "2,567.82", "change": "+0.8%", "color": "#2E7D32"},
        "ドル/円": {"value": "152.64", "change": "-0.3%", "color": "#C62828"}
    }
    
    for market, data in market_status.items():
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
            <span>{market}</span>
            <span>{data['value']} <span style='color: {data["color"]};'>{data["change"]}</span></span>
        </div>
        """, unsafe_allow_html=True)
    
    # 現在時刻表示
    st.markdown("### 最終更新")
    st.code(f"{time.strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================
# コンテンツセクション（ナビゲーション対応）
# ============================================
if nav_selection == "🏠 ダッシュボード":
    st.markdown("## 📊 ポートフォリオ概要")
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 資産サマリー
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("総資産", "5,280,500円", "↑2.3%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("月間リターン", "+78,500円", "↑1.5%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("年初来リターン", "+320,500円", "↑6.8%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # UI要素を2カラムに整理
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>💹 資産配分状況</div>", unsafe_allow_html=True)
        
        # 円グラフ用のサンプルデータ
        portfolio_data = {
            '国内株式': 35,
            '米国株式': 25,
            '新興国株式': 10,
            '国内債券': 15,
            '海外債券': 10,
            '不動産': 5
        }
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(portfolio_data.values(), labels=portfolio_data.keys(), autopct='%1.1f%%', 
               startangle=90, colors=['#4CAF50', '#81C784', '#A5D6A7', '#2196F3', '#64B5F6', '#FFB74D'])
        ax.axis('equal')
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>📋 最近の取引</div>", unsafe_allow_html=True)
        
        recent_trades = pd.DataFrame({
            '日付': ['2025-04-28', '2025-04-25', '2025-04-20', '2025-04-15', '2025-04-10'],
            '銘柄': ['トヨタ自動車', 'ソフトバンクG', 'S&P500 ETF', '日経225 ETF', 'アマゾン'],
            '取引': ['買付', '買付', '買付', '売却', '買付'],
            '金額': ['120,000円', '85,000円', '50,000円', '100,000円', '70,000円']
        })
        st.table(recent_trades)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>📈 資産推移</div>", unsafe_allow_html=True)
        
        # ラインチャート用のサンプルデータ
        dates = pd.date_range(start="2025-01-01", end="2025-05-01", freq="W")
        values = np.array([4800000, 4780000, 4850000, 4900000, 4850000, 4920000, 4970000, 
                          4950000, 5050000, 5100000, 5080000, 5130000, 5180000, 5220000])
        
        # Ensure the lengths of `dates` and `values` match
        if len(dates) > len(values):
            dates = dates[:len(values)]
        elif len(values) > len(dates):
            values = values[:len(dates)]
        
        asset_data = pd.DataFrame({
            '日付': dates,
            '資産額': values
        })
        
        st.line_chart(asset_data.set_index('日付'), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>🤖 AIアドバイス要約</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
            <div style='font-weight: bold; margin-bottom: 5px;'>💡 ポートフォリオ最適化の提案</div>
            <div>現在の市場動向から、米国株式の比率を<span class='profit-up'>+5%</span>増加し、国内債券を<span class='profit-down'>-5%</span>減少させることで、リスク調整後リターンが改善する可能性があります。</div>
        </div>
        
        <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px;'>
            <div style='font-weight: bold; margin-bottom: 5px;'>📊 パフォーマンス分析</div>
            <div>過去3ヶ月の運用成績は市場平均を<span class='profit-up'>1.2%上回っています</span>。主な要因は国内株式の銘柄選択と資産配分の最適化によるものです。</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🤖 詳細なAIアドバイスを見る"):
            st.success("AIアドバイザーページに移動します...")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 次回の投資計画
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>📆 次回の投資計画</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px;'>
            <div style='font-weight: bold; font-size: 18px; margin-bottom: 10px;'>💰 毎月の積立計画</div>
            <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                <span>積立金額:</span>
                <span style='font-weight: bold;'>50,000円</span>
            </div>
            <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                <span>次回積立日:</span>
                <span style='font-weight: bold;'>2025年5月10日</span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>積立商品:</span>
                <span style='font-weight: bold;'>全世界株式インデックス</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        change_plan = st.selectbox(
            "積立プランを変更",
            ["現在のプラン", "積立金額を増額", "積立金額を減額", "積立商品を変更", "積立を一時停止"]
        )
        
        if change_plan != "現在のプラン":
            st.text_input("変更理由（任意）")
            if st.button("プラン変更を申請"):
                st.success("プラン変更申請を受け付けました。審査後に反映されます。")
                
    st.markdown("</div>", unsafe_allow_html=True)

elif nav_selection == "📊 ポートフォリオ分析":
    st.markdown("## 📊 ポートフォリオ詳細分析")
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # サンプルデータフレームを作成（銘柄一覧）
    df = pd.DataFrame({
        '銘柄名': ['トヨタ自動車', 'ソニーグループ', '任天堂', '三菱UFJ', 'ソフトバンクG', 'S&P500 ETF', '全世界株式ETF', 'REIT ETF'],
        '保有数': [50, 30, 15, 200, 40, 10, 25, 30],
        '現在価格': [3200, 12500, 6800, 1250, 8300, 25000, 18000, 12000],
        '評価額': [160000, 375000, 102000, 250000, 332000, 250000, 450000, 360000],
        'リターン': ['+12.5%', '+8.3%', '+22.1%', '-3.2%', '+15.6%', '+10.2%', '+7.5%', '+3.1%']
    })
    
    tab1, tab2, tab3 = st.tabs(["📋 保有銘柄", "📊 リスク分析", "📌 パフォーマンス"])
    
    with tab1:
        st.markdown("""
        <div class='card'>
        <div class='subheader'>保有銘柄一覧</div>
        銘柄ごとの保有状況と評価額を確認できます。
        </div>
        """, unsafe_allow_html=True)
        
        # 評価額でソート
        df_sorted = df.sort_values(by='評価額', ascending=False)
        
        # リターンに色付け
        def color_returns(val):
            if val.startswith('+'):
                return 'color: green'
            elif val.startswith('-'):
                return 'color: red'
            else:
                return ''
        
        st.dataframe(df_sorted.style.applymap(color_returns, subset=['リターン']), use_container_width=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<div class='subheader'>銘柄検索/フィルター</div>", unsafe_allow_html=True)
            search = st.text_input("銘柄名で検索")
            
            if search:
                filtered_df = df[df['銘柄名'].str.contains(search)]
                st.dataframe(filtered_df, use_container_width=True)
        
        with col2:
            st.markdown("<div class='subheader'>取引操作</div>", unsafe_allow_html=True)
            selected_stock = st.selectbox("銘柄を選択", df['銘柄名'].tolist())
            action = st.radio("取引タイプ", ["買付", "売却"])
            
            if st.button("取引画面へ"):
                st.success(f"{selected_stock}の{action}画面へ移動します...")
    
    with tab2:
        st.markdown("""
        <div class='card'>
        <div class='subheader'>ポートフォリオリスク分析</div>
        あなたのポートフォリオのリスク特性を多角的に分析します。
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='subheader'>リスク指標</div>", unsafe_allow_html=True)
            
            metrics = {
                "標準偏差": "12.3%",
                "シャープレシオ": "0.85",
                "最大ドローダウン": "-18.2%",
                "ベータ値": "0.92"
            }
            
            for metric, value in metrics.items():
                st.markdown(f"""
                <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                    <span>{metric}</span>
                    <span style='font-weight: bold;'>{value}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='subheader'>リスク分散状況</div>", unsafe_allow_html=True)
            
            # リスク分散グラフ用のサンプルデータ
            risk_data = {
                '市場リスク': 45,
                '金利リスク': 20,
                '為替リスク': 15,
                '信用リスク': 10,
                'その他': 10
            }
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(risk_data.keys(), risk_data.values(), color='#81C784')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='subheader'>リスク/リターン散布図</div>", unsafe_allow_html=True)
            
            # 散布図用のサンプルデータ
            scatter_data = pd.DataFrame({
                '銘柄': df['銘柄名'],
                'リスク': [8.2, 12.5, 15.8, 6.3, 18.2, 10.5, 9.2, 7.5],
                'リターン': [9.5, 8.3, 22.1, 3.8, 15.6, 10.2, 7.5, 6.1],
                '評価額': df['評価額'] / 10000  # サイズ表示用に調整
            })
            
            fig, ax = plt.subplots(figsize=(8, 6))
            scatter = ax.scatter(scatter_data['リスク'], scatter_data['リターン'], 
                      s=scatter_data['評価額'], alpha=0.7, c=range(len(scatter_data)), cmap='viridis')
            
            # 散布図の銘柄名ラベル追加
            for i, txt in enumerate(scatter_data['銘柄']):
                ax.annotate(txt, (scatter_data['リスク'][i], scatter_data['リターン'][i]),
                           fontsize=8, ha='center')
            
            ax.set_xlabel('リスク (%)')
            ax.set_ylabel('リターン (%)')
            ax.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='subheader'>最適化シミュレーション</div>", unsafe_allow_html=True)
            st.write("AIがリスク許容度に応じた最適なポートフォリオを提案します")
            
            risk_tolerance = st.slider("リスク許容度", 1, 10, 5)
            
            if st.button("ポートフォリオを最適化"):
                with st.spinner("AIが最適な資産配分を計算中..."):
                    time.sleep(2)
                    st.success("最適化計算が完了しました！")
                    
                    st.markdown("""
                    <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 15px;'>
                        <div style='font-weight: bold; margin-bottom: 10px;'>最適化された資産配分</div>
                        <div>国内株式: <b>30%</b> (現在 35%)</div>
                        <div>米国株式: <b>30%</b> (現在 25%)</div>
                        <div>新興国株式: <b>15%</b> (現在 10%)</div>
                        <div>国内債券: <b>10%</b> (現在 15%)</div>
                        <div>海外債券: <b>10%</b> (現在 10%)</div>
                        <div>不動産: <b>5%</b> (現在 5%)</div>
                        <div style='margin-top: 10px;'>期待リターン: <b>7.8%</b> (現在 6.5%)</div>
                        <div>推定リスク: <b>13.2%</b> (現在 12.3%)</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class='card'>
        <div class='subheader'>パフォーマンス分析</div>
        ポートフォリオのパフォーマンスを時系列で分析します。
        </div>
        """, unsafe_allow_html=True)
        
        # パフォーマンスチャート用のサンプルデータ
        dates = pd.date_range(start="2024-05-01", end="2025-05-01", freq="M")
        portfolio_returns = [1.2, 0.8, -0.5, 1.5, 2.1, -0.3, 0.9, 1.2, 1.8, 0.6, -0.8, 1.5, 2.3]
        benchmark_returns = [1.0, 0.5, -0.8, 1.2, 1.8, -0.5, 0.7, 1.0, 1.5, 0.3, -1.0, 1.2, 2.0]
        
        # 累積リターンに変換
        portfolio_cumulative = [100]
        benchmark_cumulative = [100]
        
        for ret in portfolio_returns:
            portfolio_cumulative.append(portfolio_cumulative[-1] * (1 + ret/100))
            
        for ret in benchmark_returns:
            benchmark_cumulative.append(benchmark_cumulative[-1] * (1 + ret/100))
        
        performance_data = pd.DataFrame({
            '日付': list(dates) + [pd.Timestamp("2025-05-01")],
            'ポートフォリオ': portfolio_cumulative,
            'ベンチマーク': benchmark_cumulative
        })
        
        st.line_chart(performance_data.set_index('日付'), use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='subheader'>期間別リターン</div>", unsafe_allow_html=True)
            
            periods = {
                "1ヶ月": {"portfolio": "+2.3%", "benchmark": "+2.0%", "diff": "+0.3%"},
                "3ヶ月": {"portfolio": "+3.0%", "benchmark": "+2.2%", "diff": "+0.8%"},
                "6ヶ月": {"portfolio": "+5.7%", "benchmark": "+4.7%", "diff": "+1.0%"},
                "1年": {"portfolio": "+11.2%", "benchmark": "+9.5%", "diff": "+1.7%"},
                "年初来": {"portfolio": "+6.8%", "benchmark": "+5.6%", "diff": "+1.2%"}
            }
            
            for period, data in periods.items():
                st.markdown(f"""
                <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                    <span>{period}</span>
                    <span>
                        <span style='color: {"green" if data["portfolio"].startswith("+") else "red"};'>{data["portfolio"]}</span> vs 
                        <span style='color: {"green" if data["benchmark"].startswith("+") else "red"};'>{data["benchmark"]}</span>
                        (<span style='color: {"green" if data["diff"].startswith("+") else "red"};'>{data["diff"]}</span>)
                    </span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='subheader'>パフォーマンス寄与度</div>", unsafe_allow_html=True)
            
            # パフォーマンス寄与度用のサンプルデータ
            contribution_data = pd.DataFrame({
                '資産クラス': ['国内株式', '米国株式', '新興国株式', '国内債券', '海外債券', '不動産'],
                '寄与度': [3.2, 4.5, 1.8, 0.5, 0.7, 0.5]
            }).sort_values(by='寄与度', ascending=False)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            bars = ax.barh(contribution_data['資産クラス'], contribution_data['寄与度'], color='#81C784')
            ax.set_xlabel('寄与度 (%)')
            ax.grid(True, linestyle='--', alpha=0.7, axis='x')
            
            # 値ラベルを追加
            for i, bar in enumerate(bars):
                ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                        f"{contribution_data['寄与度'].iloc[i]}%", va='center')
            
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        time_range = st.select_slider(
            "分析期間",
            options=["1ヶ月", "3ヶ月", "6ヶ月", "1年", "3年", "5年", "全期間"],
            value="1年"
        )
        
        comparison = st.multiselect(
            "比較対象",
            ["日経平均", "TOPIX", "S&P500", "全世界株式", "バランス型ファンド"],
            default=["日経平均", "TOPIX"]
        )
        
        if st.button("分析を更新"):
            st.success(f"パフォーマンス分析を更新しました。期間: {time_range}, 比較対象: {', '.join(comparison)}")
        st.markdown("</div>", unsafe_allow_html=True)

elif nav_selection == "📈 市場動向":
    st.markdown("## 📈 市場動向分析")
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # ダミーチャートデータ
    dates = pd.date_range(start="2025-01-01", end="2025-05-01", freq="B")
    nikkei_values = 100 + np.cumsum(np.random.normal(0.05, 1, len(dates)))
    sp500_values = 100 + np.cumsum(np.random.normal(0.07, 1.1, len(dates)))
    topix_values = 100 + np.cumsum(np.random.normal(0.04, 0.9, len(dates)))
    
    market_data = pd.DataFrame({
        '日付': dates,
        '日経平均': nikkei_values,
        'S&P500': sp500_values,
        'TOPIX': topix_values
    })
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>主要市場インデックス</div>", unsafe_allow_html=True)
    
    index_selection = st.multiselect(
        "表示するインデックスを選択",
        ['日経平均', 'S&P500', 'TOPIX'],
        default=['日経平均', 'S&P500', 'TOPIX']
    )
    
    chart_data = market_data[['日付'] + index_selection].set_index('日付')
    st.line_chart(chart_data)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>市場ニュースと分析</div>", unsafe_allow_html=True)
        
        news_items = [
            {"title": "日銀、金融政策の維持を決定", "date": "2025-05-01", "source": "日本経済新聞"},
            {"title": "米国雇用統計、予想を上回る結果に", "date": "2025-04-28", "source": "ロイター"},
            {"title": "大手IT企業、好決算で株価上昇", "date": "2025-04-25", "source": "ブルームバーグ"},
            {"title": "原油価格、供給懸念で上昇傾向", "date": "2025-04-20", "source": "WSJ"},
            {"title": "アジア市場、中国の景気対策で上昇", "date": "2025-04-15", "source": "CNBC"}
        ]
        
        for item in news_items:
            st.markdown(f"""
            <div style='border-left: 3px solid #2E7D32; padding-left: 10px; margin-bottom: 15px;'>
                <div style='font-weight: bold;'>{item['title']}</div>
                <div style='font-size: 12px; color: #666;'>{item['date']} | {item['source']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("過去のニュースをもっと見る"):
            for i in range(3):
                st.markdown(f"""
                <div style='border-left: 3px solid #2E7D32; padding-left: 10px; margin-bottom: 15px;'>
                    <div style='font-weight: bold;'>過去のニュース記事 {i+1}</div>
                    <div style='font-size: 12px; color: #666;'>2025-04-0{i} | 金融メディア</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>セクターパフォーマンス</div>", unsafe_allow_html=True)
        
        # セクターパフォーマンス用のサンプルデータ
        sectors = {
            'テクノロジー': 8.5,
            'ヘルスケア': 5.2,
            '金融': 3.8,
            '一般消費財': 4.1,
            '素材': -1.2,
            'エネルギー': -2.5,
            '公共事業': 1.8,
            '通信': 2.3,
            '生活必需品': 0.9,
            '不動産': -0.8
        }
        
        sectors_df = pd.DataFrame({
            'セクター': list(sectors.keys()),
            'パフォーマンス': list(sectors.values())
        }).sort_values(by='パフォーマンス', ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.barh(sectors_df['セクター'], sectors_df['パフォーマンス'], 
                color=[('#4CAF50' if x >= 0 else '#F44336') for x in sectors_df['パフォーマンス']])
        
        # 値ラベルを追加
        for i, bar in enumerate(bars):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                   f"{sectors_df['パフォーマンス'].iloc[i]}%", va='center')
        
        ax.set_xlabel('月間パフォーマンス (%)')
        ax.grid(True, linestyle='--', alpha=0.7, axis='x')
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # マクロ経済指標
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>マクロ経済指標</div>", unsafe_allow_html=True)
    
    macro_tab1, macro_tab2 = st.tabs(["国内", "海外"])
    
    with macro_tab1:
        macro_japan = pd.DataFrame({
            '指標': ['GDP成長率', '消費者物価指数', '失業率', '日銀政策金利', '10年国債利回り'],
            '最新値': ['2.1%', '0.8%', '2.4%', '0.1%', '0.25%'],
            '前回': ['1.9%', '0.7%', '2.5%', '0.1%', '0.22%'],
            '変化': ['+0.2%', '+0.1%', '-0.1%', '0.0%', '+0.03%']
        })
        
        st.table(macro_japan)
        
    with macro_tab2:
        macro_global = pd.DataFrame({
            '国/地域': ['米国', '欧州', '中国', '英国', 'インド'],
            'GDP成長率': ['3.2%', '1.8%', '5.5%', '1.5%', '7.2%'],
            '政策金利': ['5.5%', '3.75%', '3.45%', '5.0%', '6.5%'],
            '失業率': ['3.5%', '6.5%', '5.0%', '4.0%', '7.5%']
        })
        
        st.table(macro_global)
    
    chart_period = st.select_slider(
        "チャート期間",
        options=["1週間", "1ヶ月", "3ヶ月", "6ヶ月", "1年", "3年", "5年"],
        value="3ヶ月"
    )
    
    st.markdown(f"<div style='text-align: center; color: #666;'>※表示期間: {chart_period}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif nav_selection == "🤖 AIアドバイス":
    st.markdown("## 🤖 AIによる投資アドバイス")
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card' style='background: linear-gradient(to right, #e8f5e9, #f1f8e9); border-left: 5px solid #2E7D32;'>
        <div style='display: flex; align-items: center;'>
            <span style='font-size: 40px; margin-right: 15px;'>🤖</span>
            <div>
                <div style='font-weight: bold; font-size: 20px;'>AIファイナンシャルアドバイザー</div>
                <div>あなたの投資目標と市場環境に基づいた最適なアドバイスを提供します</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>📊 ポートフォリオ分析レポート</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: #f8f9fa; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
            <h4 style='color: #2E7D32; margin-top: 0;'>現在のポートフォリオ評価</h4>
            <p>
                あなたのポートフォリオは<strong>適度にバランス</strong>が取れていますが、いくつかの改善点があります。
                全体的なリスク調整後リターンは市場平均を<span style='color: #2E7D32;'>1.2%上回っています</span>。
                ただし、国内株式への比重がやや高く、グローバル分散の観点では改善の余地があります。
            </p>
            
            <h4 style='color: #2E7D32;'>強み</h4>
            <ul>
                <li>優良企業への投資が中心で長期的な成長期待が高い</li>
                <li>テクノロジーセクターの銘柄選定が優れており、超過リターンに貢献</li>
                <li>配当利回りが平均3.2%と市場平均を上回る</li>
            </ul>
            
            <h4 style='color: #2E7D32;'>改善点</h4>
            <ul>
                <li>国内株式への比重が高く、地域分散が不足している</li>
                <li>債券のデュレーションが長く、金利上昇リスクに弱い</li>
                <li>新興国市場へのエクスポージャーが限定的</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: #e8f5e9; border-radius: 10px; padding: 20px;'>
            <h4 style='color: #2E7D32; margin-top: 0;'>AIアドバイス</h4>
            <p>
                <strong>資産配分の最適化</strong>：国内株式の比率を5%減らし、その分を新興国株式に振り替えることで、
                リスクを増やさずにリターンが0.3%向上する可能性があります。
            </p>
            <p>
                <strong>セクター配分</strong>：景気循環への対応として、防衛的セクター（生活必需品、ヘルスケア）の
                比率を2-3%増やすことで、ポートフォリオの下方耐性を高めることができます。
            </p>
            <p>
                <strong>債券ポートフォリオ</strong>：現在の長期債中心の構成から、短中期債を増やすことで
                金利上昇リスクを軽減しつつ、安定したインカムを確保できます。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("AIによる詳細分析を見る"):
            st.markdown("""
            <div style='background-color: #f8f9fa; border-radius: 10px; padding: 20px;'>
                <h4 style='color: #2E7D32;'>現在の市場環境分析</h4>
                <p>
                    インフレ圧力はピークアウトしつつあるものの、中央銀行の金融引き締め政策は続く見通しです。
                    このような環境では、バリュエーションの高い成長株よりも、キャッシュフローの安定した優良企業や
                    配当利回りの高い銘柄が相対的に優位となる可能性があります。
                </p>
                
                <h4 style='color: #2E7D32;'>中長期投資見通し</h4>
                <p>
                    今後3-5年の市場見通しでは、テクノロジー革新（特にAI、クラウド、グリーンエネルギー）と
                    高齢化社会に関連するセクターが引き続き成長することが予想されます。
                    これらの分野への長期的なエクスポージャーを維持することが推奨されます。
                </p>
                
                <h4 style='color: #2E7D32;'>最適化シミュレーション結果</h4>
                <p>
                    AIモデルによる1000回のモンテカルロシミュレーションでは、提案された資産配分に変更した場合、
                    期待リターンが年率6.8%から7.1%に向上する一方で、ボラティリティは12.3%から12.1%に低下する
                    結果となりました。これはシャープレシオが0.55から0.59に改善することを意味します。
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>🎯 投資目標設定</div>", unsafe_allow_html=True)
        
        goal_options = {
            "資産形成": "長期的な資産の成長を目指す",
            "インカム重視": "安定した配当・利息収入を重視",
            "バランス型": "成長と安定のバランスを取る",
            "リスク抑制": "値動きを抑えた安定運用",
            "テーマ投資": "特定のテーマに集中投資"
        }
        
        selected_goal = st.selectbox("投資目標", list(goal_options.keys()))
        st.markdown(f"<div style='font-size: 12px; color: #666;'>{goal_options[selected_goal]}</div>", unsafe_allow_html=True)
        
        risk_level = st.slider("リスク許容度", 1, 10, 6)
        
        risk_description = {
            1: "非常に保守的。元本の安全性を最重視。",
            2: "保守的。安定性重視で小さなリスクのみ許容。",
            3: "やや保守的。安定性を重視しつつ緩やかな成長を期待。",
            4: "控えめ。安定性と成長のバランスを重視するが安全寄り。",
            5: "バランス型。安定性と成長を均等に重視。",
            6: "やや積極的。成長を重視しつつ一定の安定性も確保。",
            7: "積極的。高い成長を目指し、相応のリスクを許容。",
            8: "より積極的。高いリターンを優先し、大きなリスクも許容。",
            9: "非常に積極的。最大限のリターンを追求し、高いリスクを許容。",
            10: "最大リスク。リターン最大化のみを追求。"
        }
        
        st.markdown(f"<div style='font-size: 12px; color: #666;'>{risk_description[risk_level]}</div>", unsafe_allow_html=True)
        
        time_horizon = st.radio("投資期間", ["短期（1-3年）", "中期（3-10年）", "長期（10年以上）"])
        
        special_focuses = st.multiselect(
            "特に重視したい項目",
            ["高配当", "ESG投資", "テクノロジー成長", "国内重視", "グローバル分散", "インフレヘッジ", "節税対策"]
        )
        
        if st.button("AIアドバイスを更新"):
            with st.spinner("AIが最適なアドバイスを生成中..."):
                time.sleep(2)
                st.success("あなた専用のアドバイスを更新しました！")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>📅 定期ミーティング予約</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; margin-bottom: 10px;'>
            <div>専門アドバイザーとのオンライン面談</div>
            <div style='font-size: 12px; color: #666;'>AIアドバイスに加えて人間の専門家によるアドバイス</div>
        </div>
        """, unsafe_allow_html=True)
        
        meeting_date = st.date_input("希望日", value=pd.Timestamp("2025-05-15"))
        meeting_time = st.selectbox("希望時間", ["10:00", "11:00", "13:00", "14:00", "15:00", "16:00"])
        
        if st.button("ミーティングを予約"):
            st.success(f"ミーティングが予約されました: {meeting_date.strftime('%Y年%m月%d日')} {meeting_time}")
            st.info("ミーティング確認メールをお送りしました。")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # AIアシスタント質問セクション
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>❓ AIアシスタントに質問</div>", unsafe_allow_html=True)
        
        user_question = st.text_input("投資に関する質問を入力してください")
        
        if user_question:
            st.markdown("""
            <div style='background-color: #e8f5e9; border-radius: 10px; padding: 15px; margin-top: 10px;'>
                <div style='display: flex; align-items: center;'>
                    <span style='font-size: 24px; margin-right: 10px;'>🤖</span>
                    <div>
                        <div style='font-weight: bold;'>AIアシスタント回答</div>
                        <div>ご質問ありがとうございます。質問の回答は通常、専門的な金融アドバイスとなりますので、
                        投資判断の際には専門家にもご相談ください。詳細なご質問には、より具体的な情報が必要になる場合があります。</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:  # 設定画面
    st.markdown("## ⚙️ アカウント設定")
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 プロフィール", "🔔 通知設定", "🔒 セキュリティ", "💳 支払い情報"])
    
    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>👤 基本情報</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("姓", value="山田")
            st.text_input("メールアドレス", value="yamada.taro@example.com")
            st.text_input("電話番号", value="090-1234-5678")
        
        with col2:
            st.text_input("名", value="太郎")
            st.date_input("生年月日", value=pd.Timestamp("1980-01-15"))
            st.selectbox("職業", ["会社員", "自営業", "公務員", "経営者", "専門職", "定年退職", "その他"])
        
        st.markdown("<div class='subheader'>📮 連絡先住所</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("郵便番号", value="100-0001")
            st.text_input("市区町村", value="千代田区千代田")
        
        with col2:
            st.text_input("都道府県", value="東京都")
            st.text_input("番地・建物名", value="1-1-1 サンプルマンション101")
        
        if st.button("プロフィールを更新"):
            st.success("プロフィール情報が正常に更新されました。")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>📋 投資プロフィール</div>", unsafe_allow_html=True)
        
        experience = st.select_slider(
            "投資経験",
            options=["初心者", "1-3年", "3-5年", "5-10年", "10年以上"],
            value="3-5年"
        )
        
        knowledge = st.select_slider(
            "投資知識レベル",
            options=["基礎的", "一般的", "中級", "高度", "専門的"],
            value="中級"
        )
        
        st.multiselect(
            "投資経験のある商品",
            ["国内株式", "米国株式", "投資信託", "ETF", "債券", "FX", "仮想通貨", "不動産", "商品先物", "その他"],
            default=["国内株式", "投資信託", "ETF"]
        )
        
        st.markdown("<div class='subheader'>🎯 投資目的</div>", unsafe_allow_html=True)
        
        goals = st.multiselect(
            "主な投資目的（複数選択可）",
            ["老後資金", "資産形成", "教育資金", "住宅購入", "定期的な収入", "短期的な利益", "その他"],
            default=["老後資金", "資産形成"]
        )
        
        if st.button("投資プロフィールを更新"):
            st.success("投資プロフィール情報が正常に更新されました。")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>🔔 通知設定</div>", unsafe_allow_html=True)
        
        st.markdown("**通知方法の選択**")
        
        push_notify = st.checkbox("アプリのプッシュ通知", value=True)
        email_notify = st.checkbox("メール通知", value=True)
        sms_notify = st.checkbox("SMS通知", value=False)
        
        st.markdown("**受け取る通知タイプ**")
        
        notification_types = {
            "マーケットアラート": True,
            "価格変動アラート": True,
            "ニュースダイジェスト": True,
            "AIアドバイス更新": True,
            "ポートフォリオレポート": True,
            "入出金通知": True,
            "サービスアップデート": False,
            "プロモーション情報": False
        }
        
        for notify_type, default_val in notification_types.items():
            notification_types[notify_type] = st.checkbox(notify_type, value=default_val)
        
        st.markdown("**通知頻度**")
        
        frequency = st.radio(
            "ニュースダイジェストの頻度",
            ["リアルタイム", "1日1回", "週1回", "月1回"],
            index=1
        )
        
        quiet_hours = st.checkbox("通知サイレント時間を設定", value=True)
        if quiet_hours:
            col1, col2 = st.columns(2)
            with col1:
                start_time = st.time_input("開始時間", value=pd.Timestamp("22:00:00").time())
            with col2:
                end_time = st.time_input("終了時間", value=pd.Timestamp("08:00:00").time())
            
            st.markdown(f"<div style='font-size: 12px; color: #666;'>{start_time.strftime('%H:%M')}から{end_time.strftime('%H:%M')}までは通知が送信されません</div>", unsafe_allow_html=True)
        
        if st.button("通知設定を更新"):
            st.success("通知設定が正常に更新されました。")
        st.markdown("</div>", unsafe_allow_html=True)
        with tab3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='subheader'>🔒 セキュリティ設定</div>", unsafe_allow_html=True)
            
            st.markdown("**パスワード変更**")
            current_password = st.text_input("現在のパスワード", type="password")
            new_password = st.text_input("新しいパスワード", type="password")
            confirm_password = st.text_input("新しいパスワード（確認用）", type="password")
            
            if st.button("パスワードを変更"):
                if new_password == confirm_password:
                    st.success("パスワードが正常に変更されました。")
                else:
                    st.error("新しいパスワードが一致しません。")
            
            st.markdown("**2段階認証**")
            two_factor_enabled = st.checkbox("2段階認証を有効にする", value=False)
            if two_factor_enabled:
                st.info("2段階認証を有効にするには、認証アプリを使用してQRコードをスキャンしてください。")
                st.image("https://via.placeholder.com/150", caption="QRコード")
            
            st.markdown("**ログイン履歴**")
            login_history = pd.DataFrame({
                "日時": ["2025-05-01 10:00", "2025-04-30 18:45", "2025-04-29 08:15"],
                "デバイス": ["iPhone 13", "Windows PC", "MacBook Pro"],
                "IPアドレス": ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
            })
            st.table(login_history)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab4:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='subheader'>💳 支払い情報</div>", unsafe_allow_html=True)
            
            st.markdown("**現在のプラン**")
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px;'>
                <div style='font-weight: bold;'>プレミアムプラン</div>
                <div style='font-size: 12px; color: #666;'>月額: 3,000円（税込）</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**支払い方法**")
            payment_method = st.radio("支払い方法", ["クレジットカード", "銀行振込", "PayPal"], index=0)
            if payment_method == "クレジットカード":
                st.text_input("カード番号", placeholder="1234 5678 9012 3456")
                st.text_input("有効期限", placeholder="MM/YY")
                st.text_input("セキュリティコード", placeholder="123", type="password")
            elif payment_method == "銀行振込":
                st.info("銀行振込の詳細はメールでお送りします。")
            elif payment_method == "PayPal":
                st.info("PayPalアカウントでの支払いを設定してください。")
            
            if st.button("支払い情報を更新"):
                st.success("支払い情報が正常に更新されました。")
            
            st.markdown("</div>", unsafe_allow_html=True)