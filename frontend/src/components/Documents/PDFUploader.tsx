import {uploadPDF} from "../../api/documents";

import type { PDFUploadResponse } from "../../types/document";

import { useState } from "react";

interface PDFUploaderProps {
  onUploadSuccess: (document: PDFUploadResponse) => void;
}


export default function PDFUploader({ onUploadSuccess }: PDFUploaderProps) {

    const [file, setFile] = useState<File | null>(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);


    async function handleUpload() {
        if (!file) {
            setError("No file selected");
            return;
        }
    

        setLoading(true);
        setError("");

        try{
            const document= await uploadPDF(file);
            onUploadSuccess(document);
        } catch (err:any) {
            setError(err.message || "Failed to upload PDF");
        } finally {
            setLoading(false);

        }

    }

    return(
        <section>
            <h2> Upload a document</h2>
            <input type="file" accept="application/pdf" onChange={(e)=>{
                if (e.target.files && e.target.files.length > 0) {
                    setFile(e.target.files[0]);
                }}
            }/>
            <button onClick={handleUpload} disabled={loading}>
                {loading ? "Uploading...": "Upload PDF"}
            </button>

            {error && <p role="alert" style={{color:"red"}}>{error}</p>}
        </section>
    )
}
