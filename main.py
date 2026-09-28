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

# 감정 선택 (이모지와 함께)
mood = st.selectbox(
    "😊 오늘의 기분은 어떤가요?",
    [
        "✨ 신나고 에너지가 넘치는 날",
        "😌 마음이 편안하고 평화로운 날",
        "💧 조금 지치고 위로가 필요한 날",
        "🌧️ 우울하고 혼자만의 시간이 필요한 날",
        "🔥 의욕이 불타오르는 날"
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
    else:
        st.success(f"✨ [{diary_date}] 감정 기록이 성공적으로 작성되었습니다!")
