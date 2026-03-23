AI Study Assistant

A web-based study tool that combines question answering, planning, and memory tracking in a single interface. The system is built around simple ideas: retrieve relevant knowledge, schedule study time, and reinforce learning through repetition.


## Overview

This project brings together three core components:

* A question-answering module based on semantic retrieval
* A study planner that prioritizes topics using simple heuristics
* A spaced repetition system that models memory decay and schedules revision

The interface is implemented using Gradio and runs as a lightweight web application.

## Features

### Question Answering

Accepts natural language queries and retrieves the most relevant information from a predefined knowledge base. Responses are also converted to speech.

### Study Planner

Generates a daily plan based on:

* available study time
* number of days remaining
* topic difficulty and retention

### Spaced Repetition

Tracks concepts over time and updates confidence based on performance.
Includes:

* revision scheduling
* performance tracking
* forgetting curve visualization

### Authentication

A basic login and signup system using JSON storage for user data.


## Tech Stack

* Python
* Gradio
* SentenceTransformers
* FAISS
* NumPy
* Matplotlib
* gTTS

## Project Structure

```
app.py                 # main application
spaced_repetition.py  # learning and revision logic
users.json            # user data storage
```

## Setup Instructions

1. Install dependencies:

```
pip install gradio sentence-transformers faiss-cpu gtts matplotlib numpy
```

2. Run the application:

```
python app.py
```

3. Open the generated link in your browser.


## How It Works

* The tutor converts text into embeddings and retrieves similar content using FAISS
* The planner assigns priority scores using retention and difficulty
* The repetition module updates confidence and schedules future reviews
* Graphs are generated using Matplotlib to visualize learning behavior

## Limitations

* User data is stored locally in a JSON file
* Knowledge base is limited and manually defined
* No persistent cloud deployment
* No per-user model personalization yet


## Possible Improvements

* Replace JSON storage with a database
* Expand the knowledge base with structured datasets
* Add user-specific tracking and analytics
* Improve the UI with a dedicated frontend
* Integrate adaptive learning based on performance history

This project is intended for academic and experimental use.

