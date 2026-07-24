import os
import sys
from pathlib import Path
from typing import List
from dotenv import load_dotenv

from langchain_core.embeddings import Embeddings

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
CHROMA_DB_DIR = BASE_DIR / os.getenv("CHROMA_DB_DIR", "chroma_db")

# Collection settings
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "product_manual")

# Chunking settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Embedding settings
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").lower()
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

class ChromaONNXEmbeddings(Embeddings):
    """
    LangChain Embeddings adapter for ChromaDB's native ONNX DefaultEmbeddingFunction.
    Provides zero-dependency ONNX embeddings for all-MiniLM-L6-v2 without PyTorch.
    """
    def __init__(self):
        from chromadb.utils import embedding_functions
        self._ef = embedding_functions.DefaultEmbeddingFunction()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._ef(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._ef([text])[0]

def validate_environment():
    """Validates configuration and required API keys before execution."""
    if EMBEDDING_PROVIDER not in ["local", "openai"]:
        raise ValueError(
            f"Invalid EMBEDDING_PROVIDER '{EMBEDDING_PROVIDER}'. Must be 'local' or 'openai'."
        )
    
    if EMBEDDING_PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError(
                "OPENAI_API_KEY is not set or contains default placeholder. "
                "Please set a valid key in your .env file."
            )

def get_embedding_function() -> Embeddings:
    """
    Factory function returning a LangChain Embeddings instance.
    Supports local ONNX-based all-MiniLM-L6-v2 embeddings and OpenAI API.
    """
    validate_environment()

    if EMBEDDING_PROVIDER == "local":
        try:
            print(f"[INFO] Initializing local ONNX embedding adapter: {LOCAL_EMBEDDING_MODEL}")
            return ChromaONNXEmbeddings()
        except Exception as e:
            raise ImportError(
                "Failed to initialize ChromaONNXEmbeddings adapter. "
                "Ensure 'chromadb' and 'onnxruntime' are installed."
            ) from e
    elif EMBEDDING_PROVIDER == "openai":
        try:
            from langchain_openai import OpenAIEmbeddings
            print(f"[INFO] Initializing OpenAI embeddings: {OPENAI_EMBEDDING_MODEL}")
            return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
        except ImportError as e:
            raise ImportError(
                "Failed to import OpenAIEmbeddings. "
                "Ensure 'langchain-openai' is installed."
            ) from e
