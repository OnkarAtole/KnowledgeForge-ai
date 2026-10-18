
import { useState } from "react";
import { askQuestion, type ChatResponse } from "../../api/chat";

interface ChatPanelProps {
  documentId: string;
}

export default function ChatPanel({ documentId }: ChatPanelProps) {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAsk() {
    if (!question.trim() || loading) return;

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const result = await askQuestion(documentId, question.trim());
      setResponse(result);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="chat-panel">
      <h2>Ask your document</h2>

      <textarea
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        placeholder="Ask a question about this PDF..."
        rows={3}
      />

      <button onClick={handleAsk} disabled={loading || !question.trim()}>
        {loading ? "Thinking..." : "Ask question"}
      </button>

      {error && <p role="alert">{error}</p>}

      {response && (
        <div className="chat-answer">
          <h3>Answer</h3>
          <p>{response.answer}</p>

          <h3>Sources</h3>
          {response.sources.length === 0 ? (
            <p>No source passages found.</p>
          ) : (
            response.sources.map((source, index) => (
              <article key={`${source.page_number}-${index}`}>
                <strong>Page {source.page_number}</strong>
                <p>{source.text}</p>
              </article>
            ))
          )}
        </div>
      )}
    </section>
  );
}
