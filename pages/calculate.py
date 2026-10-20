preference_options = [
    "닭고기",
    "생선",
    "달걀",
    "두부",
    "소고기",
    "돼지고기",
    "채소",
    "과일",
    "우유",
    "견과류",
    "직접 입력"
]

preference = st.multiselect(
    "선호하는 음식",
    preference_options,
    default=["닭고기", "달걀", "채소"]
)

custom_preference = []

if "직접 입력" in preference:
    custom_preference_text = st.text_input(
        "선호 음식 입력",
        placeholder="예: 고구마, 바나나"
    )

    custom_preference = [
        food.strip()
        for food in custom_preference_text.split(",")
        if food.strip()
    ]

all_preferences = list(dict.fromkeys(
    [food for food in preference if food != "직접 입력"]
    + custom_preference
))
