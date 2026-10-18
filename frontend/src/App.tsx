import { useState } from 'react'
import { useEffect } from 'react'
import './App.css'
import ChatPanel from "./components/chat/ChatPanel";
import PDFUploader from './components/Documents/PDFUploader'
import type { PDFUploadResponse } from './types/document'

type HealthResponse={
  status: string;
  application: string;
}

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [document,setDocument]=useState<PDFUploadResponse | null>(null);

  useEffect(()=>{
    fetch('http://localhost:8000/health')
      .then((response)=>{
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(setHealth)
      .catch((error)=>{
        setError("backend unavailable");
      });
  }, []);

  return (
    <main className="app">
      <h1>KnowledgeForge AI</h1>
      <p>Understand documents. Discover Knowledge</p>

      {/* {health && (
        <p>
          Backend Status: {health.status} - Application: {health.application}
        </p>
      )}

      {error && (
        <p style={{ color: 'red' }}>{error}</p>
      )} */}


      <PDFUploader onUploadSuccess={(document)=>{
        setDocument(document);
      }
      }/>

      {document && (
        <section>
            <h2>{document.filename}</h2>
           <p>Pages: {document.page_count}</p>
           <p>Size: {(document.file_size / 1024).toFixed(1)} KB</p>

           <h3>Extracted text preview</h3>
           <pre style={{ whiteSpace: "pre-wrap" }}>
            {document.full_text.slice(0, 5000)}
           </pre>

           <p>Chunks stored: {document.chunks_stored}</p>
           <p>Document ID: {document.document_id}</p>

           <ChatPanel documentId={document.document_id} />
        </section>
      )}
    </main>
  )
}

export default App
