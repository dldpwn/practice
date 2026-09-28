import streamlit as st

# 1. 페이지 기본 설정 (와이드 레이아웃 적용)
st.set_page_config(
    page_title="오늘의 감정 뮤직 다이어리",
    page_icon="🎵",
    layout="centered"
)

# 2. 메인 화면 타이틀 및 소개
st.title("🎵 오늘의 감정 뮤직 다이어리")
st.caption("그날의 기분을 기록하고, 어울리는 음악을 함께 남겨보세요.")

st.write("---")

# 3. 일기 작성 입력 폼 영역
st.subheader("📝 오늘 하루 기록하기")

# 날짜 선택
diary_date = st.date_input("📅 날짜 선택")

# 💡 여러 개 선택할 수 있도록 multiselect로 변경한 감정 선택 옵션
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

# 4. 저장 버튼 영역
if st.button("💾 다이어리 저장하기", use_container_width=True):
    if diary_text.strip() == "":
        st.warning("⚠️ 일기 내용을 한 줄 이상 적어주세요!")
    elif not selected_moods:
        st.warning("⚠️ 오늘의 기분을 최소 1개 이상 선택해 주세요!")
    else:
        moods_str = ", ".join(selected_moods)
        st.success(f"✨ [{diary_date}] ({moods_str}) 감정 기록이 성공적으로 작성되었습니다!")
