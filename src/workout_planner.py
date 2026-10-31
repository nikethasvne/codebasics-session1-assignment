import os

from dotenv import load_dotenv
import streamlit as st
from groq import Groq


load_dotenv()

st.write("Welcome to the Workout Planner!")
name = st.text_input("Enter your name")
age = st.number_input("Enter your age")
weight = st.number_input("Enter your weight")

height = st.text_input("Enter your height in feet and inches")


gender = st.selectbox("Select your gender", ["Male", "Female"])
activity_level = st.selectbox("Select your activity level", ["Sedentary", "Lightly active", "Moderately active", "Very active"])
goal = st.selectbox("Select your goal", ["Build muscle", "Lose fat", "General fitness", "Improve endurance"])
time_frame = st.selectbox("Select your time frame", ["1 week", "2 weeks", "3 weeks", "4 weeks"])
equipment = st.selectbox("Select your equipment", ["No equipment", "Home dumbbells", "Full gym"])
location = st.selectbox("Select your location", ["Home", "Gym"])
days_available = st.slider("Select the number of days you are available to workout", 1, 7, 3)   
#instead of using st.selectbox, use st.multiselect for equipment_access
#equipment_access = st.multiselect("Select your equipment access", ["No equipment", "Home dumbbells", "Full gym"])   
injuries_or_limitations = st.text_input("Enter your injuries or limitations")

#print the name and age
#comment out the print statements
#st.write(f"Hello, {name}! You are {age} years old.")
#st.write(f"You are {weight} pounds and {height} inches tall.")
#st.write(f"You are {gender} and your activity level is {activity_level}.")
#st.write(f"Your goal is {goal} and your time frame is {time_frame}.")
#st.write(f"You are using {equipment} and your location is {location}.")
#st.write(f"You are available to workout {days_available} days a week.")
#st.write(f"You have access to {equipment_access}.")
#st.write(f"You have {injuries_or_limitations}.")

#generate the input for the groq api
input = f"Generate a workout plan for {name} who is {age} years old, {weight} pounds, {height} inches tall, {gender}, {activity_level}, {goal}, {time_frame}, {equipment}, {location}, {days_available}, {injuries_or_limitations}"

def generate_workout_plan(name, age, weight, height, gender, activity_level, goal, time_frame, equipment, location, days_available, injuries_or_limitations):
    #call the groq api to generate a workout plan
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise Exception("Missing GROQ_API_KEY in environment")

    client = Groq()
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a workout planner."},
            {"role": "user", "content": input},
        ],
        temperature=0.8,
        max_tokens=5000,
    )

    workout_plan = completion.choices[0].message.content
    if not workout_plan:
        raise Exception("No workout plan generated")

    return workout_plan.strip()

if st.button("Generate Workout Plan"):
    st.write(generate_workout_plan(name, age, weight, height, gender, activity_level, goal, time_frame, equipment, location, days_available, injuries_or_limitations))