!pip install fastapi nest-asyncio uvicorn
from pydantic import BaseModel
from typing import List

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
  import math

# 📉 Forgetting curve (retention)
def retention_score(days):
    return math.exp(-0.3 * days)

# 🎯 Weakness calculation
def weakness_score(topic):
    retention = retention_score(topic.last_studied)
    return (1 - topic.accuracy) * topic.difficulty + (1 - retention)

# 🔥 Priority score
def priority_score(topic):
    return weakness_score(topic) * topic.importance

# 📅 Generate study plan
def generate_plan(topics, daily_hours):
    topics_sorted = sorted(topics, key=lambda x: priority_score(x), reverse=True)

    plan = []
    remaining = daily_hours

    for topic in topics_sorted:
        if remaining <= 0:
            break

        time_alloc = min(1.5, remaining)

        plan.append({
            "topic": topic.name,
            "subject": topic.subject,
            "hours": round(time_alloc, 2),
            "priority": round(priority_score(topic), 2)
        })

        remaining -= time_alloc

    return plan
  sample_data = {
    "exam_days_left": 30,
    "daily_hours": 5,
    "topics": [
        {
            "name": "Human Physiology",
            "subject": "Biology",
            "difficulty": 4,
            "importance": 5,
            "last_studied": 3,
            "accuracy": 0.5,
            "time_spent": 2
        },
        {
            "name": "Thermodynamics",
            "subject": "Physics",
            "difficulty": 5,
            "importance": 4,
            "last_studied": 5,
            "accuracy": 0.4,
            "time_spent": 3
        }
    ]
}

student = StudentInput(**sample_data)

plan = generate_plan(student.topics, student.daily_hours)

plan
# 🧠 Add memory tracking to each topic

def get_topic_state(topic):
    return {
        "name": topic.name,
        "subject": topic.subject,
        "retention": round(retention_score(topic.last_studied), 2),
        "accuracy": topic.accuracy
    }

# Show memory state
def show_memory(topics):
    return [get_topic_state(t) for t in topics]
  show_memory(student.topics)
# 📊 Error log system
error_log = []

def log_error(topic_name, error_type):
    error_log.append({
        "topic": topic_name,
        "error_type": error_type
    })

def get_error_summary():
    summary = {}
    for e in error_log:
        summary[e["topic"]] = summary.get(e["topic"], 0) + 1
    return summary
  log_error("Human Physiology", "conceptual")
log_error("Human Physiology", "silly")
log_error("Thermodynamics", "conceptual")

get_error_summary()
# 🔄 Update after quiz (auto-rebalancing)

def update_after_quiz(topic, new_accuracy):
    # Update accuracy
    topic.accuracy = (topic.accuracy + new_accuracy) / 2

    # Reset study time (just revised)
    topic.last_studied = 0

    return topic
  # Simulate poor performance
student.topics[0] = update_after_quiz(student.topics[0], 0.3)

# Generate new plan
new_plan = generate_plan(student.topics, student.daily_hours)

new_plan
def enhanced_priority(topic):
    error_count = get_error_summary().get(topic.name, 0)
    base_priority = priority_score(topic)

    return base_priority + (0.5 * error_count)
  topics_sorted = sorted(student.topics, key=lambda x: enhanced_priority(x), reverse=True)

for t in topics_sorted:
    print(t.name, enhanced_priority(t))
  # 🚨 Identify topics that need urgent revision

def get_revision_alerts(topics, threshold=0.5):
    alerts = []

    for topic in topics:
        retention = retention_score(topic.last_studied)

        if retention < threshold:
            alerts.append({
                "topic": topic.name,
                "subject": topic.subject,
                "retention": round(retention, 2),
                "message": f"⚠️ Revise {topic.name} now!"
            })

    return alerts
  alerts = get_revision_alerts(student.topics)
alerts
def smart_revision_alerts(topics):
    alerts = []

    for topic in topics:
        retention = retention_score(topic.last_studied)
        errors = get_error_summary().get(topic.name, 0)

        if retention < 0.6 or errors > 1:
            alerts.append({
                "topic": topic.name,
                "priority": round(enhanced_priority(topic), 2),
                "reason": "Low retention or high errors"
            })

    # Sort alerts by priority
    alerts = sorted(alerts, key=lambda x: x["priority"], reverse=True)

    return alerts
  smart_revision_alerts(student.topics)
final_plan = generate_plan(student.topics, student.daily_hours)
alerts = smart_revision_alerts(student.topics)

print("📅 DAILY PLAN:")
for p in final_plan:
    print(p)

print("\n🚨 REVISION ALERTS:")
for a in alerts:
    print(a)
  # 🎯 NEET Exam Mode (Last days strategy)

def exam_mode_plan(topics, daily_hours, exam_days_left):
    if exam_days_left > 7:
        return generate_plan(topics, daily_hours)

    # Only high importance + weak topics
    filtered = []

    for t in topics:
        if t.importance >= 4 or enhanced_priority(t) > 3:
            filtered.append(t)

    # Sort by priority
    filtered = sorted(filtered, key=lambda x: enhanced_priority(x), reverse=True)

    plan = []
    remaining = daily_hours

    for t in filtered:
        if remaining <= 0:
            break

        time_alloc = min(2, remaining)

        plan.append({
            "topic": t.name,
            "type": "REVISION",
            "hours": time_alloc
        })

        remaining -= time_alloc

    return plan
  exam_mode_plan(student.topics, 5, exam_days_left=5)
def final_ai_system(student):
    print("📊 MEMORY STATUS:")
    for m in show_memory(student.topics):
        print(m)

    print("\n🚨 ALERTS:")
    alerts = smart_revision_alerts(student.topics)
    for a in alerts:
        print(a)

    print("\n📅 STUDY PLAN:")
    plan = exam_mode_plan(student.topics, student.daily_hours, student.exam_days_left)
    for p in plan:
        print(p)
      final_ai_system(student)
!pip install gradio
import gradio as gr
def dashboard():
    memory = show_memory(student.topics)
    alerts = smart_revision_alerts(student.topics)
    plan = exam_mode_plan(student.topics, student.daily_hours, student.exam_days_left)

    memory_text = "📊 MEMORY STATUS\n"
    for m in memory:
        memory_text += f"{m['name']} → Retention: {m['retention']}\n"

    alerts_text = "\n🚨 ALERTS\n"
    for a in alerts:
        alerts_text += f"{a['topic']} → Priority: {a['priority']}\n"

    plan_text = "\n📅 STUDY PLAN\n"
    for p in plan:
        plan_text += f"{p['topic']} ({p.get('type','Study')}) → {p['hours']} hrs\n"
    return memory_text + alerts_text + plan_text
def simulate_error():
    log_error("Human Physiology", "conceptual")
    return dashboard()
import gradio as gr

def dashboard_ui():
    memory = show_memory(student.topics)
    alerts = smart_revision_alerts(student.topics)
    plan = exam_mode_plan(student.topics, student.daily_hours, student.exam_days_left)

    # 📊 MEMORY SECTION (with color)
    memory_html = "<h2>📊 Memory Status</h2>"
    for m in memory:
        color = "green" if m['retention'] > 0.7 else "orange" if m['retention'] > 0.4 else "red"
        memory_html += f"""
        <div style="padding:10px; margin:5px; border-radius:10px; background:{color}; color:white;">
        {m['name']} → Retention: {m['retention']}
        </div>
        """

    # 🚨 ALERT SECTION
    alert_html = "<h2>🚨 Alerts</h2>"
    for a in alerts:
        alert_html += f"""
        <div style="padding:10px; margin:5px; border-radius:10px; background:#ff4d4d; color:white;">
        {a['topic']} → Priority: {a['priority']}
        </div>
        """

    # 📅 PLAN SECTION
    plan_html = "<h2>📅 Study Plan</h2>"
    for p in plan:
        plan_html += f"""
        <div style="padding:10px; margin:5px; border-radius:10px; background:#4CAF50; color:white;">
        {p['topic']} → {p['hours']} hrs
        </div>
        """

    return memory_html + alert_html + plan_html
memory = show_memory(student.topics)

memory_html = "<h2>📊 Memory Status</h2>"

for m in memory:
    memory_html += f"""
    <div style="margin:10px;">
    <b>{m['name']}</b><br>
    <progress value="{m['retention']}" max="1" style="width:100%"></progress>
    </div>
    """
    import matplotlib.pyplot as plt

def plot_retention(topics):
    names = [t.name for t in topics]
    values = [retention_score(t.last_studied) for t in topics]

    plt.figure()
    plt.bar(names, values)
    plt.title("Retention Levels")
    plt.xlabel("Topics")
    plt.ylabel("Retention")
    plt.ylim(0, 1)
    plt.show()
    def overall_memory_score(topics):
    scores = [retention_score(t.last_studied) for t in topics]
    return round(sum(scores) / len(scores), 2)
    score = overall_memory_score(student.topics)
    score_html = f"<h2>🧠 Overall Memory Score: {score * 100}%</h2>"
    def dashboard_ui():

    memory = show_memory(student.topics)
    alerts = smart_revision_alerts(student.topics)
    plan = exam_mode_plan(student.topics, student.daily_hours, student.exam_days_left)

    # 🧠 Score
    score = overall_memory_score(student.topics)
    score_html = f"<h2>🧠 Overall Memory Score: {score * 100}%</h2>"

    # 📊 Memory
    memory_html = "<h2>📊 Memory Status</h2>"
    for m in memory:
        memory_html += f"""
        <div style="margin:10px;">
        <b>{m['name']}</b><br>
        Retention: {m['retention']} | Accuracy: {m['accuracy']}<br>
        <progress value="{m['retention']}" max="1" style="width:100%"></progress>
        </div>
        """

    # 🚨 Alerts
    alert_html = "<h2>🚨 Alerts</h2>"
    for a in alerts:
        alert_html += f"""
        <div style="padding:10px; background:red; color:white; margin:5px;">
        {a['topic']} → Priority: {a['priority']}
        </div>
        """

    # 📅 Plan
    plan_html = "<h2>📅 Study Plan</h2>"
    for p in plan:
        plan_html += f"""
        <div style="padding:10px; background:green; color:white; margin:5px;">
        {p['topic']} → {p['hours']} hrs
        </div>
        """

    return score_html + memory_html + alert_html + plan_html
  dashboard_ui()
  def function():
    return something
    dashboard_ui()
    import gradio as gr

def dashboard_ui():

    memory = show_memory(student.topics)
    alerts = smart_revision_alerts(student.topics)
    plan = exam_mode_plan(student.topics, student.daily_hours, student.exam_days_left)

    # 🧠 Overall Score
    score = overall_memory_score(student.topics)
    score_html = f"""
    <h2>🧠 Overall Memory Score: {score * 100}%</h2>
    <h3>🎯 Focus: Weak topics prioritized for maximum retention</h3>
    """

    # 📊 Memory Section
    memory_html = "<h2>📊 Memory Status</h2>"
    for m in memory:
        status = "🟢 Strong" if m['retention'] > 0.7 else "🟠 Medium" if m['retention'] > 0.4 else "🔴 Weak"

        memory_html += f"""
        <div style="margin:10px;">
        <b>{m['name']}</b> ({status})<br>
        Retention: {m['retention']} | Accuracy: {m['accuracy']}<br>
        <progress value="{m['retention']}" max="1" style="width:100%"></progress>
        </div>
        """

    # 🚨 Alerts Section
    alert_html = "<h2>🚨 Alerts</h2>"
    for a in alerts:
        alert_html += f"""
        <div style="padding:10px; background:red; color:white; margin:5px;">
        {a['topic']} → Priority: {a['priority']} <br>
        Reason: Low retention / High errors
        </div>
        """

    # 📅 Study Plan Section
    plan_html = "<h2>📅 Study Plan</h2>"
    for p in plan:
        type_label = "🔁 Revision" if p.get("type") == "REVISION" else "📖 Study"

        plan_html += f"""
        <div style="padding:10px; background:green; color:white; margin:5px;">
        {p['topic']} → {p['hours']} hrs ({type_label})
        </div>
        """

    return score_html + memory_html + alert_html + plan_html


# 🚀 Launch Dashboard
iface = gr.Interface(
    fn=dashboard_ui,
    inputs=[],
    outputs="html",
    title="🧠 NEET AI Dashboard",
    description="AI-powered retention-based study planner"
)

iface.launch(share=True)
    
