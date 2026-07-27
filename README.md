# Document QA RAG 📄

An AI-powered document Q&A app that lets you upload your own documents (PDF, DOCX, TXT, CSV) and ask questions about them. Answers are generated strictly from your document's content using Retrieval-Augmented Generation (RAG) — no hallucinated information.

## Features

- 📂 Supports PDF, DOCX, TXT, and CSV files
- 🔍 Semantic search over document content using vector embeddings
- 🧠 Context-grounded answers powered by Groq's LLaMA 3.1
- 📚 Add multiple documents over time — all searchable together
- 🚫 Says "I don't know based on the document" instead of guessing when the answer isn't found
- 💾 Persistent local vector database — no need to re-process documents every run

## How It Works

1. **Load** — Reads your document and extracts its text
2. **Chunk** — Splits the text into overlapping chunks for better retrieval
3. **Embed & Store** — Converts chunks into vector embeddings and stores them in a local Chroma database
4. **Retrieve** — Finds the most relevant chunks for your question using similarity search
5. **Answer** — Sends the retrieved context + your question to Groq's LLM, which answers using only that context

## Tech Stack

| Component | Tool |
|---|---|
| LLM | Groq — `llama-3.1-8b-instant` |
| Embeddings | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | Chroma (local, persistent) |
| Orchestration | LangChain |
| Document Loaders | PyMuPDF, Docx2txt, CSVLoader, TextLoader |
| Config | python-dotenv |

## Project Structure

```
document-qa-rag/
├── loader.py         # Loads documents (PDF/TXT/CSV/DOCX) into LangChain Document objects
├── ingest.py          # Chunks documents and stores/appends them to the vector database
├── retrieve.py        # Performs similarity search against the vector database
├── qa.py              # Builds the prompt and queries the Groq LLM for an answer
├── main.py            # Entry point — manages document ingestion and the query loop
├── requirements.txt   # Python dependencies
├── .gitignore         # Excludes .env and chroma_db/ from version control
└── README.md
```
## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/document-qa-rag.git
cd document-qa-rag
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Groq API key**

Create a `.env` file in the project root:
GROQ_API_KEY=your_groq_api_key_here
Get a free key at [console.groq.com/keys](https://console.groq.com/keys).

**4. Run the app**
```bash
python3 main.py
```

## Usage

On first run, you'll be asked to add a document:
drag and drop/write the file name: /path/to/your/document.pdf

Then ask questions freely:
Ask question: What is the difference between DFA and NFA?
Answer:
A DFA (Deterministic Finite Automaton) has exactly one transition
for each input symbol from a given state, while an NFA
(Non-deterministic Finite Automaton) can have multiple or zero
transitions for the same input symbol...
Sources:
Page: 3
Page: 4

Type `exit` to quit.

On future runs, you'll be asked whether to add another document. New documents are appended to the existing database — nothing is overwritten.

## Notes

- Get your free Groq API key at [console.groq.com](https://console.groq.com)
- The vector database (`chroma_db/`) is generated locally when you run the app — it's not tracked in this repo, so it won't exist until you ingest your first document
- Supports adding multiple documents over time — each new document is appended to the existing database, not overwritten
- Answers are strictly grounded in the uploaded document's content — if the answer isn't found, the assistant will say so instead of guessing
- Currently supports PDF, DOCX, TXT, and CSV files
