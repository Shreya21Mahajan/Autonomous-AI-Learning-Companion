# 🔧 Install libraries
!pip install gradio pydantic

#  Imports
import math
import gradio as gr
from pydantic import BaseModel
from typing import List

# -------------------------------
#  DATA MODELS
# -------------------------------

class Topic(BaseModel):
    name: str
    subject: str
    difficulty: float
    importance: float
    last_studied: int
    accuracy: float
    time_spent: float

class StudentInput(BaseModel):
    exam_days_left: int
    daily_hours: float
    topics: List[Topic]

# -------------------------------
#  AI LOGIC
# -------------------------------

def retention_score(days):
    return math.exp(-0.3 * days)

def weakness_score(topic):
    retention = retention_score(topic.last_studied)
    return (1 - topic.accuracy) * topic.difficulty + (1 - retention)

def priority_score(topic):
    return weakness_score(topic) * topic.importance

#  Error tracking
error_log = []

def get_error_summary():
    summary = {}
    for e in error_log:
        summary[e["topic"]] = summary.get(e["topic"], 0) + 1
    return summary

def enhanced_priority(topic):
    return priority_score(topic) + (0.5 * get_error_summary().get(topic.name, 0))

#  Memory tracking
def show_memory(topics):
    return [{
        "name": t.name,
        "retention": round(retention_score(t.last_studied), 2),
        "accuracy": t.accuracy
    } for t in topics]

#  Alerts
def smart_revision_alerts(topics):
    alerts = []
    for t in topics:
        if retention_score(t.last_studied) < 0.6:
            alerts.append({
                "topic": t.name,
                "priority": round(enhanced_priority(t), 2)
            })
    return sorted(alerts, key=lambda x: x["priority"], reverse=True)

#  Plan
def generate_plan(topics, daily_hours):
    topics_sorted = sorted(topics, key=lambda x: enhanced_priority(x), reverse=True)
    plan = []
    remaining = daily_hours

    for t in topics_sorted:
        if remaining <= 0:
            break
        time_alloc = min(1.5, remaining)
        plan.append({"topic": t.name, "hours": time_alloc})
        remaining -= time_alloc

    return plan

#  Exam mode
def exam_mode_plan(topics, daily_hours, exam_days_left):
    if exam_days_left > 7:
        return generate_plan(topics, daily_hours)

    topics = sorted(topics, key=lambda x: enhanced_priority(x), reverse=True)
    return [{"topic": t.name, "hours": min(2, daily_hours), "type": "REVISION"} for t in topics[:3]]

#  Score
def overall_memory_score(topics):
    scores = [retention_score(t.last_studied) for t in topics]
    return round(sum(scores) / len(scores), 2)

# -------------------------------
#  USER INPUT (MULTIPLE TOPICS)
# -------------------------------

def process_user_input(exam_days, daily_hours, topics_text):

    topic_names = topics_text.split("\n")
    topics = []

    for i, name in enumerate(topic_names):
        if name.strip() == "":
            continue

        topics.append(
            Topic(
                name=name.strip(),
                subject="General",
                difficulty=3 + (i % 2),
                importance=4 + (i % 2),
                last_studied=2 + i,
                accuracy=0.5,
                time_spent=2
            )
        )

    return StudentInput(
        exam_days_left=int(exam_days),
        daily_hours=float(daily_hours),
        topics=topics
    )

# -------------------------------
#  DASHBOARD UI
# -------------------------------

def dashboard_ui(exam_days, daily_hours, topics_text):

    student = process_user_input(exam_days, daily_hours, topics_text)

    memory = show_memory(student.topics)
    alerts = smart_revision_alerts(student.topics)
    plan = exam_mode_plan(student.topics, student.daily_hours, student.exam_days_left)

    score = overall_memory_score(student.topics)

    html = f"<h2> Memory Score: {score*100}%</h2>"
    html += "<h3> Focus: Weak topics prioritized</h3>"

    #  Memory
    html += "<h2> Memory Status</h2>"
    for m in memory:
        status = "🟢 Strong" if m['retention'] > 0.7 else "🔴 Weak"
        html += f"""
        <div>
        <b>{m['name']}</b> ({status})<br>
        Retention: {m['retention']} | Accuracy: {m['accuracy']}<br>
        <progress value="{m['retention']}" max="1" style="width:100%"></progress>
        </div><br>
        """

    #  Alerts
    html += "<h2>🚨 Alerts</h2>"
    for a in alerts:
        html += f"""
        <div style="background:red; color:white; padding:10px;">
        {a['topic']} → Priority: {a['priority']} <br>
        Reason: Low retention / High errors
        </div><br>
        """

    #  Plan
    html += "<h2>📅 Study Plan</h2>"
    for p in plan:
        type_label = "🔁 Revision" if p.get("type") == "REVISION" else "📖 Study"
        html += f"""
        <div style="background:green; color:white; padding:10px;">
        {p['topic']} → {p['hours']} hrs ({type_label})
        </div><br>
        """

    return html

# -------------------------------
#  LAUNCH APP
# -------------------------------

iface = gr.Interface(
    fn=dashboard_ui,
    inputs=[
        gr.Number(label="📅 Days Left"),
        gr.Number(label="⏳ Study Hours"),
        gr.Textbox(
            label="📚 Enter Topics (one per line)",
            lines=6,
            placeholder="Human Physiology\nThermodynamics\nOrganic Chemistry"
        )
    ],
    outputs="html",
    title="🧠 NEET AI Smart Planner",
    description="Enter multiple topics to get AI study plan"
)

iface.launch(share=True)
