# ThreadQA

A robust LLM-powered Q&A system for extracting answers from messy, multi-turn Reddit threads. Designed for research on robust LLMs, knowledge extraction, and noisy corpora (inspired by Dr. Kuan-Hao Huang, Texas A&M FLAIR Lab).

## Research Alignment
ThreadQA is inspired by the work of Dr. Kuan-Hao Huang and the FLAIR Lab at Texas A&M University. This project aims to address key challenges in robust, trustworthy, and generalizable language AI systems, including:
- **Robustness to Noise:** Handles messy, multi-turn Reddit threads with speaker changes, off-topic comments, and out-of-order data.
- **Knowledge Extraction:** Extracts structured answers from unstructured, real-world corpora.
- **Trust & Reliability:** Logs confidence scores and failed queries to support trustworthy QA.
- **Extensibility:** Designed for multimodal, multilingual, and compositional reasoning research.

If you are interested in large language models, multimodal learning, or multilingual NLP, please reach out to Dr. Huang at khhuang [at] tamu [dot] edu.

## Features
- Ingest Reddit thread data (JSON, CSV, or live via Reddit API)
- Ask natural language questions about threads
- Uses OpenAI for retrieval and answering
- Robust to noise, speaker changes, and off-topic comments
- Logs confidence scores and failed queries
- Speaker attribution in answers
- Simulate noisy/out-of-order data
- Multilingual/multimodal extension ready

## Quickstart
1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Set your OpenAI API key**
   ```bash
   export OPENAI_API_KEY=your-key
   ```
3. **Run the app**
   ```bash
   python src/qa_openai.py
   ```

## Data Format
- See `data/sample_thread.json` for example Reddit thread data.
- You can also ingest threads live using the Reddit API (see below).

## Using the Reddit API
To fetch threads directly from Reddit, you can use the `praw` library:
```python
import praw
reddit = praw.Reddit(client_id='YOUR_ID', client_secret='YOUR_SECRET', user_agent='ThreadQA')
thread = reddit.submission(url='REDDIT_THREAD_URL')
for comment in thread.comments:
    print(comment.author, comment.body)
```
- Save comments to JSON for use with ThreadQA.
- See `src/fetch_reddit.py` for a sample script.

## Example Output
```
Q: What is the best way to learn Python?
A: According to userB, online courses are great. userC suggests freeCodeCamp, while userE prefers books.
[Confidence: 0.92]
```

## Research Extensions
- Log attention drift, LLM uncertainty, or hallucinations
- Simulate out-of-order/noisy data
- Add speaker attribution
- Multilingual/multimodal extension stub in `src/multimodal_extension.py`

## Citation & Contact
For research, cite this repo and contact the author for collaboration.

---

> “This project is designed to demonstrate my interest in robust, trustworthy, and generalizable LLMs, and my alignment with the FLAIR Lab’s research directions. I am excited to contribute to the lab’s mission and explore new frontiers in NLP and multimodal AI.”