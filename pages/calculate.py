
    st.metric(
        "식이섬유",
        f"{totals['fiber']:.1f} g",
    )

    # --------------------------------------------------
    # 끼니별 에너지
    # --------------------------------------------------
    st.markdown("#### 🍽️ 끼니별 에너지 구성")

    meal_energy_rows = []

    for meal_name, meal_items in selected_meal.items():
        if meal_name == "일차":
            continue

        meal_energy_rows.append({
            "끼니": meal_name,
            "에너지(kcal)": calculate_meal_energy(meal_items),
        })

    meal_energy_df = pd.DataFrame(meal_energy_rows)

    fig_meal = px.bar(
        meal_energy_df,
        x="끼니",
        y="에너지(kcal)",
        text="에너지(kcal)",
        title="끼니별 에너지",
    )

    fig_meal.update_layout(
        paper_bgcolor="#FBF9F1",
        plot_bgcolor="#FBF9F1",
        font=dict(family="Gowun Dodum"),
        showlegend=False,
        xaxis_title="",
        yaxis_title="에너지 (kcal)",
    )

    st.plotly_chart(
        fig_meal,
        use_container_width=True,
    )

    # --------------------------------------------------
    # 영양소 상세표
    # --------------------------------------------------
    with st.expander("영양소별 합계 자세히 보기"):

        detail_df = pd.DataFrame([
            ["에너지", f"{totals['kcal']:.1f}", "kcal"],
            ["탄수화물", f"{totals['carbs']:.1f}", "g"],
            ["단백질", f"{totals['protein']:.1f}", "g"],
            ["지방", f"{totals['fat']:.1f}", "g"],
            ["식이섬유", f"{totals['fiber']:.1f}", "g"],
            ["칼슘", f"{totals['calcium']:.1f}", "mg"],
            ["철분", f"{totals['iron']:.1f}", "mg"],
            ["칼륨", f"{totals['potassium']:.1f}", "mg"],
            ["나트륨", f"{totals['sodium']:.1f}", "mg"],
            ["비타민 A", f"{totals['vitamin_a']:.1f}", "μg RAE"],
            ["비타민 C", f"{totals['vitamin_c']:.1f}", "mg"],
            ["비타민 D", f"{totals['vitamin_d']:.1f}", "μg"],
        ], columns=["영양소", "합계", "단위"])

        st.dataframe(
            detail_df,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------
    # 전체 30일 식단표
    # --------------------------------------------------
    st.divider()
    st.markdown("#### 📋 전체 30일 식단표")

    table_rows = []

    for day in plan:
        row = {
            "일차": day["일차"],
        }

        for meal_name, meal_items in day.items():
            if meal_name == "일차":
                continue

            row[meal_name] = format_meal_items(meal_items)

        table_rows.append(row)

    plan_df = pd.DataFrame(table_rows)

    st.dataframe(
        plan_df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "📥 30일 식단표 다운로드",
        data=plan_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="NutriDay_30day_meal_plan.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # --------------------------------------------------
    # 식사 기록 페이지 이동
    # --------------------------------------------------
    st.button(
        "🍽️ 식사 기록 & 영양 관리로 이동하기 →",
        key="go_to_record",
        use_container_width=True,
        on_click=lambda: st.switch_page("pages/record.py"),
    )

else:
    st.info(
        "식단 생성 버튼을 눌러 나만의 식단을 만들어 보세요!"
    )
