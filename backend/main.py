from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI(title="ZDS GenAI Simple Backend")

# Load extracted knowledge
with open("data/knowledge.json", "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)

class Query(BaseModel):
    query: str

@app.post("/ask")
def ask(q: Query):
    ql = q.query.lower()

    for chunk in KNOWLEDGE:
        if ql in chunk.lower():
            return {
                "answer": chunk[:1000]
            }

    return {
        "answer": "Answer not found, but documents are loaded correctly."
    }

