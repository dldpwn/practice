import streamlit as st
from datetime import datetime

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Mood & Music Diary",
    page_icon="🎵",
    layout="centered"
)

# 2. 감성적인 웹폰트 및 파일 업로더 박스 커스텀 CSS
st.markdown("""
    <style>
    /* 구글 웹폰트 (고운 돋움) 불러오기 */
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

    /* 전체 앱 및 모든 컴포넌트의 기본 폰트를 동글동글한 폰트로 지정 */
    .stApp, * {
        font-family: 'Gowun Dodum', sans-serif !important;
    }

    /* 전체 앱 배경을 부드러운 아이보리 톤으로 설정 */
    .stApp {
        background-color: #FDFBF7 !important;
    }

    /* 1. 다중 선택(기분 선택) 박스 테두리 및 배경 */
    [data-testid="stMultiSelect"] div[data-baseweb="select"] {
        border: 1px solid #EAE5DC !important;
        background-color: #FDFBF7 !important;
        border-radius: 12px !important;
    }

    /* 2. 텍스트 입력 영역 테두리 및 배경 */
    [data-testid="stTextArea"] textarea {
        border: 1px solid #EAE5DC !important;
        background-color: #FDFBF7 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* 3. 파일 업로더 외곽 박스를 완전히 감싸고 불필요한 텍스트 숨기기 */
    [data-testid="stFileUploader"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
    }
    
    /* 파일 업로더 내부의 복잡한 안내 문구 숨기기 */
    [data-testid="stFileUploader"] section div span,
    [data-testid="stFileUploader"] section div small {
        display: none !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #FDFBF7 !important;
        border: 1px dashed #D5CEC3 !important;
        border-radius: 12px !important;
        padding: 5px !important;
    }
    
    /* 포커스 시 테두리 색상 부드럽게 유지 */
    input:focus, textarea:focus, div[data-baseweb="select"]:focus-within {
        box-shadow: none !important;
        border-color: #C5BCB3 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화
if "diary_list" not in st.session_state:
    st.session_state["diary_list"] = []

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "write"

# -------------------------------------------------------------------------
# [페이지 1] 오늘 하루 기록하기 화면
# -------------------------------------------------------------------------
if st.session_state["current_page"] == "write":
    
    # 상단 '기록 보기' 버튼 (오른쪽 정렬)
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("📚 기록 보기", use_container_width=True):
            st.session_state["current_page"] = "archive"
            st.rerun()

    # 오늘 날짜를 감성적인 큰 타이틀로 표시
    today_str = datetime.now().strftime("%Y년 %m월 %d일")
    st.markdown(f"### ✨ {today_str}")
    st.write("")

    # 감정 다중 선택 옵션
    selected_moods = st.multiselect(
        "😊 오늘의 기분은 어땠나요? (여러 개 선택 가능)",
        [
            "😊 행복",
            "😌 평온",
            "😴 피곤",
            "🛋️ 귀찮음",
            "💧 슬픔",
            "🌧️ 우울",
            "😡 분노",
            "✨ 설렘"
        ]
    )

    # 일기 내용 작성 텍스트 박스
    diary_text = st.text_area(
        "오늘 어떤 하루를 보냈나요?",
        placeholder="여기에 일기나 생각을 자유롭게 적어보세요...",
        height=180,
        label_visibility="collapsed"
    )

    # 깔끔한 커스텀 텍스트 라벨과 미니멀해진 업로드 영역
    st.markdown("➕ **오늘의 사진 첨부하기 (PNG, JPG)**")
    uploaded_file = st.file_uploader(
        "사진 업로드",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

    st.write("")

    # '저장하기' 버튼 (오른쪽 정렬)
    col_save_left, col_save_right = st.columns([4, 1])
    with col_save_right:
        if st.button("💾 저장하기", use_container_width=True):
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
                st.success("✨ 사진과 함께 감정 기록이 성공적으로 저장되었습니다!")

# -------------------------------------------------------------------------
# [페이지 2] 지난 기록 보기 화면
# -------------------------------------------------------------------------
elif st.session_state["current_page"] == "archive":
    
    # 상단 '기록하러 가기' 버튼
    if st.button("⬅️ 기록하러 가기", use_container_width=True):
        st.session_state["current_page"] = "write"
        st.rerun()

    st.write("")
    st.subheader("📚 지난 감정 기록 아카이브")

    if len(st.session_state["diary_list"]) == 0:
        st.info("💡 아직 작성된 감정 기록이 없습니다.")
    else:
        for i, entry in enumerate(st.session_state["diary_list"]):
            with st.container(border=True):
                moods_str = ", ".join(entry["moods"])
                st.markdown(f"**📅 날짜:** {entry['date']}")
                st.markdown(f"**🏷️ 기분:** {moods_str}")
                
                if entry.get("image"):
                    st.image(entry["image"], use_container_width=True)
                
                st.markdown(f"**✍️ 내용:** {entry['text']}")
