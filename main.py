from loader import get_path, load_document
from ingest import chunk, embed_and_store
from qa import ask_llm

import os


def setup_database():

    if not os.path.exists("./chroma_db"):
        print("No database found. Let's add your first document.")
        add_document()
    else:
        choice = input("Add a new document? (y/n): ").lower()
        if choice == "y":
            add_document()
        else:
            print("Using existing vector database.")


def add_document():
    path = get_path()
    print("Processing document...")

    doc = load_document(path)
    chunks = chunk(doc)
    embed_and_store(chunks)

    print("Document added to database.")


if __name__ == "__main__":

    setup_database()

    print("\nDocument QA ready")
    print("Type exit to quit")

    while True:

        query = input("\nAsk question: ")

        if query.lower() == "exit":
            break

        answer, docs = ask_llm(query)

        print("\nAnswer:")
        print(answer)

        print("\nSources:")

        for doc, score in docs:
            print(
                "Page:",
                doc.metadata.get("page")
            )
            
