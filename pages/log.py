import streamlit as st
from datetime import datetime
import calendar

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Mood & Music Archive",
    page_icon="📚",
    layout="centered"
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
        border-radius: 10px !important;
    }
    [data-testid="stButton"] button:hover {
        background-color: #ECE4DA !important;
    }
    </style>
""", unsafe_allow_html=True)

st.subheader("🗓️ 감정 캘린더")
st.write("")

# 기록이 없을 경우
if "diary_list" not in st.session_state or len(st.session_state["diary_list"]) == 0:
    st.info("💡 아직 작성된 감정 기록이 없습니다. 오늘 하루를 먼저 기록해 보세요!")
else:
    # 현재 연도/월 세션 상태 초기화 (기본은 이번 달)
    now = datetime.now()
    if "cal_year" not in st.session_state:
        st.session_state["cal_year"] = now.year
    if "cal_month" not in st.session_state:
        st.session_state["cal_month"] = now.month

    # 월 이동 버튼 (◀ 이전 달 / 다음 달 ▶)
    col_prev, col_title, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("◀ 이전", use_container_width=True):
            if st.session_state["cal_month"] == 1:
                st.session_state["cal_month"] = 12
                st.session_state["cal_year"] -= 1
            else:
                st.session_state["cal_month"] -= 1
            st.rerun()

    with col_title:
        st.markdown(f"<h4 style='text-align: center; color: #5C5346; margin: 0;'>{st.session_state['cal_year']}년 {st.session_state['cal_month']}월</h4>", unsafe_allow_html=True)

    with col_next:
        if st.button("다음 ▶", use_container_width=True):
            if st.session_state["cal_month"] == 12:
                st.session_state["cal_month"] = 1
                st.session_state["cal_year"] += 1
            else:
                st.session_state["cal_month"] += 1
            st.rerun()

    st.write("")

    # 선택된 연도/월의 달력 데이터 가져오기 (월요일 시작 기준)
    cal = calendar.monthcalendar(st.session_state["cal_year"], st.session_state["cal_month"])
    
    # 요일 헤더 표시
    days_ko = ["월", "화", "수", "목", "금", "토", "일"]
    cols = st.columns(7)
    for i, day in enumerate(days_ko):
        with cols[i]:
            st.markdown(f"<p style='text-align: center; font-weight: bold; color: #8C8275;'>{day}</p>", unsafe_allow_html=True)

    # 이미 기록이 있는 날짜들 세트(Set)로 추출 ("YYYY년 MM월 DD일" 형태)
    recorded_dates = {entry["date"] for entry in st.session_state["diary_list"]}

    # 선택된 날짜 저장을 위한 세션 상태
    if "selected_calendar_date" not in st.session_state:
        st.session_state["selected_calendar_date"] = None

    # 달력 그리드 출력 (버튼 형태)
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("") # 빈 칸
                else:
                    # 날짜 문자열 생성 (예: "2026년 09월 28일")
                    date_str = f"{st.session_state['cal_year']}년 {st.session_state['cal_month']:02d}월 {day:02d}일"
                    
                    # 기록이 있는 날은 버튼에 이모지 표시
                    has_record = date_str in recorded_dates
                    btn_label = f"{day} ✨" if has_record else f"{day}"
                    
                    if st.button(btn_label, key=f"date_{st.session_state['cal_year']}_{st.session_state['cal_month']}_{day}", use_container_width=True):
                        st.session_state["selected_calendar_date"] = date_str

    st.write("")
    st.divider()

    # 사용자가 달력에서 날짜를 클릭했을 때 해당 날짜 일기 보여주기
    if st.session_state["selected_calendar_date"]:
        selected_date_str = st.session_state["selected_calendar_date"]
        st.markdown(f"### 📌 선택한 날짜: {selected_date_str}")
        
        filtered_entries = [entry for entry in st.session_state["diary_list"] if entry["date"] == selected_date_str]
        
        if filtered_entries:
            for entry in filtered_entries:
                with st.container(border=True):
                    moods_str = ", ".join(entry["moods"])
                    st.markdown(f"**🏷️ 기분:** {moods_str}")
                    
                    if entry.get("image"):
                        st.image(entry["image"], use_container_width=True)
                    
                    st.markdown(f"**✍️ 내용:** {entry['text']}")
        else:
            st.info(f"💡 {selected_date_str}에는 작성된 기록이 없습니다. (달력에 ✨표시가 있는 날짜를 눌러보세요!)")
