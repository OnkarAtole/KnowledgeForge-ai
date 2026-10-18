import pymupdf

def extract_pdf_text(pdf_bytes:bytes)->dict:
    """
    Extracts text from a PDF file preserving page numbers. 
    
    Args:
        pdf_bytes (bytes): The PDF file in bytes
    """

    pages=[]

    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as document:
        if document.is_encrypted:
            raise ValueError("The PDF is encrypted and cannot be processed.")
        for page_number, page in enumerate(document, start=1):
            text=page.get_text()
            pages.append({"page_number":page_number, "text":text})


    full_text="\n\n".join(page["text"] for page in pages if page["text"])

    if not full_text:
        raise ValueError("No text found in the PDF. This may be a scanned PDF or an image-based PDF.")

    return {
        "page_count":len(pages),
        "pages":pages,
        "full_text":full_text,
    }   

 