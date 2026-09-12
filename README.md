# 🥗 AI Tamil Nadu Vegetarian Meal Planner

An AI-powered **7-Day Vegetarian Meal Planner** built with **Python, Streamlit, and Ollama**.

The application generates a personalized vegetarian meal plan based on the user's age, gender, height, weight, activity level, food preferences, food allergies, and disliked foods.

The generated plan focuses primarily on **Tamil Nadu and South Indian vegetarian cuisine** and is designed to provide practical guidance for healthy and sustainable weight management.

---

## 📌 Overview

The **AI Tamil Nadu Vegetarian Meal Planner** provides an interactive web interface where users can enter their personal and dietary information.

The application then:

* Calculates the user's BMI.
* Collects personal information.
* Collects food preferences.
* Collects food allergies.
* Collects disliked foods.
* Considers the user's activity level.
* Sends the information to a locally running Ollama AI model.
* Generates a personalized **7-day vegetarian meal plan**.
* Displays the meal plan in a clean Markdown table.
* Provides nutrition guidance.
* Provides portion guidance.
* Provides healthy weight-loss tips.
* Provides food substitutions.
* Displays BMI information.
* Keeps the generated meal plan visible after Streamlit reruns.

The application uses Streamlit's session state to retain the generated meal plan and user inputs.

---

## ✨ Features

### 👤 Personal Information

Users can provide:

* Age
* Gender
* Height in centimeters
* Weight in kilograms
* Activity level

The application validates the input ranges before generating the meal plan.

---

### 🥗 Food Preferences

Users can specify their preferred foods or dietary preferences.

Example:

```text
South Indian, high protein, millet-based
```

---

### ⚠️ Food Allergies

Users can provide foods they are allergic to.

Example:

```text
Peanuts, dairy
```

The AI prompt instructs the model not to include foods listed under the user's allergies.

---

### 🚫 Disliked Foods

Users can enter foods they do not like.

Example:

```text
Bitter gourd, oats
```

The generated meal plan is instructed to avoid these foods.

---

### 📊 BMI Calculation

The application calculates BMI using:

```text
BMI = Weight (kg) / Height² (m)
```

The Python script converts height from centimeters to meters before performing the calculation.

The calculated BMI is displayed in the profile/results section.

> **Note:** BMI is provided only as general context and should not be considered a standalone medical assessment.

---

### 🤖 AI Meal Plan Generation

The application uses **Ollama** to generate the meal plan locally.

The configured model is:

```text
qwen2.5:0.5b
```

The application sends a structured prompt containing the user's information and dietary requirements to Ollama.

---

### 🍛 Tamil Nadu & South Indian Cuisine

The AI prompt specifically asks for practical vegetarian foods commonly available in Indian households and prefers Tamil Nadu and South Indian cuisine.

Examples of suitable meal styles include:

* Idli
* Dosa
* Pongal
* Sambar
* Rasam
* Vegetable poriyal
* Kootu
* Rice-based meals
* Millet-based meals
* Legumes and pulses
* Fruits
* Nuts and seeds

The exact meals are generated dynamically by the AI model.

---

## 🧠 AI Output Structure

The generated meal plan is requested in Markdown format and contains the following sections:

### 1. 7-Day Meal Plan

The application asks Ollama to generate a table containing:

| Day   | Early Morning | Breakfast | Mid-Morning | Lunch | Evening Snack | Dinner |
| ----- | ------------- | --------- | ----------- | ----- | ------------- | ------ |
| Day 1 | ...           | ...       | ...         | ...   | ...           | ...    |
| Day 2 | ...           | ...       | ...         | ...   | ...           | ...    |
| Day 3 | ...           | ...       | ...         | ...   | ...           | ...    |
| Day 4 | ...           | ...       | ...         | ...   | ...           | ...    |
| Day 5 | ...           | ...       | ...         | ...   | ...           | ...    |
| Day 6 | ...           | ...       | ...         | ...   | ...           | ...    |
| Day 7 | ...           | ...       | ...         | ...   | ...           | ...    |

The prompt explicitly requires exactly seven days and all meal columns.

---

### 2. Daily Nutrition Guidance

The AI is instructed to provide:

* Approximate daily calorie range
* Protein-focused foods
* Fiber-rich foods
* Hydration guidance

---

### 3. Portion Guidance

Portion recommendations can use:

* Cups
* Bowls
* Tablespoons
* Pieces
* Grams

---

### 4. Healthy Weight-Loss Tips

The generated response includes approximately **5–7 practical healthy weight-management tips** suitable for an Indian office worker.

---

### 5. Food Substitutions

The AI generates a substitution table such as:

| Instead of   | Try              |
| ------------ | ---------------- |
| Example food | Alternative food |
| Example food | Alternative food |

---

### 6. Professional Disclaimer

The generated meal plan includes a professional disclaimer explaining that the plan is general nutritional guidance and is not a replacement for professional medical or dietary advice.

---

## 🛠️ Technologies Used

| Technology        | Purpose                                |
| ----------------- | -------------------------------------- |
| **Python**        | Application development                |
| **Streamlit**     | Web-based user interface               |
| **Ollama**        | Local AI model execution               |
| **Qwen 2.5 0.5B** | Meal-plan generation                   |
| **Regex (`re`)**  | Text cleaning and food-list processing |
| **Session State** | Preserving generated results           |

---

## 📁 Project Structure

Recommended project structure:

```text
Meal_Planner/
│
├── Meal_Planner.py
├── requirements.txt
└── README.md
```

### File Description

| File               | Description                |
| ------------------ | -------------------------- |
| `Meal_Planner.py`  | Main Streamlit application |
| `requirements.txt` | Python dependencies        |
| `README.md`        | Project documentation      |

---

# ⚙️ Installation

## 1. Clone the Repository

Clone your GitHub repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Navigate into the project directory:

```bash
cd Meal_Planner
```

---

## 2. Create a Virtual Environment

It is recommended to use a Python virtual environment.

### Windows

```powershell
python -m venv venv
```

Activate the environment:

```powershell
venv\Scripts\activate
```

If PowerShell prevents script execution, you can use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate:

```powershell
venv\Scripts\activate
```

You should see something similar to:

```text
(venv) PS I:\Your_Project\Meal_Planner>
```

---

## 3. Install Python Dependencies

Install the required packages:

```powershell
pip install streamlit ollama
```

The application imports both `ollama` and `streamlit`.

You can also create a `requirements.txt` file containing:

```text
streamlit
ollama
```

Then install all dependencies using:

```powershell
pip install -r requirements.txt
```

---

# 🤖 Install Ollama

This application requires **Ollama** because the meal plan is generated using a locally running AI model.

Install Ollama on your system before running the application.

After installation, verify that Ollama is available:

```powershell
ollama --version
```

---

# 📦 Download the AI Model

The application is configured to use:

```text
qwen2.5:0.5b
```

Download the model using:

```powershell
ollama pull qwen2.5:0.5b
```

Verify that the model is installed:

```powershell
ollama list
```

You should see the model in the list.

Example:

```text
NAME
qwen2.5:0.5b
```

The Python application checks for this configured model when communicating with Ollama.

---

# ▶️ Running the Application

Make sure your virtual environment is activated.

From the project directory, run:

```powershell
streamlit run Meal_Planner.py
```

Streamlit will start the local web server.

You should see output similar to:

```text
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

Open the displayed URL in your browser.

---

# 🖥️ Application Workflow

The application follows this workflow:

```text
Start Application
       │
       ▼
Enter Personal Information
       │
       ▼
Enter Food Preferences
       │
       ▼
Enter Allergies
       │
       ▼
Enter Disliked Foods
       │
       ▼
Click "Generate My Meal Plan"
       │
       ▼
Calculate BMI
       │
       ▼
Build AI Prompt
       │
       ▼
Send Prompt to Ollama
       │
       ▼
Generate 7-Day Meal Plan
       │
       ▼
Display Results
       │
       ▼
Show BMI + Nutrition Guidance
```

---

# 📝 Input Example

You can enter information such as:

```text
Age: 30

Gender: Male

Height: 172 cm

Weight: 85 kg

Activity Level: Moderately Active

Food Preferences:
South Indian, high protein, millet-based

Food Allergies:
Peanuts

Foods Disliked:
Bitter gourd, oats
```

Then click:

```text
🍽️ Generate My Meal Plan
```

---

# 📊 Example Output

After successful generation, the application displays a profile summary similar to:

```text
📊 Your Profile Summary

Age       Height       Weight       Activity
30 years  172.0 cm     85.0 kg      Moderately Active
```

The application then displays:

```text
📅 Your 7-Day Meal Plan
```

Example structure:

| Day   | Early Morning | Breakfast       | Mid-Morning | Lunch                          | Evening Snack | Dinner                      |
| ----- | ------------- | --------------- | ----------- | ------------------------------ | ------------- | --------------------------- |
| Day 1 | Warm water    | Idli + Sambar   | Fruit       | Rice + Sambar + Poriyal        | Sundal        | Vegetable Dosa              |
| Day 2 | Herbal drink  | Vegetable Upma  | Fruit       | Millet Rice + Kootu            | Nuts          | Chapati + Vegetable Curry   |
| Day 3 | Warm water    | Pongal + Sambar | Fruit       | Rice + Rasam + Poriyal         | Sundal        | Idiyappam + Vegetable Curry |
| Day 4 | Warm water    | Dosa + Sambar   | Fruit       | Millet Rice + Dal + Vegetables | Fruit         | Chapati + Kootu             |
| Day 5 | Warm water    | Idli + Sambar   | Fruit       | Rice + Rasam + Vegetables      | Sundal        | Vegetable Adai              |
| Day 6 | Warm water    | Upma            | Fruit       | Rice + Kootu + Poriyal         | Nuts          | Dosa + Vegetable Sambar     |
| Day 7 | Warm water    | Pongal + Sambar | Fruit       | Millet Rice + Dal + Vegetables | Sundal        | Chapati + Vegetable Curry   |

> **Note:** The above table is only an example of the output structure. Actual meals are generated dynamically by the Ollama AI model.

---

# 📈 BMI Output

The application calculates and displays BMI based on the entered height and weight.

Example:

```text
📈 BMI Information

Your calculated BMI is approximately 28.7.
```

The BMI calculation is performed directly by the Python application.

---

# 🔄 Generate a New Meal Plan

After generating a meal plan, the application provides:

```text
🔄 Generate New Plan
```

Clicking this button clears the existing meal plan and allows a new plan to be generated.

---

# 💾 Session State

The application uses Streamlit session state to preserve important information such as:

* Generated meal plan
* Last submitted inputs
* Generation errors
* Generation status

This allows the generated result to remain available across Streamlit reruns.

---

# 🛡️ Food Restriction Validation

The application performs an additional check on the generated meal plan.

It searches the generated response for foods listed under:

* Food allergies
* Disliked foods

If a matching item is detected, the application displays a warning asking the user to review the generated plan.

> **Important:** This is a text-matching safety check, not a guarantee that every ingredient or derivative of an allergen has been detected.

---

# 🧹 AI Output Cleaning

The application includes a function that cleans the AI response before displaying it.

It removes:

* Markdown code fences
* Accidental HTML wrapper tags
* Unwanted formatting returned by the model

The final response is displayed using Streamlit's Markdown renderer.

---

# ⚠️ Troubleshooting

## Ollama Connection Error

If you see:

```text
Unable to connect to Ollama.
```

Check that:

1. Ollama is installed.
2. Ollama is running.
3. The required model is installed.

Run:

```powershell
ollama list
```

If the model is missing:

```powershell
ollama pull qwen2.5:0.5b
```

The application itself provides these troubleshooting instructions when Ollama communication fails.

---

## Model Not Found

If you receive a model-related error, verify:

```powershell
ollama list
```

Make sure the model name matches:

```text
qwen2.5:0.5b
```

If necessary:

```powershell
ollama pull qwen2.5:0.5b
```

---

## Streamlit Command Not Found

If PowerShell displays:

```text
streamlit : The term 'streamlit' is not recognized...
```

Make sure your virtual environment is activated:

```powershell
venv\Scripts\activate
```

Then install Streamlit:

```powershell
pip install streamlit
```

Verify:

```powershell
streamlit --version
```

Then run:

```powershell
streamlit run Meal_Planner.py
```

---

## Ollama Package Not Found

If Python reports:

```text
ModuleNotFoundError: No module named 'ollama'
```

Install the Python Ollama package:

```powershell
pip install ollama
```

---

# 🔐 Privacy

The application is designed around a **locally running Ollama model**.

The Python application sends the meal-planning prompt to the local Ollama service rather than requiring a cloud-based AI API key.

However, users should still avoid entering unnecessary sensitive personal information.

---

# ⚠️ Medical Disclaimer

This application is intended for **general educational and nutritional guidance only**.

The generated meal plan is **not a substitute for professional medical or dietary advice**.

The application itself includes a disclaimer recommending consultation with a qualified healthcare professional or registered dietitian for users with medical conditions, significant food allergies, pregnancy, medication use, or therapeutic nutrition requirements.

---

# 🚀 Future Improvements

Possible future enhancements include:

* 📅 Custom meal-plan duration
* 🎯 Custom weight-management goals
* 🧮 Estimated calorie requirements
* 💪 Detailed macro-nutrient calculations
* 🥘 More regional Indian cuisines
* 🛒 Automatic grocery-list generation
* 📥 Export meal plan to PDF
* 📊 Nutrition charts
* 💾 Save previous meal plans
* 🌐 Multi-language support
* 🔄 Regenerate individual meals
* 🍱 Meal-preparation suggestions

---

# 📌 Important Notes

* The application requires Python.
* Streamlit must be installed.
* Ollama must be installed and running.
* The `qwen2.5:0.5b` model must be available in Ollama.
* Low level model used for education and practical purpose, For better results use higher models.
* Internet access is not required for AI generation once Ollama and the model are installed locally.
* Generated meal plans should be reviewed carefully, especially when food allergies are involved.
* AI-generated nutritional information should not be treated as professional medical advice.
---

# 📜 License

This project is intended for educational and personal use.

You may modify and extend the project according to your requirements.

---

# 👨‍💻 Author

**Jaya Praveen K**

Built with:

```text
🐍 Python
🎈 Streamlit
🤖 Ollama
🥗 Qwen 2.5
```

---

## ⭐ If You Like This Project

If this project is useful, consider giving the GitHub repository a ⭐ **Star** and sharing it with others interested in Python, Streamlit, local AI, and nutrition applications.
