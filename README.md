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

⚙️ Setup & Run
1. Create a virtual environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
2. Install requirements
bash
Copy
Edit
pip install -r requirements.txt
3. Run the API
bash
Copy
Edit
python app.py
App will run at:

cpp
Copy
Edit
http://0.0.0.0:5000
📦 Deployment Tips
Tested on Ubuntu EC2 (t3.micro)

Open ports 22, 5000 in security group

You can use screen, tmux, or a WSGI server (like gunicorn) for production

✍️ Author
Zeeshan – AI Developer & Citation Model Trainer
For deployment help, contact via [Upwork/Freelance]
