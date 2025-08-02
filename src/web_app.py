"""
ThreadQA Web UI using Streamlit
Features: Upload/fetch Reddit data, ask questions, show answers/confidence, speaker summary, and log results.
"""
import streamlit as st
import json
import openai
import os
from datetime import datetime

def load_posts(path):
    with open(path, 'r') as f:
        return json.load(f)

def get_speaker_summary(posts):
    speakers = {}
    for p in posts:
        speakers.setdefault(p['author'], []).append(p['message'])
    summary = []
    for author, msgs in speakers.items():
        summary.append(f"{author}: {', '.join(msgs[:2])}{'...' if len(msgs)>2 else ''}")
    return " | ".join(summary)

def get_context(posts):
    return "\n".join([f"[{p['timestamp']}] {p['author']}: {p['message']}" for p in posts])

def ask_openai(context, question):
    prompt = f"Thread:\n{context}\n\nQuestion: {question}\nAnswer:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a robust Q&A assistant for noisy Reddit threads."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=256
    )
    answer = response['choices'][0]['message']['content']
    confidence = 0.9 if response['choices'][0]['finish_reason'] == 'stop' else 0.5
    failed = False
    return answer, confidence, failed

def log_qa(question, answer, confidence, failed):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "failed": failed
    }
    with open("logs/qa_log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

st.title("ThreadQA: Subreddit-scale Q&A Web App")
st.markdown("Robust, research-aware, and ready for FLAIR Lab")

uploaded_file = st.file_uploader("Upload Reddit data (JSON)", type=["json"])
if uploaded_file:
    posts = json.load(uploaded_file)
else:
    default_path = "data/subreddit_dump.json"
    if os.path.exists(default_path):
        posts = load_posts(default_path)
    else:
        st.warning("No data file found. Please upload a Reddit JSON file.")
        st.stop()

st.markdown(f"**Speaker summary:** {get_speaker_summary(posts)}")
context = get_context(posts)

question = st.text_input("Ask a question about the subreddit:")
if question:
    with st.spinner("Getting answer..."):
        answer, confidence, failed = ask_openai(context, question)
        st.success(answer)
        st.markdown(f"**Confidence:** {confidence:.2f}  **Failed:** {failed}")
        log_qa(question, answer, confidence, failed)
        st.info("Result logged for research analysis.")
