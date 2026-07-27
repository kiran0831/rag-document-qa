"""
loader.py — Loads documents (PDF, TXT, CSV, DOCX) into LangChain Document
objects, ready to be chunked and embedded.
"""

from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, Docx2txtLoader, CSVLoader
import os


def load_document(path):
    """Pick the right LangChain loader based on file extension and load the document."""
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        loader = PyMuPDFLoader(path)
    elif ext == ".txt":
        loader = TextLoader(path)
    elif ext == ".csv":
        loader = CSVLoader(path)
    elif ext == ".docx":
        loader = Docx2txtLoader(path)
    else:
        # Stop immediately on unsupported types instead of silently continuing
        raise ValueError(f"Unsupported file type: {ext}")

    return loader.load()


def get_path():
    """Ask the user for a file path and clean up quotes/escape chars from drag-and-drop."""
    path = input("drag and drop/write the file name").strip()
    path = path.strip("'").strip('"')
    path = path.lstrip("\x1b")  # some terminals prefix drag-and-drop paths with this escape char
    return path


if __name__ == "__main__":
    # Quick manual test: load a file and print how many chunks/pages came back
    path = get_path()
    loader = load_document(path)
    print("len of doc", len(loader))
    print(loader)
