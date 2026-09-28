import streamlit as st

# 1. 페이지 기본 설정 (와이드 레이아웃 적용)
st.set_page_config(
    page_title="Mood & Music Diary",
    page_icon="🎵",
    layout="centered"
)

# 2. 세션 상태에 다이어리 기록 저장소 초기화
if "diary_list" not in st.session_state:
    st.session_state["diary_list"] = []

# 3. 사이드바 영역: 지난 기록 보기 버튼/토글 배치
with st.sidebar:
    st.subheader("🗂️ 메뉴")
    # 토글 버튼을 눌러서 지난 기록을 열고 닫을 수 있게 설정
    show_archive = st.toggle("📚 지난 기록 보기", value=False)
    
    st.write("---")
    st.caption("✨ 오늘의 감정을 음악과 함께 기록해보세요.")

# 4. 메인 화면: 군더더기 없이 오직 '오늘 하루 기록'에만 집중하는 입력 폼
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
    height=200,
    label_visibility="collapsed"
)

# 저장 버튼 영역
if st.button("💾 저장하기", use_container_width=True):
    if diary_text.strip() == "":
        st.warning("⚠️ 일기 내용을 한 줄 이상 적어주세요!")
    elif not selected_moods:
        st.warning("⚠️ 오늘의 기분을 최소 1개 이상 선택해 주세요!")
    else:
        new_entry = {
            "date": str(diary_date),
            "moods": selected_moods,
            "text": diary_text
        }
        # 세션 리스트에 데이터 추가 (가장 최근 것이 위로 오게)
        st.session_state["diary_list"].insert(0, new_entry)
        st.success("✨ 감정 기록이 성공적으로 저장되었습니다!")

# 5. 사이드바 토글이 켜졌을 때만 나타나는 지난 기록 아카이브 영역
if show_archive:
    st.write("---")
    st.subheader("📚 지난 감정 기록 아카이브")

    if len(st.session_state["diary_list"]) == 0:
        st.info("💡 아직 작성된 감정 기록이 없습니다.")
    else:
        for i, entry in enumerate(st.session_state["diary_list"]):
            with st.container(border=True):
                moods_str = ", ".join(entry["moods"])
                st.markdown(f"**📅 날짜:** {entry['date']}")
                st.markdown(f"**🏷️ 기분:** {moods_str}")
                st.markdown(f"**✍️ 내용:** {entry['text']}")
