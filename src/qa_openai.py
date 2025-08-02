"""
ThreadQA: Impressive Q&A App for Subreddit-scale Data
Features: Interactive Q&A, confidence/error logging, speaker attribution, noise simulation, answer highlighting, and research-aware UI.
"""
import os
import json
import openai
import random
from datetime import datetime
from rich import print as rprint
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

LOG_PATH = "logs/qa_log.jsonl"
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Simulate noisy/out-of-order data
def simulate_noise(posts, shuffle=True, drop_rate=0.1):
    noisy = posts.copy()
    if shuffle:
        random.shuffle(noisy)
    noisy = [p for p in noisy if random.random() > drop_rate]
    return noisy

# Load Reddit thread/subreddit data
def load_thread(path, noisy=False):
    with open(path, 'r') as f:
        posts = json.load(f)
    if noisy:
        posts = simulate_noise(posts)
    context = "\n".join([f"[{p['timestamp']}] {p['author']}: {p['message']}" for p in posts])
    return context, posts

# Speaker attribution helper
def get_speaker_summary(posts):
    speakers = {}
    for p in posts:
        speakers.setdefault(p['author'], []).append(p['message'])
    summary = []
    for author, msgs in speakers.items():
        summary.append(f"[bold]{author}[/bold]: {', '.join(msgs[:2])}{'...' if len(msgs)>2 else ''}")
    return " | ".join(summary)

# Log QA results
def log_qa(question, answer, confidence, failed):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "failed": failed
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

# OpenAI QA with confidence estimation
def ask_openai(context, question):
    prompt = f"Thread:\n{context}\n\nQuestion: {question}\nAnswer:"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a robust Q&A assistant for noisy Reddit threads."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=256
        )
        answer = response.choices[0].message.content
        confidence = 0.9 if response.choices[0].finish_reason == 'stop' else 0.5
        failed = False
    except Exception as e:
        answer = f"[Error: {e}]"
        confidence = 0.0
        failed = True
    log_qa(question, answer, confidence, failed)
    return answer, confidence, failed

# Highlight answer
def highlight_answer(answer):
    return f"[bold green]{answer}[/bold green]"

# Interactive Q&A App
if __name__ == "__main__":
    thread_path = "data/subreddit_dump.json"  # Use all subreddit data by default
    context, posts = load_thread(thread_path, noisy=True)
    rprint(Panel("[bold magenta]ThreadQA: Subreddit-scale Q&A App[/bold magenta]\n[italic]Robust, research-aware, and ready for FLAIR Lab[/italic]", title="ThreadQA"))
    rprint(Panel(f"Speaker summary:\n{get_speaker_summary(posts)}", title="Speakers"))
    while True:
        q = Prompt.ask("[bold blue]Ask a question about the subreddit[/bold blue]")
        if not q.strip():
            break
        answer, confidence, failed = ask_openai(context, q)
        rprint(Panel(highlight_answer(answer), title="Answer"))
        rprint(f"[yellow]Confidence:[/yellow] {confidence:.2f}    [red]Failed:[/red] {failed}")
    rprint("[bold green]Session ended. All results logged in logs/qa_log.jsonl.[/bold green]")
