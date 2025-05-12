import streamlit as st
import matplotlib.pyplot as plt

# ページ設定
st.set_page_config(page_title="第一印象トーン診断", layout="centered")

# 差し替えたロゴ画像（GitHubから読み込み）
new_logo_url = "https://github.com/yorifuji7/Shirono_labo/blob/main/city_whitening_logo.jpg?raw=true"
st.image(new_logo_url, use_container_width=True)

# タイトル表示
st.markdown("<h2 style='text-align: center; color: #000000;'>第一印象トーン診断</h2>", unsafe_allow_html=True)

# 以下、診断機能や入力フォームなどを続けて書く
