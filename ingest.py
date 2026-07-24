import os
import sys
import uuid
from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config import (
    DATA_DIR,
    CHROMA_DB_DIR,
    COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    get_embedding_function,
)

def find_pdf_files(data_dir: Path) -> List[Path]:
    """Finds all PDF files in the target data directory."""
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"[WARNING] Directory '{data_dir}' was missing. Created empty folder.")
        return []
    
    pdfs = list(data_dir.glob("*.pdf"))
    return pdfs

def load_pdf_documents(file_path: Path) -> List[Document]:
    """
    Loads and extracts text from a PDF file using PyPDFLoader.
    Validates readability and content existence.
    """
    print(f"[INFO] Loading PDF: {file_path.name}...")
    try:
        loader = PyPDFLoader(str(file_path))
        pages = loader.load()
    except Exception as e:
        print(f"[ERROR] Failed to read PDF file '{file_path.name}': {e}")
        return []

    if not pages:
        print(f"[WARNING] PDF file '{file_path.name}' contained no pages.")
        return []

    # Clean metadata & validate page content
    valid_pages = []
    empty_page_count = 0
    for page in pages:
        page_text = page.page_content.strip()
        if not page_text:
            empty_page_count += 1
            continue
        
        # Ensure standardized metadata keys
        page.metadata["source"] = file_path.name
        # PyPDFLoader populates 'page' (0-indexed). Convert/ensure 1-indexed page number.
        if "page" in page.metadata:
            page.metadata["page_number"] = page.metadata["page"] + 1
        elif "page_number" not in page.metadata:
            page.metadata["page_number"] = 1

        valid_pages.append(page)

    print(f"[SUCCESS] Extracted {len(valid_pages)} non-empty pages from {file_path.name}.")
    if empty_page_count > 0:
        print(f"[NOTICE] Skipped {empty_page_count} empty or image-only pages.")
    
    return valid_pages

def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Splits documents into smaller overlapping chunks and assigns deterministic chunk IDs.
    """
    if not documents:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )
    chunks = splitter.split_documents(documents)

    # Assign structured chunk IDs: <filename>_p<page>_c<index>
    page_chunk_counters = {}
    for chunk in chunks:
        source = chunk.metadata.get("source", "doc")
        page_num = chunk.metadata.get("page_number", 1)
        key = f"{source}_p{page_num}"
        
        count = page_chunk_counters.get(key, 0) + 1
        page_chunk_counters[key] = count
        
        chunk_id = f"{key}_c{count}"
        chunk.metadata["chunk_id"] = chunk_id

    print(f"[SUCCESS] Created {len(chunks)} text chunks from {len(documents)} pages.")
    return chunks

def store_in_chroma(chunks: List[Document]):
    """
    Stores document chunks with embeddings into persistent ChromaDB storage.
    """
    if not chunks:
        print("[WARNING] No chunks to index into ChromaDB.")
        return None

    embeddings = get_embedding_function()
    
    print(f"[INFO] Connecting to ChromaDB at: {CHROMA_DB_DIR}")
    db = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DB_DIR),
    )

    print(f"[INFO] Generating embeddings and indexing {len(chunks)} chunks into ChromaDB...")
    
    # Store chunks in batch
    db.add_documents(documents=chunks, ids=[c.metadata["chunk_id"] for c in chunks])
    print(f"[SUCCESS] Successfully indexed {len(chunks)} chunks into collection '{COLLECTION_NAME}'.")
    return db

def main():
    print("=" * 60)
    print("      RAG INGESTION PIPELINE: PDF -> CHROMA DB")
    print("=" * 60)

    pdf_files = find_pdf_files(DATA_DIR)
    if not pdf_files:
        print(f"[ERROR] No PDF files found in '{DATA_DIR}'. Please place your product manual PDF in the '{DATA_DIR}' directory and try again.")
        sys.exit(1)

    all_chunks = []
    for pdf_path in pdf_files:
        pages = load_pdf_documents(pdf_path)
        chunks = chunk_documents(pages)
        all_chunks.extend(chunks)

    if not all_chunks:
        print("[ERROR] Processing yielded zero text chunks. Ingestion aborted.")
        sys.exit(1)

    db = store_in_chroma(all_chunks)
    print("=" * 60)
    print("Ingestion process complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
