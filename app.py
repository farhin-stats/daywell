import streamlit as st
import random

st.image("banner.jpg", width=700)

st.title("🌿 DayWell")
st.subheader("Your daily health companion")
st.write("Track your habits. Understand your patterns. Feel better every day.")

quotes = [
    "Take care of your body. It's the only place you have to live.",
    "Health is not about the weight you lose, but the life you gain.",
    "A healthy outside starts from the inside.",
    "Your body hears everything your mind says.",
    "Small daily improvements lead to stunning results."
]

st.info(random.choice(quotes))

st.page_link("pages/1_Daily_Log.py", label="Get Started →")
