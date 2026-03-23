
# AI STUDY ASSISTANT

import gradio as gr
import math
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from difflib import get_close_matches
from gtts import gTTS
import tempfile

import spaced_repetition

# AI TUTOR (RAG)

documents = [
    "Photosynthesis is the process by which plants make food using sunlight.",
    "Mitochondria is the powerhouse of the cell.",
    "DNA carries genetic information.",
    "Force equals mass multiplied by acceleration.",
    "The pH of a neutral solution is 7."
]

model = SentenceTransformer('all-MiniLM-L6-v2')
doc_embeddings = model.encode(documents)

index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(np.array(doc_embeddings))

def retrieve(query):
    q_vec = model.encode([query])
    _, I = index.search(np.array(q_vec), k=2)
    return [documents[i] for i in I[0]]

def correct_query(query):
    keywords = ["photosynthesis", "mitochondria", "dna", "force", "ph"]
    match = get_close_matches(query.lower(), keywords, n=1)
    return match[0] if match else query

def generate_answer(query):
    query = correct_query(query)
    context = retrieve(query)

    if not context:
        return "Answer not found", None

    main = context[0]

    tts = gTTS(main)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp.name)

    answer = f"""
### Answer:
{main}

### Simple:
{main.lower()}
"""
    return answer, temp.name

# STUDY PLANNER

def retention_score(days):
    return math.exp(-0.3 * days)

def priority_score(topic):
    retention = retention_score(topic["last"])
    return (1 - topic["acc"]) * topic["diff"] + (1 - retention)

def generate_plan(topics, hours):
    topics = sorted(topics, key=priority_score, reverse=True)
    plan = []
    for t in topics:
        if hours <= 0:
            break
        h = min(1.5, hours)
        plan.append(f"{t['name']} → {h} hrs")
        hours -= h
    return plan

def planner_ui(days, hours, text):
    names = text.split("\n")
    topics = []

    for i, n in enumerate(names):
        if n.strip():
            topics.append({
                "name": n.strip(),
                "diff": 3 + i % 2,
                "acc": 0.5,
                "last": 2 + i
            })

    plan = generate_plan(topics, hours)
    return "\n".join(plan)

# SPACED REPETITION HELPERS

def update_fn(c, cor, t):
    return spaced_repetition.update_concept(c, cor == "Yes", t)

def graphs():
    return (
        spaced_repetition.plot_forgetting_curve(),
        spaced_repetition.plot_learning_trend()
    )

# UI DESIGN

with gr.Blocks(
    theme=gr.themes.Soft(),
    css="""
    body {background-color: #0f172a;}
    .gradio-container {max-width: 1100px; margin: auto;}

    #card {
        background: #1e293b;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    }

    textarea {
        border-radius: 10px !important;
        padding: 10px !important;
    }

    button {
        border-radius: 10px !important;
        font-weight: bold;
    }

    #btn {
        background: linear-gradient(90deg, #6366f1, #3b82f6);
        color: white;
    }
    """
) as app:

    # HEADER
    gr.Markdown("""
    <div style="text-align:center;">
        <h1 style="color:#38bdf8;">Smart Study Assistant</h1>
        <p style="color:gray;">Smart Learning • Adaptive Planning • Spaced Repetition</p>
    </div>
    """)

    with gr.Tabs():

        # AI TUTOR
        with gr.Tab(" AI Tutor"):

            with gr.Column(elem_id="card"):

                gr.Markdown("### 💬 Ask your question")

                q = gr.Textbox(
                    placeholder="e.g. What is photosynthesis?",
                    lines=2,
                    show_label=False
                )

                btn = gr.Button(" Get Answer", elem_id="btn")

                out_text = gr.Markdown()

                gr.Markdown("### Voice Answer")
                out_audio = gr.Audio()

                btn.click(generate_answer, inputs=q, outputs=[out_text, out_audio])

        # STUDY PLANNER
        with gr.Tab(" Study Planner"):

            with gr.Column(elem_id="card"):

                days = gr.Number(label=" Days Left", value=10)
                hours = gr.Number(label=" Study Hours", value=5)

                topics = gr.Textbox(
                    lines=5,
                    label=" Topics",
                    placeholder="Physics\nChemistry\nBiology"
                )

                btn2 = gr.Button(" Generate Plan", elem_id="btn")

                plan_out = gr.Textbox(label=" Plan")

                btn2.click(planner_ui, inputs=[days, hours, topics], outputs=plan_out)

        #SPACED REPETITION
        with gr.Tab("Spaced Repetition"):

            with gr.Column(elem_id="card"):

                # Add
                gr.Markdown("### Add Concept")

                name = gr.Textbox(label="Concept Name")
                subject = gr.Textbox(label="Subject")

                add_out = gr.Textbox(label="Status")
                btn_add = gr.Button("➕ Add Concept", elem_id="btn")

                btn_add.click(
                    spaced_repetition.add_concept,
                    inputs=[name, subject, gr.State([])],
                    outputs=add_out
                )

                gr.Markdown("---")

                # Practice
                gr.Markdown("### Practice")

                concept = gr.Textbox(label="Concept")
                correct = gr.Radio(["Yes", "No"], label="Correct?")
                time = gr.Slider(1, 30, value=10)

                update_out = gr.Textbox(label="Result")
                btn_update = gr.Button(" Update", elem_id="btn")

                btn_update.click(update_fn, inputs=[concept, correct, time], outputs=update_out)

                gr.Markdown("---")

                # Dashboard + Graphs
                dash = gr.Textbox(label="Dashboard", lines=8)

                graph1 = gr.Plot(label="Forgetting Curve")
                graph2 = gr.Plot(label="Learning Trend")

                btn_dash = gr.Button("Show Dashboard", elem_id="btn")
                btn_graph = gr.Button("Show Graphs", elem_id="btn")

                btn_dash.click(spaced_repetition.get_dashboard, outputs=dash)
                btn_graph.click(graphs, outputs=[graph1, graph2])

# RUN
app.launch(share=True)
