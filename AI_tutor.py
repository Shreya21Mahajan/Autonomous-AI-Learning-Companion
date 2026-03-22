#  Install libraries
!pip install gradio sentence-transformers faiss-cpu gtts

import gradio as gr
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from difflib import get_close_matches
from gtts import gTTS
import tempfile

# -------------------------------
#  Knowledge Base (NCERT style)
# -------------------------------

documents = [
    "Photosynthesis is the process by which plants make food using sunlight, carbon dioxide and water.",
    "Mitochondria is known as the powerhouse of the cell because it produces energy.",
    "DNA carries genetic information and is present in the nucleus.",
    "Newton's second law states that Force equals mass multiplied by acceleration.",
    "The pH of a neutral solution is 7.",
]

# -------------------------------
#  Embedding Model
# -------------------------------

model = SentenceTransformer('all-MiniLM-L6-v2')
doc_embeddings = model.encode(documents)

# -------------------------------
#  FAISS Index
# -------------------------------

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings))

# -------------------------------
#  Retrieval
# -------------------------------

def retrieve(query):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k=2)
    return [documents[i] for i in I[0]]

# -------------------------------
#  Auto Spell Correction
# -------------------------------

def correct_query(query):
    keywords = ["photosynthesis", "mitochondria", "dna", "force", "ph"]
    match = get_close_matches(query.lower(), keywords, n=1)
    return match[0] if match else query

# -------------------------------
#  RAG Answer
# -------------------------------

def generate_answer(query):
    context = retrieve(query)

    if not context:
        return " Answer not found in trusted sources.", None

    main = context[0]

    answer = f"""
###  NCERT-Based Answer:
{main}

###  Simple Explanation (Hinglish):
Iska matlab hai ki {main.lower()}

###  Source:
- {context[0]}
- {context[1] if len(context) > 1 else ""}
"""

    #  Convert to voice
    tts = gTTS(main)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)

    return answer, temp_file.name

# -------------------------------
#  Voice Input Handler
# -------------------------------

def voice_to_text(audio):
    return "Voice input received (demo). Please type your query for best result."

# -------------------------------
#  Gradio UI
# -------------------------------

with gr.Blocks() as app:

    gr.Markdown("## 🧠 AI Tutor with RAG + Voice (NEET Assistant)")

    # Text input
    query = gr.Textbox(label="❓ Ask your doubt (Hindi / Hinglish allowed)")

    # Voice input
    audio_input = gr.Audio(type="filepath", label="🎤 Speak your doubt")

    btn = gr.Button("Ask AI Tutor")

    output_text = gr.Markdown(label="📖 Answer")
    output_audio = gr.Audio(label="🔊 Voice Answer")

    # Button click
    def handle_query(q):
        q = correct_query(q)
        return generate_answer(q)

    btn.click(handle_query, inputs=query, outputs=[output_text, output_audio])

app.launch(share=True)
