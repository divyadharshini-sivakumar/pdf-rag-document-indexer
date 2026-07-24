# Lab 1: Product Manual Indexing with LangChain & ChromaDB

A production-grade implementation for loading, chunking, embedding, and indexing a ~100-page product manual PDF into ChromaDB using Python 3.11+, LangChain, PyPDF, and configurable embedding backends (Local HuggingFace vs OpenAI API).

---

## 📁 Project Architecture

```
rag_lab1_chromadb/
│── data/                     # Directory storing source PDF product manuals
│── chroma_db/                # Persistent vector database output directory
│── config.py                 # Central configuration & embedding factory
│── ingest.py                 # Ingestion pipeline: PDF -> Chunks -> ChromaDB
│── search.py                 # Similarity search validation CLI tool
│── create_sample_pdf.py      # Utility script for generating test data
│── requirements.txt          # Production dependencies
│── .env.example              # Environment variables template
└── README.md                 # Documentation
```

---

## ⚡ Quick Start

### 1. Environment Setup

```bash
# Navigate to project directory
cd C:\Users\DIVYA DHARSHINI S\.gemini\antigravity\scratch\rag_lab1_chromadb

# Create & activate virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Default config uses local HuggingFace embeddings (`all-MiniLM-L6-v2`), which requires no external API keys.

---

## 🚀 Execution & Verification

### Step 1: Add a PDF Document
Place your product manual PDF inside the `data/` folder:
```
data/product_manual.pdf
```

### Step 2: Run Ingestion Pipeline
```bash
python ingest.py
```

### Step 3: Run Vector Similarity Search
```bash
python search.py "What are the safety instructions and installation requirements?"
```

---

## 💡 Switching Embedding Backends

To switch from local HuggingFace embeddings to OpenAI embeddings:

1. Open `.env`
2. Update key settings:
   ```env
   EMBEDDING_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-...
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   ```
3. Re-run `python ingest.py` to rebuild vectors using OpenAI embeddings.
