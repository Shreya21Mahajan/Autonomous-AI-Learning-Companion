import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

# ===============================
# INIT
# ===============================
st.set_page_config(layout="wide")

if "concepts_db" not in st.session_state:
    st.session_state.concepts_db = {}

def today():
    return datetime.now()

# ===============================
# SPACED REPETITION LOGIC
# ===============================
def next_revision_days(conf):
    if conf < 0.3: return 1
    elif conf < 0.6: return 3
    elif conf < 0.8: return 7
    else: return 15

def add_concept(name, subject, connections):
    st.session_state.concepts_db[name] = {
        "subject": subject,
        "confidence": 0.5,
        "last_reviewed": None,
        "next_review": today(),
        "connections": connections,
        "history": []
    }

def update_concept(name, correct, time_taken):
    c = st.session_state.concepts_db[name]
    conf = c["confidence"]

    if correct:
        conf += 0.15 if time_taken < 10 else 0.05
    else:
        conf -= 0.2

    conf = max(0, min(1, conf))
    c["confidence"] = conf
    c["last_reviewed"] = today()
    c["next_review"] = today() + timedelta(days=next_revision_days(conf))
    c["history"].append(conf)

# ===============================
# 📉 FORGETTING CURVE GRAPH
# ===============================
def plot_forgetting_curve():
    t = np.linspace(0, 10, 100)
    retention = np.exp(-0.5 * t)

    fig, ax = plt.subplots()
    ax.plot(t, retention)
    ax.set_title("Forgetting Curve")
    ax.set_xlabel("Days")
    ax.set_ylabel("Retention")
    ax.grid()

    return fig

# ===============================
# 🎯 DASHBOARD UI
# ===============================
st.title("🧠 AI Spaced Repetition Dashboard")

# 📊 Metrics
col1, col2, col3 = st.columns(3)

total = len(st.session_state.concepts_db)
weak = sum(1 for c in st.session_state.concepts_db.values() if c["confidence"] < 0.4)
strong = sum(1 for c in st.session_state.concepts_db.values() if c["confidence"] > 0.75)

col1.metric("Total Concepts", total)
col2.metric("Weak Concepts", weak)
col3.metric("Strong Concepts", strong)

# ===============================
# ➕ ADD CONCEPT (SIDEBAR)
# ===============================
st.sidebar.header("➕ Add Concept")

name = st.sidebar.text_input("Concept")
subject = st.sidebar.selectbox("Subject", ["Biology", "Physics", "Chemistry"])
connections = st.sidebar.text_input("Connections (comma separated)")

if st.sidebar.button("Add"):
    add_concept(name, subject, connections.split(","))
    st.sidebar.success("Added!")

# ===============================
# 🎮 PRACTICE SIMULATOR
# ===============================
st.header("🎮 Practice Simulator")

if st.session_state.concepts_db:
    selected = st.selectbox("Select Concept", list(st.session_state.concepts_db.keys()))
    correct = st.radio("Correct?", ["Yes", "No"]) == "Yes"
    time_taken = st.slider("Time Taken", 1, 30, 10)

    if st.button("Submit"):
        update_concept(selected, correct, time_taken)
        st.success("Updated!")

# ===============================
# 🚨 AI COACH
# ===============================
st.header("🚨 AI Coach Insights")

for name, c in st.session_state.concepts_db.items():
    if c["confidence"] < 0.4:
        st.error(f"Focus NOW: {name}")
    elif c["confidence"] > 0.8:
        st.info(f"You're strong in: {name}")

# ===============================
# 📅 TODAY TASKS
# ===============================
st.header("📅 Today's Tasks")

for name, c in st.session_state.concepts_db.items():
    if c["next_review"] <= today():
        st.warning(f"{name} → Revise NOW!")

# ===============================
# ⏳ FORGETTING PREDICTION
# ===============================
st.header("⏳ Forgetting Prediction")

for name, c in st.session_state.concepts_db.items():
    time_left = c["next_review"] - today()
    hours = int(time_left.total_seconds() / 3600)

    if hours > 0:
        st.write(f"{name}: {hours} hrs left")

# ===============================
# 📉 FORGETTING CURVE
# ===============================
st.header("📉 Forgetting Curve")

fig = plot_forgetting_curve()
st.pyplot(fig)

# ===============================
# 📈 LEARNING TREND
# ===============================
st.header("📈 Learning Trend")

for name, c in st.session_state.concepts_db.items():
    if c["history"]:
        st.write(f"### {name}")
        st.line_chart(c["history"])
