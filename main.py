import streamlit as st

# 1. 페이지 기본 설정 (와이드 레이아웃 적용)
st.set_page_config(
    page_title="오늘의 감정 뮤직 다이어리",
    page_icon="🎵",
    layout="centered"
)

# 2. 세션 상태에 다이어리 기록 저장소 초기화
if "diary_list" not in st.session_state:
    st.session_state["diary_list"] = []

# 3. 메인 화면 타이틀 및 소개
st.title("🎵 오늘의 감정 뮤직 다이어리")
st.caption("그날의 기분을 기록하고, 어울리는 음악을 함께 남겨보세요.")

st.write("---")

# 4. 💡 페이지 이동을 위한 네비게이션 버튼 (라디오 버튼을 탭 스타일로 활용)
page = st.radio(
    "🧭 메뉴 선택",
    ["✏️ 다이어리 작성하기", "📚 지난 기록 보기"],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")

# -------------------------------------------------------------------------
# [페이지 1] 다이어리 작성하기 화면
# -------------------------------------------------------------------------
if page == "✏️ 다이어리 작성하기":
    st.subheader("📝 오늘 하루 기록하기")

    # 날짜 선택
    diary_date = st.date_input("📅 날짜 선택")

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
        "✍️ 오늘의 일기나 생각을 자유롭게 적어주세요.",
        placeholder="예: 오늘 하루 있었던 일이나 떠오르는 생각을 남겨보세요...",
        height=150
    )

    # 저장 버튼 영역
    if st.button("💾 다이어리 저장하기", use_container_width=True):
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
            st.success(f"✨ [{diary_date}] 감정 기록이 성공적으로 저장되었습니다!")

# -------------------------------------------------------------------------
# [페이지 2] 지난 기록 보기 화면
# -------------------------------------------------------------------------
elif page == "📚 지난 기록 보기":
    st.subheader("📚 지난 감정 기록 아카이브")

    if len(st.session_state["diary_list"]) == 0:
        st.info("💡 아직 작성된 감정 기록이 없습니다. '다이어리 작성하기'에서 첫 기록을 남겨보세요!")
    else:
        # 저장된 기록들을 하나씩 카드 형식으로 출력
        for i, entry in enumerate(st.session_state["diary_list"]):
            with st.container(border=True):
                moods_str = ", ".join(entry["moods"])
                st.markdown(f"**📅 날짜:** {entry['date']}")
                st.markdown(f"**🏷️ 기분:** {moods_str}")
                st.markdown(f"**✍️ 내용:** {entry['text']}")
