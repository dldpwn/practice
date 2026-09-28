import streamlit as st
from datetime import datetime

# 1. 페이지 설정 (사이드바 기본 숨김 처리)
st.set_page_config(
    page_title="Mood & Music Diary",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed" # 평소엔 사이드바 숨김
)

# 2. 아이보리 감성 디자인 CSS 적용
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

    .stApp, * {
        font-family: 'Gowun Dodum', sans-serif !important;
    }

    .stApp {
        background-color: #FDFBF7 !important;
    }

    /* 버튼 아이보리 톤 통일 */
    [data-testid="stButton"] button {
        background-color: #F5EBE6 !important;
        color: #5C5346 !important;
        border: 1px solid #EAE5DC !important;
        border-radius: 12px !important;
    }
    [data-testid="stButton"] button:hover {
        background-color: #ECE4DA !important;
    }

    /* 사이드바 배경도 아이보리로 맞춤 */
    [data-testid="stSidebar"] {
        background-color: #F9F6F0 !important;
        border-right: 1px solid #EAE5DC;
    }

    /* 입력 영역 톤 통일 */
    [data-testid="stMultiSelect"] div[data-baseweb="select"],
    [data-testid="stTextArea"] textarea {
        border: 1px solid #EAE5DC !important;
        background-color: #FDFBF7 !important;
        border-radius: 12px !important;
        color: #5C5346 !important;
    }
    div[data-baseweb="tag"] {
        background-color: #F0EAE1 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화
if "diary_list" not in st.session_state:
    st.session_state["diary_list"] = []

# --- 사이드바 영역 (평소엔 숨겨져 있다가 왼쪽 위 메뉴를 누르면 나타남) ---
with st.sidebar:
    st.markdown("### 🧭 메뉴 이동")
    st.info("💡 왼쪽 위의 **`>` (화살표)**를 누르면 사이드바를 다시 숨길 수 있어요!")
    st.page_link("main.py", label="✨ 오늘 기록하기", icon="📝")
    st.page_link("pages/2_📚_기록보기.py", label="🗓️ 감정 캘린더 보기", icon="📚")

# --- 메인 화면 ---
today_str = datetime.now().strftime("%Y년 %m월 %d일")
st.markdown(f"### ✨ {today_str}")
st.write("")

# 기분 선택
selected_moods = st.multiselect(
    "😊 오늘의 기분은 어땠나요? (여러 개 선택 가능)",
    ["😊 행복", "😌 평온", "😴 피곤", "🛋️ 귀찮음", "💧 슬픔", "🌧️ 우울", "😡 분노", "✨ 설렘"]
)

# 일기 내용 작성
diary_text = st.text_area(
    "오늘 어떤 하루를 보냈나요?",
    placeholder="여기에 일기나 생각을 자유롭게 적어보세요...",
    height=180,
    label_visibility="collapsed"
)

# 사진 첨부
st.markdown("➕ **오늘의 사진 첨부하기 (PNG, JPG)**")
uploaded_file = st.file_uploader("사진 업로드", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

if uploaded_file is not None:
    st.write("")
    st.image(uploaded_file, width=300)

st.write("")

# 저장하기 버튼
col_s1, col_s2 = st.columns([4, 1])
with col_s2:
    save_clicked = st.button("💾 저장하기", use_container_width=True)

if save_clicked:
    if diary_text.strip() == "":
        st.warning("⚠️ 일기 내용을 한 줄 이상 적어주세요!")
    elif not selected_moods:
        st.warning("⚠️ 오늘의 기분을 최소 1개 이상 선택해 주세요!")
    else:
        image_bytes = uploaded_file.getvalue() if uploaded_file else None
        new_entry = {
            "date": today_str,
            "moods": selected_moods,
            "text": diary_text,
            "image": image_bytes
        }
        st.session_state["diary_list"].insert(0, new_entry)
        st.success("✨ 감정 기록이 성공적으로 저장되었습니다!")
