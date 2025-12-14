from PyPDF2 import PdfReader
import os
import json

PDF_DIR = "data/docs"
OUT_FILE = "data/knowledge.json"

texts = []

for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        print(f"Reading {file} ...")
        reader = PdfReader(os.path.join(PDF_DIR, file))
        for page in reader.pages:
            text = page.extract_text()
            if text:
                texts.append(text.strip())

if not texts:
    print("❌ No text extracted from PDFs")
else:
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(texts, f, indent=2)
    print(f"✅ Extracted {len(texts)} pages and saved to {OUT_FILE}")

