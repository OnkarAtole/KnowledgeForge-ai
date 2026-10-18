from io import BytesIO
from hashlib import sha256
from fastapi import UploadFile, File, APIRouter, HTTPException
from app.schemas.document import PDFUploadResponse, PDFPage
from app.services.pdf_service import extract_pdf_text
from uuid import uuid4
from app.services.chunking_service import chunk_pages
from app.services.vector_store import store_chunks

router=APIRouter(
    prefix="/documents",
    tags=["documents"],
)



MAx_FILE_SIZE=10*1024*1024  # 10 MB

@router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(file:UploadFile=File(...)):
    # Check if the uploaded file is a PDF
    if not file.content_type=="application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    pdf_bytes=await file.read(MAx_FILE_SIZE+1)

    if len(pdf_bytes)>MAx_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 10 MB.")

    if not pdf_bytes.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF.")

    try:
        result=extract_pdf_text(pdf_bytes)
        document_id=str(uuid4())
        chunks=chunk_pages(result["pages"])
        stored_count=store_chunks(document_id, chunks)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the PDF.")

    finally:
        await file.close()

    return PDFUploadResponse(
        filename=file.filename,
        content_type="application/pdf",
        file_size=len(pdf_bytes),
        sha256_hash=sha256(pdf_bytes).hexdigest(),
        document_id=document_id,
        chunks_stored=stored_count,
        **result,
    )
    