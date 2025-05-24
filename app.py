from flask import Flask, request, jsonify
import os
import spacy
import pdfplumber
import pandas as pd
import re
from difflib import SequenceMatcher
import io

# === CONFIG ===
MODEL_PATH = "/home/ubuntu/citation_ner_model_v6"
CITATION_CSV = "/home/ubuntu/Citation Data For Fine-Tuning - Sheet1 up.csv"

# === Load model and citation phrases once
nlp = spacy.load(MODEL_PATH)
df = pd.read_csv(CITATION_CSV, encoding='ISO-8859-1')
known_phrases = df['Citation Language'].dropna().unique().tolist()

# === Citation Filtering Rules
regex_patterns = [
    r"\bEx\.?\s*\d+[a-zA-Z]?\b",
    r"\bExhibit\s+[A-Z0-9]+\b",
    r"\bDkt\. No\. \d+(?:; [A-Za-z]{3}\. \d{1,2}, \d{4})?",
    r"\bGroup Ex\. [A-Z0-9]+(?:,? \d+(-\d+)?)?",
    r"\bSchedule\s+[A-Z0-9]+\b",
    r"\bEx\.?\s+[A-Z]\b",
    r"\bEx\.?\s+[A-Z] at \d+\b",
]

def is_case_law_citation(text):
    return (
        " v. " in text or
        "U.S.C." in text or
        "WL" in text or
        "F. Supp." in text or
        "F.3d" in text or
        re.search(r"\b§\s*\d+", text) or
        re.search(r"\bsee also\b", text, re.IGNORECASE)
    )

def is_close_match(text, phrases, threshold=0.85):
    return any(SequenceMatcher(None, text.lower(), phrase.lower()).ratio() >= threshold for phrase in phrases)

# === Flask App ===
app = Flask(__name__)

# === 1. API: Extract from PDF ===
@app.route("/api/extract-pdf", methods=["POST"])
def extract_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400

    file = request.files["pdf"]
    file_bytes = file.read()
    results = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            page_key = f"page_{i+1}"

            # NER
            doc = nlp(text)
            for ent in doc.ents:
                citation = ent.text.strip()
                if ent.label_ == "CITATION" and not is_case_law_citation(citation) and is_close_match(citation, known_phrases):
                    results.append({"page": page_key, "source": "model", "citation": citation})

            # Regex
            for pattern in regex_patterns:
                found = re.findall(pattern, text, flags=re.IGNORECASE)
                for match in found:
                    citation = match.strip()
                    if not is_case_law_citation(citation):
                        results.append({"page": page_key, "source": "regex", "citation": citation})

    return jsonify({"citations": results})

# === 2. API: Extract from Text ===
@app.route("/api/extract-text", methods=["POST"])
def extract_text():
    data = request.get_json()
    input_text = data.get("text", "").strip()

    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    results = []

    doc = nlp(input_text)
    for ent in doc.ents:
        citation = ent.text.strip()
        if ent.label_ == "CITATION" and not is_case_law_citation(citation) and is_close_match(citation, known_phrases):
            results.append({"source": "model", "citation": citation})

    for pattern in regex_patterns:
        found = re.findall(pattern, input_text, flags=re.IGNORECASE)
        for match in found:
            citation = match.strip()
            if not is_case_law_citation(citation):
                results.append({"source": "regex", "citation": citation})

    return jsonify({"citations": results})

# === Run Server ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

