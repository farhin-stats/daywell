import streamlit as st 
import random
st.image("banner.jpg", width = 700)

st.title("🌿 DayWell")
st.subheader("Your daily health companion")
st.write("Track your habits. Understand Your patterns. Feel better every day.")

quotes = [
    "Take care of your body. It's the only place you have to live.",
    "Health is not about the weight you lose, but the life you gain.",
    "A healthy outside starts from the inside.",
    "Your body hears everything your mind says.",
    "Small daily improvements lead to stunning results."
]

 
st.info(random.choice(quotes))
st.button("Get Started →")


st.divider()
st.header("📋 Today's Log")

name = st.text_input("Your name")
water = st.slider("Glasses of water today", 0, 15,8)
sleep = st.slider("Hours of sleep last night", 0, 12,7)
exercise = st.radio("Did you exercise today?", ["Yes", "No"])
mood = st.slider("Your mood today (1-5)", 1, 5, 3)

if st.button("Save Today's Log"):
    import pandas as pd
    from datetime import date
    today = str(date.today())
    data = {
        "date": [today],
        "name": [name.strip().capitalize()],
        "water": [water],
        "sleep": [sleep],
        "exercise": [exercise],
        "mood": [mood],
        "calories": [0],
        "diet_message": ["not logged"]
    }
    df = pd.DataFrame(data)
    df.to_csv("health_log.csv", mode="a", header=False, index=False)
    st.success("✅ Today's log saved! See you tomorrow.")

st.divider()
st.header("📊 Your Weekly Stats")

import pandas as pd
df = pd.read_csv("health_log.csv",header=None,
     names =["date","name","water","sleep","exercise","mood","calories","diet_message"])

df = df.drop_duplicates(subset ="date", keep = "last")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💧 Avg Water", f"{round(df['water'].mean(),1)} glasses")
col2.metric("😴 Avg Sleep", f"{round(df['sleep'].mean(),1)} hrs")
col3.metric("🏃 Exercise Days", f"{df[df['exercise']=='Yes'].shape[0]}")
col4.metric("😊 Avg Mood", f"{round(df['mood'].mean(),1)}/5")

st.subheader("💧 Water Intake This Week")

import matplotlib.pyplot as plt

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")


fig , ax = plt.subplots()
ax.bar(df["date"].astype(str),df["water"].astype(int),color ="skyblue")
ax.set_xlabel("Date")
ax.set_ylabel("Glasses")
ax.set_title("Daily Water Intake")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)