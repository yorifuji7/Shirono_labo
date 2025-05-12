import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ページ設定
st.set_page_config(page_title="第一印象トーン診断", layout="centered")

# トーンスコアマッピング（25トーン）
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
    if score <= 2: return -5
    elif score <= 4: return -4
    elif score <= 7: return -3
    elif score <= 11: return -2
    elif score <= 14: return -1
    elif score <= 17: return 0
    elif score <= 20: return 1
    elif score <= 22: return 2
    elif score <= 23: return 3
    elif score == 24: return 4
    else: return 5

question_map = {
    "ホワイトニングをしたことがある": "はい",
    "カレーやトマトなど色の濃い食べ物が好き": "いいえ",
    "タバコを吸っている": "いいえ",
    "歯磨きは丁寧にできている": "はい",
    "年齢と共に歯が黄ばんできたと感じる": "いいえ"
}

advice_comments = {
    "S": "素晴らしい！誰もがうらやむ美しい歯をお持ちですね。でも、油断は禁物です。\n"
         "放っておくと少しずつ着色していってしまうので、月1回のメンテナンスで清潔感をキープしましょう！",
    "A": "とても好印象な口元です！この清潔感をキープするためにも、月一回のメンテナンスを忘れずに！\n"
         "放っておくと着色してトーンが落ちてきてしまいます。綺麗な白い歯を大事にしてくださいね！",
    "B": "もう一息で理想的な印象に近づけます！期間を空けずに数回のケアをしてあげれば、もうワンランク上の自分になれます。\n"
         "逆にトーンダウンしやすい状態でもあるので、放っておくのは要注意です！",
    "C": "人から見たあなたの印象に悪影響が出ている可能性があります！仕事やプライベートで損をしているかもしれません。\n"
         "気になりはじめた今こそ、集中的なケアをして印象改善に取り組みましょう！",
    "D": "緊急ケアが必要な状態です！あなたの印象が実際より悪く見えてしまっている可能性があります。\n"
         "口元の印象のせいで色んな努力がプラマイゼロになってしまうことも...。\n"
         "でも、諦めることはありません！集中的なケアで見違えるほど印象をアップできます！"
}

st.title("第一印象トーン診断")
with st.form("diagnosis_form"):
    tone_selected = st.selectbox("歯のトーンを選んでください", list(tone_score_map.keys()))
    age = st.number_input("あなたの実年齢を入力してください", min_value=10, max_value=100, value=30)
    responses = {q: st.radio(q, ("はい", "いいえ"), key=q) for q in question_map}
    submitted = st.form_submit_button("診断する")

if submitted:
    with st.spinner("診断中... あなたの印象を分析しています"):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(5 / 100)
            progress.progress(i + 1)

    tone_score = tone_score_map[tone_selected]
    age_offset = tone_to_age_offset(tone_score)
    visual_age = age + age_offset

    # スコア変換（滑らかな10段階）
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

    st.subheader("診断結果")
    st.write(f"選択された歯のトーン: {tone_selected}（スコア: {tone_score}）")
    st.write(f"見た目年齢：実年齢 {age} → {visual_age} 歳")

    # カラースケール定義（赤→青）
    def get_color_scale(n):
        return [
            f"rgba({int(255 - (i / (n - 1)) * 255)}, {int((i / (n - 1)) * 128)}, {int((i / (n - 1)) * 255)}, 1)"
            for i in range(n)
        ]

    # 横ゲージ：清潔感、緊急性、メンテ必要性
    def render_score_bar(label, value):
        colors = get_color_scale(10)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(range(1, 11)),
            y=[1] * 10,
            marker_color=colors,
            hoverinfo='x',
            showlegend=False,
            width=0.8,
            text=[str(i) for i in range(1, 11)],
            textposition="outside",
            textfont=dict(color="black", size=16)
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
            xaxis=dict(range=[0, 11], tickmode="linear", dtick=1, title="", color="black"),
            yaxis=dict(visible=False),
            margin=dict(l=40, r=40, t=40, b=30)
        )
        st.plotly_chart(fig)

    render_score_bar("清潔感", cleanliness)
    render_score_bar("緊急性", urgency)
    render_score_bar("メンテ必要性", maintenance)

    # トーンレベル表示バー
    st.markdown("### あなたのトーンレベル")
    tone_levels = list(range(1, 26))
    tone_colors = get_color_scale(25)
    fig_tone = go.Figure()
    fig_tone.add_trace(go.Bar(
        x=tone_levels,
        y=[1] * 25,
        marker_color=tone_colors,
        hoverinfo='x',
        showlegend=False,
        width=0.8,
        text=[str(i) for i in tone_levels],
        textposition="outside",
        textfont=dict(color="black", size=16)
    ))
    fig_tone.add_trace(go.Scatter(
        x=[tone_score],
        y=[1.1],
        mode="markers",
        marker=dict(color="black", size=14),
        showlegend=False
    ))
    fig_tone.update_layout(
        height=160,
        xaxis=dict(title="トーンレベル（明るい→暗い）", tickmode="linear", dtick=1, color="black"),
        yaxis=dict(visible=False),
        margin=dict(l=40, r=40, t=30, b=30)
    )
    st.plotly_chart(fig_tone)

    st.markdown(f"### 総合評価ランク：{rank}")
    st.info(advice_comments[rank])

    st.markdown("### \U0001F4E9 診断結果をLINEで送りたい方はこちら")
    line_url = "https://lin.ee/xxxxxxxx"  # ご自身のLINE公式URLに差し替えてください
    if st.button("LINEで診断結果を送る"):
        st.markdown(f'<meta http-equiv="refresh" content="0; URL={line_url}">', unsafe_allow_html=True)
