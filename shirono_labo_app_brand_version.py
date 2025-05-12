import streamlit as st
import matplotlib.pyplot as plt

# ⚠️ これが「一番上」にあることが大事！！
st.set_page_config(page_title="SHIRONO LABO 印象診断", layout="centered")

# ロゴ画像（GitHubから表示）
logo_url = "https://github.com/yorifuji7/Shirono_labo/blob/main/city_whitening_logo.jpg?raw=true"
st.image(logo_url, use_container_width=True)

# タイトル
st.markdown("<h2 style='text-align: center; color: #000000;'>SHIRONO LABO 印象診断</h2>", unsafe_allow_html=True)

# ↓ここから先はあなたの診断ロジックなどを続けてOK！
