import type { PDFUploadResponse } from '../types/document';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'; // Replace with your backend URL

export async function uploadPDF(file: File): Promise<PDFUploadResponse> {

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: 'POST',
        body: formData,
    })

    const data= await response.json();
    if (!response.ok) {
        throw new Error(data.detail || 'Failed to upload PDF');
    }
    
    return data as PDFUploadResponse;
}