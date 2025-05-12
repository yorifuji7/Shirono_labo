import streamlit as st
import plotly.graph_objects as go
import time

st.set_page_config(page_title="第一印象トーン診断", layout="centered")

# スタイリッシュなフォントを適用（Google Fonts連携）
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Noto Sans JP', sans-serif;
        color: #111;
    }
    .stButton>button {
        background-color: #2c7be5;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    </style>
""", unsafe_allow_html=True)

# トーンスコアマップ（25段階）
tone_score_map = {
    "1M-1": 1, "1M-2": 2,
    "2L-1": 3, "2L-2": 4,
    "2M-1": 5, "2M-2": 6, "2M-3": 7,
    "2R-1": 8, "2R-2": 9,
    "3L-1": 10, "3L-2": 11,
    "3M-1": 12, "3M-2": 13, "3M-3": 14,
    "3R-1": 15, "3R-2": 16,
    "4L-1": 17, "4L-2": 18,
    "4M-1": 19, "4M-2": 20, "4M-3": 21,
    "4R-1": 22, "4R-2": 23,
    "5M-1": 24, "5M-2": 25
}

# 年齢補正関数
def tone_to_age_offset(score):
    return (score - 13) // 2

# グレードコメント
grades = {
    "S": "✨ 素晴らしい歯のトーンです！清潔感があり、第一印象も抜群です。",
    "A": "◎ 好印象の口元です。この調子で維持できれば完璧です。",
    "B": "〇 まずまずの状態です。軽いケアでより魅力がアップします。",
    "C": "△ 少し印象に影響が出ているかもしれません。ケアを始めましょう。",
    "D": "⚠ 印象を下げている可能性大。集中ケアが必要です。"
}

# スコアをゲージで可視化
def render_gauge(title, value, max_val=10):
    color_scale = [
        [0.0, "#d3d3d3"],
        [1.0, "#2c7be5"]
    ]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [None, max_val]},
            'bar': {'color': "#2c7be5"},
            'bgcolor': "white",
            'steps': [
                {'range': [0, max_val], 'color': '#e6e6e6'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        },
        number={'suffix': "/10", 'font': {'size': 20}}
    ))
    st.plotly_chart(fig, use_container_width=True)

# タイトル
title_html = """
<h1 style='text-align: center; font-weight:700; color:#2c7be5;'>SHIRONO LABO 印象診断</h1>
<p style='text-align: center; font-size: 16px;'>測定器と専門ガイドを用いた本格診断</p>
"""
st.markdown(title_html, unsafe_allow_html=True)

# 入力フォーム
with st.form("tone_diagnosis"):
    st.subheader("\n① 現在の歯のトーンを選択")
    tone_selected = st.selectbox("※ 測定器で確認したシェード番号を選んでください", list(tone_score_map.keys()))

    st.subheader("② 実年齢を入力")
    age = st.slider("あなたの年齢は？", min_value=10, max_value=80, value=35)

    st.subheader("③ 生活習慣に関する質問")
    q1 = st.radio("色の濃い食べ物（カレー・トマト等）をよく摂る", ["はい", "いいえ"])
    q2 = st.radio("コーヒー・紅茶・ワインを日常的に飲む", ["はい", "いいえ"])
    q3 = st.radio("喫煙の習慣がある", ["はい", "いいえ"])
    q4 = st.radio("歯磨きは丁寧に1本ずつ磨いている", ["はい", "いいえ"])

    submitted = st.form_submit_button("診断する")

if submitted:
    with st.spinner("診断結果を生成中..."):
        time.sleep(2)

    tone_score = tone_score_map[tone_selected]
    age_offset = tone_to_age_offset(tone_score)
    visual_age = age + age_offset

    # 清潔感スコア（明るさ逆換算）
    cleanliness = max(1, round(10 - tone_score * 10 / 25))

    # 着色リスク
    stain_risk = 0
    stain_risk += 2 if q1 == "はい" else 0
    stain_risk += 2 if q2 == "はい" else 0
    stain_risk += 2 if q3 == "はい" else 0
    stain_risk += -2 if q4 == "はい" else 0
    stain_risk = max(1, min(10, stain_risk + 5))

    # 年齢ギャップ（見た目年齢）
    gap = visual_age - age
    age_gap_score = min(10, max(1, 5 + gap))

    # ランク決定（平均）
    avg_score = round((cleanliness + (10 - stain_risk) + (10 - age_gap_score)) / 3)
    if avg_score >= 9:
        rank = "S"
    elif avg_score >= 7:
        rank = "A"
    elif avg_score >= 5:
        rank = "B"
    elif avg_score >= 3:
        rank = "C"
    else:
        rank = "D"

    # 表示セクション
    st.markdown("---")
    st.subheader("\U0001F4CA 診断スコア")
    render_gauge("清潔感スコア", cleanliness)
    render_gauge("着色リスク", stain_risk)
    render_gauge("見た目年齢ギャップ", age_gap_score)

    st.markdown("---")
    st.subheader("\U0001F4C8 総合評価ランク：" + rank)
    st.success(grades[rank])

    st.markdown("<small style='color:#666'>この診断はSHIRONO LABOの専用測定器と印象設計ガイドに基づいて作成されています。</small>", unsafe_allow_html=True)
