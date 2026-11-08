import streamlit as st
import pandas as pd
import plotly.express as px
import random
import re

from food_data import load_food_database


# ==================================================
# 페이지 설정
# ==================================================
st.set_page_config(
    page_title="NutriDay | 한 달 맞춤 식단",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# 디자인
# ==================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

    html, body, [class*="css"], p, label,
    h1, h2, h3, h4, span, div {
        font-family: 'Gowun Dodum', sans-serif;
    }

    .stApp {
        background: #FBF9F1;
        color: #263B32;
    }

    [data-testid="stSidebar"] {
        background: #EEF6EF;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    .main-title {
        color: #377D61;
        font-size: 2rem;
        font-weight: 800;
    }

    .meal-card, .info-card {
        background: #F0F7F0;
        border: 1px solid #DCEADF;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: .7rem;
    }

    .meal-card {
        min-height: 150px;
        text-align: center;
    }

    div[data-testid="stMetric"] {
        background: #F0F7F0;
        border: 1px solid #DCEADF;
        border-radius: 14px;
        padding: 1rem;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background: #4D9274;
        color: white;
        border: 0;
        border-radius: 12px;
        padding: .65rem 1rem;
        font-weight: 700;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background: #377D61;
        color: white;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] > div {
        background: white;
        border-radius: 10px;
        border-color: #DCEADF;
    }
