import json
import os

from dotenv import load_dotenv
import streamlit as st
from groq import AuthenticationError,Groq
import logging
import re

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_workout_plan(profile_json):
    #call the groq api to generate a workout plan
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("Missing GROQ_API_KEY in environment")
        st.write("Sorry, something went wrong. Please try again later.")
        return None

    client = Groq()
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    try:
        messages=[
                {"role": "system", "content": "You are a workout planner. Generate a practical workout plan from the user's JSON profile. Respect their injuries, equipment, location, experience, goal, and days available."},
                {"role": "user", "content": profile_json},
        ]
        st.write(messages)
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
            max_tokens=5000,
        )
    except AuthenticationError as e:
        st.write("Sorry, something went wrong. Please try again later.")
        logger.error(f"Invalid API Key: {e}")
        return None

    workout_plan = completion.choices[0].message.content
    if not workout_plan:
        logger.error("No workout plan generated")
        st.write("Sorry, something went wrong. Please try again later.")
        return None
    return workout_plan.strip()

def display_workout_planner():
    st.set_page_config(layout="wide")
    st.markdown("**Welcome to the Workout Planner!**")

    # Intake form for the user to fill out
    left, right = st.columns(2)
    with left:
        name = st.text_input("Enter your name")
        age = st.number_input("Enter your age")
        weight = st.number_input("Enter your weight")
        height = st.text_input("Enter your height in feet and inches", value="5'10\"")
        gender = st.selectbox("Select your gender", ["Male", "Female"])
        fitness_goal = st.selectbox("Select your fitness goal", ["Build muscle", "Lose fat", "General fitness", "Improve endurance"])
        experience_level = st.selectbox("Select your training experience", ["Beginner", "Intermediate", "Advanced"])
        activity_level = st.selectbox("Select your activity level", ["Sedentary", "Lightly active", "Moderately active", "Very active"])
        time_frame = st.selectbox("Select your time frame", ["1 week", "2 weeks", "3 weeks", "4 weeks"])
        location = st.selectbox("Select your location", ["Home", "Gym"])
        days_available = st.slider("Select the number of days available weekly to workout", 1, 7, 3)
        equipment_access = st.multiselect("Select your equipment access", ["No equipment", "Home dumbbells", "Full gym"])   
        injuries = st.multiselect("Enter your injuries or limitations", ["None", "bad knees", "backpain"])
        pressed = st.button("Generate Workout Plan")

    # --- Validation Checks ---
    errors = validate_inputs(name, age, weight, equipment_access, injuries)

    profile = {
        "name": name,
        "age": int(age),
        "weight": weight,
        "height": height,
        "gender": gender,
        "activity_level": activity_level,
        "experience_level": experience_level,
        "fitness_goal": fitness_goal,
        "time_frame": time_frame,
        "equipment_access": equipment_access,
        "location": location,
        "days_available": int(days_available),
        "injuries": injuries,
    }
    profile_json = json.dumps(profile)

    if pressed:
        with right:
            if errors:
                for err in errors:
                    st.error(err)
            else:
                plan = generate_workout_plan(profile_json)
                if plan:
                    st.write(f"<div style='border: 1px solid black; padding: 10px;'>{plan}</div>", unsafe_allow_html=True)
                else:
                    st.write("Sorry, something went wrong. Please try again later.")

def validate_inputs(name, age, weight, equipment_access, injuries):
    errors = []
    
    # Check name
    # Check if name is empty/whitespace
    if not name or not name.strip():
        errors.append("Please enter a valid name.")
    # Check if the name starts with an alphabet letter (A-Z or a-z)
    elif not re.match(r"^[A-Za-z]", name.strip()):
        errors.append("Name must start with an alphabet letter (cannot start with a number, space, or special character).")

    # Check age
    if age <= 0 or age > 120:
        errors.append("Please enter a realistic age between 1 and 120.")
        
    # Check weight
    if weight <= 0 or weight > 500:
        errors.append("Weight must be between 1 and 500 pounds.")

    # Check if equipment_access is empty/whitespace
    if not equipment_access:
        errors.append("Equipment access is required.")
    
    # Check if injuries is empty/whitespace
    if not injuries:
        errors.append("Provide your injuries or mention none")
        
    return errors

if __name__ == "__main__":
    display_workout_planner()