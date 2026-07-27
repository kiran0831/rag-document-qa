"""
ingest.py — Splits loaded documents into chunks, embeds them, and stores
them in a persistent Chroma vector database. Appends to the existing
database if one already exists, instead of overwriting it.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loader import get_path, load_document
import os

DB_DIR = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def chunk(data):
    """Split loaded documents into overlapping chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(data)
    return chunks


def embed_and_store(chunks):
    """Embed chunks and store them in Chroma — creates a new DB if none exists,
    otherwise adds to the existing one so old documents aren't lost."""
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if os.path.exists(DB_DIR):
        # DB already exists — load it and append the new chunks
        vector_store = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embedding_model
        )
        vector_store.add_documents(chunks)
    else:
        # First time — create a fresh DB from these chunks
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=DB_DIR
        )

    return vector_store


if __name__ == "__main__":
    path = get_path()
    doc = load_document(path)

    chunks = chunk(doc)
    vectors = embed_and_store(chunks)

    print("len of chunks", len(chunks))
