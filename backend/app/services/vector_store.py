
import chromadb
from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

db = chromadb.PersistentClient(
    path=str(settings.CHROMA_PERSIST_DIRECTORY)
)

collection = db.get_or_create_collection(
    name="knowledgeforge_documents"
)

def store_chunks(document_id: str, chunks: list[dict]) -> int:
    texts = [chunk["text"] for chunk in chunks]

    if not texts:
        return 0

    response = client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=texts,
    )

    embeddings = [item.embedding for item in response.data]

    collection.upsert(
        ids=[f"{document_id}-{chunk['id']}" for chunk in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            {
                "document_id": document_id,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ],
    )

    return len(texts)


def search_chunks(question:str, document_id:str, top_k=5)->list[dict]:
    """
    Search for relevant chunks in the vector store based on the question and document_id.
    """

    response = client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=question,
    )

    question_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        where={"document_id": document_id},
    )   

    matches=[]

    for i, text in enumerate(results["documents"][0]):
        matches.append({
            "text":text,
            "page_number":results["metadatas"][0][i]["page_number"],
            "distance":results["distances"][0][i],
        })

    return matches