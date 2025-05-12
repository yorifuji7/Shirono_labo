import streamlit as st
import plotly.graph_objects as go
import time

st.set_page_config(page_title="第一印象トーン診断", layout="centered")

# スタイリッシュなフォントを適用
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

def tone_to_age_offset(score):
    return (score - 13) // 2

def get_color_scale_gray_to_blue(n):
    return [
        f"rgba({int(180 - (i / (n - 1)) * 100)}, {int(180 - (i / (n - 1)) * 100)}, {int(200 + (i / (n - 1)) * 55)}, 1)"
        for i in range(n)
    ]

def render_score_bar(label, value, max_value=10):
    colors = get_color_scale_gray_to_blue(max_value)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(range(1, max_value + 1)),
        y=[0.6] * max_value,
        marker_color=colors,
        width=0.4,
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[value],
        y=[0.7],
        mode="markers+text",
        marker=dict(color="red", size=18, symbol="diamond"),
        text=[f"← あなたの位置: {value}"],
        textposition="top center",
        textfont=dict(size=14, color="black"),
        showlegend=False
    ))
    fig.update_layout(
        height=120,
        title=dict(text=label, font=dict(color="black", size=20)),
        xaxis=dict(range=[0, max_value + 1], tickmode="linear", dtick=1, color="black"),
        yaxis=dict(visible=False),
        margin=dict(l=40, r=40, t=40, b=20)
    )
    st.plotly_chart(fig)

st.markdown("""
<h1 style='text-align: center; font-weight:700; color:#2c7be5;'>SHIRONO LABO 印象診断</h1>
<p style='text-align: center; font-size: 16px;'>測定器と専門ガイドを用いた本格診断</p>
""", unsafe_allow_html=True)

# 質問セット
def get_responses():
    questions = {
        "ホワイトニングをしたことがある": "はい",
        "カレーやトマトなど色の濃い食べ物が好き": "いいえ",
        "タバコを吸っている": "いいえ",
        "歯磨きは丁寧にできている": "はい",
        "年齢と共に歯が黄ばんできたと感じる": "いいえ",
        "面接や商談などで第一印象を気にすることが多いですか？": "はい",
        "笑顔に自信がありますか？": "はい",
        "最近「疲れてる？」と言われることがありますか？": "いいえ",
        "歯を見せて笑うことに抵抗がありますか？": "いいえ",
        "初対面での印象を意識してケアしていますか？": "はい"
    }
    return {q: st.radio(q, ("はい", "いいえ"), key=q) for q in questions}, questions

grades = {
    "S": "✨ 素晴らしい歯のトーンです！清潔感があり、第一印象も抜群です。",
    "A": "◎ 好印象の口元です。この調子で維持できれば完璧です。",
    "B": "〇 まずまずの状態です。軽いケアでより魅力がアップします。",
    "C": "△ 少し印象に影響が出ているかもしれません。ケアを始めましょう。",
    "D": "⚠ 印象を下げている可能性大。集中ケアが必要です。"
}

with st.form("tone_diagnosis"):
    st.subheader("① 測定結果のトーンを選択")
    tone_selected = st.selectbox("※ 測定器で確認したシェード番号を選んでください", list(tone_score_map.keys()))

    st.subheader("② 実年齢を入力")
    age = st.slider("あなたの年齢は？", min_value=10, max_value=80, value=35)

    st.subheader("③ 印象に関わるライフスタイル診断")
    responses, expected = get_responses()

    submitted = st.form_submit_button("診断する")

if submitted:
    with st.spinner("診断結果を生成中..."):
        time.sleep(2)

    tone_score = tone_score_map[tone_selected]
    age_offset = tone_to_age_offset(tone_score)
    visual_age = age + age_offset

    cleanliness = max(1, round(10 - tone_score * 10 / 25))
    urgency = min(10, round(tone_score * 10 / 25))
    correct = sum([1 for q, a in responses.items() if a == expected[q]])
    maintenance = max(1, min(10, 10 - (correct * 2)))

    first_impression = sum([responses[q] == expected[q] for q in [
        "面接や商談などで第一印象を気にすることが多いですか？",
        "初対面での印象を意識してケアしていますか？"
    ]])
    love_score = sum([responses[q] == expected[q] for q in [
        "笑顔に自信がありますか？",
        "歯を見せて笑うことに抵抗がありますか？"
    ]])
    damage_score = sum([responses[q] != expected[q] for q in [
        "最近「疲れてる？」と言われることがありますか？",
        "歯を見せて笑うことに抵抗がありますか？"]]) + (tone_score > 15)

    avg_score = round((cleanliness + (10 - urgency) + (10 - maintenance)) / 3)
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

    st.markdown("---")
    st.subheader("🧪 プロ診断データ")
    st.write(f"実年齢: {age} 歳 / 見た目年齢: {visual_age} 歳")
    render_score_bar("清潔感スコア", cleanliness)
    render_score_bar("ホワイトニング緊急性", urgency)
    render_score_bar("メンテナンス必要性", maintenance)

    st.markdown("---")
    st.subheader("🧠 印象診断スコア")
    render_score_bar("商談・面接での第一印象レベル", first_impression * 5)
    render_score_bar("恋愛魅力レベル", love_score * 5)
    render_score_bar("損してるレベル", damage_score * 3)

    st.markdown("---")
    st.subheader(f"総合評価ランク：{rank}")
    st.success(grades[rank])
    st.markdown("<small style='color:#666'>※この診断はSHIRONO LABOの測定器と印象設計ガイドに基づいています。</small>", unsafe_allow_html=True)
