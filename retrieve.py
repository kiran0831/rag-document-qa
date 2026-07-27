"""
retrieve.py — Performs similarity search against the persisted Chroma
vector database and returns the top-k matching document chunks with scores.
"""

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load once at import time instead of on every retrieve() call
_embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
_vector_store = Chroma(
    persist_directory=DB_DIR,
    embedding_function=_embedding_model
)


def retrieve(query, k=5):
    """Return the top-k most similar chunks to the query, each with a similarity score."""
    results = _vector_store.similarity_search_with_score(
        query,
        k=k
    )
    return results


if __name__ == "__main__":
    query = input("enter Query: ")

    docs = retrieve(query)

    for doc, score in docs:
        print("\n----------------")
        print("Score:", score)
        print(doc.metadata)
        print(doc.page_content)
