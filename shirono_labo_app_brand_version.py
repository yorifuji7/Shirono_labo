import streamlit as st
import pandas as pd
import plotly.express as px
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

    # 線形に10段階スケーリング（より滑らかに）
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

    # Plotlyで横棒グラフ
    chart_data = pd.DataFrame({
        "項目": ["清潔感", "緊急性", "メンテ必要性"],
        "スコア": [cleanliness, urgency, maintenance]
    })
    fig = px.bar(chart_data, x="スコア", y="項目", orientation="h", range_x=[0,10], text="スコア")
    fig.update_traces(marker_color='skyblue', textposition='outside')
    fig.update_layout(xaxis_title="10段階評価", yaxis_title="", height=400)
    st.plotly_chart(fig)

    st.markdown(f"### 総合評価ランク：{rank}")
    st.info(advice_comments[rank])

    st.markdown("### \U0001F4E9 診断結果をLINEで送りたい方はこちら")
    line_url = "https://lin.ee/xxxxxxxx"  # ご自身のLINE公式URLに差し替えてください
    if st.button("LINEで診断結果を送る"):
        st.markdown(f'<meta http-equiv="refresh" content="0; URL={line_url}">', unsafe_allow_html=True)
