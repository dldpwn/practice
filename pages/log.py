import streamlit as st
from datetime import datetime

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
        border-radius: 12px !important;
    }

    /* 날짜 선택(달력) 박스 테두리 및 배경 톤 맞춤 */
    [data-testid="stDateInput"] input {
        background-color: #FDFBF7 !important;
        border: 1px solid #EAE5DC !important;
        border-radius: 12px !important;
        color: #5C5346 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.subheader("📚 감정 기록 캘린더")
st.write("")

# 기록이 없을 경우
if "diary_list" not in st.session_state or len(st.session_state["diary_list"]) == 0:
    st.info("💡 아직 작성된 감정 기록이 없습니다. 오늘 하루를 먼저 기록해 보세요!")
else:
    # 캘린더(날짜 선택) 위젯
    st.markdown("📅 **달력에서 조회할 날짜를 선택하세요:**")
    selected_date = st.date_input("날짜 선택", datetime.now(), label_visibility="collapsed")
    
    # 선택한 날짜를 메인에서 저장한 형식("YYYY년 MM월 DD일")으로 변환
    selected_date_str = selected_date.strftime("%Y년 %m월 %d일")
    
    # 해당 날짜의 일기만 필터링
    filtered_entries = [entry for entry in st.session_state["diary_list"] if entry["date"] == selected_date_str]
    
    st.write("")
    
    # 선택한 날짜에 기록이 있는 경우
    if filtered_entries:
        st.success(f"✨ {selected_date_str}에 작성된 기록이에요.")
        for entry in filtered_entries:
            with st.container(border=True):
                moods_str = ", ".join(entry["moods"])
                st.markdown(f"**🏷️ 기분:** {moods_str}")
                
                if entry.get("image"):
                    st.image(entry["image"], use_container_width=True)
                
                st.markdown(f"**✍️ 내용:** {entry['text']}")
    else:
        st.info(f"💡 {selected_date_str}에는 작성된 기록이 없습니다.")

    st.write("")
    st.divider()
    st.write("")

    # 📖 전체 기록을 한눈에 볼 수 있는 펼쳐보기 섹션
    with st.expander("📖 전체 감정 기록 모아보기"):
        if len(st.session_state["diary_list"]) == 0:
            st.info("작성된 기록이 없습니다.")
        else:
            for entry in st.session_state["diary_list"]:
                with st.container(border=True):
                    moods_str = ", ".join(entry["moods"])
                    st.markdown(f"**📅 날짜:** {entry['date']}")
                    st.markdown(f"**🏷️ 기분:** {moods_str}")
                    
                    if entry.get("image"):
                        st.image(entry["image"], use_container_width=True)
                    
                    st.markdown(f"**✍️ 내용:** {entry['text']}")
