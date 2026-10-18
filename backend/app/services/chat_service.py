
from openai import OpenAI

from app.core.config import settings
from app.services.vector_store import search_chunks

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def answer_question(
    document_id: str,
    question: str,
    top_k: int = 5,
) -> dict:
    # 1. Retrieve relevant chunks from ChromaDB
    chunks = search_chunks(
        question=question,
        document_id=document_id,
        top_k=top_k,
    )

    if not chunks:
        return {
            "answer": "No relevant information was found in this document.",
            "sources": [],
        }

    # 2. Build the context for the AI
    context = "\n\n".join(
        f"Page {chunk['page_number']}:\n{chunk['text']}"
        for chunk in chunks
    )

    # 3. Generate an answer using OpenAI
    response = client.chat.completions.create(
        model=settings.OPENAI_CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the "
                    "provided document context. If the answer is "
                    "not present, say so. Cite supporting pages "
                    "using [Page N]. Do not invent facts."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Document context:\n{context}\n\n"
                    f"Question: {question}"
                ),
            },
        ],
    )

    answer = response.choices[0].message.content or ""

    # 4. Return the answer and its source passages
    return {
        "answer": answer,
        "sources": [
            {
                "page_number": chunk["page_number"],
                "text": chunk["text"],
            }
            for chunk in chunks
        ],
    }
