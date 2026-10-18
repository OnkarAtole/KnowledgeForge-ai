
from fastapi import APIRouter, HTTPException

from app.schemas.chat import QuestionRequest, QuestionResponse
from app.services.chat_service import answer_question

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        result = answer_question(
            document_id=request.document_id,
            question=request.question,
            top_k=request.top_k,
        )

        return QuestionResponse(
            question=request.question,
            answer=result["answer"],
            sources=result["sources"],
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to answer the question. Please try again.",
        ) from exc
