import gradio as gr
import numpy as np

from ui_components import CUSTOM_CSS, render_header
from model_loader import ModelLoader
from health_metrics import HealthMetrics
from planner import WorkoutPlanner, DietPlanner

# Load models once
models = ModelLoader()


# ─────────────────────────────────────────────
# Core Logic
# ─────────────────────────────────────────────
def compute_plan(
    age, gender, height, weight,
    activity_level, fitness_goal,
    dietary_preference, cultural_food,
    budget, equipment, free_text
):

    user_data = {
        "age": age,
        "gender": gender,
        "height_cm": height,
        "weight_kg": weight,
        "activity_level": activity_level,
        "fitness_goal": fitness_goal,
        "dietary_preference": dietary_preference,
        "cultural_food_habits": cultural_food,
        "budget_usd_per_day": budget,
        "available_equipment": equipment,
        "free_text_prefs": free_text
    }

    # ── Health Metrics ───────────────────────
    metrics = HealthMetrics(user_data)
    bmi = round(metrics.bmi(), 2)
    bmr = round(metrics.bmr(), 1)
    tdee = round(metrics.tdee(), 1)

    # ── Fitness Cluster ──────────────────────
    cluster_features = np.array([[age, bmi, 0, 0, 0, 0, 0]])
    scaled = models.scale(cluster_features)
    cluster = models.predict_cluster(scaled)

    # ── Calorie Prediction ───────────────────
    calorie_features = models.preprocess_calories({
        "age": age,
        "gender": gender,
        "height_cm": height,
        "weight_kg": weight,
        "activity_level": activity_level,
        "fitness_goal": fitness_goal,
        "bmi": bmi,
        "bmr": bmr,
        "tdee": tdee,
    })

    predicted_calories = models.predict_calories(calorie_features)

    # ── Workout Plan ─────────────────────────
    workout_plan = WorkoutPlanner.generate(
        fitness_level="Intermediate",
        fitness_goal=fitness_goal,
        available_equipment=equipment,
        notes=[]
    )

    # ── Diet Plan ────────────────────────────
    diet_plan = DietPlanner.generate(
        daily_calories=predicted_calories,
        macros={"protein_pct": 30, "carbs_pct": 40, "fat_pct": 30},
        dietary_preference=dietary_preference,
        cultural_food_habits=cultural_food,
        budget_usd=budget,
        notes=[]
    )

    # ── Output Formatting ────────────────────
    workout_days = ", ".join([d["day"] for d in workout_plan])

    return f"""
## 📊 Health Metrics
**BMI:** {bmi}  
**BMR:** {bmr} kcal  
**TDEE:** {tdee} kcal  
**Predicted Calories:** {round(predicted_calories)} kcal  

---

## 🏋 Workout Plan
Days Scheduled:  
{workout_days}

---

## 🥗 Diet Plan
Personalized meal plan generated successfully.
"""


# ─────────────────────────────────────────────
# Gradio UI
# ─────────────────────────────────────────────
with gr.Blocks(css=CUSTOM_CSS, title="AI Fitness Planner") as app:

    # Header from ui_components.py
    render_header()

    with gr.Row():
        age = gr.Slider(16, 80, value=28, label="Age")
        gender = gr.Dropdown(["Male", "Female", "Other"], label="Gender")
        height = gr.Number(value=170, label="Height (cm)")
        weight = gr.Number(value=70, label="Weight (kg)")

    activity = gr.Dropdown(
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
        label="Activity Level"
    )

    fitness_goal = gr.Dropdown(
        ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness", "Maintenance"],
        label="Fitness Goal"
    )

    dietary_preference = gr.Dropdown(
        ["Non-Vegetarian", "Vegetarian", "Vegan", "Pescatarian", "Keto", "Paleo"],
        label="Dietary Preference"
    )

    cultural_food = gr.Dropdown(
        ["South Asian", "Western", "Middle Eastern", "East Asian"],
        label="Cultural Food Habits"
    )

    budget = gr.Slider(2, 50, value=10, label="Daily Budget ($)")

    equipment = gr.CheckboxGroup(
        ["Bodyweight", "Dumbbells", "Barbell", "Resistance Bands", "Machines"],
        label="Available Equipment"
    )

    free_text = gr.Textbox(
        label="Preferences / Injuries",
        lines=2
    )

    output = gr.Markdown()

    generate_btn = gr.Button("🚀 Generate My Plan")

    generate_btn.click(
        compute_plan,
        inputs=[
            age, gender, height, weight,
            activity, fitness_goal,
            dietary_preference, cultural_food,
            budget, equipment, free_text
        ],
        outputs=output
    )


# ─────────────────────────────────────────────
# Launch App
# ─────────────────────────────────────────────
app.launch()
