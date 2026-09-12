import re
from typing import List

import ollama
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Tamil Nadu Vegetarian Meal Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f8fafc 0%,
        #eef7f1 50%,
        #f0fdf4 100%
    );
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main title */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #166534;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #64748b;
    margin-bottom: 30px;
}

/* Section headers */
.section-header {
    font-size: 24px;
    font-weight: 750;
    color: #166534;
    margin-top: 20px;
    margin-bottom: 15px;
}

/* Cards */
.card-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 24px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
}

/* Metrics */
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e2e8f0;
    padding: 15px;
    border-radius: 14px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    width: 100%;
    min-height: 50px;
    border-radius: 12px;
    font-weight: 700;
}

/* Tables */
[data-testid="stMarkdownContainer"] table {
    width: 100%;
    border-collapse: collapse;
}

[data-testid="stMarkdownContainer"] th {
    background-color: #166534;
    color: white;
    padding: 10px;
    text-align: left;
}

[data-testid="stMarkdownContainer"] td {
    padding: 10px;
    border: 1px solid #dbe4df;
    vertical-align: top;
}

[data-testid="stMarkdownContainer"] tr:nth-child(even) {
    background-color: #f8fafc;
}

/* Disclaimer */
.disclaimer {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 14px;
    padding: 18px;
    color: #7c2d12;
    line-height: 1.6;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = None

if "generation_error" not in st.session_state:
    st.session_state.generation_error = None

if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = {}

if "generated" not in st.session_state:
    st.session_state.generated = False


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🥗 AI Tamil Nadu Vegetarian Meal Planner</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Your personalized 7-day vegetarian meal plan for healthy and sustainable weight management.</div>',
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate BMI."""

    if height_cm <= 0:
        return 0.0

    height_m = height_cm / 100

    return weight_kg / (height_m ** 2)


def split_food_list(value: str) -> List[str]:
    """Convert comma/semicolon/newline separated foods into a list."""

    if not value:
        return []

    if value.strip().lower() in {
        "none",
        "no",
        "nil",
        "n/a",
        "not applicable",
    }:
        return []

    items = re.split(r"[,;\n]+", value)

    return [
        item.strip().lower()
        for item in items
        if item.strip()
    ]


def clean_ai_output(text: str) -> str:
    """
    Clean formatting returned by Ollama.
    """

    if not text:
        return ""

    text = text.strip()

    # Remove code fences
    text = re.sub(
        r"```(?:markdown|md|text)?",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = text.replace("```", "")

    # Remove accidental HTML tags that Ollama may return
    text = re.sub(
        r"</?(?:html|body|markdown|response)>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return text.strip()


def find_restricted_foods(
    meal_plan: str,
    allergies: str,
    disliked_foods: str,
) -> List[str]:

    plan_lower = meal_plan.lower()

    found = []

    allergy_items = split_food_list(allergies)
    disliked_items = split_food_list(disliked_foods)

    for food in allergy_items:

        if food in plan_lower:
            found.append(
                f"Allergy: {food}"
            )

    for food in disliked_items:

        if food in plan_lower:
            found.append(
                f"Disliked: {food}"
            )

    return found


# ============================================================
# BUILD AI PROMPT
# ============================================================

def build_meal_plan_prompt(
    age: int,
    gender: str,
    height: float,
    weight: float,
    activity_level: str,
    food_preferences: str,
    food_allergies: str,
    disliked_foods: str,
    bmi: float,
) -> str:

    return f"""
Act as a Certified Nutritionist and Indian Vegetarian Meal Planner
specializing in South Indian and Tamil Nadu cuisine.

Create a practical and sustainable 7-day vegetarian meal plan
for healthy weight management.

USER INFORMATION

Age: {age} years
Gender: {gender}
Height: {height:.1f} cm
Weight: {weight:.1f} kg
Activity Level: {activity_level}
BMI: {bmi:.1f}

Food Preferences:
{food_preferences if food_preferences.strip() else "Not specified"}

Food Allergies:
{food_allergies if food_allergies.strip() else "None"}

Foods Disliked:
{disliked_foods if disliked_foods.strip() else "None"}


IMPORTANT RULES

1. The user follows a vegetarian diet.

2. NEVER include:
- Meat
- Chicken
- Fish
- Seafood
- Eggs

3. NEVER include foods listed under Food Allergies.

4. NEVER include foods listed under Foods Disliked.

5. Prefer Tamil Nadu and South Indian vegetarian foods.

6. Prefer practical foods available in Indian households.

7. Consider the user's activity level.

8. Include protein sources in major meals.

9. Include vegetables and fruits.

10. Include whole grains, millets, legumes, pulses,
    nuts and seeds where appropriate.

11. Limit deep-fried foods, sweets, sugary drinks,
    refined foods and excessive oil.

12. Do not recommend crash diets.

13. Do not recommend extreme calorie restriction.

14. Do not recommend skipping meals.

15. Do not diagnose medical conditions.


OUTPUT RULES

IMPORTANT:

Return ONLY normal Markdown.

DO NOT use HTML.

DO NOT use <p>, <div>, <h1>, <h2>, <table>,
or any other HTML tags.

DO NOT return Python code.

DO NOT wrap the response in triple backticks.

Use Markdown headings and Markdown tables.


## 1. 7-Day Meal Plan

Use exactly this table:

| Day | Early Morning | Breakfast | Mid-Morning | Lunch | Evening Snack | Dinner |
|---|---|---|---|---|---|---|
| Day 1 | ... | ... | ... | ... | ... | ... |
| Day 2 | ... | ... | ... | ... | ... | ... |
| Day 3 | ... | ... | ... | ... | ... | ... |
| Day 4 | ... | ... | ... | ... | ... | ... |
| Day 5 | ... | ... | ... | ... | ... | ... |
| Day 6 | ... | ... | ... | ... | ... | ... |
| Day 7 | ... | ... | ... | ... | ... | ... |


## 2. Daily Nutrition Guidance

Include:

- Approximate daily calorie range
- Protein-focused foods
- Fiber-rich foods
- Hydration guidance


## 3. Portion Guidance

Use:

- Cups
- Bowls
- Tablespoons
- Pieces
- Grams


## 4. Healthy Weight-Loss Tips

Provide 5-7 practical tips suitable for an Indian office worker.


## 5. Food Substitutions

Use:

| Instead of | Try |
|---|---|
| ... | ... |


## 6. Professional Disclaimer

State:

This meal plan provides general nutritional guidance and is not
a substitute for professional medical or dietary advice.


FINAL CHECK

Before responding verify:

- Exactly 7 days are present.
- All meal columns are present.
- No allergy food is included.
- No disliked food is included.
- No meat is included.
- No chicken is included.
- No fish is included.
- No seafood is included.
- No eggs are included.
- Meals are vegetarian.
- Meals are primarily Tamil Nadu / South Indian style.
- Meals are practical for an office worker.
"""


# ============================================================
# OLLAMA
# ============================================================

def generate_meal_plan(
    age: int,
    gender: str,
    height: float,
    weight: float,
    activity_level: str,
    food_preferences: str,
    food_allergies: str,
    disliked_foods: str,
) -> str:

    bmi = calculate_bmi(
        height,
        weight,
    )

    prompt = build_meal_plan_prompt(
        age=age,
        gender=gender,
        height=height,
        weight=weight,
        activity_level=activity_level,
        food_preferences=food_preferences,
        food_allergies=food_allergies,
        disliked_foods=disliked_foods,
        bmi=bmi,
    )

    model_name = "qwen2.5:0.5b"

    try:

        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": 0.3,
            },
        )

    except Exception as exc:

        raise RuntimeError(
            f"""
Unable to connect to Ollama.

Please check:

1. Ollama is installed.
2. Ollama is running.
3. The model '{model_name}' exists.

Run:

ollama list

If the model is missing:

ollama pull {model_name}

Original error:
{exc}
"""
        )

    if not response:

        raise RuntimeError(
            "Ollama returned an empty response."
        )

    message = response.get(
        "message",
        {},
    )

    result = message.get(
        "content",
        "",
    )

    if not result:

        raise RuntimeError(
            "Ollama returned an empty meal plan."
        )

    return clean_ai_output(result)


# ============================================================
# USER INPUT SECTION
# ============================================================

st.markdown(
    '<div class="card-box">',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-header">👤 Personal Information</div>',
    unsafe_allow_html=True,
)


with st.form("meal_planner_form"):

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=30,
            step=1,
        )

    with col2:

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other",
                "Prefer not to say",
            ],
        )


    col3, col4 = st.columns(2)

    with col3:

        height = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=250.0,
            value=165.0,
            step=0.5,
        )

    with col4:

        weight = st.number_input(
            "Weight (kg)",
            min_value=20.0,
            max_value=250.0,
            value=70.0,
            step=0.5,
        )


    activity_level = st.selectbox(
        "Activity Level",
        [
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
        ],
    )


    st.markdown(
        '<div class="section-header">🥗 Food Preferences</div>',
        unsafe_allow_html=True,
    )


    food_preferences = st.text_area(
        "Food Preferences",
        placeholder=(
            "Example: South Indian, high protein, "
            "millet-based"
        ),
        height=90,
    )


    food_allergies = st.text_area(
        "Food Allergies",
        placeholder=(
            "Example: Peanuts, dairy, none"
        ),
        height=90,
    )


    disliked_foods = st.text_area(
        "Foods Disliked",
        placeholder=(
            "Example: Bitter gourd, oats, none"
        ),
        height=90,
    )


    generate_clicked = st.form_submit_button(
        "🍽️ Generate My Meal Plan",
        use_container_width=True,
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# GENERATE
# ============================================================

if generate_clicked:

    st.session_state.generation_error = None

    if not 10 <= age <= 100:

        st.session_state.generation_error = (
            "Age must be between 10 and 100 years."
        )

    elif not 100 <= height <= 250:

        st.session_state.generation_error = (
            "Height must be between 100 and 250 cm."
        )

    elif not 20 <= weight <= 250:

        st.session_state.generation_error = (
            "Weight must be between 20 and 250 kg."
        )

    else:

        with st.spinner(
            "🥗 Creating your personalized meal plan..."
        ):

            try:

                plan = generate_meal_plan(
                    age=int(age),
                    gender=gender,
                    height=float(height),
                    weight=float(weight),
                    activity_level=activity_level,
                    food_preferences=food_preferences,
                    food_allergies=food_allergies,
                    disliked_foods=disliked_foods,
                )


                restricted_items = find_restricted_foods(
                    plan,
                    food_allergies,
                    disliked_foods,
                )


                if restricted_items:

                    st.session_state.generation_error = (
                        "⚠️ Warning: The generated plan contains "
                        "a term matching your allergy/dislike list. "
                        "Please review the plan carefully."
                    )


                st.session_state.meal_plan = plan

                st.session_state.last_inputs = {
                    "age": age,
                    "gender": gender,
                    "height": height,
                    "weight": weight,
                    "activity_level": activity_level,
                    "food_preferences": food_preferences,
                    "food_allergies": food_allergies,
                    "disliked_foods": disliked_foods,
                }

                st.session_state.generated = True

            except Exception as exc:

                st.session_state.generation_error = str(exc)


# ============================================================
# ERROR
# ============================================================

if st.session_state.generation_error:

    st.error(
        st.session_state.generation_error
    )


# ============================================================
# DISPLAY RESULT
# ============================================================

if st.session_state.meal_plan:

    data = st.session_state.last_inputs

    bmi = calculate_bmi(
        data["height"],
        data["weight"],
    )


    # ========================================================
    # PROFILE
    # ========================================================

    st.markdown(
        '<div class="section-header">📊 Your Profile Summary</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Age",
            f'{int(data["age"])} years',
        )

    with m2:

        st.metric(
            "Height",
            f'{data["height"]:.1f} cm',
        )

    with m3:

        st.metric(
            "Weight",
            f'{data["weight"]:.1f} kg',
        )

    with m4:

        st.metric(
            "Activity",
            data["activity_level"],
        )


    # ========================================================
    # MEAL PLAN
    # ========================================================

    st.markdown(
        '<div class="section-header">📅 Your 7-Day Meal Plan</div>',
        unsafe_allow_html=True,
    )

    # IMPORTANT:
    # This is pure Markdown.
    # No HTML is used for the AI response.

    st.markdown(
        st.session_state.meal_plan
    )


    # ========================================================
    # BMI
    # ========================================================

    st.markdown(
        '<div class="section-header">📈 BMI Information</div>',
        unsafe_allow_html=True,
    )

    st.info(
        f"Your calculated BMI is approximately **{bmi:.1f}**. "
        "BMI is provided for general context and should not "
        "be used as a standalone medical assessment."
    )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.markdown(
        '<div class="disclaimer">'
        '<strong>⚠️ Important Disclaimer</strong>'
        '<br><br>'
        'This meal plan provides general nutritional guidance '
        'and is not a substitute for professional medical or '
        'dietary advice.'
        '<br><br>'
        'If you have a medical condition, significant food '
        'allergies, are pregnant, take medication, or require '
        'therapeutic nutrition, consult a qualified healthcare '
        'professional or registered dietitian.'
        '</div>',
        unsafe_allow_html=True,
    )


    st.write("")


    # ========================================================
    # NEW PLAN
    # ========================================================

    if st.button(
        "🔄 Generate New Plan",
        use_container_width=True,
    ):

        st.session_state.meal_plan = None
        st.session_state.generation_error = None
        st.session_state.last_inputs = {}
        st.session_state.generated = False

        st.rerun()


else:

    st.info(
        "👆 Enter your details above and click "
        "**🍽️ Generate My Meal Plan** to create your "
        "personalized 7-day vegetarian meal plan."
    )