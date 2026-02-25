"""ui_components.py — All Streamlit rendering functions."""

from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

from health_metrics import ACTIVITY_MULTIPLIERS

# ── Plotly theme to match cream/editorial palette ─────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(245,240,232,0.5)",
    font=dict(family="Epilogue, sans-serif", color="#1A1A18", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
)

RUST   = "#C4511A"
SAGE   = "#4A6741"
GOLD   = "#B8963E"
INK    = "#1A1A18"
MUTED  = "#8C8878"
BORDER = "#D4CEC2"


# ─── Header ───────────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="app-header">
        <span class="app-kicker">✦ AI-Powered Fitness Intelligence ✦</span>
        <h1 class="app-title">Personal <em>Fitness</em> Planner</h1>
        <p class="app-tagline">Machine learning meets nutrition science — built around you.</p>
        <div class="app-header-rule"></div>
    </div>
    """, unsafe_allow_html=True)


# ─── User Input ───────────────────────────────────────────────────────────────
def render_user_input_section() -> dict:
    age    = st.slider("Age", 16, 80, 28)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", 140, 230, 170, step=1)
    weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, step=0.5)

    st.markdown("---")

    activity = st.selectbox(
        "Activity Level",
        list(ACTIVITY_MULTIPLIERS.keys()),
        index=2,
    )
    fitness_goal = st.selectbox(
        "Fitness Goal",
        ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness", "Maintenance"],
    )
    dietary_pref = st.selectbox(
        "Dietary Preference",
        ["Non-Vegetarian", "Vegetarian", "Vegan", "Pescatarian", "Keto", "Paleo"],
    )
    cultural_food = st.selectbox(
        "Cultural Food Habits",
        [
            "South Asian (Indian/Pakistani/Sri Lankan)",
            "East Asian (Chinese/Japanese/Korean)",
            "Southeast Asian (Thai/Vietnamese/Filipino)",
            "Middle Eastern",
            "Western (European/American)",
            "Latin American",
            "African",
        ],
        index=4,
    )

    st.markdown("---")

    budget = st.number_input("Daily Food Budget (USD $)", 2.0, 50.0, 10.0, step=0.5)
    equipment = st.multiselect(
        "Available Equipment",
        ["Bodyweight", "Dumbbells", "Barbell", "Resistance Bands",
         "Machines", "Pull-up Bar", "Kettlebell"],
        default=["Bodyweight", "Dumbbells"],
    )
    if not equipment:
        equipment = ["Bodyweight"]

    st.markdown("---")

    free_text = st.text_area(
        "Preferences / Injuries / Notes",
        placeholder="e.g. bad left knee, love spicy food, prefer morning workouts...",
        height=80,
    )

    activity_map = {k: i for i, k in enumerate(ACTIVITY_MULTIPLIERS.keys())}
    goal_map = {
        "Weight Loss": 0, "Muscle Gain": 1, "Endurance": 2,
        "General Fitness": 3, "Maintenance": 4,
    }

    return {
        "age":                    age,
        "gender":                 gender,
        "height_cm":              height,
        "weight_kg":              weight,
        "activity_level":         activity,
        "activity_level_encoded": activity_map.get(activity, 2),
        "fitness_goal":           fitness_goal,
        "fitness_goal_encoded":   goal_map.get(fitness_goal, 3),
        "dietary_preference":     dietary_pref,
        "cultural_food_habits":   cultural_food,
        "budget_usd_per_day":     budget,
        "available_equipment":    equipment,
        "free_text_prefs":        free_text.strip() if free_text.strip() else None,
    }


# ─── Health Metrics Dashboard ─────────────────────────────────────────────────
def render_health_metrics_dashboard(plan: dict):
    st.markdown("""
    <div class="section-header">
        Health Metrics
        <span class="section-header-sub">Computed from your biometrics</span>
    </div>
    """, unsafe_allow_html=True)

    bmi_cat = plan["bmi_category"]

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "plain", "plain", "BMI",              plan['bmi'],              bmi_cat['emoji'] + " " + bmi_cat['label']),
        (c2, "rust",  "rust",  "BMR",              f"{plan['bmr']:.0f}",     "kcal / day at rest"),
        (c3, "sage",  "sage",  "TDEE",             f"{plan['tdee']:.0f}",    "kcal / day total"),
        (c4, "gold",  "gold",  "Predicted Intake", f"{plan['predicted_calories']:.0f}", "kcal / day (AI model)"),
    ]
    for col, card_cls, val_cls, label, value, unit in cards:
        with col:
            st.markdown(f"""
            <div class="metric-card {card_cls}">
                <span class="metric-label">{label}</span>
                <span class="metric-value {val_cls}">{value}</span>
                <span class="metric-unit">{unit}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown(f"""
        <div class="info-box">
            AI Fitness Level &nbsp;→&nbsp;
            <span class="fitness-badge">{plan['fitness_level']}</span>
            &nbsp; <span style="color:var(--ink-muted);font-size:0.82rem;">
            K-Means Cluster {plan['fitness_cluster']}</span>
        </div>""", unsafe_allow_html=True)

        macros = plan["macros"]
        fig = go.Figure(go.Pie(
            labels=["Protein", "Carbs", "Fat"],
            values=[macros["protein_pct"], macros["carbs_pct"], macros["fat_pct"]],
            hole=0.62,
            marker=dict(
                colors=[RUST, SAGE, GOLD],
                line=dict(color="rgba(245,240,232,1)", width=3),
            ),
            textinfo="label+percent",
            textfont=dict(size=12, family="Epilogue, sans-serif"),
            hovertemplate="<b>%{label}</b><br>%{customdata[0]}g<extra></extra>",
            customdata=[[macros["protein_g"]], [macros["carbs_g"]], [macros["fat_g"]]],
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Macro Split", font=dict(size=13, color=MUTED)),
            showlegend=False,
            height=270,
            annotations=[dict(
                text=f"<b>{plan['predicted_calories']:.0f}</b><br><span style='font-size:10px'>kcal</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=18, family="Playfair Display, serif", color=INK),
            )],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        macros = plan["macros"]
        macro_data = {
            "Macro":   ["Protein", "Carbohydrates", "Fat"],
            "Grams":   [macros["protein_g"], macros["carbs_g"], macros["fat_g"]],
        }
        fig2 = go.Figure()
        for i, (macro, grams, color) in enumerate(zip(
            macro_data["Macro"], macro_data["Grams"], [RUST, SAGE, GOLD]
        )):
            cal = grams * 4 if macro != "Fat" else grams * 9
            fig2.add_trace(go.Bar(
                name=macro, x=[macro], y=[grams],
                marker=dict(color=color, line=dict(width=0)),
                text=[f"{grams}g"],
                textposition="inside",
                textfont=dict(color="white", size=11, family="Roboto Mono, monospace"),
                hovertemplate=f"<b>{macro}</b><br>{grams}g · {cal:.0f} kcal<extra></extra>",
            ))
        fig2.update_layout(
            **PLOTLY_LAYOUT,
            showlegend=False,
            barmode="group",
            title=dict(text="Daily Macro Targets", font=dict(size=13, color=MUTED)),
            xaxis=dict(showgrid=False, color=INK),
            yaxis=dict(showgrid=True, gridcolor=BORDER, title="Grams", color=MUTED),
            height=270,
        )
        st.plotly_chart(fig2, use_container_width=True)


# ─── Workout Plan ─────────────────────────────────────────────────────────────
def render_workout_plan(plan: dict, user_data: dict):
    st.markdown("""
    <div class="section-header">
        Workout Plan
        <span class="section-header-sub">7-day personalised programme</span>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_burn = st.columns([3, 1])
    with col_info:
        st.markdown(f"""
        <div class="info-box">
            <b>{plan['fitness_level']}</b> programme · Goal: <b>{user_data['fitness_goal']}</b> ·
            Equipment: {', '.join(user_data['available_equipment'])}
        </div>""", unsafe_allow_html=True)
    with col_burn:
        st.metric("Weekly Burn Est.", f"{plan.get('weekly_burn', 0):.0f} kcal")

    if plan.get("embedding_notes"):
        st.markdown("**Personalisation notes from your preferences:**")
        for note in plan["embedding_notes"]:
            st.markdown(f'<div class="nlp-note">✦ {note}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(2)

    for i, day_data in enumerate(plan["workout_plan"]):
        with cols[i % 2]:
            if day_data["type"] == "rest":
                st.markdown(f"""
                <div class="day-card rest-day">
                    <div class="day-title">
                        {day_data['day']}
                        <span class="day-focus-tag rest">{day_data['focus']}</span>
                    </div>
                    <div style="color:var(--ink-muted);font-size:0.85rem;font-style:italic;">
                        {day_data['notes']}
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                exercises_html = "".join([
                    f"""<div class="exercise-row">
                        <span class="ex-dot"></span>
                        <span class="ex-name">{ex['name']}</span>
                        <span class="ex-sets">{ex['sets']}</span>
                        <span class="ex-muscle">{ex['muscle']}</span>
                    </div>"""
                    for ex in day_data["exercises"]
                ])
                st.markdown(f"""
                <div class="day-card">
                    <div class="day-title">
                        {day_data['day']}
                        <span class="day-focus-tag">{day_data['focus']}</span>
                    </div>
                    {exercises_html}
                    <div class="day-note">
                        ↳ {day_data['notes']}
                        &nbsp;&nbsp;·&nbsp;&nbsp; ~{day_data['duration_min']} min
                    </div>
                </div>""", unsafe_allow_html=True)


# ─── Diet Plan ────────────────────────────────────────────────────────────────
def render_diet_plan(plan: dict, user_data: dict):
    st.markdown("""
    <div class="section-header">
        Diet Plan
        <span class="section-header-sub">Culturally tailored daily meals</span>
    </div>
    """, unsafe_allow_html=True)

    diet = plan["diet_plan"]

    col_info, col_cost = st.columns([3, 1])
    with col_info:
        st.markdown(f"""
        <div class="info-box">
            <b>{user_data['dietary_preference']}</b> ·
            {user_data['cultural_food_habits']} ·
            Budget: <b>${user_data['budget_usd_per_day']:.2f} / day</b>
        </div>""", unsafe_allow_html=True)
    with col_cost:
        daily_cost = sum(m["cost"] for m in diet["weekly_plan"][0]["meals"])
        st.metric("Est. Daily Cost", f"${daily_cost:.2f}")

    if diet.get("nlp_adjustment"):
        st.markdown(
            f'<div class="nlp-note">✦ Dietary Adjustment: {diet["nlp_adjustment"]}</div>',
            unsafe_allow_html=True,
        )

    selected_day = st.select_slider(
        "Select Day", options=[d["day"] for d in diet["weekly_plan"]], value="Monday"
    )
    day_plan = next(d for d in diet["weekly_plan"] if d["day"] == selected_day)

    st.markdown(f"<br>", unsafe_allow_html=True)
    meal_cols = st.columns(len(day_plan["meals"]))
    for col, meal in zip(meal_cols, day_plan["meals"]):
        with col:
            st.markdown(f"""
            <div class="meal-card">
                <div class="meal-header">
                    <span class="meal-title">{meal['name']}</span>
                    <span class="meal-calories">{meal['calories']} <span>kcal</span></span>
                </div>
                <div class="meal-item">{meal['item']}</div>
                <div class="meal-macros">
                    <span class="macro-pill">P <b>{meal['protein']}g</b></span>
                    <span class="macro-pill">C <b>{meal['carbs']}g</b></span>
                    <span class="macro-pill">F <b>{meal['fat']}g</b></span>
                    <span class="macro-pill" style="margin-left:auto;">${meal['cost']:.2f}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>**Weekly Meal Overview**", unsafe_allow_html=True)
    rows = []
    for day_data in diet["weekly_plan"]:
        for meal in day_data["meals"]:
            rows.append({
                "Day":      day_data["day"],
                "Meal":     meal["name"],
                "Item":     meal["item"],
                "Calories": meal["calories"],
                "Protein":  f"{meal['protein']}g",
                "Carbs":    f"{meal['carbs']}g",
                "Fat":      f"{meal['fat']}g",
                "Cost":     f"${meal['cost']:.2f}",
            })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─── Calorie Balance Visualization ────────────────────────────────────────────
def render_calorie_visualization(plan: dict):
    st.markdown("""
    <div class="section-header">
        Calorie Balance
        <span class="section-header-sub">TDEE · intake · burn analysis</span>
    </div>
    """, unsafe_allow_html=True)

    tdee        = plan["tdee"]
    predicted   = plan["predicted_calories"]
    weekly_burn = plan.get("weekly_burn", 0)
    daily_burn  = weekly_burn / 7
    net_balance = predicted - tdee

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TDEE",            f"{tdee:.0f} kcal")
    c2.metric("Target Intake",   f"{predicted:.0f} kcal")
    c3.metric("Workout Burn",    f"{daily_burn:.0f} kcal/day")
    balance_label = "Surplus" if net_balance > 0 else "Deficit"
    c4.metric(balance_label,     f"{abs(net_balance):.0f} kcal",
              delta=f"{net_balance:+.0f}", delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        cats   = ["TDEE", "Target Intake", "Net After Workout"]
        vals   = [tdee, predicted, predicted - daily_burn]
        colors = [GOLD, RUST, SAGE]
        fig = go.Figure(go.Bar(
            x=cats, y=vals,
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v:.0f}" for v in vals],
            textposition="outside",
            textfont=dict(color=INK, family="Roboto Mono, monospace", size=11),
        ))
        fig.add_hline(y=tdee, line=dict(color=MUTED, dash="dash", width=1.5),
                      annotation_text="TDEE", annotation_font_color=MUTED)
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Calorie Comparison", font=dict(size=13, color=MUTED)),
            yaxis=dict(showgrid=True, gridcolor=BORDER, color=MUTED),
            xaxis=dict(showgrid=False, color=INK),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        days      = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        burns     = []
        cum_nets  = []
        cum_net   = 0
        for i, day_data in enumerate(plan.get("workout_plan", [])):
            b = daily_burn * 1.5 if day_data.get("type") == "workout" else daily_burn * 0.3
            burns.append(b)
            cum_net += (predicted - tdee - b)
            cum_nets.append(cum_net)

        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(
            x=days, y=burns, name="Workout Burn",
            marker=dict(color=GOLD, line=dict(width=0)), opacity=0.85,
        ), secondary_y=False)
        fig2.add_trace(go.Scatter(
            x=days, y=cum_nets, name="Cumulative Balance",
            mode="lines+markers",
            line=dict(color=RUST, width=2.5),
            marker=dict(size=7, color=RUST, line=dict(color="white", width=1.5)),
        ), secondary_y=True)
        fig2.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Weekly Burn & Cumulative Balance", font=dict(size=13, color=MUTED)),
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
            height=320,
        )
        fig2.update_yaxes(title_text="Burn (kcal)", secondary_y=False,
                          gridcolor=BORDER, color=MUTED)
        fig2.update_yaxes(title_text="Cumulative (kcal)", secondary_y=True,
                          showgrid=False, color=MUTED)
        st.plotly_chart(fig2, use_container_width=True)

    # Macro calorie waterfall
    macros      = plan["macros"]
    protein_cal = macros["protein_g"] * 4
    carbs_cal   = macros["carbs_g"]   * 4
    fat_cal     = macros["fat_g"]     * 9
    total       = protein_cal + carbs_cal + fat_cal

    fig3 = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=["Protein", "Carbs", "Fat", "Total"],
        y=[protein_cal, carbs_cal, fat_cal, 0],
        text=[f"{protein_cal:.0f}", f"+{carbs_cal:.0f}", f"+{fat_cal:.0f}", f"{total:.0f}"],
        textposition="outside",
        textfont=dict(family="Roboto Mono, monospace", color=INK, size=11),
        connector=dict(line=dict(color=BORDER, width=1)),
        increasing=dict(marker=dict(color=SAGE)),
        decreasing=dict(marker=dict(color=RUST)),
        totals=dict(marker=dict(color=INK)),
    ))
    fig3.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Calories by Macronutrient", font=dict(size=13, color=MUTED)),
        yaxis=dict(showgrid=True, gridcolor=BORDER, color=MUTED),
        xaxis=dict(showgrid=False, color=INK),
        height=290,
    )
    st.plotly_chart(fig3, use_container_width=True)


# ─── Explainability / AI Insights ─────────────────────────────────────────────
def render_explainability_section(plan: dict, user_data: dict):
    st.markdown("""
    <div class="section-header">
        AI Insights
        <span class="section-header-sub">How your plan was generated</span>
    </div>
    """, unsafe_allow_html=True)

    pipeline_steps = [
        ("Step 1 — Biometric Equations",
         "Harris-Benedict BMI / BMR / TDEE",
         f"BMI {plan['bmi']} · BMR {plan['bmr']:.0f} kcal · TDEE {plan['tdee']:.0f} kcal"),
        ("Step 2 — Fitness Clustering",
         "scaler.pkl → kmeans_model.pkl",
         f"Cluster {plan['fitness_cluster']} → **{plan['fitness_level']}** fitness level"),
        ("Step 3 — Calorie Prediction",
         "calorie_preprocessor.pkl → dtr_model.pkl",
         f"Predicted {plan['predicted_calories']:.0f} kcal/day for goal: {user_data['fitness_goal']}"),
        ("Step 4 — NLP Preference Matching",
         "sentence_transformer_model.pkl → cosine similarity",
         f"{len(plan.get('embedding_notes', []))} personalisation notes applied"),
        ("Step 5 — Plan Generation",
         "Rules engine using ML outputs",
         f"7-day {user_data['fitness_goal']} plan · {plan['fitness_level']} · "
         f"{', '.join(user_data['available_equipment'])}"),
    ]

    for step, method, outcome in pipeline_steps:
        with st.expander(f"{step}  ·  {method}"):
            st.markdown(f"**Outcome:** {outcome}")
            if "Clustering" in step:
                st.markdown("""
                Features passed to scaler → KMeans:
                `age`, `bmi`, `activity_level_active`, `activity_level_light`,
                `activity_level_moderate`, `activity_level_sedentary`, `activity_level_very active`
                """)
            elif "Calorie" in step:
                st.markdown("""
                `calorie_preprocessor.pkl` encodes categoricals + scales numerics,
                then `dtr_model.pkl` (Decision Tree Regressor) predicts target daily calories.
                """)
            elif "NLP" in step:
                notes = plan.get("embedding_notes", [])
                if notes:
                    for note in notes:
                        st.markdown(f"- {note}")
                else:
                    st.info("Add preferences in the sidebar to activate NLP personalisation.")

    st.markdown("<br>**Macro Target Rationale**", unsafe_allow_html=True)
    rationale = {
        "Weight Loss":     "High protein (35%) preserves lean mass during a calorie deficit. Moderate carbs fuel training; healthy fats support hormonal function.",
        "Muscle Gain":     "Elevated carbs (45%) fuel hypertrophy sessions. High protein supports muscle protein synthesis. Moderate fat for hormone production.",
        "Endurance":       "Carbohydrate-dominant (55%) split fuels aerobic systems. Lower protein is sufficient for endurance athletes. Controlled fat for sustained energy.",
        "General Fitness": "Balanced split supporting overall health, energy levels, and recovery.",
        "Maintenance":     "Maintenance split mirrors General Fitness — sustains current body composition.",
    }
    st.info(f"**{user_data['fitness_goal']}** — {rationale.get(user_data['fitness_goal'], '')}")

    macros = plan["macros"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Protein", f"{macros['protein_g']}g", f"{macros['protein_pct']*100:.0f}% of calories")
    c2.metric("Carbs",   f"{macros['carbs_g']}g",   f"{macros['carbs_pct']*100:.0f}% of calories")
    c3.metric("Fat",     f"{macros['fat_g']}g",     f"{macros['fat_pct']*100:.0f}% of calories")

    st.markdown("<br>**Export**", unsafe_allow_html=True)
    import json
    export_data = {
        "user_profile":    {k: v for k, v in user_data.items() if k != "free_text_prefs"},
        "health_metrics":  {
            "bmi": plan["bmi"], "bmi_category": plan["bmi_category"]["label"],
            "bmr": plan["bmr"], "tdee": plan["tdee"],
            "fitness_level": plan["fitness_level"], "fitness_cluster": plan["fitness_cluster"],
        },
        "targets":         {"daily_calories": plan["predicted_calories"], "macros": plan["macros"]},
        "workout_summary": [
            {"day": d["day"], "focus": d["focus"], "type": d["type"]}
            for d in plan["workout_plan"]
        ],
    }
    st.download_button(
        "↓ Download Plan (JSON)",
        data=json.dumps(export_data, indent=2),
        file_name="fitness_plan.json",
        mime="application/json",
    )
