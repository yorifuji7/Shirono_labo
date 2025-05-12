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

def get_color_scale_gray_to_blue(n):
    return [
        f"rgba({int(180 - (i / (n - 1)) * 100)}, {int(180 - (i / (n - 1)) * 100)}, {int(200 + (i / (n - 1)) * 55)}, 1)"
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

advice_comments = {
    "S": "素晴らしい！誰もがうらやむ美しい歯をお持ちですね。でも、油断は禁物です。\n放っておくと少しずつ着色していってしまうので、月1回のメンテナンスで清潔感をキープしましょう！",
    "A": "とても好印象な口元です！この清潔感をキープするためにも、月一回のメンテナンスを忘れずに！\n放っておくと着色してトーンが落ちてきてしまいます。綺麗な白い歯を大事にしてくださいね！",
    "B": "もう一息で理想的な印象に近づけます！期間を空けずに数回のケアをしてあげれば、もうワンランク上の自分になれます。\n逆にトーンダウンしやすい状態でもあるので、放っておくのは要注意です！",
    "C": "人から見たあなたの印象に悪影響が出ている可能性があります！仕事やプライベートで損をしているかもしれません。\n気になりはじめた今こそ、集中的なケアをして印象改善に取り組みましょう！",
    "D": "緊急ケアが必要な状態です！あなたの印象が実際より悪く見えてしまっている可能性があります。\n口元の印象のせいで色んな努力がプラマイゼロになってしまうことも...。\nでも、諦めることはありません！集中的なケアで見違えるほど印象をアップできます！"
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

    st.subheader("診断結果")
    st.write(f"実年齢: {age} 歳 / 見た目年齢: {visual_age} 歳")

    render_score_bar("清潔感", cleanliness)
    render_score_bar("ホワイトニング緊急性", urgency)
    render_score_bar("メンテナンス必要性", maintenance)
    render_score_bar("商談・面接での第一印象レベル", first_impression * 5)
    render_score_bar("恋愛魅力レベル", love_score * 5)
    render_score_bar("損してるレベル", damage_score * 3)

    st.markdown(f"### 総合評価ランク：{rank}")
    st.info(advice_comments[rank])
