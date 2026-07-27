"""
qa.py — Given a user query, retrieves relevant chunks from the vector
database and asks Groq's LLM to answer using only that context.
"""

from groq import Groq
from dotenv import load_dotenv
import os

from retrieve import retrieve

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(query):
    """Retrieve relevant chunks for the query, build a context-grounded prompt,
    and ask the LLM to answer using only that context."""

    # 1. Similarity search from Chroma
    docs = retrieve(query, k=15)

    # 2. Convert retrieved documents into a single context block
    context = "\n\n".join(
        [
            doc.page_content
            for doc, score in docs
        ]
    )

    # 3. Build the prompt — instruct the model to stick strictly to the context
    prompt = f"""
You are a helpful document assistant.

Answer the question only using the context below.
If the answer is not present in the context, say:
"I don't know based on the document."

Context:
{context}

Question:
{query}
"""

    # 4. Send to Groq's LLM
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2  # low temperature keeps answers grounded/factual, not creative
    )

    answer = response.choices[0].message.content

    return answer, docs


if __name__ == "__main__":
    # Standalone test loop — lets you query without going through main.py
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
                doc.metadata.get("source"),
                "page:",
                doc.metadata.get("page")
            )
