import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Your Weekly Dashboard")

df = pd.read_csv("health_log.csv", header=None,
    names=["date","name","water","sleep","exercise","mood","calories","diet_message"])

df = df.drop_duplicates(subset="date", keep="last")

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

streak = 1
for i in range (1,len(df)):
    diff = (df["date"].iloc[i]-df["date"].iloc[i-1]).days
    if diff == 1:
        streak += 1
    else:
        streak = 1

st.metric("🔥 Current Streak", f"{streak} days")
st.divider()
st.subheader("📅 This Week's Log")

from datetime import datetime, timedelta
today = datetime.today().date()
days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

logged_dates = df["date"].dt.date.tolist()

cols = st.columns(7)
for i, day in enumerate(days):
    if day in logged_dates:
        cols[i].markdown(f"✅\n\n**{day.strftime('%a')}**")
    else:
        cols[i].markdown(f"⬜\n\n**{day.strftime('%a')}**")

st.subheader("This Week's Stats")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💧 Avg Water", f"{round(df['water'].mean(),1)} glasses")
col2.metric("😴 Avg Sleep", f"{round(df['sleep'].mean(),1)} hrs")
col3.metric("🏃 Exercise Days", f"{df[df['exercise']=='Yes'].shape[0]}")
col4.metric("😊 Avg Mood", f"{round(df['mood'].mean(),1)}/5")

st.divider()

st.subheader("💧 Water Intake This Week")
fig, ax = plt.subplots()
ax.bar(df["date"].astype(str), df["water"].astype(int), color="#2eb2cc")
ax.set_xlabel("Date")
ax.set_ylabel("Glasses")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)



st.divider()

st.subheader("🍽️ Calories This Week")
fig2 , ax2 = plt.subplots()
ax2.bar(df["date"].astype(str), df["calories"].astype(float),color = "#e74c3c")
ax2.set_xlabel("Date")
ax2.set_ylabel("Calories")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)

avg_water = df["water"].mean()
avg_sleep = df["sleep"].mean()
exercise_days = df[df["exercise"]=="Yes"].shape[0]
total_days = df.shape[0]
avg_mood = df["mood"].mean()

summary = f"This week you averaged {round(avg_water,1)} glasses of water and {round(avg_sleep,1)} hours of sleep. "

if exercise_days >= total_days/2:
    summary += "You stayed active most days. "
else:
    summary += "Try to move a bit more next week. "

if avg_mood >= 4:
    summary += "Your mood was great overall!"
elif avg_mood >= 3:
    summary += "Your mood stayed fairly steady."
else:
    summary += "Your mood was a bit low - take care of yourself."

st.subheader("📝 Weekly Summary")
st.info(summary)



