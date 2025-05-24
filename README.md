# 🧾 Legal Citation Extractor (PDF & Text)

This project provides an API to extract legal citations from **PDF documents** or **raw text** using a custom-trained [spaCy](https://spacy.io) model and custom regex patterns. It detects common legal references such as Exhibits, Schedules, Dkt. numbers, and more.

## 🔧 Features

- ✅ Upload PDF and extract citations with page numbers  
- ✅ Send raw legal text and extract citations  
- ✅ Returns clean JSON output with regex/model source  
- ✅ Ignores U.S. case law citations (e.g., `v.`, `WL`, `U.S.C.`)  
- ✅ Lightweight Flask-based API

---

## 🚀 API Endpoints

### 🔹 1. Extract from PDF

**URL:** `POST /api/extract-pdf`  
**Request:** `multipart/form-data` with key `pdf`  
**Response:**
```json
{
  "citations": [
    {"page": "page_3", "source": "model", "citation": "Ex. A"},
    {"page": "page_3", "source": "regex", "citation": "Schedule B"}
  ]
}
