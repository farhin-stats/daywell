import streamlit as st
import pandas as pd
from datetime import date
import requests

if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    st.title("👋 What's your name?")
    name = st.text_input("")
    if st.button("Next →"):
        st.session_state.name = name
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.title("💧 How many glasses of water today?")
    water = st.slider("", 0, 15, 8)
    if st.button("Next →"):
        st.session_state.water = water
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.title("😴 How many hours did you sleep?")
    sleep = st.slider("", 0, 12, 7)
    if st.button("Next →"):
        st.session_state.sleep = sleep
        st.session_state.step = 4
        st.rerun()

elif st.session_state.step == 4:
    st.title("🏃 Did you exercise today?")
    exercise = st.radio("", ["Yes", "No"])
    if st.button("Next →"):
        st.session_state.exercise = exercise
        st.session_state.step = 5
        st.rerun()

elif st.session_state.step == 5:
    st.title("😊 What's your mood today?")
    mood = st.slider("", 1, 5, 3)
    if st.button("Next →"):
        st.session_state.mood = mood
        st.session_state.step = 6
        st.rerun()

        

elif st.session_state.step == 6:
    st.title("🍽️ What did you eat today?")
    st.write("Add your meals one by one.")
    
    if "total_calories" not in st.session_state:
        st.session_state.total_calories = 0
    if "meals_logged" not in st.session_state:
        st.session_state.meals_logged = []
    
    food = st.text_input("Enter a food item")
    
    if st.button("Add Meal"):
        api_key = "bdrtPbLpSLadcCQH4OYgsVSNHviouVBI8HkxPzZ7"
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food}&api_key={api_key}"
        response = requests.get(url)
        data = response.json()
        calories = data["foods"][0]["foodNutrients"][0]["value"]
        st.session_state.total_calories += calories
        st.session_state.meals_logged.append(f"{food} - {round(calories)} cal")
        st.rerun()
    
    if st.session_state.meals_logged:
        st.write("**Meals logged:**")
        for meal in st.session_state.meals_logged:
            st.write(f"✅ {meal}")
        st.write(f"**Total: {round(st.session_state.total_calories)} calories**")
    
    if st.button("Done with meals →"):
        if st.session_state.total_calories < 1200:
            diet_message = "Light day - make sure you're eating enough."
        elif st.session_state.total_calories < 2200:
            diet_message = "Balanced day - well done!"
        else:
            diet_message = "Heavy day - try lighter meals tomorrow."
        st.session_state.diet_message = diet_message
        st.session_state.step = 7
        st.rerun()

elif st.session_state.step == 7:
    import pandas as pd
    from datetime import date
    today = str(date.today())
    data = {
        "date": [today],
        "name": [st.session_state.name.strip().capitalize()],
        "water": [st.session_state.water],
        "sleep": [st.session_state.sleep],
        "exercise": [st.session_state.exercise],
        "mood": [st.session_state.mood],
        "calories": [round(st.session_state.total_calories)],
        "diet_message": [st.session_state.diet_message]
    }
    df = pd.DataFrame(data)
    df.to_csv("health_log.csv", mode="a", header=False, index=False)
    st.title("🎉 All done!")
    st.success("Your day has been logged. See you tomorrow!")
    st.info(st.session_state.diet_message)
    st.balloons()
    if st.button("Start Over"):
        st.session_state.step = 1
        st.session_state.total_calories = 0
        st.session_state.meals_logged = []
        st.rerun()


        
