from pydantic import BaseModel
from pydantic import Field
class QuestionRequest(BaseModel):
    document_id: str
    question: str=Field(..., min_length=1, description="The question to ask about the document.")
    top_k: int=Field(5, ge=1, le=20, description="The number of top relevant chunks to retrieve from the vector store.")


class SourceChunk(BaseModel):
    page_number:int
    text: str

class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk]