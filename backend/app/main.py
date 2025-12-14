from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI(title="ZDS GenAI RAG Backend")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "..", "data", "knowledge.json")

class Query(BaseModel):
    query: str

def load_documents():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

DOCUMENTS = load_documents()

def simple_rag_search(query: str):
    q = query.lower()
    results = []
    for doc in DOCUMENTS:
        if q in doc.lower():
            results.append(doc)
    return results

@app.post("/ask")
def ask(q: Query):
    hits = simple_rag_search(q.query)
    if not hits:
        return {
            "answer": "Answer not found",
            "sources": []
        }
    return {
        "answer": hits[0],
        "sources": hits
    }

@app.post("/agent-ask")
def agent_ask(q: Query):
    parts = q.query.split(" and ")
    collected = []

    for part in parts:
        hits = simple_rag_search(part)
        if hits:
            collected.append(hits[0])

    if not collected:
        return {
            "final_answer": "No relevant information found.",
            "context": []
        }

    return {
        "final_answer": " ".join(collected),
        "context": collected
    }
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "data", "knowledge.json")
)

app = FastAPI(title="ZDS GenAI Assignment Backend")

class Query(BaseModel):
    query: str

def load_docs():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

DOCUMENTS = load_docs()

@app.post("/ask")
def ask(q: Query):
    q_lower = q.query.lower()
    for doc in DOCUMENTS:
        if q_lower in doc.lower():
            return {"answer": doc, "sources": [doc]}
    return {"answer": "Answer not found", "sources": []}

@app.post("/agent-ask")
def agent_ask(q: Query):
    parts = q.query.split(" and ")
    context = []
    for p in parts:
        for doc in DOCUMENTS:
            if p.lower() in doc.lower():
                context.append(doc)
                break
    if not context:
        return {"final_answer": "No relevant info", "context": []}
    return {"final_answer": " ".join(context), "context": context}

