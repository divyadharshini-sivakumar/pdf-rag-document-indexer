import sys
import argparse
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_chroma import Chroma

from config import CHROMA_DB_DIR, COLLECTION_NAME, get_embedding_function

def search_vector_db(query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
    """
    Performs a similarity search with relevance scoring in ChromaDB.
    """
    embeddings = get_embedding_function()

    db = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DB_DIR),
    )

    results = db.similarity_search_with_score(query, k=top_k)
    return results

def format_search_results(results: List[Tuple[Document, float]], query: str):
    """Formats and prints search results to the terminal."""
    print("=" * 70)
    print(f"SEARCH QUERY: '{query}'")
    print("=" * 70)

    if not results:
        print("[NOTICE] No relevant documents found.")
        return

    for idx, (doc, score) in enumerate(results, 1):
        metadata = doc.metadata
        chunk_id = metadata.get("chunk_id", "N/A")
        source = metadata.get("source", "N/A")
        page_num = metadata.get("page_number", "N/A")

        print(f"\nResult #{idx} | Score (Distance): {score:.4f}")
        print(f"Source: {source} | Page: {page_num} | Chunk ID: {chunk_id}")
        print("-" * 70)
        content_preview = doc.page_content.strip()
        print(content_preview)
        print("-" * 70)

def main():
    parser = argparse.ArgumentParser(description="Query ChromaDB Vector Store")
    parser.add_argument(
        "query", 
        type=str, 
        nargs="?", 
        default="What are the safety instructions and installation requirements?",
        help="Search query to execute against the indexed documents."
    )
    parser.add_argument(
        "-k", "--top_k", 
        type=int, 
        default=3, 
        help="Number of top matching chunks to return."
    )
    args = parser.parse_args()

    try:
        results = search_vector_db(args.query, top_k=args.top_k)
        format_search_results(results, args.query)
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
