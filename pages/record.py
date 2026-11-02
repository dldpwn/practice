
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
from datetime import date, timedelta

# ==================================================
# 페이지 설정
# ==================================================

st.set_page_config(
    page_title="식사 기록 | NutriDay",
    page_icon="🍽️",
    layout="wide"
)

# ==================================================
# 디자인
# ==================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

    html, body, [class*="css"], p, label,
    h1, h2, h3, h4, span, div {
        font-family: 'Gowun Dodum', sans-serif;
    }

    .stApp {
        background: #FBF9F1;
        color: #263B32;
    }

    [data-testid="stSidebar"] {
        background: #EEF6EF;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    .main-title {
        color: #377D61;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: .25rem;
    }

    .sub-text {
        color: #69756E;
        margin-bottom: 1.2rem;
    }

    .info-card {
        background: #F0F7F0;
        border: 1px solid #DCEADF;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-bottom: .7rem;
    }

    div[data-testid="stMetric"] {
        background: #F0F7F0;
        border: 1px solid #DCEADF;
        border-radius: 14px;
        padding: 1rem;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background: #4D9274;
        color: white;
        border: 0;
        border-radius: 12px;
        padding: .65rem 1rem;
        font-weight: 700;
        transition: .2s;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background: #377D61;
        color: white;
        border: 0;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] > div {
        background: #FFFFFF;
        border-radius: 10px;
        border-color: #DCEADF;
    }

    button[data-baseweb="tab"] {
        color: #69756E;
        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #377D61;
        border-bottom-color: #4D9274;
    }

    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        border: 1px solid #DCEADF;
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: #DCEADF;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# 기본 설정
# ==================================================

st.title("🍽️ 식사 기록 & 영양 관리")

st.markdown(
    "매일 먹은 음식을 기록하고 나의 영양 섭취 현황을 관리해 보세요."
)

st.divider()

MEALS = ["아침", "점심", "저녁", "간식"]

COLUMNS = ["음식 이름", "섭취량(g)"]

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "meal_records.json"
)

# ==================================================
# 사이드바
# ==================================================

with st.sidebar:

    st.markdown("## 🥗 NutriDay")
    st.caption("나에게 맞는 하루 영양 관리")
    st.divider()

    email = st.session_state.get("auth_email")

    st.markdown("### 👤 내 계정")
    st.caption(email or "계정 이메일을 확인할 수 없어요.")

    st.divider()

    st.page_link(
        "main.py",
        label="🧪 기초대사량 & 영양 가이드"
    )

    st.page_link(
        "pages/calculate.py",
        label="🥗 한 달 맞춤 식단"
    )

    st.page_link(
        "pages/record.py",
        label="🍽️ 식사 기록 & 영양 관리"
    )

    st.divider()

    if st.button(
        "로그아웃",
        key="record_logout",
        use_container_width=True
    ):

        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        for key in [
            "auth_access_token",
            "auth_refresh_token",
            "auth_email"
        ]:
            st.session_state.pop(key, None)

        st.rerun()


# ==================================================
# 데이터 저장 및 불러오기
# ==================================================

def load_records():

    if DATA_FILE.exists():

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

        except (json.JSONDecodeError, OSError):
            st.warning(
                "저장된 기록을 불러오지 못했습니다."
            )

    return {}


def save_records(records):

    with open(DATA_FILE, "w", encoding="utf-8") as file:

        json.dump(
            records,
            file,
            ensure_ascii=False,
            indent=4
        )


def normalize_foods(food_list):
    """
    기존 기록에 영양성분 정보가 들어 있더라도
    음식 이름과 섭취량만 가져오도록 변환
    """

    normalized = []

    for food in food_list:

        if not isinstance(food, dict):
            continue

        name = str(food.get("음식 이름", "")).strip()

        if not name:
            continue

        try:
            amount = float(food.get("섭취량(g)", 0) or 0)
        except (ValueError, TypeError):
            amount = 0.0

        normalized.append({
            "음식 이름": name,
            "섭취량(g)": amount
        })

    return normalized


if "meal_records" not in st.session_state:
    st.session_state["meal_records"] = load_records()

records = st.session_state["meal_records"]


# ==================================================
# 날짜 선택
# ==================================================

st.subheader("📅 기록할 날짜")

selected_date = st.date_input(
    "식사 기록 날짜를 선택하세요.",
    value=date.today(),
    key="record_date"
)

date_key = selected_date.isoformat()

st.caption(
    f"선택한 날짜: {selected_date.strftime('%Y년 %m월 %d일')}"
)


# ==================================================
# 식사 기록 입력
# ==================================================

st.divider()

st.subheader("🥗 오늘 먹은 음식 입력")

st.info(
    "음식 이름과 섭취량만 입력해 주세요. "
    "영양성분은 식품 데이터베이스 연결 후 자동으로 분석됩니다."
)

tabs = st.tabs(MEALS)

meal_data = {}

for index, meal in enumerate(MEALS):

    with tabs[index]:

        st.markdown(f"### 🍴 {meal}")

        saved_foods = records.get(
            date_key, {}
        ).get(meal, [])

        saved_foods = normalize_foods(saved_foods)

        if saved_foods:

            default_df = pd.DataFrame(
                saved_foods,
                columns=COLUMNS
            )

        else:

            default_df = pd.DataFrame(
                columns=COLUMNS
            )

        edited_df = st.data_editor(
            default_df,
            key=f"editor_{date_key}_{meal}",
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config={

                "음식 이름": st.column_config.TextColumn(
                    "음식 이름",
                    help="먹은 음식의 이름을 입력하세요.",
                    required=True
                ),

                "섭취량(g)": st.column_config.NumberColumn(
                    "섭취량(g)",
                    help="실제로 먹은 양을 입력하세요.",
                    min_value=0,
                    step=10,
                    format="%.1f",
                    required=True
                )

            }
        )

        meal_data[meal] = edited_df


# ==================================================
# 기록 저장
# ==================================================

st.divider()

st.subheader("💾 기록 관리")

col1, col2 = st.columns(2)

with col1:

    save_button = st.button(
        "💾 식사 기록 저장",
        use_container_width=True,
        type="primary"
    )

with col2:

    delete_button = st.button(
        "🗑️ 선택한 날짜 기록 삭제",
        use_container_width=True
    )


if save_button:

    new_day_record = {}

    for meal in MEALS:

        df = meal_data[meal].copy()

        df = df.dropna(subset=["음식 이름"])

        df["음식 이름"] = (
            df["음식 이름"]
            .astype(str)
            .str.strip()
        )

        df = df[df["음식 이름"] != ""]

        saved_list = []

        for _, row in df.iterrows():

            try:
                amount = float(row["섭취량(g)"])
            except (ValueError, TypeError):
                amount = 0.0

            if amount <= 0:
                continue

            saved_list.append({
                "음식 이름": str(row["음식 이름"]),
                "섭취량(g)": amount
            })

        new_day_record[meal] = saved_list

    if not any(new_day_record.values()):

        records.pop(date_key, None)

    else:

        records[date_key] = new_day_record

    save_records(records)

    st.session_state["meal_records"] = records

    st.success("식사 기록이 저장되었습니다!")

    st.rerun()


# ==================================================
# 날짜별 기록 삭제
# ==================================================

if delete_button:

    if date_key in records:

        del records[date_key]

        save_records(records)

        st.session_state["meal_records"] = records

        # 해당 날짜의 입력창 상태 초기화
        for meal in MEALS:

            editor_key = f"editor_{date_key}_{meal}"

            st.session_state.pop(editor_key, None)

        st.success(
            "선택한 날짜의 모든 식사 기록을 삭제했습니다."
        )

        st.rerun()

    else:

        st.warning("삭제할 기록이 없습니다.")


# ==================================================
# 저장된 음식 기록 확인
# ==================================================

st.divider()

st.subheader("📋 선택한 날짜의 식사 기록")

day_record = records.get(date_key, {})

has_records = False

for meal in MEALS:

    foods = normalize_foods(
        day_record.get(meal, [])
    )

    if foods:

        has_records = True

        with st.expander(
            f"🍴 {meal} ({len(foods)}개 음식)",
            expanded=True
        ):

            display_df = pd.DataFrame(foods)

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            total_amount = sum(
                food["섭취량(g)"]
                for food in foods
            )

            st.caption(
                f"총 섭취량: {total_amount:,.1f}g"
            )

if not has_records:

    st.info(
        "선택한 날짜에 저장된 식사 기록이 없습니다."
    )


# ==================================================
# 영양 분석 영역
# ==================================================

st.divider()

st.subheader("📊 하루 영양 분석")

st.info(
    """
    **영양성분 자동 분석 기능을 준비하고 있습니다.**

    식품영양성분 데이터베이스를 연결하면 입력한 음식 이름과
    섭취량을 바탕으로 다음 정보를 자동 계산합니다.

    - 총 섭취 열량
    - 탄수화물 · 단백질 · 지방
    - 나트륨 · 칼슘 · 철분 · 칼륨
    - 식사별 영양성분 및 하루 총섭취량
    """
)


# ==================================================
# 영양 섭취 그래프 영역
# ==================================================

st.divider()

st.subheader("📈 영양 섭취 현황 그래프")

graph_mode = st.radio(
    "조회 기간을 선택하세요.",
    ["하루", "최근 7일"],
    horizontal=True,
    key="graph_mode"
)

if graph_mode == "하루":

    st.caption(
        f"{selected_date.strftime('%Y년 %m월 %d일')}의 영양 섭취 분석"
    )

else:

    start_date = selected_date - timedelta(days=6)

    st.caption(
        f"{start_date.strftime('%Y년 %m월 %d일')} ~ "
        f"{selected_date.strftime('%Y년 %m월 %d일')}"
    )

st.info(
    "식품영양성분 데이터베이스 연결 후 "
    "영양소별 섭취량과 기간별 변화 그래프가 표시됩니다."
)


# ==================================================
# 기록 다운로드
# ==================================================

st.divider()

st.subheader("📥 식사 기록 다운로드")

if records:

    export_rows = []

    for saved_date, day_record in records.items():

        for meal in MEALS:

            foods = normalize_foods(
                day_record.get(meal, [])
            )

            for food in foods:

                row = {
                    "날짜": saved_date,
                    "식사": meal,
                    "음식 이름": food["음식 이름"],
                    "섭취량(g)": food["섭취량(g)"]
                }

                export_rows.append(row)

    if export_rows:

        export_df = pd.DataFrame(export_rows)

        export_df["날짜"] = pd.to_datetime(
            export_df["날짜"]
        )

        export_df = export_df.sort_values(
            by=["날짜", "식사"]
        )

        export_df["날짜"] = (
            export_df["날짜"]
            .dt.strftime("%Y-%m-%d")
        )

        st.download_button(
            "📥 식사 기록 CSV 다운로드",

            data=export_df.to_csv(
                index=False
            ).encode("utf-8-sig"),

            file_name="NutriDay_meal_records.csv",

            mime="text/csv",

            use_container_width=True
        )

else:

    st.info("다운로드할 식사 기록이 없습니다.")


# ==================================================
# 마무리
# ==================================================

st.divider()

st.caption(
    "NutriDay | 나의 식사 기록을 통해 건강한 식습관을 만들어 보세요."
)
