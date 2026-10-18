export interface PDFPage {
    page_number: number;
    text: string;
}

export interface PDFUploadResponse {
    filename: string;
    content_type: string;
    file_size: number;
    sha256:string;
    page_count: number;
    pages: PDFPage[];
    full_text: string;
    document_id: string;
    chunks_stored: number;
    
}