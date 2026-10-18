from pydantic import BaseModel
from pydantic import Field

class PDFPage(BaseModel):
    page_number:int=Field(...,ge=1, description="The page number of the PDF page")
    text:str

class PDFUploadResponse(BaseModel):
    filename:str
    content_type:str
    file_size:int
    sha256_hash:str
    page_count:int
    pages:list[dict]
    full_text:str
    document_id:str
    chunks_stored:int


