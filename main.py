import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Mood & Music Diary",
    page_icon="🎵",
    layout="centered"
)

# 2. 💡 모든 컴포넌트의 테두리를 완벽하게 없애는 강화된 CSS
st.markdown("""
    <style>
    /* 전체 앱 배경을 부드러운 아이보리 톤으로 변경 */
    .stApp {
        background-color: #FDFBF7;
    }
    
    /* 멀티셀렉트(기분 선택) 박스 테두리 제거 및 배경 색상 통일 */
    div[data-baseweb="select"] {
        background-color: #F4F1EA !important;
        border-radius: 12px !important;
        border: none !important;
    }
    div[data-baseweb="select"] > div {
        border: none !important;
        background-color: transparent !important;
    }

    /* 날짜 선택 입력창 박스 테두리 제거 */
    div[data-baseweb="input"] > div {
        border: none !important;
        background-color: #F4F1EA !important;
        border-radius: 12px !important;
    }

    /* 사진 첨부 파일 업로더 전체 박스 테두리 제거 */
    [data-testid="stFileUploader"] {
        background-color: #F4F1EA !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 5px !important;
    }
    [data-testid="stFileUploader"] section {
        border: none !important;
        background-color: transparent !important;
    }
    
    /* 텍스트 입력창(text_area) 테두리 제거 */
    textarea[aria-label="오늘 어떤 하루를 보냈나요?"] {
        border: none !important;
        background-color: #F4F1EA !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    /* 포커스될 때 생기는 기본 테두리 제거 */
    textarea:focus, input:focus {
        box-shadow: none !important;
        border: none !important;
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
    
    # 상단 '기록 보기' 버튼
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("📚 기록 보기", use_container_width=True):
            st.session_state["current_page"] = "archive"
            st.rerun()

    st.subheader("✍️ 오늘 하루 기록하기")

    # 날짜 선택
    diary_date = st.date_input("📅 날짜 선택", label_visibility="collapsed")

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

    # 사진 첨부 파일 업로더
    uploaded_file = st.file_uploader(
        "➕ 오늘의 사진 첨부하기 (PNG, JPG)",
        type=["png", "jpg", "jpeg"]
    )

    # 저장 버튼 영역
    if st.button("💾 저장하기", use_container_width=True):
        if diary_text.strip() == "":
            st.warning("⚠️ 일기 내용을 한 줄 이상 적어주세요!")
        elif not selected_moods:
            st.warning("⚠️ 오늘의 기분을 최소 1개 이상 선택해 주세요!")
        else:
            image_bytes = uploaded_file.getvalue() if uploaded_file else None

            new_entry = {
                "date": str(diary_date),
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
                
                if entry["image"]:
                    st.image(entry["image"], use_container_width=True)
                
                st.markdown(f"**✍️ 내용:** {entry['text']}")
