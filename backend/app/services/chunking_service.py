from app.core.config import settings

def chunk_pages(pages:list[dict])->list[dict]:
    chunks = []

    chunk_size = settings.CHUNK_SIZE
    overlap = settings.CHUNK_OVERLAP
    step = chunk_size - overlap

    if chunk_size <= 0 or overlap < 0 or step <= 0:
        raise ValueError("Invalid chunk size or overlap values.")

    for page in pages:
        text=page["text"].strip()
        page_number=page["page_number"]

        if not text:
            continue

        for start in range(0, len(text), step):
            chunk_text=text[start:start + chunk_size]
            if chunk_text.strip():
                chunks.append({
                    "id": f"{page_number}_{start}",
                    "chunk_index":len(chunks),
                    "text": chunk_text,
                    "page_number": page_number
                })
    return chunks