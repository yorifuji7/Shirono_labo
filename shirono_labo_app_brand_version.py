
import streamlit as st
import matplotlib.pyplot as plt

# ページ設定
st.set_page_config(page_title="SHIRONO LABO 印象診断", layout="centered")

# ロゴ画像表示
st.image("https://raw.githubusercontent.com/yorifuji7/shirono-labo/main/whiteninglabo_shirono_logo.jpg", width=300)

# タイトル
st.markdown("<h2 style='text-align: center; color: #000000;'>SHIRONO LABO 印象診断</h2>", unsafe_allow_html=True)

# トーンスコア定義
tone_scores = {
    'A4': (8, 4.0, 4.5),
    'A3': (5, 5.0, 5.5),
    'A2': (3, 6.0, 6.5),
    'A1': (0, 7.0, 7.5),
    'B4': (4, 5.5, 5.8),
    'B3': (2, 6.5, 6.8),
    'B2': (-2, 8.0, 8.5),
    'B1': (-5, 9.0, 9.2),
    'BL3': (-6, 9.5, 9.6),
    'BL2': (-8, 9.8, 9.8),
    'BL1': (-10, 10.0, 10.0),
}

# 入力
st.markdown("### お客様情報の入力")
tone = st.selectbox("現在の歯のトーンを選んでください", list(tone_scores.keys()))
age = st.number_input("お客様の実年齢を入力してください", min_value=10, max_value=100, step=1)

if st.button("診断スタート", help="ボタンを押すと診断が始まります"):
    gap, clean_score, impression_score = tone_scores[tone]
    est_age = age + gap

    # コメント生成
    if gap > 0:
        comment = f"現在の歯のトーンでは、見た目年齢が実年齢よりも約{gap}歳高く見られている可能性があります。\n明るいトーンへ改善することで、より若々しく清潔感のある印象が期待できます。"
    else:
        comment = "現在の歯のトーンは非常に良好で、実年齢よりも若く見られる可能性があります。この状態をぜひ維持していきましょう。"

    # 結果表示
    st.markdown("### 📝 診断結果")
    st.write(f"**見た目年齢（推定）**：{est_age} 歳")
    st.write(f"**見た目年齢ギャップ**：{gap:+} 歳")
    st.write(f"**清潔感スコア**：{clean_score}/10")
    st.write(f"**好印象スコア**：{impression_score}/10")
    st.markdown("#### 💬 コメント")
    st.success(comment)

    # グラフ表示
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    ax[0].pie([clean_score, 10-clean_score], labels=["清潔感", ""], colors=["#00AEEF", "#ffffff"], startangle=90)
    ax[0].set_title("清潔感スコア")

    ax[1].pie([impression_score, 10-impression_score], labels=["好印象", ""], colors=["#7ED6DF", "#ffffff"], startangle=90)
    ax[1].set_title("好印象スコア")

    st.pyplot(fig)
