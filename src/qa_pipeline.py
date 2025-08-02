"""
ThreadQA: Minimal Working Version
Basic pipeline for ingesting Reddit thread data, retrieving relevant chunks, and answering user questions using LangChain + OpenAI.
"""
import json
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load Reddit thread data
def load_thread(path):
    with open(path, 'r') as f:
        posts = json.load(f)
    # Concatenate posts for chunking
    docs = [f"[{p['timestamp']}] {p['author']}: {p['message']}" for p in posts]
    return docs

# Chunk posts (simple splitter)
def chunk_posts(docs, chunk_size=300):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=20)
    return text_splitter.create_documents(docs)

# Build retriever
def build_retriever(docs):
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    return db.as_retriever()

# QA pipeline
class ThreadQA:
    def __init__(self, thread_path):
        docs = load_thread(thread_path)
        chunks = chunk_posts(docs)
        retriever = build_retriever(chunks)
        self.qa = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

    def ask(self, question):
        result = self.qa({"query": question})
        answer = result['result']
        sources = result['source_documents']
        print("Answer:", answer)
        print("\nSources:")
        for src in sources:
            print(src.page_content)
        return answer, sources

if __name__ == "__main__":
    import sys
    thread_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_thread.json"
    qa = ThreadQA(thread_path)
    print("ThreadQA ready. Type your question:")
    while True:
        q = input("Q: ")
        if not q.strip():
            break
        qa.ask(q)
