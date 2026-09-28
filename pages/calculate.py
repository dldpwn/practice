import streamlit as st

# 1. 페이지 설정 (사이드바 기본 숨김)
st.set_page_config(
    page_title="탐구 기록장",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 디자인 및 사이드바 스타일 적용
st.markdown("""
    
""", unsafe_allow_html=True)

# --- 사이드바 영역 ---
with st.sidebar:
    st.markdown("### 🧭 메뉴 이동")
    st.info("💡 왼쪽 위의 **`>` (화살표)**를 누르면 사이드바를 다시 숨길 수 있어요!")
    st.page_link("app.py", label="🧪 영양소 & 화학 계산기", icon="🧮")
    st.page_link("pages/2_📝_탐구_기록장.py", label="📝 나의 탐구 기록장", icon="📚")

# --- 메인 화면 ---
st.subheader("📝 나의 과학 탐구 및 식단 기록장")
st.write("계산해 본 결과를 바탕으로 오늘 느낀 점이나 생명과학/화학 교과 연계 탐구 내용을 자유롭게 적어보세요.")
st.divider()

# 세션 상태로 기록 저장 기능 구현
if "memo_list" not in st.session_state:
    st.session_state["memo_list"] = []

memo_input = st.text_area("탐구 및 식단 메모", placeholder="예: 오늘 계산해보니 내 기초대사량이 생각보다 높았다. 탄수화물 대사 과정에 대해 더 찾아봐야겠다...")

if st.button("기록 저장하기", use_container_width=True):
    if memo_input.strip() == "":
        st.warning("⚠️ 내용을 입력해 주세요!")
    else:
        st.session_state["memo_list"].insert(0, memo_input)
        st.success("✨ 기록이 저장되었습니다!")

st.write("")
st.markdown("### 📚 저장된 탐구 기록 목록")

if not st.session_state["memo_list"]:
    st.info("💡 아직 작성된 기록이 없습니다.")
else:
    for idx, memo in enumerate(st.session_state["memo_list"]):
        with st.container(border=True):
            st.markdown(f"**기록 #{len(st.session_state['memo_list']) - idx}**")
            st.write(memo)
