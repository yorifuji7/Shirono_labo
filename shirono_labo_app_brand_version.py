import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

st.set_page_config(page_title="第一印象トーン診断", layout="centered")

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
    return (score - 13) // 3

def get_color_scale(n):
    return [
        f"rgba({int(255 - (i / (n - 1)) * 255)}, {int((i / (n - 1)) * 128)}, {int((i / (n - 1)) * 255)}, 1)"
        for i in range(n)
    ]

question_map = {
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

st.title("第一印象トーン診断")
with st.form("diagnosis_form"):
    tone_selected = st.selectbox("歯のトーンを選んでください", list(tone_score_map.keys()))
    age = st.number_input("あなたの実年齢を入力してください", min_value=10, max_value=100, value=30)
    responses = {q: st.radio(q, ("はい", "いいえ"), key=q) for q in question_map}
    submitted = st.form_submit_button("診断する")

if submitted:
    with st.spinner("診断中..."):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(5 / 100)
            progress.progress(i + 1)

    tone_score = tone_score_map[tone_selected]
    age_offset = tone_to_age_offset(tone_score)
    visual_age = age + age_offset

    cleanliness = max(1, round(10 - tone_score * 10 / 25))
    urgency = min(10, round(tone_score * 10 / 25))
    correct = sum([1 for q, a in responses.items() if a == question_map[q]])
    maintenance = max(1, min(10, 10 - (correct * 2)))

    # 新項目スコア
    first_impression = sum([responses[q] == question_map[q] for q in [
        "面接や商談などで第一印象を気にすることが多いですか？",
        "初対面での印象を意識してケアしていますか？"
    ]])
    love_score = sum([responses[q] == question_map[q] for q in [
        "笑顔に自信がありますか？",
        "歯を見せて笑うことに抵抗がありますか？"
    ]])
    damage_score = sum([responses[q] != question_map[q] for q in [
        "最近「疲れてる？」と言われることがありますか？",
        "歯を見せて笑うことに抵抗がありますか？"]]) + (tone_score > 15)

    def render_score_bar(label, value, max_value=10):
        colors = get_color_scale(max_value)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(range(1, max_value + 1)),
            y=[1] * max_value,
            marker_color=colors,
            width=0.8,
            text=[str(i) for i in range(1, max_value + 1)],
            textposition="outside",
            textfont=dict(color="black", size=16),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[value],
            y=[1.1],
            mode="markers",
            marker=dict(color="black", size=14),
            showlegend=False
        ))
        fig.update_layout(
            height=130,
            title=dict(text=label, font=dict(color="black", size=20)),
            xaxis=dict(range=[0, max_value + 1], tickmode="linear", dtick=1, color="black"),
            yaxis=dict(visible=False),
            margin=dict(l=40, r=40, t=40, b=30)
        )
        st.plotly_chart(fig)

    st.subheader("診断結果")
    st.write(f"実年齢: {age} 歳 / 見た目年齢: {visual_age} 歳")

    render_score_bar("清潔感", cleanliness)
    render_score_bar("ホワイトニング緊急性", urgency)
    render_score_bar("メンテナンス必要性", maintenance)
    render_score_bar("商談・面接での第一印象レベル", first_impression * 5)
    render_score_bar("恋愛魅力レベル", love_score * 5)
    render_score_bar("損してるレベル", damage_score * 3)
